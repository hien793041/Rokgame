"""
Infantry Training Sequence - Clean and optimized
"""
import pyautogui
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_utils import ensure_assets_directory

try:
    from .shared_utils import (
        try_click_button,
        retry_with_esc,
        check_and_click_go_home,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        retry_with_esc,
        check_and_click_go_home,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )


class AssetPaths:
    """Asset paths for infantry training"""
    BASE_DIR = "assets/troop"
    TROOP_HOUSE = f"{BASE_DIR}/infantry_house.png"
    TROOP_TRAIN = f"{BASE_DIR}/infantry_train.png"
    CONFIRM_TRAIN = f"{BASE_DIR}/confirm_train.png"


def check_confirm_train_available() -> bool:
    """Check if confirm train button is available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.CONFIRM_TRAIN, confidence=0.8)
        return location is not None
    except Exception:
        return False


def execute_infantry_sequence() -> bool:
    """Execute infantry training sequence"""
    try:
        check_and_click_help_button()
        check_and_click_close_esc()
        check_and_click_go_home()
        
        # Click troop house
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
        else:
            print("Confirm train not found - pressing ESC and ending session", flush=True)
            pyautogui.press('escape')
            time.sleep(Config.STEP_DELAY)
            return False
        
        return True
    
    except Exception as e:
        print(f"Error in infantry sequence: {e}, ending session", flush=True)
        return False


def main():
    """Main execution for standalone infantry training bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Infantry Training Bot starting in {Config.STEP_DELAY} seconds...")
    time.sleep(Config.STEP_DELAY)
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting infantry training cycle...", flush=True)
            
            if execute_infantry_sequence():
                print("Infantry training cycle completed successfully", flush=True)
            else:
                print("Infantry training cycle failed, retrying...", flush=True)
            
            time.sleep(Config.STEP_DELAY)
            
    except KeyboardInterrupt:
        print("Infantry training bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()