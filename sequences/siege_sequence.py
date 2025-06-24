"""
Siege Training Sequence - Clean and optimized
"""
import pyautogui
import time
import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_utils import ensure_assets_directory, move_mouse_zigzag

try:
    from .shared_utils import (
        try_click_button,
        try_click_button_silent,
        retry_with_esc,
        check_and_click_go_home,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        try_click_button_silent,
        retry_with_esc,
        check_and_click_go_home,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )


class AssetPaths:
    """Asset paths for siege training"""
    BASE_DIR = "assets/troop"
    TROOP_HOUSE = f"{BASE_DIR}/siege_house.png"
    TROOP_TRAIN = f"{BASE_DIR}/siege_train.png"
    CONFIRM_TRAIN = f"{BASE_DIR}/confirm_train.png"
    ADD_RSS = f"{BASE_DIR}/add_rss.png"
    SIEGE_TRAINING_CHECK = f"{BASE_DIR}/siege_training_check.png"


def check_confirm_train_available() -> bool:
    """Check if confirm train button is available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.CONFIRM_TRAIN, confidence=0.8)
        return location is not None
    except Exception:
        return False


def check_siege_training_check() -> bool:
    """Check if siege training check is found on screen"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.SIEGE_TRAINING_CHECK, confidence=0.9)
        if location:
            print("Siege training check found - ending session", flush=True)
            return True
        return False
    except pyautogui.ImageNotFoundException:
        return False
    except Exception as e:
        print(f"Error checking siege training check: {e}", flush=True)
        return False


def check_and_click_add_rss() -> bool:
    """Check for ADD_RSS and click if found"""
    try:
        if try_click_button_silent(AssetPaths.ADD_RSS):
            print("ADD_RSS found - clicking it", flush=True)
            time.sleep(Config.STEP_DELAY())
            return True
        return False
    except Exception as e:
        print(f"Error checking ADD_RSS: {e}", flush=True)
        return False


def execute_siege_sequence() -> bool:
    """Execute siege training sequence"""
    try:
        check_and_click_help_button()
        check_and_click_close_esc()
        check_and_click_go_home()
        
        # Check siege training check - if found, end session
        if check_siege_training_check():
            return False
        
        # Click troop house (2 times)
        if not try_click_button(AssetPaths.TROOP_HOUSE):
            return False
        if not try_click_button(AssetPaths.TROOP_HOUSE):
            return False
        
        # Click train button
        if not try_click_button(AssetPaths.TROOP_TRAIN):
            return False
        
        # Check if confirm train button is available
        if check_confirm_train_available():
            print("Confirm train found - proceeding with training", flush=True)
            if not retry_with_esc(AssetPaths.CONFIRM_TRAIN):
                return False
            
            # After confirm train click, check for ADD_RSS
            if check_and_click_add_rss():
                # If ADD_RSS was found and clicked, click CONFIRM_TRAIN again
                print("ADD_RSS clicked - clicking CONFIRM_TRAIN again", flush=True)
                if not retry_with_esc(AssetPaths.CONFIRM_TRAIN):
                    return False
            
        else:
            print("Confirm train not found - pressing ESC and ending session", flush=True)
            pyautogui.press('escape')
            time.sleep(Config.STEP_DELAY())
            return False
        
        return True
    
    except Exception as e:
        print(f"Error in siege sequence: {e}, ending session", flush=True)
        return False


def main():
    """Main execution for standalone siege training bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Siege Training Bot starting in {Config.STEP_DELAY()} seconds...")
    time.sleep(Config.STEP_DELAY())
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting siege training cycle...", flush=True)
            
            if execute_siege_sequence():
                print("Siege training cycle completed successfully", flush=True)
                print("//============================================", flush=True)
            else:
                print("Siege training cycle failed, retrying...", flush=True)
                print("//============================================", flush=True)
            
            time.sleep(Config.STEP_DELAY())
            
    except KeyboardInterrupt:
        print("Siege training bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()