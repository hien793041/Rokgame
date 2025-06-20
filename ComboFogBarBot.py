"""
Combo Bot - Alternating Fog Scout and Barbarian Farming
Switches between activities with max 2 entries per session
"""
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
import random
from enum import Enum
from bot_utils import click_button, ensure_assets_directory


class ActivityType(Enum):
    """Types of activities the bot can perform"""
    FOG_SCOUT = "fog_scout"
    BARBARIAN_FARM = "barbarian_farm"


class Config:
    """Configuration for combo bot"""
    MIN_RETRY_WAIT = 1
    MAX_RETRY_WAIT = 2
    MAX_RETRIES = 2
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.3
    
    # Wait times between activities
    ACTIVITY_SWITCH_DELAY_MIN = 2
    ACTIVITY_SWITCH_DELAY_MAX = 4
    ESC_WAIT_AFTER = 1.5


class AssetPaths:
    """Asset paths for both activities"""
    
    # Fog Scout assets
    class FogScout:
        BASE_DIR = "assets/fog"
        SCOUT_CAMP = f"{BASE_DIR}/scout_camp.png"
        EXPLORE = f"{BASE_DIR}/explore_button.png"
        CONFIRM = f"{BASE_DIR}/confirm_button.png"
        SEND = f"{BASE_DIR}/send_button.png"
    
    # Barbarian Farm assets
    class BarbarianFarm:
        BASE_DIR = "assets/barbarian"
        FIND_BAR = f"{BASE_DIR}/find_bar_button.png"
        CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
        ATTACK = f"{BASE_DIR}/attack_button.png"
        ADD_TROOP = f"{BASE_DIR}/add_troop_button.png"
        SEND_TROOP = f"{BASE_DIR}/send_troop_button.png"
    
    # Shared assets
    class Shared:
        BASE_DIR = "assets"
        GO_OUTSIDE = f"{BASE_DIR}/go_outside.png"
        GO_HOME = f"{BASE_DIR}/go_home.png"
        CLOSE_ESC = f"{BASE_DIR}/close_esc.png"
        HELP_BUTTON = f"{BASE_DIR}/help_button.png"


class ActivityTracker:
    """Track current activity and entry counts"""
    def __init__(self):
        self.current_activity = ActivityType.FOG_SCOUT
        self.fog_scout_entries = 0
        self.barbarian_farm_entries = 0
        self.total_cycles = 0
    
    def get_current_entries(self):
        """Get current entry count for active activity"""
        if self.current_activity == ActivityType.FOG_SCOUT:
            return self.fog_scout_entries
        else:
            return self.barbarian_farm_entries
    
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
        """Chuyển sang hoạt động khác và reset bộ đếm"""
        if self.current_activity == ActivityType.FOG_SCOUT:
            self.current_activity = ActivityType.BARBARIAN_FARM
            self.fog_scout_entries = 0
        else:
            self.current_activity = ActivityType.FOG_SCOUT
            self.barbarian_farm_entries = 0
        
        self.total_cycles += 1
        activity_name = "Trinh Sát Sương Mù" if self.current_activity == ActivityType.FOG_SCOUT else "Farm Barbarian"
        print(f"Đã chuyển sang {activity_name}", flush=True)
    
    def print_status(self):
        """In trạng thái hiện tại"""
        activity_name = "Trinh Sát Sương Mù" if self.current_activity == ActivityType.FOG_SCOUT else "Farm Barbarian"
        print(f"Hoạt động hiện tại: {activity_name}")
        print(f"Tổng lần thực hiện: {self.get_current_entries()}")
        print(f"Tổng chu kỳ đã hoàn thành: {self.total_cycles}")


# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = Config.SCREENSHOT_PAUSE




def try_click_button_with_retry(button_path: str, button_name: str, max_retries: int = None) -> bool:
    """Thử click nút với nhiều lần thử lại"""
    if max_retries is None:
        max_retries = Config.MAX_RETRIES
        
    for attempt in range(max_retries):
        if click_button(button_path):
            time.sleep(random.uniform(0.5, 1.0))
            return True
        
        print(f"Không tìm thấy nút '{button_name}', thử lại {attempt + 1}/{max_retries}", flush=True)
        time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
    
    print(f"Không thể tìm thấy '{button_name}' sau {max_retries} lần thử, nhấn ESC...", flush=True)
    pyautogui.press('escape')  # Nhấn ESC khi hết số lần thử
    time.sleep(random.uniform(1.0, 1.5))  # Chờ sau khi nhấn ESC
    return False


def check_and_click_go_home() -> bool:
    """Kiểm tra và click nút về nhà nếu tìm thấy"""
    print("Đang kiểm tra nút về nhà...", flush=True)
    
    # Thử tìm nút về nhà nhưng không nhấn ESC khi thất bại
    if try_click_button_without_esc(AssetPaths.Shared.GO_HOME, "Về Nhà", 2):
        print("Đã tìm thấy và click nút về nhà", flush=True)
        time.sleep(random.uniform(1.0, 1.5))  # Delay ngẫu nhiên 1-1.5s
        return True
    else:
        print("Không tìm thấy nút về nhà, tiếp tục luồng bình thường", flush=True)
        return False


def execute_fog_scout_cycle() -> bool:
    """Thực hiện chu kỳ trinh sát sương mù hoàn chỉnh"""
    print("Đang thực hiện chu kỳ trinh sát sương mù...", flush=True)
    
    # Kiểm tra nút trợ giúp đầu tiên
    check_and_click_help_button()
    
    # Kiểm tra nút đóng ESC trước khi bắt đầu
    check_and_click_close_esc()
    
    # Kiểm tra nút về nhà trước
    check_and_click_go_home()
    
    # Mở trại trinh sát
    if not try_click_button_with_retry(AssetPaths.FogScout.SCOUT_CAMP, "Trại Trinh Sát", 2):
        return False
    
    time.sleep(random.uniform(1.0, 1.5))  # Chờ giao diện tải
    
    # Chuỗi trinh sát
    scout_sequence = [
        (AssetPaths.FogScout.EXPLORE, "Thăm Dò"),
        (AssetPaths.FogScout.CONFIRM, "Xác Nhận Lần 1"),
        (AssetPaths.FogScout.CONFIRM, "Xác Nhận Lần 2"),
        (AssetPaths.FogScout.SEND, "Gửi")
    ]
    
    for button_path, button_name in scout_sequence:
        if not try_click_button_with_retry(button_path, button_name):
            print(f"Trinh sát sương mù thất bại tại: {button_name}", flush=True)
            return False
    
    print("Chu kỳ trinh sát sương mù hoàn thành thành công", flush=True)
    return True
    


def check_and_click_go_outside() -> bool:
    """Kiểm tra và click nút ra ngoài nếu tìm thấy"""
    print("Đang kiểm tra nút ra ngoài...", flush=True)
    
    # Thử tìm nút ra ngoài nhưng không nhấn ESC khi thất bại
    if try_click_button_without_esc(AssetPaths.Shared.GO_OUTSIDE, "Ra Ngoài", 2):
        print("Đã tìm thấy và click nút ra ngoài", flush=True)
        time.sleep(random.uniform(1.0, 1.5))  # Delay ngẫu nhiên 1-1.5s
        return True
    else:
        print("Không tìm thấy nút ra ngoài, tiếp tục luồng bình thường", flush=True)
        return False


def try_click_button_without_esc(button_path: str, button_name: str, max_retries: int = None) -> bool:
    """Thử click nút nhưng không nhấn ESC khi thất bại"""
    if max_retries is None:
        max_retries = Config.MAX_RETRIES
        
    for attempt in range(max_retries):
        if click_button(button_path):
            time.sleep(random.uniform(0.5, 1.0))
            return True
        
        print(f"Không tìm thấy nút '{button_name}', thử lại {attempt + 1}/{max_retries}", flush=True)
        time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
    
    print(f"Không thể tìm thấy '{button_name}' sau {max_retries} lần thử", flush=True)
    return False


def check_and_click_close_esc() -> bool:
    """Kiểm tra và click nút đóng ESC nếu tìm thấy"""
    print("Đang kiểm tra nút đóng ESC...", flush=True)
    
    # Thử tìm nút đóng ESC nhưng không nhấn ESC khi thất bại
    if try_click_button_without_esc(AssetPaths.Shared.CLOSE_ESC, "Đóng ESC", 2):
        print("Đã tìm thấy và click nút đóng ESC", flush=True)
        time.sleep(random.uniform(1.0, 1.5))  # Delay ngẫu nhiên 1-1.5s
        return True
    else:
        print("Không tìm thấy nút đóng ESC, tiếp tục luồng bình thường", flush=True)
        return False


def check_and_click_help_button() -> bool:
    """Kiểm tra và click nút trợ giúp nếu tìm thấy"""
    print("Đang kiểm tra nút trợ giúp...", flush=True)
    
    # Thử tìm nút trợ giúp nhưng không nhấn ESC khi thất bại
    if try_click_button_without_esc(AssetPaths.Shared.HELP_BUTTON, "Trợ Giúp", 2):
        print("Đã tìm thấy và click nút trợ giúp", flush=True)
        time.sleep(random.uniform(1.0, 1.5))  # Delay ngẫu nhiên 1-1.5s
        return True
    else:
        print("Không tìm thấy nút trợ giúp, tiếp tục luồng bình thường", flush=True)
        return False


def execute_barbarian_farm_cycle() -> bool:
    """Thực hiện chu kỳ farm barbarian hoàn chỉnh"""
    print("Đang thực hiện chu kỳ farm barbarian...", flush=True)
    
    # Kiểm tra nút trợ giúp đầu tiên
    check_and_click_help_button()
    
    # Kiểm tra nút đóng ESC trước khi bắt đầu
    check_and_click_close_esc()
    
    # Kiểm tra nút ra ngoài trước khi bắt đầu chuỗi
    check_and_click_go_outside()
    
    attack_sequence = [
        (AssetPaths.BarbarianFarm.FIND_BAR, "Tìm Barbarian"),
        (AssetPaths.BarbarianFarm.CONFIRM_FIND, "Xác Nhận Tìm"),
        (AssetPaths.BarbarianFarm.ATTACK, "Tấn Công"),
        (AssetPaths.BarbarianFarm.ADD_TROOP, "Thêm Quân"),
        (AssetPaths.BarbarianFarm.SEND_TROOP, "Gửi Quân")
    ]
    
    for button_path, button_name in attack_sequence:
        if not try_click_button_with_retry(button_path, button_name, 2):
            print(f"Farm barbarian thất bại tại: {button_name}", flush=True)
            return False
    
    print("Chu kỳ farm barbarian hoàn thành thành công", flush=True)
    return True


def execute_current_activity(tracker: ActivityTracker) -> bool:
    """Execute the current activity"""
    if tracker.current_activity == ActivityType.FOG_SCOUT:
        return execute_fog_scout_cycle()
    else:
        return execute_barbarian_farm_cycle()


def main():
    """Thực thi chính của combo bot"""
    print(f"RoK Combo Bot (Trinh Sát Sương Mù + Farm Barbarian) bắt đầu sau {Config.STARTUP_DELAY} giây...")
    print("Cấu hình: Chuyển hoạt động sau mỗi chu kỳ")
    time.sleep(Config.STARTUP_DELAY)
    
    tracker = ActivityTracker()
    
    try:
        while True:
            print(f"\n--- Chu Kỳ {tracker.get_current_entries() + 1} ---")
            tracker.print_status()
            
            # Thực hiện hoạt động hiện tại
            success = execute_current_activity(tracker)
            
            if success:
                tracker.increment_current_entries()
                print(f"Hoạt động hoàn thành thành công", flush=True)
            else:
                print("Hoạt động thất bại, sẽ thử lại sau khi chuyển nếu cần", flush=True)
                # Vẫn tăng để tránh bị kẹt
                tracker.increment_current_entries()
            
            # Kiểm tra chuyển hoạt động sau mỗi chu kỳ
            if tracker.should_switch_activity():
                print("\nChuyển sang hoạt động khác sau 1 chu kỳ", flush=True)
                tracker.switch_activity()
                
                # Chờ trước khi bắt đầu hoạt động tiếp theo
                switch_delay = random.uniform(Config.ACTIVITY_SWITCH_DELAY_MIN, Config.ACTIVITY_SWITCH_DELAY_MAX)
                print(f"Chờ {switch_delay:.1f}s trước khi bắt đầu hoạt động tiếp theo...", flush=True)
                time.sleep(switch_delay)
            else:
                # Chờ ngắn giữa các chu kỳ
                time.sleep(random.uniform(1.0, 1.5))
            
    except KeyboardInterrupt:
        print("\nCombo bot đã dừng bởi người dùng", flush=True)
        tracker.print_status()
        
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}", flush=True)
        tracker.print_status()


if __name__ == "__main__":
    ensure_assets_directory()
    main()