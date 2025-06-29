"""
Cavalry Training Sequence - Clean and optimized
"""
import pyautogui
import time
import sys
import os
import random
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_utils import ensure_assets_directory, move_mouse_zigzag

# Global flag for F12 stop signal
stop_bot_flag = threading.Event()

def monitor_f12_key():
    """Monitor for F12 key press to stop the bot"""
    try:
        import keyboard
        keyboard.wait('f12')
        print("F12 pressed - Stopping bot...", flush=True)
        stop_bot_flag.set()
    except ImportError:
        pass
    except Exception:
        pass

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
    """Asset paths for cavalry training"""
    BASE_DIR = "assets/troop"
    TROOP_HOUSE = f"{BASE_DIR}/cavalry_house.png"
    TROOP_TRAIN = f"{BASE_DIR}/cavalry_train.png"
    CONFIRM_TRAIN = f"{BASE_DIR}/confirm_train.png"
    ADD_RSS = f"{BASE_DIR}/add_rss.png"
    CAVALRY_TRAINING_CHECK = f"{BASE_DIR}/cavalry_training_check.png"


def check_confirm_train_available() -> bool:
    """Check if confirm train button is available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.CONFIRM_TRAIN, confidence=0.8)
        return location is not None
    except Exception:
        return False


def check_cavalry_training_check() -> bool:
    """Check if cavalry training check is found on screen"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.CAVALRY_TRAINING_CHECK, confidence=0.6)
        if location:
            print("Cavalry training check found - ending session", flush=True)
            center_x = location.left + location.width // 2
            center_y = location.top + location.height // 2
            move_mouse_zigzag(center_x, center_y)
            return True
        return False
    except pyautogui.ImageNotFoundException:
        print("Cavalry training check image not found", flush=True)
        return False
    except Exception as e:
        print(f"Error checking cavalry training check: {e}", flush=True)
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


def execute_cavalry_sequence() -> bool:
    """Execute cavalry training sequence"""
    try:
        check_and_click_close_esc()
        check_and_click_help_button()
        check_and_click_go_home()
        
        # Check cavalry training check - if found, end session
        if check_cavalry_training_check():
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
        print(f"Error in cavalry sequence: {e}, ending session", flush=True)
        return False


def main():
    """Main execution for standalone cavalry training bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Cavalry Training Bot starting in {Config.STEP_DELAY()} seconds...")
    print("🔴 Press F12 anytime to stop the bot")
    time.sleep(Config.STEP_DELAY())
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    # Start F12 key monitoring in a separate thread
    f12_thread = threading.Thread(target=monitor_f12_key, daemon=True)
    f12_thread.start()
    
    try:
        while True:
            # Check if F12 was pressed
            if stop_bot_flag.is_set():
                print("🛑 Bot stopped by F12 key press", flush=True)
                break
                
            print("Starting cavalry training cycle...", flush=True)
            
            if execute_cavalry_sequence():
                print("Cavalry training cycle completed successfully", flush=True)
                print("//============================================", flush=True)
            else:
                print("Cavalry training cycle failed, retrying...", flush=True)
                print("//============================================", flush=True)
            
            time.sleep(Config.STEP_DELAY())
            
    except KeyboardInterrupt:
        print("Cavalry training bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()