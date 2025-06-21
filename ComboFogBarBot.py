"""
Combo Bot - Clean and optimized alternating Fog Scout and Barbarian Farming
"""
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
from enum import Enum
from bot_utils import ensure_assets_directory
from sequences import execute_fog_scout_sequence, execute_barbarian_farm_sequence


class ActivityType(Enum):
    """Types of activities the bot can perform"""
    FOG_SCOUT = "fog_scout"
    BARBARIAN_FARM = "barbarian_farm"


class Config:
    """Configuration for combo bot"""
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.3
    ACTIVITY_SWITCH_DELAY = 1.3


class ActivityTracker:
    """Track current activity and entry counts"""
    def __init__(self):
        self.current_activity = ActivityType.FOG_SCOUT
        self.fog_scout_entries = 0
        self.barbarian_farm_entries = 0
        self.total_cycles = 0
    
    def get_current_entries(self):
        """Get current entry count for active activity"""
        return (self.fog_scout_entries if self.current_activity == ActivityType.FOG_SCOUT 
                else self.barbarian_farm_entries)
    
    def increment_current_entries(self):
        """Increment entry count for current activity"""
        if self.current_activity == ActivityType.FOG_SCOUT:
            self.fog_scout_entries += 1
        else:
            self.barbarian_farm_entries += 1
    
    def should_switch_activity(self):
        """Always switch after each single cycle"""
        return True
    
    def switch_activity(self):
        """Switch to other activity and reset counter"""
        if self.current_activity == ActivityType.FOG_SCOUT:
            self.current_activity = ActivityType.BARBARIAN_FARM
            self.fog_scout_entries = 0
        else:
            self.current_activity = ActivityType.FOG_SCOUT
            self.barbarian_farm_entries = 0
        
        self.total_cycles += 1
        activity_name = ("Trinh Sát Sương Mù" if self.current_activity == ActivityType.FOG_SCOUT 
                        else "Farm Barbarian")
        print(f"Đã chuyển sang {activity_name}", flush=True)
    
    def print_status(self):
        """Print current status"""
        activity_name = ("Trinh Sát Sương Mù" if self.current_activity == ActivityType.FOG_SCOUT 
                        else "Farm Barbarian")
        print(f"Hoạt động hiện tại: {activity_name}")
        print(f"Tổng lần thực hiện: {self.get_current_entries()}")
        print(f"Tổng chu kỳ đã hoàn thành: {self.total_cycles}")


def execute_current_activity(tracker: ActivityTracker) -> bool:
    """Execute the current activity"""
    return (execute_fog_scout_sequence() if tracker.current_activity == ActivityType.FOG_SCOUT 
            else execute_barbarian_farm_sequence())


def main():
    """Main execution of combo bot"""
    print(f"RoK Combo Bot (Trinh Sát Sương Mù + Farm Barbarian) bắt đầu sau {Config.STARTUP_DELAY} giây...")
    print("Cấu hình: Chuyển hoạt động sau mỗi chu kỳ")
    time.sleep(Config.STARTUP_DELAY)
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = Config.SCREENSHOT_PAUSE
    
    tracker = ActivityTracker()
    
    try:
        while True:
            print(f"\n--- Chu Kỳ {tracker.get_current_entries() + 1} ---")
            tracker.print_status()
            
            # Execute current activity
            success = execute_current_activity(tracker)
            
            if success:
                tracker.increment_current_entries()
                print(f"Hoạt động hoàn thành thành công", flush=True)
            else:
                print("Hoạt động thất bại, sẽ thử lại sau khi chuyển nếu cần", flush=True)
                tracker.increment_current_entries()
            
            # Switch activity after each cycle
            if tracker.should_switch_activity():
                print("\nChuyển sang hoạt động khác sau 1 chu kỳ", flush=True)
                tracker.switch_activity()
                
                # Wait before starting next activity
                print(f"Chờ {Config.ACTIVITY_SWITCH_DELAY}s trước khi bắt đầu hoạt động tiếp theo...", flush=True)
                time.sleep(Config.ACTIVITY_SWITCH_DELAY)
            else:
                time.sleep(Config.ACTIVITY_SWITCH_DELAY)
            
    except KeyboardInterrupt:
        print("\nCombo bot đã dừng bởi người dùng", flush=True)
        tracker.print_status()
        
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}", flush=True)
        tracker.print_status()


if __name__ == "__main__":
    ensure_assets_directory()
    main()