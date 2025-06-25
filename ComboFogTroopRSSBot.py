"""
Combo Bot - Fog Scout + Troop Training (Infantry, Archers, Cavalry, Siege)
"""
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
import threading
from enum import Enum
from bot_utils import ensure_assets_directory
from sequences import (
    execute_fog_scout_sequence,
    execute_infantry_sequence,
    execute_archers_sequence,
    execute_cavalry_sequence,
    execute_siege_sequence
)
from sequences.resources_sequence import check_joan_rss, check_gaius_rss, check_constance_rss, check_sarka_rss, execute_resource_gathering
from sequences.reconnect_sequence import execute_reconnect_sequence

# Global flag for F12 stop signal
stop_bot_flag = threading.Event()


def monitor_f12_key():
    """Monitor for F12 key press to stop the bot"""
    try:
        import keyboard
        print("F12 key monitoring active - Press F12 to stop the bot", flush=True)
        keyboard.wait('f12')
        print("F12 pressed - Stopping bot...", flush=True)
        stop_bot_flag.set()
    except ImportError:
        print("keyboard module not available - F12 monitoring disabled", flush=True)
    except Exception as e:
        print(f"Error in F12 monitoring: {e}", flush=True)


class ActivityType(Enum):
    """Types of activities the bot can perform"""
    FOG_SCOUT = "fog_scout"
    INFANTRY = "infantry"
    ARCHERS = "archers"
    CAVALRY = "cavalry"
    SIEGE = "siege"
    RESOURCES = "resources"


class Config:
    """Configuration for combo bot"""
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.3
    ACTIVITY_SWITCH_DELAY = 1.5


class ActivityTracker:
    """Track current activity and entry counts"""
    def __init__(self):
        self.activities = [
            ActivityType.FOG_SCOUT,
            ActivityType.INFANTRY,
            ActivityType.FOG_SCOUT,
            ActivityType.RESOURCES,
            ActivityType.ARCHERS,
            ActivityType.FOG_SCOUT,
            ActivityType.RESOURCES,
            ActivityType.CAVALRY,
            ActivityType.FOG_SCOUT,
            ActivityType.RESOURCES,
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
            ActivityType.INFANTRY: "Huấn Luyện Bộ Binh",
            ActivityType.ARCHERS: "Huấn Luyện Cung Thủ",
            ActivityType.CAVALRY: "Huấn Luyện Kỵ Binh",
            ActivityType.SIEGE: "Huấn Luyện Công Thành",
            ActivityType.RESOURCES: "Thu Thập Tài Nguyên"
        }
        
        activity_name = activity_names[self.current_activity]
        print(f"\n★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★", flush=True)
        print(f"★                   CHUYỂN HOẠT ĐỘNG                    ★", flush=True) 
        print(f"★              Đã chuyển sang {activity_name:<18} ★", flush=True)
        print(f"★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★", flush=True)
    
    def print_status(self):
        """Print current status"""
        activity_names = {
            ActivityType.FOG_SCOUT: "Trinh Sát Sương Mù",
            ActivityType.INFANTRY: "Huấn Luyện Bộ Binh",
            ActivityType.ARCHERS: "Huấn Luyện Cung Thủ",
            ActivityType.CAVALRY: "Huấn Luyện Kỵ Binh",
            ActivityType.SIEGE: "Huấn Luyện Công Thành",
            ActivityType.RESOURCES: "Thu Thập Tài Nguyên"
        }
        
        activity_name = activity_names[self.current_activity]
        print(f"┌─────────────────────────────────────────────────────┐", flush=True)
        print(f"│  🎯 Hoạt động hiện tại: {activity_name:<20} │", flush=True)
        print(f"│  🔄 Lần thực hiện: {self.get_current_entries():<25} │", flush=True)
        print(f"│  ✅ Tổng chu kỳ hoàn thành: {self.total_cycles:<18} │", flush=True)
        print(f"└─────────────────────────────────────────────────────┘", flush=True)


def execute_current_activity(tracker: ActivityTracker) -> bool:
    """Execute the current activity"""
    if tracker.current_activity == ActivityType.RESOURCES:
        # Resources activity has special logic - check if 3 out of 4 RSS commanders are available
        rss_checks = [
            check_joan_rss(),
            check_gaius_rss(), 
            check_constance_rss(),
            check_sarka_rss()
        ]
        available_count = sum(rss_checks)
        
        if available_count >= 3:
            print(f"RSS commanders available ({available_count}/4) - no gathering needed", flush=True)
            return True
        else:
            print("Starting resource gathering sequence...", flush=True)
            return execute_resource_gathering()
    
    activity_map = {
        ActivityType.FOG_SCOUT: execute_fog_scout_sequence,
        ActivityType.INFANTRY: execute_infantry_sequence,
        ActivityType.ARCHERS: execute_archers_sequence,
        ActivityType.CAVALRY: execute_cavalry_sequence,
        ActivityType.SIEGE: execute_siege_sequence
    }
    
    return activity_map[tracker.current_activity]()


def main():
    """Main execution of combo bot"""
    print(f"RoK Combo Bot (Fog Scout + Troop Training) bắt đầu sau {Config.STARTUP_DELAY} giây...")
    print("Cấu hình: Fog Scout → Infantry → Archers → Cavalry → Siege → Resources → Lặp lại")
    print("🔴 Press F12 anytime to stop the bot")
    time.sleep(Config.STARTUP_DELAY)
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = Config.SCREENSHOT_PAUSE
    
    tracker = ActivityTracker()
    
    # Start F12 key monitoring in a separate thread
    f12_thread = threading.Thread(target=monitor_f12_key, daemon=True)
    f12_thread.start()
    
    try:
        while True:
            # Check if F12 was pressed
            if stop_bot_flag.is_set():
                print("🛑 Bot stopped by F12 key press", flush=True)
                break
            print(f"\n🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥", flush=True)
            print(f"🔥                        HOẠT ĐỘNG {tracker.get_current_entries() + 1:<3}                        🔥", flush=True)
            print(f"🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥", flush=True)
            tracker.print_status()
            
            # Execute current activity
            success = execute_current_activity(tracker)
            
            if success:
                tracker.increment_current_entries()
                print(f"✅ Hoạt động hoàn thành thành công", flush=True)
            else:
                print("❌ Hoạt động thất bại, sẽ thử lại sau khi chuyển nếu cần", flush=True)
                tracker.increment_current_entries()
            
            # Check for reconnection needs
            print(f"\n🔌 Kiểm tra kết nối...", flush=True)
            reconnect_result = execute_reconnect_sequence()
            if reconnect_result:
                print("🔌 Đã kết nối lại thành công", flush=True)
            
            # Switch to next activity after each cycle
            if tracker.should_switch_activity():
                print(f"\n⚡⚡⚡ ĐANG CHUYỂN ĐỔII HOẠT ĐỘNG TIẾP THEO ⚡⚡⚡", flush=True)
                tracker.switch_activity()
                
                # Wait before starting next activity
                print(f"⏰ Chờ {Config.ACTIVITY_SWITCH_DELAY}s trước khi bắt đầu hoạt động tiếp theo...", flush=True)
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