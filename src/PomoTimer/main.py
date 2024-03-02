from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QTimer

from pomodoro_timer import PomodoroTimerTab
from short_break_timer import ShortBreakTimerTab
from long_break_timer import LongBreakTimerTab

class PomoTimer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pomodoro_timer = QTimer(self)
        self.short_break_timer = QTimer(self)
        self.long_break_timer = QTimer(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pomo Timer")
        self.setGeometry(100, 100, 400, 200)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        pomodoro_tab = PomodoroTimerTab()
        short_break_tab = ShortBreakTimerTab()
        long_break_tab = LongBreakTimerTab()

        self.tab_widget.addTab(pomodoro_tab, "Pomodoro")
        self.tab_widget.addTab(short_break_tab, "Short Break")
        self.tab_widget.addTab(long_break_tab, "Long Break")
        self.tab_widget.setCurrentIndex(0)

        self.setCentralWidget(self.tab_widget)

        self.show()

if __name__ == "__main__":
    app = QApplication([])
    pomo_timer = PomoTimer()
    app.exec()
