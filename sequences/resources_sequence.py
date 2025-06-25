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
        check_and_click_if_found,
        try_click_button_silent,
        move_mouse_zigzag,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        retry_with_esc,
        check_and_click_go_outside,
        check_and_click_close_esc,
        check_and_click_help_button,
        check_and_click_if_found,
        try_click_button_silent,
        move_mouse_zigzag,
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
    GAIUS_RSS = f"{BASE_DIR}/gaius.png"
    CONSTANCE_RSS = f"{BASE_DIR}/constance.png"
    SARKA_RSS = f"{BASE_DIR}/sarka.png"
    CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
    GATHER = f"{BASE_DIR}/gather.png"
    ADD_TROOP = f"{BASE_DIR}/add_troop_button.png"
    SEND_TROOP = f"{BASE_DIR}/send_troop_button.png"
    REMOVE_SECOND_COMMANDER = f"{BASE_DIR}/remove_second_commander.png"
    SAVE_TROOP = f"{BASE_DIR}/save_troop.png"
    HOME_CENTER = f"{BASE_DIR}/home_center.png"


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

def check_gaius_rss():
    """Check if Gaius RSS is available and print result"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.GAIUS_RSS, confidence=0.8)
        if location is not None:
            print("Gaius RSS found - resource available", flush=True)
            return True
        else:
            print("Gaius RSS not found - resource not available", flush=True)
            return False
    except Exception:
        print("Gaius RSS check failed - error occurred", flush=True)
        return False

def check_constance_rss():
    """Check if Constance RSS is available and print result"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.CONSTANCE_RSS, confidence=0.8)
        if location is not None:
            print("Constance RSS found - resource available", flush=True)
            return True
        else:
            print("Constance RSS not found - resource not available", flush=True)
            return False
    except Exception:
        print("Constance RSS check failed - error occurred", flush=True)
        return False

def check_sarka_rss():
    """Check if Sarka RSS is available and print result"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.SARKA_RSS, confidence=0.8)
        if location is not None:
            print("Sarka RSS found - resource available", flush=True)
            return True
        else:
            print("Sarka RSS not found - resource not available", flush=True)
            return False
    except Exception:
        print("Sarka RSS check failed - error occurred", flush=True)
        return False

def execute_resource_gathering():
    """Execute resource gathering sequence when Joan RSS not found"""
    try:
        # Step 1: Setup - Press ESC to clear UI
        check_and_click_help_button()
        check_and_click_close_esc()
        check_and_click_go_outside()
        
        # Check and click HOME_CENTER if found
        if try_click_button_silent(AssetPaths.HOME_CENTER):
            print("HOME_CENTER found - clicked it", flush=True)
            time.sleep(0.5)
        else:
            print("HOME_CENTER not found - continuing process", flush=True)
        
        # Click FIND_BAR
        if not try_click_button(AssetPaths.FIND_BAR):
            return False
        
        # Randomly select one of the resource types
        resource_options = [AssetPaths.LUA_RSS, AssetPaths.GO_RSS, AssetPaths.DA_RSS]
        # resource_options = [AssetPaths.LUA_RSS, AssetPaths.GO_RSS]
        # resource_options = [AssetPaths.GO_RSS]
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
        
        # Check if remove second commander button is found and click it
        check_and_click_if_found(AssetPaths.REMOVE_SECOND_COMMANDER, "Remove second commander")
        
        # Check if save_troop found and click 10 pixels to the left of its center
        try:
            location = pyautogui.locateOnScreen(AssetPaths.SAVE_TROOP, confidence=0.8)
            if location is not None:
                print("Save troop found - clicking 10 pixels to the left", flush=True)
                center_x = location.left + location.width // 2
                center_y = location.top + location.height // 2
                click_x = center_x - 30  # Move 30 pixels to the left
                move_mouse_zigzag(click_x, center_y)
                pyautogui.click(click_x, center_y)
                time.sleep(Config.STEP_DELAY())
            else:
                print("Save troop not found - continuing", flush=True)
        except Exception as e:
            print(f"Error checking save troop: {e}", flush=True)
        
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
            
            # Check RSS commanders and count how many are available
            rss_checks = [
                check_joan_rss(),
                check_gaius_rss(), 
                check_constance_rss(),
                check_sarka_rss()
            ]
            available_count = sum(rss_checks)
            
            if available_count >= 3:
                print(f"RSS commanders available ({available_count}/4) - no gathering needed", flush=True)
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
