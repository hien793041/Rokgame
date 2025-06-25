"""
Shared utilities for bot sequences
"""
import pyautogui
import time
import sys
import os
import random

# Add parent directory to path when running as standalone
if __name__ == '__main__' or '.' not in __name__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_utils import click_button


class Config:
    """Configuration constants"""
    MAX_RETRIES = 2
    STEP_DELAY = lambda: random.uniform(1.5, 2.5)
    BUTTON_DELAY = lambda: random.uniform(1.5, 2.5)
    RETRY_DELAY = lambda: random.uniform(1.5, 2.5)


class SharedAssetPaths:
    """Shared asset paths"""
    BASE_DIR = "assets"
    GO_OUTSIDE = f"{BASE_DIR}/go_outside.png"
    GO_HOME = f"{BASE_DIR}/go_home.png"
    CLOSE_ESC = f"{BASE_DIR}/close_esc.png"
    HELP_BUTTON = f"{BASE_DIR}/help_button.png"


def try_click_button(button_path: str) -> bool:
    """Try to click button once"""
    if click_button(button_path):
        time.sleep(Config.BUTTON_DELAY())
        return True
    return False


def try_click_button_silent(button_path: str) -> bool:
    """Try to click button once without delays"""
    return click_button(button_path)


def check_and_click_go_home() -> bool:
    """Check go home button and press space if found"""
    try:
        # Check if GO_HOME button exists
        location = pyautogui.locateOnScreen(SharedAssetPaths.GO_HOME, confidence=0.7)
        if location is not None:
            print("GO_HOME found - pressing space", flush=True)
            pyautogui.press('space')
            time.sleep(Config.STEP_DELAY())
            return True
        return False
    except Exception:
        return False


def check_and_click_go_outside() -> bool:
    """Check go outside button and press space if found"""
    try:
        # Check if GO_OUTSIDE button exists
        location = pyautogui.locateOnScreen(SharedAssetPaths.GO_OUTSIDE, confidence=0.7)
        if location is not None:
            print("GO_OUTSIDE found - pressing space", flush=True)
            pyautogui.press('space')
            time.sleep(Config.STEP_DELAY())
            return True
        return False
    except Exception:
        return False


def check_and_click_close_esc() -> bool:
    """Check and click close ESC button if found"""
    try:
        if try_click_button_silent(SharedAssetPaths.CLOSE_ESC):
            time.sleep(Config.STEP_DELAY())
            return True
        return False
    except Exception:
        return False


def check_and_click_help_button() -> bool:
    """Check and click help button if found"""
    try:
        if try_click_button_silent(SharedAssetPaths.HELP_BUTTON):
            time.sleep(Config.STEP_DELAY())
            return True
        return False
    except Exception:
        return False



def retry_with_esc(button_path: str, max_retries: int = 1) -> bool:
    """Retry button click with ESC press on failure"""
    for retry_count in range(max_retries):
        if try_click_button(button_path):
            return True
        pyautogui.press('escape')
        time.sleep(Config.RETRY_DELAY())
    return False