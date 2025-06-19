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
MAX_RETRIES = 200
# Constants
MIN_RETRY_WAIT = 1
MAX_RETRY_WAIT = 2

# Cấu hình PyAutoGUI
pyautogui.FAILSAFE = True  # Di chuột góc trên-trái để dừng bot
pyautogui.PAUSE = 0.5      # Độ trễ giữa các thao tác (giây)

# Đường dẫn đến hình ảnh nút (lưu trong thư mục assets)
ASSET_PATHS = {
    "scout_camp": "assets/fog/scout_camp.png",    # Nút Trại Trinh Sát
    "explore_button": "assets/fog/explore_button.png", # Nút Thăm dò
    "confirm_button": "assets/fog/confirm_button.png",    # Nút Xác nhận
    "send_button": "assets/fog/send_button.png",          # Nút Gửi
    "back_button": "assets/fog/back_button.png"          # Nút Quay lại
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

def open_scout_camp():
    """Mở Trại Trinh Sát"""
    print("Đang mở Trại Trinh Sát...", flush=True)
    for i in range(MAX_RETRIES):
        if click_button(ASSET_PATHS["scout_camp"]):
            time.sleep(2)  # Chờ màn hình load
            return True
        print(f"Không tìm thấy scout_camp, thử lại lần {i+1}...", flush=True)
        time.sleep(random.uniform(3, 5))
    return False

def send_scout():
    """Gửi trinh sát dò sương, thử lại sau 3s nếu không tìm thấy nút"""
    print("Đang gửi trinh sát...", flush=True)

    # Thử tìm nút Thăm dò
    for _ in range(MAX_RETRIES):  # Thử 50 lần
        if click_button(ASSET_PATHS["explore_button"]):
            time.sleep(random.uniform(0.5, 1))
            break
        print("Không tìm thấy explore_button, thử lại sau 3s... lần thứ " + str(_ + 1), flush=True)
        time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
    else:
        print("Bỏ qua explore_button sau 50 lần thử.", flush=True)
        return False

    # Thử tìm nút Xác nhận (lần 1)
    for _ in range(MAX_RETRIES):
        if click_button(ASSET_PATHS["confirm_button"]):
            time.sleep(random.uniform(0.5, 1))
            break
        print("Không tìm thấy confirm_button, thử lại sau 7s... lần thứ " + str(_ + 1), flush=True)
        time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
    else:
        print("Bỏ qua confirm_button sau 50 lần thử.", flush=True)
        return False

    # Thử tìm nút Xác nhận (lần 2) - confirm_more
    for _ in range(MAX_RETRIES):
        if click_button(ASSET_PATHS["confirm_button"]):
            time.sleep(random.uniform(0.5, 1))
            break
        print("Không tìm thấy confirm_more, thử lại sau 7s... lần thứ " + str(_ + 1), flush=True)
        time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
    else:
        print("Bỏ qua confirm_more sau 50 lần thử.", flush=True)
        return False

    # Thử tìm nút Gửi
    for _ in range(MAX_RETRIES):
        if click_button(ASSET_PATHS["send_button"]):
            time.sleep(random.uniform(0.5, 1))
            break
        print("Không tìm thấy send_button, thử lại sau 3s... lần thứ " + str(_ + 1), flush=True)
        time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
    else:
        print("Bỏ qua send_button sau 50 lần thử.", flush=True)
        return False

    # Thử tìm nút Quay lại
    for _ in range(MAX_RETRIES):
        if click_button(ASSET_PATHS["back_button"]):
            time.sleep(2)
            break
        print("Không tìm thấy back_button, thử lại sau 3s... lần thứ " + str(_ + 1), flush=True)
        time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))
    else:
        print("Bỏ qua back_button sau 50 lần thử.", flush=True)
        return False

    return True

def main():
    """Chạy bot chính"""
    print("Bot dò sương RoK khởi động sau 2 giây...", flush=True)
    time.sleep(2)  # Chờ để chuyển sang giả lập
    try:
        while True:
            if not open_scout_camp():
                print("Lỗi mở Trại Trinh Sát, thử lại...", flush=True)
                time.sleep(5)
                continue
            if not send_scout():
                print("Lỗi gửi trinh sát, thử lại...", flush=True)
                time.sleep(5)
                continue
            time.sleep(random.uniform(MIN_RETRY_WAIT, MAX_RETRY_WAIT))  # Chờ trước khi lặp
    except KeyboardInterrupt:
        print("Bot đã dừng.", flush=True)

if __name__ == "__main__":
    # Kiểm tra thư mục assets
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()