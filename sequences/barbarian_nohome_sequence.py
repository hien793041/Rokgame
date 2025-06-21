"""
Barbarian No-Home Sequence - Clean and optimized with troop checking
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
        try_click_button_silent,
        retry_with_esc,
        check_and_click_go_outside,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        try_click_button_silent,
        retry_with_esc,
        check_and_click_go_outside,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )


class AssetPaths:
    """Asset paths for barbarian farm"""
    BASE_DIR = "assets/barbarian"
    FIND_BAR = f"{BASE_DIR}/find_bar_button.png"
    CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
    ATTACK = f"{BASE_DIR}/attack_button.png"
    ADD_TROOP = f"{BASE_DIR}/icon_troop_available.png"
    SEND_TROOP = f"{BASE_DIR}/send_troop_available.png"
    TROOP_AVAILABLE = f"{BASE_DIR}/icon_troop_available.png"



def check_troop_available() -> bool:
    """Check if troops are available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.TROOP_AVAILABLE, confidence=0.8)
        return location is not None
    except Exception:
        return False


def execute_barbarian_nohome_sequence() -> bool:
    """Execute barbarian no-home sequence with smart button selection"""
    try:
        check_and_click_help_button()
        check_and_click_close_esc()
        check_and_click_go_outside()
        
        # Early exit if no troops available
        if not check_troop_available():
            print("No troops available, ending session", flush=True)
            return False
        
        time.sleep(Config.STEP_DELAY)
        
        # Execute initial sequence
        if not try_click_button(AssetPaths.FIND_BAR):
            return False
        
        # Critical buttons with ESC retry
        if not retry_with_esc(AssetPaths.CONFIRM_FIND):
            return False
        
        if not retry_with_esc(AssetPaths.ATTACK):
            return False
        
        # Use current logic buttons with ESC retry
        if not retry_with_esc(AssetPaths.ADD_TROOP):
            return False
        if not retry_with_esc(AssetPaths.SEND_TROOP):
            return False
        
        return True
    
    except Exception as e:
        print(f"Error in barbarian sequence: {e}, ending session", flush=True)
        return False


def main():
    """Main execution for standalone barbarian no-home bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting barbarian no-home cycle...", flush=True)
            
            if execute_barbarian_nohome_sequence():
                print("Barbarian no-home cycle completed successfully", flush=True)
            else:
                print("Barbarian no-home cycle failed, retrying...", flush=True)
            
            time.sleep(Config.STEP_DELAY)
            
    except KeyboardInterrupt:
        print("Barbarian no-home bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()