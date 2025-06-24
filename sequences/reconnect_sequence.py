"""
Reconnect Sequence - Handle disconnection recovery
"""
import pyautogui
import time
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot_utils import ensure_assets_directory

try:
    from .shared_utils import (
        try_click_button,
        retry_with_esc,
        Config
    )
except ImportError:
    from shared_utils import (
        try_click_button,
        retry_with_esc,
        Config
    )


class AssetPaths:
    """Asset paths for reconnect sequence"""
    BASE_DIR = "assets"
    RECONNECT = f"{BASE_DIR}/reconnect_button.png"


def check_and_click_reconnect() -> bool:
    """Check for reconnect button and click if found"""
    try:
        if try_click_button(AssetPaths.RECONNECT):
            print("Reconnect button found - clicking to reconnect", flush=True)
            return True
        return False
    except Exception as e:
        print(f"Error checking reconnect button: {e}", flush=True)
        return False


def execute_reconnect_sequence() -> bool:
    """Execute reconnect sequence"""
    try:
        print("Checking for disconnection/reconnect button...", flush=True)
        
        # Try to find and click reconnect button
        if check_and_click_reconnect():
            print("✅ Reconnect successful", flush=True)
            # Wait a bit longer for reconnection to complete
            time.sleep(3.0)
            return True
        else:
            print("No reconnect button found - connection appears stable", flush=True)
            return False
            
    except Exception as e:
        print(f"Error in reconnect sequence: {e}", flush=True)
        return False


def main():
    """Main execution for standalone reconnect bot"""
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("RoK Reconnect Bot starting...", flush=True)
    
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        while True:
            print("\n🔌 Checking for reconnection needs...", flush=True)
            
            if execute_reconnect_sequence():
                print("🔌 Reconnection completed", flush=True)
            else:
                print("🔌 No reconnection needed", flush=True)
            
            print("//============================================", flush=True)
            time.sleep(5.0)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("Reconnect bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)


if __name__ == "__main__":
    ensure_assets_directory()
    main()