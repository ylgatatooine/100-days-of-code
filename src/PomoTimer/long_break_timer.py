from PyQt6.QtCore import QTime, Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class LongBreakTimerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.duration = QTime(0, 15)
        self.current_timer_value = self.duration
        self.timer_running = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    def init_ui(self):
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.time_label.font()
        font.setPointSizeF(10 * font.pointSizeF())
        self.time_label.setFont(font)
        self.update_display()

        self.start_reset_button = QPushButton("Start", self)
        self.start_reset_button.setFixedSize(100, 30)
        self.start_reset_button.clicked.connect(self.start_reset_timer)

        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_reset_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.reset_timer()

    def start_timer(self):
        if not self.timer.isActive():
            self.timer_running = True
            self.start_reset_button.setText("Reset")
            self.timer.start(1000)

    def update_timer(self):
        self.current_timer_value = self.current_timer_value.addSecs(-1)
        self.update_display()

        if self.current_timer_value == QTime(0, 0):
            self.timer.stop()
            self.timer_running = False
            self.start_reset_button.setText("Start")

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.start_reset_button.setText("Start")
        self.current_timer_value = self.duration
        self.update_display()

    def update_display(self):
        self.time_label.setText(self.current_timer_value.toString("mm:ss"))
