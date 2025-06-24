"""
Shared utility functions for RoK bot automation
"""
import os
import cv2
import numpy as np
import pyautogui
import random
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
            random_x = max_loc[0] + random.randint(0, w)
            random_y = max_loc[1] + random.randint(0, h)
            print(f"Image found with accuracy: {max_val:.3f}")
            return (random_x, random_y)
    
    except Exception as e:
        print(f"Error in image recognition: {e}", flush=True)
        
    return None


def move_mouse_zigzag(target_x: int, target_y: int, duration: float = 0.5):
    """Move mouse in natural human-like pattern to target position"""
    import math
    import time
    
    current_x, current_y = pyautogui.position()
    distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
    
    # Don't add movement complexity for very short distances
    if distance < 50:
        pyautogui.moveTo(target_x, target_y, duration=duration, tween=pyautogui.easeInOutQuad)
        return
    
    # Human-like characteristics
    num_points = random.randint(2, 6)  # More variation in movement patterns
    overshoot_chance = 0.3  # Sometimes humans overshoot slightly
    hesitation_chance = 0.2  # Sometimes humans hesitate mid-movement
    
    waypoints = [(current_x, current_y)]
    
    for i in range(1, num_points):
        progress = i / num_points
        
        # Add natural curve with some randomness
        curve_factor = random.uniform(0.1, 0.3)
        perpendicular_x = -(target_y - current_y) / distance * curve_factor * distance
        perpendicular_y = (target_x - current_x) / distance * curve_factor * distance
        
        # Base position with natural curve
        x = current_x + (target_x - current_x) * progress
        y = current_y + (target_y - current_y) * progress
        
        # Add curve offset (humans don't move in straight lines)
        curve_strength = math.sin(progress * math.pi) * random.uniform(0.7, 1.3)
        x += perpendicular_x * curve_strength
        y += perpendicular_y * curve_strength
        
        # Add small random imperfections
        x += random.uniform(-5, 5)
        y += random.uniform(-5, 5)
        
        waypoints.append((int(x), int(y)))
    
    # Final target (with possible small overshoot)
    final_x, final_y = target_x, target_y
    if random.random() < overshoot_chance:
        overshoot_x = random.uniform(-3, 3)
        overshoot_y = random.uniform(-3, 3)
        waypoints.append((target_x + overshoot_x, target_y + overshoot_y))
        waypoints.append((target_x, target_y))  # Correct back
    else:
        waypoints.append((target_x, target_y))
    
    # Move through waypoints with variable timing
    total_time = 0
    for i in range(1, len(waypoints)):
        segment_progress = i / (len(waypoints) - 1)
        
        # Variable segment duration (humans speed up/slow down naturally)
        if i == 1:
            # Start slower
            segment_duration = duration * 0.4
        elif i == len(waypoints) - 1:
            # End slower
            segment_duration = duration * 0.3
        else:
            # Middle segments faster
            segment_duration = duration * 0.3 / max(1, len(waypoints) - 2)
        
        x, y = waypoints[i]
        
        # Choose random easing function for variety
        tween_funcs = [pyautogui.easeInOutQuad, pyautogui.easeOutQuad, pyautogui.easeInQuad]
        tween = random.choice(tween_funcs)
        
        pyautogui.moveTo(x, y, duration=segment_duration, tween=tween)
        
        # Random micro-pauses (hesitation)
        if random.random() < hesitation_chance and i < len(waypoints) - 1:
            time.sleep(random.uniform(0.05, 0.15))
        
        total_time += segment_duration


def click_button(image_path: str) -> bool:
    """Click button if found"""
    position = _find_button(image_path)
    if position:
        print(f"Clicking {os.path.basename(image_path)} at {position}", flush=True)
        duration = random.uniform(0.08, 0.20)  # Much faster: 0.08-0.20s
        move_mouse_zigzag(*position, duration)
        pyautogui.click()
        return True
    print(f"Button not found: {os.path.basename(image_path)}", flush=True)
    return False


def ensure_assets_directory():
    """Ensure assets directory exists"""
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created {assets_dir} directory")