"""
Fog Scout Sequence - Clean and optimized
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
    """Asset paths for fog scout"""
    BASE_DIR = "assets/fog"
    SCOUT_CAMP = f"{BASE_DIR}/scout_camp.png"
    EXPLORE = f"{BASE_DIR}/explore_button.png"
    CONFIRM = f"{BASE_DIR}/confirm_button.png"
    SECOND_CONFIRM = f"{BASE_DIR}/second_confirm_button.png"
    SEND = f"{BASE_DIR}/send_button.png"



def execute_fog_scout_sequence() -> bool:
    """Execute fog scout sequence with retry logic"""
    check_and_click_help_button()
    check_and_click_close_esc()
    check_and_click_go_home()
    
    if not try_click_button(AssetPaths.SCOUT_CAMP):
        return False
    
    # time.sleep(Config.STEP_DELAY())
    
    if not try_click_button(AssetPaths.EXPLORE):
        return False
    
    # Critical buttons with ESC retry
    if not retry_with_esc(AssetPaths.CONFIRM):
        return False
    
    if not retry_with_esc(AssetPaths.SECOND_CONFIRM):
        return False
    
    if not retry_with_esc(AssetPaths.SEND):
        return False
    
    return True


def main():
    """Main execution for standalone fog scout bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting fog scout cycle...", flush=True)
            
            if execute_fog_scout_sequence():
                print("Fog scout cycle completed successfully", flush=True)
                print("//=======================================", flush=True)
            else:
                print("Fog scout cycle failed, retrying...", flush=True)
                print("//=======================================", flush=True)
            
            time.sleep(Config.STEP_DELAY())
            
    except KeyboardInterrupt:
        print("Fog scout bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()