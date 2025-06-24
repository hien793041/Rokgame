import pyautogui
import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .shared_utils import (
        try_click_button,
        retry_with_esc,
        check_and_click_go_outside,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        retry_with_esc,
        check_and_click_go_outside,
        check_and_click_close_esc,
        check_and_click_help_button,
        Config
    )


class AssetPaths:
    """Asset paths for resources farm"""
    BASE_DIR = "assets/resoureces"
    FIND_BAR = f"{BASE_DIR}/find_bar_button.png"
    LUA_RSS = f"{BASE_DIR}/lua.png"
    GO_RSS = f"{BASE_DIR}/go.png"
    DA_RSS = f"{BASE_DIR}/da.png"
    JOAN_RSS = f"{BASE_DIR}/joan.png"
    CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
    GATHER = f"{BASE_DIR}/gather.png"
    ADD_TROOP = f"{BASE_DIR}/add_troop_button.png"
    SEND_TROOP = f"{BASE_DIR}/send_troop_button.png"


def check_joan_rss():
    """Check if Joan RSS is available and print result"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.JOAN_RSS, confidence=0.8)
        if location is not None:
            print("Joan RSS found - resource available", flush=True)
            return True
        else:
            print("Joan RSS not found - resource not available", flush=True)
            return False
    except Exception:
        print("Joan RSS check failed - error occurred", flush=True)
        return False


def execute_resource_gathering():
    """Execute resource gathering sequence when Joan RSS not found"""
    try:
        # Step 1: Setup - Press ESC to clear UI
        check_and_click_help_button()
        check_and_click_close_esc()
        check_and_click_go_outside()
        
        # Click FIND_BAR
        if not try_click_button(AssetPaths.FIND_BAR):
            return False
        
        # Randomly select one of the resource types
        # resource_options = [AssetPaths.LUA_RSS, AssetPaths.GO_RSS, AssetPaths.DA_RSS]
        resource_options = [AssetPaths.LUA_RSS, AssetPaths.GO_RSS]
        selected_resource = random.choice(resource_options)
        resource_name = selected_resource.split('/')[-1].replace('.png', '')
        print(f"Selected resource: {resource_name}", flush=True)
        
        if not try_click_button(selected_resource):
            return False
        
        # Click CONFIRM_FIND
        if not retry_with_esc(AssetPaths.CONFIRM_FIND):
            return False
        
        # Click GATHER
        if not try_click_button(AssetPaths.GATHER):
            return False
        
        # Click ADD_TROOP
        if not retry_with_esc(AssetPaths.ADD_TROOP):
            return False
        
        # Click SEND_TROOP
        if not retry_with_esc(AssetPaths.SEND_TROOP):
            return False
        
        print("Resource gathering sequence completed successfully", flush=True)
        return True
        
    except Exception as e:
        print(f"Error in resource gathering: {e}", flush=True)
        return False


def main():
    """Main execution for resources sequence with continuous loop"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Resources Bot starting in {Config.STEP_DELAY()} seconds...")
    time.sleep(Config.STEP_DELAY())
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("Starting resources cycle...", flush=True)
            
            if check_joan_rss():
                print("Joan RSS available - no gathering needed", flush=True)
            else:
                print("Starting resource gathering sequence...", flush=True)
                if execute_resource_gathering():
                    print("Resource gathering cycle completed successfully", flush=True)
                else:
                    print("Resource gathering cycle failed, retrying...", flush=True)
            
            time.sleep(Config.STEP_DELAY())
            
    except KeyboardInterrupt:
        print("Resources bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    main()
