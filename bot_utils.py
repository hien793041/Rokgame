"""
Shared utility functions for RoK bot automation
"""
import os
import cv2
import numpy as np
import pyautogui
from typing import Optional, Tuple


class Config:
    """Base configuration constants"""
    ACCURACY_THRESHOLD = 0.7


def _find_button(image_path: str) -> Optional[Tuple[int, int]]:
    """Find button position on screen using image recognition"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found - {image_path}", flush=True)
        return None
        
    print(f"Searching for image: {image_path}", flush=True)
    
    try:
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Error: Could not load image - {image_path}", flush=True)
            return None
            
        screen = np.array(pyautogui.screenshot())
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > Config.ACCURACY_THRESHOLD:
            h, w = template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            print(f"Image found with accuracy: {max_val:.3f}")
            return (center_x, center_y)
    
    except Exception as e:
        print(f"Error in image recognition: {e}", flush=True)
        
    return None


def click_button(image_path: str) -> bool:
    """Click button if found"""
    position = _find_button(image_path)
    if position:
        print(f"Clicking {os.path.basename(image_path)} at {position}", flush=True)
        pyautogui.click(*position)
        return True
    print(f"Button not found: {os.path.basename(image_path)}", flush=True)
    return False


def ensure_assets_directory():
    """Ensure assets directory exists"""
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created {assets_dir} directory")