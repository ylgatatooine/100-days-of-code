import logging
import os


# set the minutes that alerts sound
ALERT_MINUTES = [24, 4, 1]

# set log level
LOG_LEVEL = logging.INFO

# set log file path
LOG_FILE = os.path.join(os.path.dirname(__file__), 'pomodoro.log')

# set voice id
VOICE_ID = "com.apple.voice.compact.en-GB.Daniel"