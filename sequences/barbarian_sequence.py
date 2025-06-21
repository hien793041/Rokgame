"""
Barbarian Farm Sequence - Clean and optimized
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
        check_and_click_go_outside,
        check_and_click_close_esc,
        retry_with_esc,
        try_click_button_silent,
        check_and_click_help_button,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        check_and_click_go_outside,
        check_and_click_close_esc,
        retry_with_esc,
        try_click_button_silent,
        check_and_click_help_button,
        Config
    )


class AssetPaths:
    """Asset paths for barbarian farm"""
    BASE_DIR = "assets/barbarian"
    FIND_BAR = f"{BASE_DIR}/find_bar_button.png"
    CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
    ATTACK = f"{BASE_DIR}/attack_button.png"
    COMMANDER = f"{BASE_DIR}/commander_barbarian.png"
    ADD_TROOP = f"{BASE_DIR}/icon_troop_available.png"
    SEND_TROOP = f"{BASE_DIR}/send_troop_available.png"
    TROOP_AVAILABLE = f"{BASE_DIR}/icon_troop_available.png"
    # Alternative buttons when no commander
    ADD_TROOP_ALT = f"{BASE_DIR}/add_troop_button.png"
    SEND_TROOP_ALT = f"{BASE_DIR}/send_troop_button.png"
    SELECT_TROOP_ALT = f"{BASE_DIR}/select_troop_button.png"

def check_troop_available() -> bool:
    """Check if troops are available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.TROOP_AVAILABLE, confidence=0.6)
        return location is not None
    except Exception:
        return False


def check_commander_available() -> bool:
    """Check if commander is available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.COMMANDER, confidence=0.6)
        return location is not None
    except Exception:
        return False

def execute_barbarian_farm_sequence() -> bool:
    """Execute barbarian farm sequence"""
    check_and_click_help_button()
    check_and_click_close_esc()
    check_and_click_go_outside()
    
    # Execute initial sequence
    if not try_click_button(AssetPaths.FIND_BAR):
        return False
    
    # Critical buttons with ESC retry
    if not retry_with_esc(AssetPaths.CONFIRM_FIND):
        return False
    
    if not retry_with_esc(AssetPaths.ATTACK):
        return False
    
    # Smart flow based on commander availability
    if check_commander_available():
        print("Commander found - using normal flow", flush=True)
        # Check troops and use normal buttons
        if not check_troop_available():
            print("No troops available, pressing ESC and ending session", flush=True)
            pyautogui.press('escape')
            time.sleep(Config.STEP_DELAY)
            return False
        
        if not retry_with_esc(AssetPaths.ADD_TROOP):
            return False
        if not retry_with_esc(AssetPaths.SEND_TROOP):
            return False
    else:
        print("No commander found - using alternative flow", flush=True)
        # No commander - use alternative buttons
        if not retry_with_esc(AssetPaths.ADD_TROOP_ALT):
            return False
        if not retry_with_esc(AssetPaths.SELECT_TROOP_ALT):
            return False
        if not retry_with_esc(AssetPaths.SEND_TROOP_ALT):
            return False
    
    return True


def main():
    """Main execution for standalone barbarian farm bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Barbarian Farm Bot starting in {Config.STEP_DELAY} seconds...")
    time.sleep(Config.STEP_DELAY)
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting barbarian farm cycle...", flush=True)
            
            if execute_barbarian_farm_sequence():
                print("Barbarian farm cycle completed successfully", flush=True)
            else:
                print("Barbarian farm cycle failed, retrying...", flush=True)
            
            time.sleep(Config.STEP_DELAY)
            
    except KeyboardInterrupt:
        print("Barbarian farm bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()