"""
Combo Bot - Fog Scout + Barbarian Farming + Troop Training (6-activity cycle)
"""
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
from enum import Enum
from bot_utils import ensure_assets_directory
from sequences import (
    execute_fog_scout_sequence, 
    execute_barbarian_farm_sequence,
    execute_infantry_sequence,
    execute_archers_sequence,
    execute_cavalry_sequence,
    execute_siege_sequence
)


class ActivityType(Enum):
    """Types of activities the bot can perform"""
    FOG_SCOUT = "fog_scout"
    BARBARIAN_FARM = "barbarian_farm"
    INFANTRY = "infantry"
    ARCHERS = "archers"
    CAVALRY = "cavalry"
    SIEGE = "siege"


class Config:
    """Configuration for combo bot"""
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.3
    ACTIVITY_SWITCH_DELAY = 1.3


class ActivityTracker:
    """Track current activity and entry counts"""
    def __init__(self):
        self.activities = [
            ActivityType.FOG_SCOUT,
            ActivityType.BARBARIAN_FARM,
            ActivityType.INFANTRY,
            ActivityType.ARCHERS,
            ActivityType.CAVALRY,
            ActivityType.SIEGE
        ]
        self.current_index = 0
        self.activity_counts = {activity: 0 for activity in self.activities}
        self.total_cycles = 0
    
    @property
    def current_activity(self):
        """Get current activity"""
        return self.activities[self.current_index]
    
    def get_current_entries(self):
        """Get current entry count for active activity"""
        return self.activity_counts[self.current_activity]
    
    def increment_current_entries(self):
        """Increment entry count for current activity"""
        self.activity_counts[self.current_activity] += 1
    
    def should_switch_activity(self):
        """Always switch after each single cycle"""
        return True
    
    def switch_activity(self):
        """Switch to next activity in sequence"""
        self.current_index = (self.current_index + 1) % len(self.activities)
        
        if self.current_index == 0:  # Completed full cycle
            self.total_cycles += 1
        
        activity_names = {
            ActivityType.FOG_SCOUT: "Trinh Sát Sương Mù",
            ActivityType.BARBARIAN_FARM: "Farm Barbarian",
            ActivityType.INFANTRY: "Huấn Luyện Bộ Binh",
            ActivityType.ARCHERS: "Huấn Luyện Cung Thủ",
            ActivityType.CAVALRY: "Huấn Luyện Kỵ Binh",
            ActivityType.SIEGE: "Huấn Luyện Công Thành"
        }
        
        activity_name = activity_names[self.current_activity]
        print(f"Đã chuyển sang {activity_name}", flush=True)
    
    def print_status(self):
        """Print current status"""
        activity_names = {
            ActivityType.FOG_SCOUT: "Trinh Sát Sương Mù",
            ActivityType.BARBARIAN_FARM: "Farm Barbarian",
            ActivityType.INFANTRY: "Huấn Luyện Bộ Binh",
            ActivityType.ARCHERS: "Huấn Luyện Cung Thủ",
            ActivityType.CAVALRY: "Huấn Luyện Kỵ Binh",
            ActivityType.SIEGE: "Huấn Luyện Công Thành"
        }
        
        activity_name = activity_names[self.current_activity]
        print(f"Hoạt động hiện tại: {activity_name}")
        print(f"Lần thực hiện hoạt động này: {self.get_current_entries()}")
        print(f"Tổng chu kỳ đầy đủ đã hoàn thành: {self.total_cycles}")


def execute_current_activity(tracker: ActivityTracker) -> bool:
    """Execute the current activity"""
    activity_map = {
        ActivityType.FOG_SCOUT: execute_fog_scout_sequence,
        ActivityType.BARBARIAN_FARM: execute_barbarian_farm_sequence,
        ActivityType.INFANTRY: execute_infantry_sequence,
        ActivityType.ARCHERS: execute_archers_sequence,
        ActivityType.CAVALRY: execute_cavalry_sequence,
        ActivityType.SIEGE: execute_siege_sequence
    }
    
    return activity_map[tracker.current_activity]()


def main():
    """Main execution of combo bot"""
    print(f"RoK Combo Bot (Fog + Barbarian + Troop Training) bắt đầu sau {Config.STARTUP_DELAY} giây...")
    print("Cấu hình: Fog → Barbarian → Infantry → Archers → Cavalry → Siege → Lặp lại")
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