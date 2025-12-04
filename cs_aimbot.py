import cv2
import numpy as np
import pyautogui
import time
import random
from PIL import ImageGrab
import win32api
import win32con
import win32gui
import mss
import keyboard
import sys

class CounterStrikeAimbot:
    def __init__(self):
        self.running = False
        self.activation_key = 'f2'
        self.exit_key = 'f10'
        self.target_color_range = {
            'lower': np.array([0, 100, 100]),    # اللون الأحمر في HSV
            'upper': np.array([10, 255, 255])
        }
        self.screen_width, self.screen_height = pyautogui.size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.sensitivity = 0.5
        self.aim_smoothness = 15
        self.triggerbot_enabled = True
        self.aimbot_enabled = True
        self.auto_shoot = True
        
    def get_screen(self):
        """Capture screen with high performance using MSS"""
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    def detect_enemies(self, frame):
        """Detect enemies using color filtering and contour detection"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for enemy color (red/orange - typical in CS)
        mask1 = cv2.inRange(hsv, self.target_color_range['lower'], self.target_color_range['upper'])
        
        # Additional color range for better detection
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Morphological operations to reduce noise
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        enemies = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 50 < area < 1000:  # Filter by size
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Calculate distance from crosshair
                distance = np.sqrt((center_x - self.center_x)**2 + (center_y - self.center_y)**2)
                
                enemies.append({
                    'x': center_x,
                    'y': center_y,
                    'width': w,
                    'height': h,
                    'area': area,
                    'distance': distance
                })
        
        # Sort by closest enemy
        enemies.sort(key=lambda x: x['distance'])
        return enemies
    
    def move_mouse(self, target_x, target_y):
        """Smooth mouse movement to target"""
        current_x, current_y = pyautogui.position()
        
        # Calculate difference
        diff_x = target_x - current_x
        diff_y = target_y - current_y
        
        # Smooth movement with easing
        steps = self.aim_smoothness
        for i in range(steps):
            progress = i / steps
            ease = 0.5 - 0.5 * np.cos(progress * np.pi)  # Cosine easing
            
            move_x = current_x + diff_x * ease
            move_y = current_y + diff_y * ease
            
            pyautogui.moveTo(move_x, move_y)
            time.sleep(0.001)
    
    def trigger_action(self):
        """Simulate mouse click for shooting"""
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05 + random.uniform(0, 0.03))  # Random delay for realism
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def is_aiming_at_target(self, target, threshold=50):
        """Check if crosshair is close enough to target"""
        current_x, current_y = pyautogui.position()
        distance = np.sqrt((target['x'] - current_x)**2 + (target['y'] - current_y)**2)
        return distance < threshold
    
    def start(self):
        """Main loop"""
        print("[+] نظام الهاك الإستراتيجي لجنود الكونتري سترايك تم تفعيله!")
        print(f"[+] مفتاح التشغيل: {self.activation_key}")
        print(f"[+] مفتاح الخروج: {self.exit_key}")
        print("[+] النظام جاهز للمعركة...")
        
        self.running = True
        last_shot_time = 0
        
        while self.running:
            try:
                # Check for exit key
                if keyboard.is_pressed(self.exit_key):
                    print("[+] النظام تم إيقافه بواسطة المستخدم")
                    self.running = False
                    break
                
                # Check for activation key
                if not keyboard.is_pressed(self.activation_key):
                    time.sleep(0.01)
                    continue
                
                # Capture screen
                screen = self.get_screen()
                
                # Detect enemies
                enemies = self.detect_enemies(screen)
                
                if enemies:
                    target = enemies[0]  # Closest enemy
                    
                    if self.aimbot_enabled:
                        # Move to target with slight randomization
                        rand_x = target['x'] + random.randint(-5, 5)
                        rand_y = target['y'] + random.randint(-5, 5)
                        self.move_mouse(rand_x, rand_y)
                    
                    if self.triggerbot_enabled and self.is_aiming_at_target(target):
                        current_time = time.time()
                        if current_time - last_shot_time > 0.1:  # Rate limiting
                            if self.auto_shoot:
                                self.trigger_action()
                                last_shot_time = current_time
                                # Random mouse movement after shot (recoil simulation)
                                pyautogui.moveRel(
                                    random.randint(-3, 3),
                                    random.randint(2, 5),
                                    duration=0.05
                                )
                
                # Small delay to prevent CPU overload
                time.sleep(0.01)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[!] خطأ: {e}")
                time.sleep(1)
    
    def calibrate_color(self):
        """Color calibration tool"""
        print("[+] وضع المعايرة: حرك الماوس على لون العدو واضغط مسافة")
        
        def on_space_press(event):
            if event.name == 'space':
                x, y = pyautogui.position()
                screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
                color = screenshot.getpixel((0, 0))
                print(f"[+] اللون المكتشف: {color}")
                
                # Convert to HSV
                color_np = np.uint8([[list(color)]])
                hsv = cv2.cvtColor(color_np, cv2.COLOR_RGB2HSV)
                print(f"[+] قيمة HSV: {hsv[0][0]}")
        
        keyboard.on_press(on_space_press)
        keyboard.wait('esc')
        keyboard.unhook_all()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║  نظام القناص الذكي - Counter Strike Aimbot ║
    ║  الإصدار: Pro Elite v2.0                 ║
    ║  المطور: الخبير التقني                   ║
    ╚══════════════════════════════════════════╝
    """)
    
    aimbot = CounterStrikeAimbot()
    
    # Start calibration if needed
    if len(sys.argv) > 1 and sys.argv[1] == "--calibrate":
        aimbot.calibrate_color()
    else:
        aimbot.start()
