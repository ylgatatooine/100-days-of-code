"""Easy to use, flexible PyQt6 Pomodoro Technique timer."""

import os

__author__ = 'yuer'
__maintainer__ = __author__
__email__ = 'yuer86@gmail.com'
__license__ = 'GPL-3.0'
__version__ = '0.3.0'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
APP_ICON = os.path.join(MEDIA_DIR, 'icon.png')

ORGANIZATION_NAME = __author__
APPLICATION_NAME = 'PomodoroTimer'

__all__ = (
    '__author__',
    '__email__',
    '__license__',
    '__maintainer__',
    '__version__',
    'BASE_DIR',
    'MEDIA_DIR',
    'APP_ICON',
    'ORGANIZATION_NAME',
    'APPLICATION_NAME',
)