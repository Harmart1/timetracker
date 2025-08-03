import sys
from PyQt5 import QtWidgets
from models import init_db, SessionLocal
from ui import TimerTab, EntriesTab, CodesStaffTab, InvoiceTab

def main():
    # Initialize DB & config
    init_db()
    session = SessionLocal()
    # seed config if empty
    if not session.query(type(session.query(type(session.query(type(session.query(type(Config)).mapper.class_).filter_by(key="firm_name")).all())))).all()):
        from models import set_config
        set_config(session, "firm_name", "Tim Harmar Legal and Consult Solutions")
        set_config(session, "address",   "67 Hugill St., Sault Ste. Marie, ON P6A 4E6")
        set_config(session, "emails",    "tharmar@timharmar.com,kburton@timharmar.com")

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    font = app.font(); font.setPointSize(10); app.setFont(font)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Tim Harmar Legal & Consult Solutions")
    tabs = QtWidgets.QTabWidget()
    tabs.addTab(TimerTab(),       "Timer")
    tabs.addTab(EntriesTab(),     "Entries")
    tabs.addTab(CodesStaffTab(),  "Codes & Staff")
    tabs.addTab(InvoiceTab(),     "Invoices")
    window.setCentralWidget(tabs)
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
