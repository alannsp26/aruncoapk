import cv2
import cv2.aruco as aruco
import numpy as np
import time
import os
from kivy.utils import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder

# Clean KV string. Reduced top panel vertical footprint.
KV = '''
<SettingsPopup>:
    title: 'Detection Configuration'
    size_hint: 0.9, 0.6
    BoxLayout:
        orientation: 'vertical'
        GridLayout:
            cols: 1
            BoxLayout:
                Label:
                    text: 'Stability (s)'
                TextInput:
                    id: cfg_stable
                    text: '0.7'
            BoxLayout:
                Label:
                    text: 'Cycle (s)'
                TextInput:
                    id: cfg_cycle
                    text: '2.0'
        Button:
            text: 'Apply & Close'
            on_release: root.dismiss()

<ArUcoLayout>:
    BoxLayout:
        size_hint: 1, 0.08
        pos_hint: {'top': 1}
        Spinner:
            id: dict_spinner
            text: '4x4_1000'
            values: ('4x4_1000', '5x5_1000', '6x6_1000', '7x7_1000', 'ARUCO_ORIGINAL', 'MIP_36h12')
        Button:
            text: 'Settings'
            on_release: root.open_settings()
        Button:
            id: btn_auto
            text: 'Auto: OFF'
            on_release: root.toggle_cycle()

    Image:
        id: cam_view
        size_hint: 1, 0.72
        pos_hint: {'center_x': 0.5, 'center_y': 0.54}

    BoxLayout:
        size_hint: 1, 0.2
        pos_hint: {'bottom': 0}
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: '=== STABLE ==='
                size_hint_y: None
                height: 30
            ScrollView:
                Label:
                    id: detected_list
                    text: ''
                    halign: 'center'
                    valign: 'top'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: '=== BLOCKED ==='
                size_hint_y: None
                height: 30
            ScrollView:
                Label:
                    id: blacklist_list
                    text: ''
                    halign: 'center'
                    valign: 'top'
'''


class SettingsPopup(Popup): pass


class ArUcoLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'win':
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Smooth rendering for Windows testing
        else:
            self.cap = cv2.VideoCapture(0)  # Default backend for Android compatibility
        self.settings = SettingsPopup()

        self.dicts = ['4x4_1000', '5x5_1000', '6x6_1000', '7x7_1000', 'ARUCO_ORIGINAL', 'MIP_36h12']
        self.dict_map = {
            '4x4_1000': aruco.DICT_4X4_1000,
            '5x5_1000': aruco.DICT_5X5_1000,
            '6x6_1000': aruco.DICT_6X6_1000,
            '7x7_1000': aruco.DICT_7X7_1000,
            'ARUCO_ORIGINAL': aruco.DICT_ARUCO_ORIGINAL,
            'MIP_36h12': aruco.DICT_ARUCO_MIP_36h12
        }

        # State tracking dictionaries
        self.stable_ids = {}
        self.blacklist = {}

        # Timers to handle continuous frame checks
        self.potential_timers = {}
        self.recovery_timers = {}
        self.blacklist_missing_timers = {}  # Tracks when blacklisted item was last seen

        self.auto_cycle_on = False
        self.last_cycle = time.time()

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def open_settings(self):
        self.settings.open()

    def toggle_cycle(self):
        self.auto_cycle_on = not self.auto_cycle_on
        self.ids.btn_auto.text = f"Auto: {'ON' if self.auto_cycle_on else 'OFF'}"

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret: return
        now = time.time()

        try:
            STABLE_LIMIT = float(self.settings.ids.cfg_stable.text)
            CYCLE_LIMIT = float(self.settings.ids.cfg_cycle.text)
        except:
            STABLE_LIMIT, CYCLE_LIMIT = 0.7, 2.0

        # Dictionary Auto-Cycling System
        if self.auto_cycle_on and (now - self.last_cycle) >= CYCLE_LIMIT:
            curr_idx = self.dicts.index(self.ids.dict_spinner.text)
            self.ids.dict_spinner.text = self.dicts[(curr_idx + 1) % len(self.dicts)]
            self.last_cycle = now
            # Clear blacklist upon dictionary cycling
            self.blacklist.clear()
            self.blacklist_missing_timers.clear()

        # Run ArUco Engine
        d_val = self.dict_map.get(self.ids.dict_spinner.text, aruco.DICT_4X4_1000)
        detector = aruco.ArucoDetector(aruco.getPredefinedDictionary(d_val), aruco.DetectorParameters())
        corners, ids, _ = detector.detectMarkers(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        found = set(ids.flatten()) if ids is not None else set()

        # --- STATE MACHINE LOGIC ---

        # Process every marker actively seen in this frame
        for m_id in found:
            # If it's found, it's not currently missing from view
            if m_id in self.blacklist_missing_timers:
                del self.blacklist_missing_timers[m_id]

            if m_id in self.stable_ids:
                continue

            elif m_id in self.blacklist:
                if m_id not in self.recovery_timers:
                    self.recovery_timers[m_id] = now
                elif now - self.recovery_timers[m_id] >= 1.0:
                    self.stable_ids[m_id] = True
                    del self.blacklist[m_id]
                    if m_id in self.recovery_timers: del self.recovery_timers[m_id]

            else:
                if m_id not in self.potential_timers:
                    self.potential_timers[m_id] = now
                elif now - self.potential_timers[m_id] >= STABLE_LIMIT:
                    self.stable_ids[m_id] = True
                    if m_id in self.potential_timers: del self.potential_timers[m_id]

        # Break continuity: Reset counters for anything missing this frame
        for m_id in list(self.potential_timers.keys()):
            if m_id not in found:
                del self.potential_timers[m_id]

        for m_id in list(self.recovery_timers.keys()):
            if m_id not in found:
                del self.recovery_timers[m_id]
                # Continuous break resets recovery clock, but stays blacklisted.
                # Start the missing countdown timer for clearing it completely.
                if m_id in self.blacklist and m_id not in self.blacklist_missing_timers:
                    self.blacklist_missing_timers[m_id] = now

        # Clear blacklisted IDs if they have not been detected for 1.0 full second
        for m_id in list(self.blacklist_missing_timers.keys()):
            if now - self.blacklist_missing_timers[m_id] >= 1.0:
                if m_id in self.blacklist: del self.blacklist[m_id]
                del self.blacklist_missing_timers[m_id]

        # Stable Demotion: If a stable ID misses a single frame, it goes to blacklist instantly
        for m_id in list(self.stable_ids.keys()):
            if m_id not in found:
                self.blacklist[m_id] = True
                self.blacklist_missing_timers[m_id] = now  # Starts missing countdown immediately
                del self.stable_ids[m_id]

        # --- RENDERING & VISUALIZATION ---
        if ids is not None:
            stable_indices = [i for i, m_id in enumerate(ids.flatten()) if m_id in self.stable_ids]
            if stable_indices:
                s_corners = [corners[i] for i in stable_indices]
                s_ids = np.array([ids[i] for i in stable_indices])
                aruco.drawDetectedMarkers(frame, s_corners, s_ids)

        self.ids.detected_list.text = "\n".join(map(str, sorted(self.stable_ids.keys())))
        self.ids.blacklist_list.text = "\n".join(map(str, sorted(self.blacklist.keys())))

        buf = cv2.flip(frame, 0).tobytes()
        tex = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.cam_view.texture = tex


class DetectorApp(App):
    def build(self):
        Builder.load_string(KV)
        return ArUcoLayout()


if __name__ == '__main__':
    DetectorApp().run()
