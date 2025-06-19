import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import pyautogui
import cv2
import numpy as np
import time
import random
import os

# Constants
MAX_RETRIES = 50
MIN_RETRY_WAIT = 7
MAX_RETRY_WAIT = 10

# Cấu hình PyAutoGUI
pyautogui.FAILSAFE = True  # Di chuột góc trên-trái để dừng bot
pyautogui.PAUSE = 0.5      # Độ trễ giữa các thao tác (giây)

# Đường dẫn đến hình ảnh nút (lưu trong thư mục assets)
ASSET_PATHS = {
    "find_bar_button": "assets/barbarian/find_bar_button.png",
    "confirm_find_button": "assets/barbarian/confirm_find_button.png",
    "attack_button": "assets/barbarian/attack_button.png",
    "add_troop_button": "assets/barbarian/add_troop_button.png",
    "select_troop_button": "assets/barbarian/select_troop_button.png",
    "send_troop_button": "assets/barbarian/send_troop_button.png"
}

def find_button(image_path):
    """Tìm vị trí nút trên màn hình bằng nhận diện hình ảnh"""
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy {image_path}", flush=True)
        return None
    print(f"Đang tìm ảnh: {image_path}", flush=True)
    template = cv2.imread(image_path, 0)  # Đọc hình ảnh nút (grayscale)
    screen = np.array(pyautogui.screenshot())  # Chụp màn hình
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)  # Chuyển sang grayscale
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)  # So khớp
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.7:  # Ngưỡng độ chính xác
        # Trả về tâm của nút (tính từ góc trên-trái)
        h, w = template.shape
        print(f"Ảnh tìm thấy với độ chính xác: {max_val}")
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)
    return None

def click_button(image_path):
    """Click vào nút nếu tìm thấy"""
    pos = find_button(image_path)
    if pos:
        print(f"Click vào {image_path} tại {pos}", flush=True)
        pyautogui.click(*pos)
        return True
    print(f"Không tìm thấy {image_path}", flush=True)
    return False

def main():
    """Chạy bot chính"""
    print("Bot farm barbarians RoK khởi động sau 5 giây...")
    time.sleep(5)  # Chờ để chuyển sang giả lập
    try:
        while True:
            print("Đang tìm và tấn công barbarians...", flush=True)

            # Tìm và click nút "Tìm Barbarian"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["find_bar_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Tìm Barbarian, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Tìm Barbarian sau 50 lần thử.", flush=True)
                continue

            # Tìm và click nút "Xác nhận Tìm Barbarian"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["confirm_find_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Xác nhận Tìm Barbarian, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Xác nhận Tìm Barbarian sau 50 lần thử.", flush=True)
                continue

            # Tìm và click nút "Tấn công"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["attack_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Tấn công, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Tấn công sau 50 lần thử.", flush=True)
                continue

            # Tìm và click nút "Thêm quân"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["add_troop_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Thêm quân, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Thêm quân sau 50 lần thử.", flush=True)
                continue

            # Tìm và click nút "Chọn quân"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["select_troop_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Chọn quân, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Chọn quân sau 50 lần thử.", flush=True)
                continue

            # Tìm và click nút "Gửi quân"
            for _ in range(MAX_RETRIES):
                if click_button(ASSET_PATHS["send_troop_button"]):
                    time.sleep(random.uniform(1, 3))
                    break
                print(f"Không tìm thấy nút Gửi quân, thử lại... lần thứ {_ + 1}", flush=True)
                time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
            else:
                print("Bỏ qua nút Gửi quân sau 50 lần thử.", flush=True)
                continue

            time.sleep(random.uniform(3, 7))  # Chờ trước khi lặp
    except KeyboardInterrupt:
        print("Bot đã dừng.", flush=True)

if __name__ == "__main__":
    # Kiểm tra thư mục assets
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()