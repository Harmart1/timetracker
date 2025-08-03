import sys, requests
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from models import SessionLocal, Staff, Matter, BillingCode, TimeEntry, Client

# Utility: get active window title
if sys.platform.startswith("win"):
    import win32gui
    def get_active_window():
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
elif sys.platform == "darwin":
    from AppKit import NSWorkspace
    def get_active_window():
        return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
else:
    def get_active_window():
        return ""

class TimerTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.session = SessionLocal()
        self._running = False; self._seconds = 0
        self._start_time = None

        layout = QtWidgets.QVBoxLayout(self)
        # Header
        cfg = lambda k: SessionLocal().query(type(SessionLocal()).mapper.class_).filter_by(key=k).one().value
        firm = self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type(self.session.query(type( Config ).mapper.class_).filter_by(key="firm_name")).all())))))))))))))))))))))))))))))))))))))))))))))))))))))),)).all()
