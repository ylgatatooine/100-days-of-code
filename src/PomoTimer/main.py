import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QWidget, QTabWidget
from PyQt6.QtGui import QIcon

from timer_tab import TimerTab
from menu import create_menu
from log import Log


class PomoTimer(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon("resources/tiger.png"))

        self.timer_tabs = [
            TimerTab(25),  # Pomodoro
            TimerTab(5),   # Short Break
            TimerTab(15)   # Long Break
        ]

        self.tab_widget = QTabWidget()
        for i, timer_tab in enumerate(self.timer_tabs):
            self.tab_widget.addTab(timer_tab, ["Pomodoro", "Short Break", "Long Break"][i])

        self.show()

        self.show_timer_window()

        log = Log()
        log.info("PomoTimer started")

    def show_timer_window(self):
        self.tab_widget.show()

    def update_icon(self, minutes, seconds):
        # Update the tray icon based on the current time (minutes, seconds)
        pass
    def quit(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pomo_timer = PomoTimer()
    create_menu(pomo_timer)  # Move the create_menu call here

    sys.exit(app.exec())
