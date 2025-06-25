"""
Barbarian Farm Sequence - Clean and optimized with stamina management
"""
import pyautogui
import time
import sys
import os
import cv2
import numpy as np
import re
import threading
from datetime import datetime
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

# Stamina detection imports
try:
    import pytesseract
    from PIL import Image
    
    # Try to set Tesseract path for Windows
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe',
        '/usr/bin/tesseract',
        '/usr/local/bin/tesseract'
    ]
    
    for path in possible_paths:
        expanded_path = os.path.expanduser(os.path.expandvars(path))
        if os.path.exists(expanded_path):
            pytesseract.pytesseract.tesseract_cmd = expanded_path
            break
    
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

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
    ADD_TROOP = f"{BASE_DIR}/commander_barbarian.png"  # Same as COMMANDER
    SEND_TROOP = f"{BASE_DIR}/send_troop_available.png"
    TROOP_AVAILABLE = f"{BASE_DIR}/icon_troop_available.png"
    COMMANDER_ONDUTY = f"{BASE_DIR}/commander_onduty.png"
    COMMANDER_BACK = f"{BASE_DIR}/commander_onduty.png"  # Same as COMMANDER_ONDUTY
    HOME_CENTER = f"{BASE_DIR}/home_center.png"
    # Alternative buttons when no commander
    ADD_TROOP_ALT = f"{BASE_DIR}/add_troop_button.png"
    SEND_TROOP_ALT = f"{BASE_DIR}/send_troop_button.png"
    SELECT_TROOP_ALT = f"{BASE_DIR}/select_troop_button.png"
    # Stamina and commander management
    STAMINA_CHECK = f"{BASE_DIR}/stamina_check.png"
    TROOP_BACK = f"{BASE_DIR}/troop_back.png"

# Stamina management constants
MIN_STAMINA = 39

def check_troop_available() -> bool:
    """Check if troops are available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.TROOP_AVAILABLE, confidence=0.7)
        return location is not None
    except Exception:
        return False

def check_commander_onduty() -> bool:
    """Check if commander is on duty"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.COMMANDER_ONDUTY, confidence=0.6)
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

def check_commander_back_available() -> bool:
    """Check if commander is available"""
    try:
        location = pyautogui.locateOnScreen(AssetPaths.COMMANDER_BACK, confidence=0.6)
        return location is not None
    except Exception:
        return False

def find_stamina_check_position():
    """Find stamina_check.png position on screen"""
    try:
        stamina_check_path = AssetPaths.STAMINA_CHECK
        
        # Take screenshot
        screenshot = np.array(pyautogui.screenshot())
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        
        # Load template image
        template = cv2.imread(stamina_check_path)
        if template is None:
            print(f"Error: Could not load {stamina_check_path}")
            return None
        
        # Convert to grayscale for template matching
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        # Check if match is good enough
        if max_val > 0.6:
            h, w = template_gray.shape
            print(f"Stamina check found with confidence: {max_val:.3f}")
            return (max_loc[0], max_loc[1], w, h)  # Return top-left corner and dimensions
        else:
            print(f"Stamina check not found (confidence: {max_val:.3f})")
            return None
            
    except Exception as e:
        print(f"Error finding stamina check: {e}")
        return None

def get_current_stamina() -> int:
    """Extract current stamina value"""
    if not TESSERACT_AVAILABLE:
        print("Tesseract not available for stamina detection")
        return 0
    
    try:
        # Find stamina check position first
        stamina_pos = find_stamina_check_position()
        if not stamina_pos:
            print("Could not find stamina check position")
            return 0
        
        stamina_x, stamina_y, stamina_w, stamina_h = stamina_pos
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Crop the stamina check area itself
        cropped = screenshot.crop((stamina_x, stamina_y, stamina_x + stamina_w, stamina_y + stamina_h))
        
        # Try Tesseract OCR with PSM 6 and 7 (known to work best)
        ocr_configs = ['--psm 6', '--psm 7']
        
        for config in ocr_configs:
            try:
                text = pytesseract.image_to_string(cropped, config=config)
                text = text.strip()
                
                if text and ('/' in text) and any(c.isdigit() for c in text):
                    # Look for stamina patterns - Most specific patterns first
                    patterns = [
                        r'(\d+[,.]\d+)/1[,.]500',     # 1,015/1.500 or 1.015/1,500 (with separators)
                        r'(\d+)/1[,.]500',            # 352/1.500 or 352/1,500 (no separator in stamina)
                        r'(\d+[,.]\d+)/\d+',          # Any XXX,XXX/YYY or XXX.XXX/YYY pattern
                        r'(\d+)/\d+',                 # Any XXX/YYY pattern (fallback)
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, text)
                        if matches:
                            print(f"OCR text: '{text}'", flush=True)
                            print(f"Matched pattern: {pattern}", flush=True)
                            print(f"Raw match: '{matches[0]}'", flush=True)
                            # Remove separators (periods, commas) from the stamina value
                            stamina_str = matches[0].replace('.', '').replace(',', '')
                            stamina_value = int(stamina_str)
                            print(f"Parsed stamina: {stamina_value}", flush=True)
                            return stamina_value
            except Exception as e:
                continue
        
        print("Could not extract stamina value")
        return 0
        
    except Exception as e:
        print(f"Error extracting stamina: {e}")
        return 0

def handle_low_stamina(combo_mode: bool = False) -> str:
    """Handle low stamina situation - try to recall troops"""
    print(f"Stamina is low, attempting to recall troops...")
    
    # Check if commander is available
    if check_commander_back_available():
        print("Commander found - clicking commander")
        if try_click_button(AssetPaths.COMMANDER_BACK):
            time.sleep(1)
            # Try to click troop back button
            if try_click_button(AssetPaths.TROOP_BACK):
                print("Troops recalled successfully")
                if combo_mode:
                    print("Running in combo mode - returning STAMINA_LOW status")
                    return "STAMINA_LOW"
                else:
                    print("Standalone mode - waiting 10 minutes for stamina recovery")
                    time.sleep(600)  # Sleep 10 minutes (600 seconds)
                    return "SUCCESS"
            else:
                print("Could not find troop back button")
                pyautogui.press('escape')  # Close commander window
                return "FAILED"
    else:
        print("No commander found - waiting 10 seconds for troops to return")
        time.sleep(10)
        return "FAILED"

def execute_barbarian_farm_sequence(combo_mode: bool = False) -> str:
    """Execute barbarian farm sequence with stamina management"""
    # Step 1: Setup - Press ESC to clear UI
    check_and_click_help_button()
    # Check commander and troop availability logic
    print("Checking commander on duty status...", flush=True)
    commander_onduty = check_commander_onduty()
    print(f"Commander on duty: {commander_onduty}", flush=True)
    
    print("Checking troop availability...", flush=True)
    troops_available = check_troop_available()
    print(f"Troops available: {troops_available}", flush=True)
    
    if commander_onduty and not troops_available:
        print("Commander on duty but no troops available - ending session", flush=True)
        return "FAILED"
    else:
        print("===> proceeding with attack", flush=True)

    check_and_click_close_esc()
    check_and_click_go_outside()

    print("Open setting by ESC", flush=True)
    pyautogui.press('escape')
    time.sleep(0.5)

    # Step 2: Check stamina
    current_stamina = get_current_stamina()
    if current_stamina == 0:
        print("Could not detect stamina, proceeding anyway", flush=True)
        pyautogui.press('escape')
        time.sleep(0.5)
    elif current_stamina <= MIN_STAMINA:
        print(f"Stamina too low ({current_stamina} <= {MIN_STAMINA})", flush=True)
        pyautogui.press('escape')
        time.sleep(0.5)
        return handle_low_stamina(combo_mode)
    else:
        print(f"Stamina sufficient ({current_stamina} > {MIN_STAMINA}), proceeding with attack", flush=True)
        pyautogui.press('escape')
        time.sleep(0.5)

    # Check and click HOME_CENTER if found
    if try_click_button_silent(AssetPaths.HOME_CENTER):
        print("HOME_CENTER found - clicked it", flush=True)
        time.sleep(0.5)
    else:
        print("HOME_CENTER not found - continuing process", flush=True)

    # Step 3-5: Normal barbarian attack flow
    # Execute initial sequence
    if not try_click_button(AssetPaths.FIND_BAR):
        return "FAILED"
    
    # Critical buttons with ESC retry
    if not retry_with_esc(AssetPaths.CONFIRM_FIND):
        return "FAILED"
    
    if not retry_with_esc(AssetPaths.ATTACK):
        return "FAILED"
    
    # Smart flow based on commander availability
    if check_commander_available():
        print("Commander found - using normal flow", flush=True)
        if not retry_with_esc(AssetPaths.ADD_TROOP):
            return "FAILED"
        if not retry_with_esc(AssetPaths.SEND_TROOP):
            return "FAILED"
    else:
        print("No commander found - using alternative flow", flush=True)
        if not retry_with_esc(AssetPaths.ADD_TROOP_ALT):
            return "FAILED"
        if not retry_with_esc(AssetPaths.SELECT_TROOP_ALT):
            return "FAILED"
        if not retry_with_esc(AssetPaths.SEND_TROOP_ALT):
            return "FAILED"
    
    return "SUCCESS"


def main():
    """Main execution for standalone barbarian farm bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"RoK Barbarian Farm Bot starting in {Config.STEP_DELAY()} seconds...")
    print("🔴 Press F12 anytime to stop the bot")
    time.sleep(Config.STEP_DELAY())
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    # Start F12 key monitoring in a separate thread
    f12_thread = threading.Thread(target=monitor_f12_key, daemon=True)
    f12_thread.start()
    
    try:
        cycle_count = 1
        while True:
            # Check if F12 was pressed
            if stop_bot_flag.is_set():
                print("🛑 Bot stopped by F12 key press", flush=True)
                break
            print(f"\n🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥", flush=True)
            print(f"🔥                      BARBARIAN FARM CHU KỲ {cycle_count:<3}                   🔥", flush=True)
            print(f"🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥", flush=True)
            
            result = execute_barbarian_farm_sequence(combo_mode=False)
            if result == "SUCCESS":
                print("✅ Barbarian farm cycle completed successfully", flush=True)
            elif result == "STAMINA_LOW":
                print("⚠️  Stamina low - troops recalled, waited 10 minutes", flush=True)
            else:
                print("❌ Barbarian farm cycle failed, retrying...", flush=True)
            
            print("//==============================================================", flush=True)
            cycle_count += 1
            time.sleep(Config.STEP_DELAY())
            
    except KeyboardInterrupt:
        print("Barbarian farm bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()