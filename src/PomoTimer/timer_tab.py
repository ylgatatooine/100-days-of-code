from PyQt6.QtCore import QTime, QTimer, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox
from voice_alert import VoiceAlert
from __init__ import ALERT_MINUTES

class TimerTab(QWidget):
    time_changed = pyqtSignal(int, int)  # Add this line to create the time_changed signal

    def __init__(self, duration_minutes):
        super().__init__()

        self.duration = QTime(0, duration_minutes)
        self.current_timer_value = self.duration
        self.timer_running = False

        self.alert_enabled = True
        self.alert_minutes = ALERT_MINUTES

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.voice_alert = VoiceAlert()

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

        self.alert_checkbox = QCheckBox("Alert", self)
        self.alert_checkbox.setChecked(True)
        self.alert_checkbox.stateChanged.connect(self.alert_changed)

        layout.addWidget(self.time_label)
        layout.addWidget(self.start_reset_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.alert_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

    def alert_changed(self, state):
        self.alert_enabled = state == Qt.CheckState.Checked

    def update_timer(self):
        self.current_timer_value = self.current_timer_value.addSecs(-1)
        self.update_display()

        for alert_minute in self.alert_minutes:
            if self.alert_enabled and self.current_timer_value.minute() == alert_minute and self.current_timer_value.second() == 0:
                self.voice_alert.speak(f"{alert_minute} minute{'s' if alert_minute != 1 else ''} left")

        if self.current_timer_value == QTime(0, 0):
            self.timer.stop()
            self.timer_running = False
            self.start_reset_button.setText("Start")

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

    # def update_timer(self):
    #     self.current_timer_value = self.current_timer_value.addSecs(-1)
    #     self.update_display()
    #
    #     if self.current_timer_value == QTime(0, 0):
    #         self.timer.stop()
    #         self.timer_running = False
    #         self.start_reset_button.setText("Start")

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.start_reset_button.setText("Start")
        self.current_timer_value = self.duration
        self.update_display()

    def update_display(self):
        self.time_label.setText(self.current_timer_value.toString("mm:ss"))

    def tick(self):
        if self.current_time == QTime(0, 0):
            self.timer.stop()
            return

        self.current_time = self.current_time.addSecs(-1)
        self.time_label.setText(self.current_time.toString("mm:ss"))
        self.time_changed.emit(self.current_time.minute(), self.current_time.second())  # Emit the signal here


