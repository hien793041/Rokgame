"""
Combo Bot - Fog Scout + Barbarian Farming (2-activity cycle)
"""
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
import random
import threading
from enum import Enum
from bot_utils import ensure_assets_directory
from sequences import execute_fog_scout_sequence, execute_barbarian_farm_sequence

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
    BARBARIAN_FARM = "barbarian_farm"


class Config:
    """Configuration for combo bot"""
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.3
    MIN_DELAY = 1.3
    MAX_DELAY = 1.5
    
    @staticmethod
    def get_random_delay():
        """Get random delay between 1.3-1.5 seconds"""
        return random.uniform(Config.MIN_DELAY, Config.MAX_DELAY)


class ActivityTracker:
    """Track current activity and entry counts"""
    def __init__(self):
        self.activities = [
            ActivityType.FOG_SCOUT,
            ActivityType.BARBARIAN_FARM
        ]
        self.current_index = 0
        self.activity_counts = {activity: 0 for activity in self.activities}
        self.total_cycles = 0
        self.barbarian_recovery_until = 0  # Timestamp when barbarian can resume
    
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
    
    def is_barbarian_recovering(self):
        """Check if barbarian is in recovery period"""
        return time.time() < self.barbarian_recovery_until
    
    def set_barbarian_recovery(self, minutes=10):
        """Set barbarian recovery period"""
        self.barbarian_recovery_until = time.time() + (minutes * 60)
        print(f"Barbarian stamina low - recovery period set for {minutes} minutes", flush=True)
    
    def get_barbarian_recovery_remaining(self):
        """Get remaining recovery time in minutes"""
        remaining = self.barbarian_recovery_until - time.time()
        return max(0, remaining / 60)
    
    def switch_activity(self):
        """Switch to next activity in sequence, considering barbarian recovery"""
        # If barbarian is recovering, only run fog scouting
        if self.is_barbarian_recovering():
            if self.current_activity == ActivityType.BARBARIAN_FARM:
                # Skip barbarian, go to fog
                self.current_index = 0  # Fog scout index
                remaining = self.get_barbarian_recovery_remaining()
                print(f"Skipping barbarian (recovery: {remaining:.1f} min left) → Fog", flush=True)
            else:
                # Stay on fog scouting
                print(f"Staying on fog scouting (barbarian recovery: {self.get_barbarian_recovery_remaining():.1f} min left)", flush=True)
        else:
            # Normal switching
            self.current_index = (self.current_index + 1) % len(self.activities)
            
            if self.current_index == 0:  # Completed full cycle
                self.total_cycles += 1
        
        activity_names = {
            ActivityType.FOG_SCOUT: "Trinh Sát Sương Mù",
            ActivityType.BARBARIAN_FARM: "Farm Barbarian"
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
            ActivityType.BARBARIAN_FARM: "Farm Barbarian"
        }
        
        activity_name = activity_names[self.current_activity]
        print(f"┌─────────────────────────────────────────────────────┐", flush=True)
        print(f"│  🎯 Hoạt động hiện tại: {activity_name:<20} │", flush=True)
        print(f"│  🔄 Lần thực hiện: {self.get_current_entries():<25} │", flush=True)
        print(f"│  ✅ Tổng chu kỳ hoàn thành: {self.total_cycles:<18} │", flush=True)
        print(f"└─────────────────────────────────────────────────────┘", flush=True)


def execute_current_activity(tracker: ActivityTracker) -> str:
    """Execute the current activity"""
    current_activity = tracker.current_activity
    
    # Skip barbarian if in recovery period
    if current_activity == ActivityType.BARBARIAN_FARM and tracker.is_barbarian_recovering():
        remaining = tracker.get_barbarian_recovery_remaining()
        print(f"Skipping barbarian activity - still recovering ({remaining:.1f} min left)", flush=True)
        return "SKIPPED"
    
    if current_activity == ActivityType.FOG_SCOUT:
        result = execute_fog_scout_sequence()
        return "SUCCESS" if result else "FAILED"
    
    elif current_activity == ActivityType.BARBARIAN_FARM:
        result = execute_barbarian_farm_sequence(combo_mode=True)
        
        # Handle barbarian-specific results
        if result == "STAMINA_LOW":
            tracker.set_barbarian_recovery(10)  # 10 minute recovery
            return "STAMINA_LOW"
        
        return result
    
    return "FAILED"


def main():
    """Main execution of combo bot"""
    print(f"RoK Combo Bot (Fog + Barbarian) bắt đầu sau {Config.STARTUP_DELAY} giây...")
    print("Cấu hình: Fog Scout → Barbarian Farm → Lặp lại")
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
            print(f"🔥                           CHU KỲ {tracker.get_current_entries() + 1:<3}                            🔥", flush=True)
            print(f"🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥", flush=True)
            tracker.print_status()
            
            # Execute current activity
            result = execute_current_activity(tracker)
            
            # Random delay after activity execution
            delay = Config.get_random_delay()
            print(f"Chờ {delay:.1f}s sau khi hoàn thành hoạt động...", flush=True)
            time.sleep(delay)
            
            # Handle different result types
            if result == "SUCCESS":
                tracker.increment_current_entries()
                print(f"✅ Hoạt động hoàn thành thành công", flush=True)
            elif result == "STAMINA_LOW":
                tracker.increment_current_entries()
                print(f"⚠️  Barbarian stamina low - troops recalled, entering recovery mode", flush=True)
            elif result == "SKIPPED":
                # Don't increment for skipped activities
                print(f"⏭️  Hoạt động đã bỏ qua do đang phục hồi", flush=True)
            else:
                print("❌ Hoạt động thất bại, sẽ thử lại sau khi chuyển nếu cần", flush=True)
                tracker.increment_current_entries()
            
            # Switch activity after each cycle
            if tracker.should_switch_activity():
                print(f"\n⚡⚡⚡ ĐANG CHUYỂN ĐỔII HOẠT ĐỘNG SAU 1 CHU KỲ ⚡⚡⚡", flush=True)
                tracker.switch_activity()
                
                # Random delay before starting next activity
                switch_delay = Config.get_random_delay()
                print(f"⏰ Chờ {switch_delay:.1f}s trước khi bắt đầu hoạt động tiếp theo...", flush=True)
                time.sleep(switch_delay)
            else:
                delay = Config.get_random_delay()
                time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nCombo bot đã dừng bởi người dùng", flush=True)
        tracker.print_status()
        
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}", flush=True)
        tracker.print_status()


if __name__ == "__main__":
    ensure_assets_directory()
    main()