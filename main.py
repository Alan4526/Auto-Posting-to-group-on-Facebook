
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
import time
import random
import platform
import subprocess
import pyperclip

print("------------------    ", platform.system(), "     -------os----------")

if platform.system() == "Windows":
    import pygetwindow as gw
    from pywinauto import Application
elif platform.system() == "Darwin":  # macOS
    import pyautogui

print('\nFB Automator - Version 1.14\nApp by: Gold Mouse!\n===========================================================================\n')
driver = ""
isPostSuccess = False

def update_status(msg):
    now_ = datetime.now()
    current_time = now_.strftime("%Y-%m-%d %H:%M:%S")
    print(str(current_time) + " - " + str(msg))

def get_random_int(min_value, max_value):
    return random.randint(min_value, max_value)

def get_group_id(url):
    pattern = r'groups/([a-zA-Z0-9._-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def activeChromeWindow(title):
    if platform.system() == "Windows":
        window = None
        try:
            window_title = title
            os_windows = gw.getAllTitles()
            for os_window in os_windows:
                if window_title in os_window:
                    print(os_window)
                    app = Application().connect(title=os_window)
                    window = app.window(title=os_window)
                    window.set_focus()
                    time.sleep(0.5)
                    window.bring_to_front()
                    print(f"Focused window: {os_window}")
                    return True
            print("No matching OS window found.")
            return False
        except Exception as e:
            print("Error focusing the latest driver window:", e)
        finally:
            if window:
                window_rect = window.rectangle()
                window_width = window_rect.right - window_rect.left
                window_height = window_rect.bottom - window_rect.top
                window_center_x = window_rect.left + window_width / 2
                window_center_y = window_rect.top + window_height / 2
                pyautogui.click(window_center_x, window_center_y)
    elif platform.system() == "Darwin":
        try:
            cmd = f'osascript -e \'activate application "Google Chrome"\''
            subprocess.call(cmd, shell=True)

            time.sleep(1)

            # Get window position and size  
            cmd = '''osascript -e 'tell application "Google Chrome" to get bounds of front window' '''  
            window_bounds = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split(',')  
            x1, y1, x2, y2 = map(int, window_bounds)  

            # Calculate center coordinates  
            center_x = (x1 + x2) // 2  
            center_y = (y1 + y2) // 2  

            # Move the mouse to the center and click  
            pyautogui.click(center_x, center_y)
            return True
        except Exception as e:
            print(f"Error while focusing window: {e}")
            return True
    return False

# Set up Chrome options and WebDriver
update_status("Opening Chrome..")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
if platform.system() == "Darwin":
    options.add_argument("--user-data-dir=" + os.path.expanduser("~/Library/Application Support/Google/Chrome/chromeProfile"))
else:
    options.add_argument(f"user-data-dir=" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromeProfile"))
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)  # Set up explicit wait

# Open Facebook login page
update_status("Navigating to base website..")
driver.get("https://facebook.com/login/")

print('\n')
update_status("STEPS:")
update_status("1. Log into your Facebook profile from the opened Chrome browser.")
update_status("2. If you are expecting to upload photos, put those photos into the 'Images' folder.")
update_status("3. Set your post's caption in the 'Caption.txt' file.")
update_status("4. Set the delay between posts via 'Config.txt' file.")
update_status("5. Make sure that you have entered all the groups into 'Groups.txt' file.")
update_status("6. Once ready, press ENTER key to start posting.")

input("\nCommand: ")
print('\n\n--------------------Don\'t change your window.------------------------------\n\n')
activeChromeWindow(driver.title)
update_status("Starting automation..")

# Load delay settings
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")
with open(config_path, "r") as file:
    cont = file.readlines()
    min_delay = int(cont[0].replace("MIN_DELAY_IN_SECONDS=", "").strip())
    max_delay = int(cont[1].replace("MAX_DELAY_IN_SECONDS=", "").strip())

# Load images and caption
images_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")
image_list = [os.path.join(images_path, f) for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.png'))]

caption_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Caption.txt")
with open(caption_path, "r", encoding="utf8") as file:
    caption = file.read()

# Load group URLs
groups_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Groups.txt")
with open(groups_path, "r") as file:
    group_list = [line.strip() for line in file if line.strip()]

update_status(f"{len(image_list)} photos found..")
update_status(f"Caption: {caption}")
update_status(f"To be posted in {len(group_list)} groups..")
update_status(f"With random delays between {min_delay} secs and {max_delay} secs..")

# Post in each group
group_list = list(set(group_list))  # Remove duplicate groups
for group in group_list:
    try:
        group_id = get_group_id(group)
        if group_id is None:
            update_status(f"Error: Couldn't get the group ID from {group}")
            continue
        
        update_status(f'Navigating to group: {group}')
        driver.get(f'https://facebook.com/groups/{group_id}')
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1i10hfl.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x78zum5.x1r8uery.x1iyjqo2.xs83m0k.xl56j7k.x1pshirs.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha")))

        photoButton = driver.find_elements(By.CSS_SELECTOR, "div.x1i10hfl.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x78zum5.x1r8uery.x1iyjqo2.xs83m0k.xl56j7k.x1pshirs.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha")[1]
        photoButton.click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] input.x1s85apg[type='file']")))
        pyperclip.copy(caption)
        time.sleep(1)

        if platform.system() == "Darwin":
            pyautogui.keyDown("command")
            pyautogui.press("v")
            pyautogui.keyUp("command")
        else:
            pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        if len(image_list) > 0:
            update_status('Uploading images..')
            for image in image_list:
                for _ in range(3):  # Try up to 3 times
                    try:
                        upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] input.x1s85apg[type='file']")))
                        upload_input.send_keys(image)
                        break
                    except Exception:
                        time.sleep(1)
                time.sleep(0.3)
        
        # Publish post
        driver.execute_script("document.querySelector('input[type=submit]').style.display = 'block';")
        time.sleep(1)
        postBTN = driver.find_element(By.CSS_SELECTOR, "input[type='submit'")
        postBTN.click()
        update_status('Successfully posted.')
        time.sleep(2)
        
        rr = get_random_int(min_delay, max_delay)
        update_status(f'Waiting {rr} sec(s)..')
        time.sleep(rr)
        isPostSuccess = True
        
    except Exception as e:
        update_status(f"Error: {e}")

# Return to homepage
if isPostSuccess:
    driver.get('https://facebook.com/')
    update_status('Completed :)')
else:
    update_status("Failed to post :(")

input("Enter any value to terminal: ")
