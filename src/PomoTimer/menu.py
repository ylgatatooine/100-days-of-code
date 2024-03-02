from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

def create_menu(pomo_timer):
    menu = QMenu()

    start_action = menu.addAction("Start Pomodoro")
    reset_action = menu.addAction("Reset Pomodoro")
    menu.addSeparator()
    quit_action = menu.addAction("Quit")

    start_action.triggered.connect(pomo_timer.timer_tabs[0].start_timer)
    reset_action.triggered.connect(pomo_timer.timer_tabs[0].reset_timer)
    quit_action.triggered.connect(pomo_timer.quit)

    pomo_timer.setContextMenu(menu)
