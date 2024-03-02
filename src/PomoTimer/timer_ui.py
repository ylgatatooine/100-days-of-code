from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog, QHBoxLayout
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QAction

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setGeometry(200, 200, 300, 100)

        layout = QVBoxLayout(self)

        about_label = QLabel("Program Author: Yuer", self)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(about_label)

class PomoTimer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pomodoro_duration = QTime(0, 25)
        self.current_timer_value = self.pomodoro_duration
        self.timer_running = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pomo Timer")
        self.setGeometry(100, 100, 400, 200)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.time_label.font()
        font.setPointSizeF(10 * font.pointSizeF())  # Make the font 10 times larger
        self.time_label.setFont(font)
        self.update_display()

        self.start_reset_button = QPushButton("Start", self)
        self.start_reset_button.clicked.connect(self.start_reset_timer)

        self.about_label = QLabel("About", self)
        self.about_label.setStyleSheet("")
        self.about_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.about_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_label.mousePressEvent = self.show_about_dialog

        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_reset_button)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.about_label, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(horizontal_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    def show_about_dialog(self, event):
        about_dialog = AboutDialog()
        about_dialog.exec()

    def start_reset_timer(self):
        if not self.timer_running:
            self.start_timer()
        else:
            self.reset_timer()

    def start_timer(self):
        if not self.timer.isActive():
            self.timer_running = True
            self.start_reset_button.setText("Reset")
            self.timer.start(1000)  # Update every second

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
        self.current_timer_value = self.pomodoro_duration
        self.update_display()

    def update_display(self):
        self.time_label.setText(self.current_timer_value.toString("mm:ss"))

if __name__ == "__main__":
    app = QApplication([])
    pomo_timer = PomoTimer()
    app.exec()
