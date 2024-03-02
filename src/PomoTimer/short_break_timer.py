from timer_tab import TimerTab

class ShortBreakTimerTab(TimerTab):
    def __init__(self):
        super().__init__(duration_minutes=5)
