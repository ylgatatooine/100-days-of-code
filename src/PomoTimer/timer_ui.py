from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog, QHBoxLayout, QTabWidget
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QAction, QColor

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
        self.short_break_duration = QTime(0, 5)
        self.long_break_duration = QTime(0, 15)

        self.pomodoro_timer = QTimer(self)
        self.short_break_timer = QTimer(self)
        self.long_break_timer = QTimer(self)

        self.pomodoro_current_timer_value = self.pomodoro_duration
        self.short_break_current_timer_value = self.short_break_duration
        self.long_break_current_timer_value = self.long_break_duration

        self.pomodoro_timer.timeout.connect(self.update_pomodoro_timer)
        self.short_break_timer.timeout.connect(self.update_short_break_timer)
        self.long_break_timer.timeout.connect(self.update_long_break_timer)

        self.init_ui()

        # Connect the custom signal for tab changes
        # self.tab_widget.currentChanged.connect(self.change_tab_background)

    def init_ui(self):
        self.setWindowTitle("Pomo Timer")
        self.setGeometry(100, 100, 400, 200)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        self.pomodoro_tab = QWidget()
        self.short_break_tab = QWidget()
        self.long_break_tab = QWidget()

        self.create_pomodoro_tab()
        self.create_short_break_tab()
        self.create_long_break_tab()

        self.tab_widget.addTab(self.pomodoro_tab, "Pomodoro")
        self.tab_widget.addTab(self.short_break_tab, "Short Break")
        self.tab_widget.addTab(self.long_break_tab, "Long Break")
        self.tab_widget.setCurrentIndex(0)  # Set the Pomodoro tab as the selected tab



        self.setCentralWidget(self.tab_widget)

        self.show()

    def create_pomodoro_tab(self):
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.time_label.font()
        font.setPointSizeF(10 * font.pointSizeF())
        self.time_label.setFont(font)
        self.update_display()

        self.start_reset_button = QPushButton("Start", self)
        self.start_reset_button.setFixedSize(100, 30)
        self.start_reset_button.clicked.connect(self.start_reset_timer)

        # self.about_label = QLabel("About", self)
        # self.about_label.setStyleSheet("")
        # self.about_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        # self.about_label.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.about_label.mousePressEvent = self.show_about_dialog

        layout = QVBoxLayout(self.pomodoro_tab)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # horizontal_layout = QHBoxLayout()
        # horizontal_layout.addWidget(self.about_label, Qt.AlignmentFlag.AlignRight)
        # layout.addLayout(horizontal_layout)

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
        self.time_label.setText(self.pomodoro_current_timer_value.toString("mm:ss"))

    def update_short_break_display(self):
        self.short_break_time_label.setText(self.short_break_current_timer_value.toString("mm:ss"))

    def update_long_break_display(self):
        self.long_break_time_label.setText(self.long_break_current_timer_value.toString("mm:ss"))

    # def change_tab_background(self, index):
    #     tab_colors = [
    #         QColor("white"),  # Pomodoro
    #         QColor("lightblue"),  # Short Break
    #         QColor("cyan")  # Long Break
    #     ]
    #
    #     current_tab_color = tab_colors[index]
    #     self.tab_widget.setStyleSheet(f"background-color: {current_tab_color.name()};")

    def create_short_break_tab(self):
        self.short_break_time_label = QLabel()
        self.short_break_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.short_break_time_label.font()
        font.setPointSizeF(10 * font.pointSizeF())
        self.short_break_time_label.setFont(font)
        self.update_short_break_display()

        self.short_break_start_reset_button = QPushButton("Start", self)
        self.short_break_start_reset_button.setFixedSize(100, 30)
        self.short_break_start_reset_button.clicked.connect(self.start_reset_short_break_timer)

        layout = QVBoxLayout(self.short_break_tab)
        layout.addWidget(self.short_break_time_label)
        layout.addWidget(self.short_break_start_reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_long_break_tab(self):
        self.long_break_time_label = QLabel()
        self.long_break_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.long_break_time_label.font()
        font.setPointSizeF(10 * font.pointSizeF())
        self.long_break_time_label.setFont(font)
        self.update_long_break_display()

        self.long_break_start_reset_button = QPushButton("Start", self)
        self.long_break_start_reset_button.setFixedSize(100, 30)
        self.long_break_start_reset_button.clicked.connect(self.start_reset_long_break_timer)

        layout = QVBoxLayout(self.long_break_tab)
        layout.addWidget(self.long_break_time_label)
        layout.addWidget(self.long_break_start_reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_reset_pomodoro_timer(self):
        if not self.pomodoro_timer.isActive():
            self.pomodoro_timer.start(1000)
            self.start_reset_button.setText("Reset")
        else:
            self.pomodoro_timer.stop()
            self.start_reset_button.setText("Start")
            self.pomodoro_current_timer_value = self.pomodoro_duration

        self.update_display()

    def start_reset_short_break_timer(self):
        if not self.short_break_timer.isActive():
            self.short_break_timer.start(1000)
            self.short_break_start_reset_button.setText("Reset")
        else:
            self.short_break_timer.stop()
            self.short_break_start_reset_button.setText("Start")
            self.short_break_current_timer_value = self.short_break_duration

        self.update_short_break_display()


    def start_reset_long_break_timer(self):
        if not self.long_break_timer.isActive():
            self.long_break_timer.start(1000)
            self.long_break_start_reset_button.setText("Reset")
        else:
            self.long_break_timer.stop()
            self.long_break_start_reset_button.setText("Start")
            self.long_break_current_timer_value = self.long_break_duration

        self.update_long_break_display()

    def update_pomodoro_timer(self):
        self.pomodoro_current_timer_value = self.pomodoro_current_timer_value.addSecs(-1)
        self.update_display()

        if self.pomodoro_current_timer_value == QTime(0, 0):
            self.pomodoro_timer.stop()
            self.start_reset_button.setText("Start")

    def update_short_break_timer(self):
        self.short_break_current_timer_value = self.short_break_current_timer_value.addSecs(-1)
        self.update_short_break_display()

        if self.short_break_current_timer_value == QTime(0, 0):
            self.short_break_timer.stop()
            self.short_break_start_reset_button.setText("Start")

    def update_long_break_timer(self):
        self.long_break_current_timer_value = self.long_break_current_timer_value.addSecs(-1)
        self.update_long_break_display()

        if self.long_break_current_timer_value == QTime(0, 0):
            self.long_break_timer.stop()
            self.long_break_start_reset_button.setText("Start")

if __name__ == "__main__":
    app = QApplication([])
    pomo_timer = PomoTimer()
    app.exec()
