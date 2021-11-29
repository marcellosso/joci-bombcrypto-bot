import cv2
import mss
import numpy as np
import pyautogui
import pyperclip
import time
import sys
import random
from datetime import datetime
import wmi
import webbrowser
import telegram
import requests
from yaml import load, Loader

# Load all assets from the game
assign_metamask_button =cv2.imread('target_images/assign-metamask-button.png')
back_button = cv2.imread('target_images/back-button.png')
close_button = cv2.imread('target_images/close-button.png')
common_label = cv2.imread('target_images/common-label.png')
connect_wallet_button = cv2.imread('target_images/connect-wallet-button.png')
full_green_bar = cv2.imread('target_images/full-green-bar.png')
half_green_bar = cv2.imread('target_images/half-green-bar.png')
heroes_button = cv2.imread('target_images/heroes-button.png')
is_selected_metamask = cv2.imread('target_images/is-selected-metamask.png')
is_working_button = cv2.imread('target_images/is-working-button.png')
not_selected_metamask = cv2.imread('target_images/not-selected-metamask.png')
not_working_button = cv2.imread('target_images/not-working-button.png')
ok_error_button = cv2.imread('target_images/ok_error_button.png')
super_rare_label = cv2.imread('target_images/super-rare-label.png')
treasure_hunt_button = cv2.imread('target_images/treasure-hunt.png')
newmap_button = cv2.imread('target_images/new-map-button.png')
charater_topbar = cv2.imread('target_images/charater-topbar.png')
error_topbar = cv2.imread('target_images/error-topbar.png')
password_field = cv2.imread('target_images/password_field.png')
unlock_metamask_button = cv2.imread('target_images/unlock-metamask-button.png')
treasure_chest_button = cv2.imread('target_images/treasure_chest.png')
coin_icon = cv2.imread('target_images/coin.png')

cat = """
====== Bomb Crypto Bot - Joci Version ======
============================================

──██████──██████──████──██──█───────────────█────
──────██──██──██──██────██──███─███─██───██─███──
──────██──██──██──██────██──█─█─█─█─█─███─█─█─█──
──────██──██──██──██────██──███─███─█──█──█─███──
──███─██──██──██──██────██───────────────────────
──██──██──██──██──██────██──█────────────────────
──██──██──██──██──██────██──███─███─███──────────
──██──██──██──██──██────██──█─█─█─█──█───────────
──██████──██████──████──██──███─███──█───────────

============================================
>> ---> Press ctrl + c to kill the bot.
"""
print(cat)

### CONFIG VARIABLES ###################################################################################################################

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

### INITIALIZING SYSTEM #################################################################################################################

# Load config data
data = []
with open('config.yaml') as f:
    data = load(f, Loader=Loader)

if data:
    print("Config loaded!")

telegram_data = data["telegram"]
system_data = data["system"]
update_data = data["update"]
metamask_data = data["metamask"]
offset_data = data["offset"]
    
# Initialize telegram
bot = telegram.Bot(token=telegram_data["telegram_bot_key"])

#Initialize windows process monitor
f = wmi.WMI()

count_enabled_to_work = 0
count_login_times = 0
count_characters_screen_times = 0

### SYSTEM AREA ##########################################################################################################################

# Simulate human like mouse movement
sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

def randonMouseMove(dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    current_x,current_y = pyautogui.position()
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-current_x,dest_y-current_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-current_x)/dist
        v_y += W_y + G_0*(dest_y-current_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        current_x += v_x
        current_y += v_y
        move_x = int(np.round(current_x))
        move_y = int(np.round(current_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            pyautogui.moveTo(move_x, move_y)
            pyautogui.sleep(system_data["mouse_speed"])

    time.sleep(1)
    return current_x,current_y

# Check if google chrome is running
def isChromeRunning():
    for process in f.Win32_Process():
        if "chrome.exe" == process.Name:
            return True
    return False

# Open the bomb game into the browser
def openBombCryptoGame():
    webbrowser.open("https://app.bombcrypto.io")
    time.sleep(5)

# Check if the internet connection is available.
def hasInternetConnection():
    url = "https://google.com.br"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

# Take a screen shot
def takeScreenshot ():
    with mss.mss() as sct:
        sct_img = np.array(sct.grab(sct.monitors[0]))
        return sct_img[:,:,:3]

# Find screenshot position and return all center points
def findPositions (target, threshold=0.9):
    screenshot = takeScreenshot()
    target_w = target.shape[1]
    target_h = target.shape[0]

    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rec = [ int(loc[0]), int(loc[1]), target_w, target_h ]
        rectangles.append(rec)
        rectangles.append(rec)

    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.5)

    points = []
    if len(rectangles):
        for (x, y, w, h) in rectangles:
             center_x = x + int(w/2)
             center_y = y + int(h/2)
             points.append((center_x, center_y, w, h))

    return points;

# Get current system time
def getCurrentTime():
    return time.time()

# Is time triggered
def isTimeTrigger(start, timeout):
    if (getCurrentTime() - start) > timeout * getRandonSeconds():
        return True
    return False

# Check is is timeout
def isTimeout(start, timeout):
    return getCurrentTime() - start > timeout

# Click in the given button
def clickButton(image, timeout=3, point = []):
    time.sleep(1)
    start_time = getCurrentTime()
    points = []
    
    while(True):
        points = findPositions(image)
        if(len(points) == 0):
            if(isTimeout(start_time, timeout)):
                pass
                return False
            time.sleep(1)
            continue

        x,y,_,_ = points[0]
        randonMouseMove(x + getRandonPixels() , y + getRandonPixels())
        pyautogui.click()
        return True

# Click in the given button
def clickExactButton(point):
    time.sleep(1)
    x,y,_,_ = point
    randonMouseMove(x + getRandonPixels() , y + getRandonPixels())
    pyautogui.click()
    return True
       

# Check if certain element list contains a give object
def containsObject(element, items):
    y = element[1]
    for(_, item_y, _, item_h) in items:
        isBelow = y < (item_y + item_h)
        isAbove = y > (item_y - item_h)
        if isBelow and isAbove:
            return True
    return False

# Refresh screen
def refreshScreen():
    pyautogui.hotkey('ctrl', 'shift', 'r')

# Get formated time. Example: "Current time : 2021-11-24 13:00:00:23333"
def getFormatedTime():
    date = datetime.now()
    print(" => Time: ", date)

# Log function
def log(message, telegram = False):
    if telegram == True:
        sendTelegramMessage(message)
    sys.stdout.write(message)
    getFormatedTime()

# Send telegram message
def sendTelegramMessage(message):
    if(telegram_data["telegram_chat_id"] is not False):
        bot.send_message(text=message, chat_id=telegram_data["telegram_chat_id"])

# Get randon number from 1 to 12
def getRandonSeconds():
    return 60 + random.randint(-5, 5)

# Get randon pixels from 1 to 6
def getRandonPixels():
    return random.randint(-5, 5)


### GAME AREA ############################################################################################################################


# Update the heroes positions on the map
def updateHeroesPosition():
    clickButton(back_button)
    clickButton(treasure_hunt_button)

# Open heroes screen
def openHeroesScreen():
    clickButton(back_button)
    clickButton(heroes_button)

# Check if modal error appears and click in close to exit
def hasModalHeroesError():
    time.sleep(1)
    error_top = findPositions(error_topbar)
    if(len(error_top) > 0):
        return error_top
    return False

# Increase heroes to work counter or set True to clear
def increaseHeroesToWorkCount(clear = False):
    global count_enabled_to_work
    count_enabled_to_work = count_enabled_to_work + 1
    if clear == True:
        count_enabled_to_work = 0

# Increase login tries counter or set True to clear
def increaseLoginCount(clear = False):
    global count_login_times
    count_login_times = count_login_times + 1
    if clear == True:
        count_login_times = 0

# Increase characters screen counter or set True to clear
def increaseCharactersScreenCount(clear = False):
    global count_characters_screen_times
    count_characters_screen_times = count_characters_screen_times + 1
    if clear == True:
        count_characters_screen_times = 0

# Click in all available buttons to work
def clickInAllHeroes(passSuper = False):

    while(True):
        
        buttons = findPositions(not_working_button)
        full_green_bars = findPositions(full_green_bar)
        super_rares = findPositions(super_rare_label)

        heroes_to_work = []

        for button in buttons:
            if containsObject(button, super_rares) and passSuper:
                if containsObject(button, full_green_bars):
                    heroes_to_work.append(button)
            else:
                heroes_to_work.append(button)

        for (x, y, _, _) in heroes_to_work:
            increaseHeroesToWorkCount()
            randonMouseMove(x + offset_data["work_button"] + getRandonPixels(), y + getRandonPixels())
            pyautogui.click()
            error = hasModalHeroesError()
            if error is not False:
                clickExactButton(error[0])
                continue
        break

# Click in all available buttons to work with half green bar
def clickInAllHeroesWithGreenBar(passSuper = False):
    while(True):
        buttons = findPositions(not_working_button)
        green_bars = findPositions(half_green_bar, 0.93)
        full_green_bars = findPositions(full_green_bar)
        super_rares = findPositions(super_rare_label)

        heroes_to_work = []

        for bar in green_bars:
            if  containsObject(bar, super_rares) and passSuper:
                if containsObject(bar, full_green_bars):
                    heroes_to_work.append(bar)
            else:
                if containsObject(bar, buttons): # Check if the buttons contains the green bar
                    heroes_to_work.append(bar)
        
        for (x, y, _, _) in heroes_to_work:
            increaseHeroesToWorkCount()
            randonMouseMove(x + offset_data["work_button"] + getRandonPixels(), y + getRandonPixels())
            pyautogui.click()
            time.sleep(1)
            error = hasModalHeroesError()
            if error is not False:
                clickExactButton(error[0])
                continue
        break

# Click in all available buttons to work with full green bar
def clickInAllHeroesWithFullGreenBar():
    while(True):
        buttons = findPositions(not_working_button)
        full_green_bars = findPositions(full_green_bar)

        heroes_to_work = []

        for bar in full_green_bars:
            if containsObject(bar, buttons): # Check if the buttons contains the green bar
                heroes_to_work.append(bar)
        
        for (x, y, _, _) in heroes_to_work:
            increaseHeroesToWorkCount()
            randonMouseMove(x + offset_data["work_button_full"] + getRandonPixels(), y + getRandonPixels())
            pyautogui.click()
            error = hasModalHeroesError()
            if error is not False:
                clickExactButton(error[0])
                continue
        break

# Scroll the heroes list
def scrollHeroesList():
    commoms = findPositions(common_label, 0.7)
    if (len(commoms) == 0):
        return
    x,y,_,_ = commoms[len(commoms)-1]
    randonMouseMove(x, y)
    pyautogui.dragRel(0,-200, 1)
        
# Put all able heroes to work
def putHeroesToWork():
    openHeroesScreen()

    time.sleep(5)

    times_scroll = 4

    while(times_scroll > 0):

        if(update_data["send_all_heroes_to_work"]):
            clickInAllHeroes(update_data["super_only_with_full_bar"])
        else:
            if(update_data["send_all_heroes_with_green_bar_to_work"]):
                clickInAllHeroesWithGreenBar(update_data["super_only_with_full_bar"])
            else:
                if(update_data["send_all_heroes_with_full_bar_to_work"]):
                  clickInAllHeroesWithFullGreenBar()

        scrollHeroesList()
        time.sleep(4)
        times_scroll = times_scroll - 1
    

    time.sleep(5)
    log("===> 👷🏽 " + str(count_enabled_to_work) + " heroes were putted to work...", True)
    increaseHeroesToWorkCount(True)
    
    clickButton(close_button)
    clickButton(treasure_hunt_button)

# Sent BCOIN report to telegram
def sendBCoinReport():
    if(telegram_data["telegram_chat_id"] is False):
        return

    chest = findPositions(treasure_chest_button)
    if len(chest) > 0:
        clickExactButton(chest[0])

    time.sleep(3)

    coin = findPositions(coin_icon)
    if len(coin) > 0:
        x, y, w, h = coin[0]

        with mss.mss() as sct:
            sct_img = np.array(sct.grab(sct.monitors[0]))
            crop_img = sct_img[y-h:y+h, x-w:x+w]
            cv2.imwrite('bcoin-report.png', crop_img)
            time.sleep(1)
            try:
                bot.send_document(chat_id=telegram_data["telegram_chat_id"], document=open('bcoin-report.png', 'rb'))
            except:
                log("Telegram offline...")
    clickButton(close_button)
    log(" ==> 💰 BCoin Report sent. ", True)

# Sent MAP report to telegram
def sendMapReport():
    if(telegram_data["telegram_chat_id"] is False):
        return

    back = findPositions(back_button)
    if len(back) <= 0:
        return

    x, y, _, _ = back[0]
    newY0 = y + 65
    newY1 = newY0 + system_data["game_height"]
    newX0 = x - 35
    newX1 = newX0 + system_data["game_width"]

    with mss.mss() as sct:
        sct_img = np.array(sct.grab(sct.monitors[0]))
        crop_img = sct_img[newY0:newY1, newX0:newX1]
        resized = cv2.resize(crop_img, (500, 250))

        cv2.imwrite('map-report.png', resized)
        time.sleep(1)
        try:
            bot.send_document(chat_id=telegram_data["telegram_chat_id"], document=open('map-report.png', 'rb'))
        except:
            log("Telegram offline...")

    clickButton(close_button)
    log(" ==> 📝 Map Report sent. ", True)

# Unlock the game if in unlock screen
def unlockGame():
    unlock_button = findPositions(unlock_metamask_button)
    if(len(unlock_button) > 0):
        log("--- Found unlock metamask button.")

        password = findPositions(password_field)
        if(len(password) > 0):
            log("--- Found password field.")
            clickExactButton(password[0])
            time.sleep(1)
            pyperclip.copy(metamask_data["password"])
            pyautogui.hotkey('ctrl', 'v')
            pyperclip.copy('')
            time.sleep(3)
        clickExactButton(unlock_button[0])

        time.sleep(5)

        sign_button = findPositions(assign_metamask_button)
        if(len(sign_button) > 0):
            log("--- Found assign button.")
            clickExactButton(sign_button[0])

# Login into the game. if error, refresh the page and try again.
def loginIntoGame():
    if count_login_times > 5:
        increaseLoginCount(True)
        log("==> ⛔ Login tries reached the limit. Stopping for now..", True)
        return
    
    increaseLoginCount()
    log("--- Starting login...")
    wallet_button = findPositions(connect_wallet_button)
    if(len(wallet_button) > 0):
        log("--- Found login button.")
        clickExactButton(wallet_button[0])
    
    time.sleep(5)

    meta_mask = findPositions(not_selected_metamask)
    if(len(meta_mask) > 0):
        log("--- Found metamask button.")
        clickExactButton(meta_mask[0])
    else:
        meta_mask = findPositions(is_selected_metamask)
        if(len(meta_mask) > 0):
            log("--- Found metamask selected button.")
            clickExactButton(meta_mask[0])

    time.sleep(5)

    sign_button = findPositions(assign_metamask_button)
    if(len(sign_button) > 0):
        log("--- Found assign button.")
        clickExactButton(sign_button[0])
    else:
        unlockGame()
    
    time.sleep(20)

    treasure = findPositions(treasure_hunt_button)
    if(not len(treasure) > 0):
        log("--- Treasure hunt not found. Trying the login again.")
        refreshScreen()
        time.sleep(8)
        loginIntoGame()
    else:
        log("--- Success logged.")
        log("--- Entering in the map view.")
        clickExactButton(treasure[0])
        time.sleep(1)
        log("--- Putting heroes to work.")
        putHeroesToWork()
        log("--- Done.")

# Press the new map button if exists
def switchToNewMap():
    newmap = findPositions(newmap_button)
    if(len(newmap) > 0):
        log("--- Found new map button.")
        clickExactButton(newmap[0])
        time.sleep(3)
        sendMapReport()
        time.sleep(2)
        sendBCoinReport()

# If error login retrying the login
def loginIntoTheGameWithError():
    error_button = findPositions(ok_error_button)
    if(len(error_button) > 0):
        log("--- Found error ok button.")
        clickExactButton(error_button[0])

    time.sleep(12)
    loginIntoGame()

# Identify the current screen
def identifyScreen():
    new_map = findPositions(newmap_button)
    if(len(new_map) > 0):
        return "newMapScreen"

    error_ok = findPositions(ok_error_button)
    if(len(error_ok) > 0):
        return "errorScreen"

    charater = findPositions(charater_topbar)
    if(len(charater) > 0):
        return "charaterScreen"
    
    treasure = findPositions(treasure_hunt_button)
    if(len(treasure) > 0):
        return "treasureHuntScreen"

    go_back = findPositions(back_button)
    if(len(go_back) > 0):
        return "mapScreen"

    unlock = findPositions(unlock_metamask_button)
    if(len(unlock) > 0):
        return "unlockScreen"

    wallet = findPositions(connect_wallet_button)
    if(len(wallet) > 0):
        return "loginScreen"

# main program
def main():
    time.sleep(3)
    work_time = getCurrentTime()
    update_time = getCurrentTime()
    message_offline = False
    log('🏁 Process initiated. 🏁 ', True)

    while(True):

        if not hasInternetConnection():
            log("==> ⛔ DANGER: No internet connection. Nothing to do..")
        else:
            if message_offline is not False:
                log("==> ⛔ DANGER: The PC was offline. Now is everything fine.", True)
                message_offline = False

        if not isChromeRunning():
            log("==> ⛔ Chrome is not running.. Restarting.. ", True)
            openBombCryptoGame()
            time.sleep(5)
            loginIntoGame()

        current_screen = identifyScreen()

        if(current_screen == "unlockScreen"):
            log("🔒 Unlock screen found. Trying to login.", True)
            unlockGame()
            time.sleep(5)

        if(current_screen == "loginScreen"):
            log("🔑 Login into the game.")
            loginIntoGame()
            time.sleep(5)

        if(current_screen == "errorScreen"):
            log("❌ Error identified, trying to login.", True)
            loginIntoTheGameWithError()
            time.sleep(5)

        if(current_screen == "newMapScreen"):
            log("🗺️ New map identified. Switching.", True)
            switchToNewMap()
            time.sleep(5)

        if(current_screen == "charaterScreen"):
            if count_characters_screen_times > 1:
                log("⛔ Character screen lock. Refreshing and trying to login.", True)
                increaseCharactersScreenCount(True)
                refreshScreen()
                time.sleep(12)
                loginIntoGame()
            else:
                log("⚠️ Character screen found. Changing to map view.")
                clickButton(close_button)
                clickButton(treasure_hunt_button)
                increaseCharactersScreenCount()
            time.sleep(5)
        else:
            increaseCharactersScreenCount(True)
        

        if(current_screen == "treasureHuntScreen"):
            log("⚠️ Treasure hunt screen found. Changing to map view.")
            clickButton(treasure_hunt_button)
            time.sleep(5)

        if(current_screen == "mapScreen"):
            if isTimeTrigger(update_time, update_data["time_heroes_position_update"]) and update_data["enable_update_positions"]:
                log("==> 📍 Updating heroes position. ")
                update_time = getCurrentTime()
                updateHeroesPosition()
                time.sleep(5)

            if isTimeTrigger(work_time, update_data["time_send_heroes_to_work_update"]):
                log("🔨 Putting heroes to work.", True)
                work_time = getCurrentTime()
                putHeroesToWork()

        randonMouseMove(100, 100)
        time.sleep(update_data["time_global_update"] * getRandonSeconds())

main()
