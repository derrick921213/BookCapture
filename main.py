import time
import pygetwindow as gw
import pyautogui
from PIL import Image
from os.path import exists,join
from os import mkdir,listdir
import sys
from shutil import rmtree as rmdir
from re import findall
def capture_window(window_title: str,screenshots: str,x,y) -> bool:
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]
            window.activate()
            left, top = window.topleft
            right, buttom = window.bottomright
            time.sleep(0.5)
            pages: int = 0
            while True:
                pyautogui.screenshot(f"{screenshots}/{pages}.png",region=(left+250, top+60, right-480, buttom-55))
                time.sleep(0.05)
                if not click_button("end.png"):
                    break
                pyautogui.moveTo(x,y, duration = 1.5)
                pyautogui.click()
                time.sleep(0.05)
                pages+=1
            return True
        else:
            print(f"No window with title '{window_title}' found.")
            return False
    except Exception as e:
        print(f"Error capturing window: {e}")
        return False
def click_button(image_path:str) -> bool:
    try:
        button_location = pyautogui.locateOnScreen(image_path, confidence=0.9)
        if button_location:
            # button_center = pyautogui.center(button_location)
            # pyautogui.moveTo(button_center.x, button_center.y, duration=1)
            # pyautogui.click()
            # pyautogui.moveTo(1550, 880, duration=1)
            return True
    except pyautogui.ImageNotFoundException as e :
        return False
def extract_number(file_name):
    numbers = findall(r'\d+', file_name)
    return int(numbers[0]) if numbers else 0

def monitor() -> None:
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        return x,y

def PngToPdf(folder_path: str, output_pdf_path: str) -> None:
    image_files = [f for f in listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
    image_files.sort(key=extract_number)
    images = []
    for image_file in image_files:
        img_path = join(folder_path, image_file)
        img = Image.open(img_path).convert("RGB")
        images.append(img)
    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    
    print(f'圖片合併完成: {output_pdf_path}')
def Main() -> None:
    x,y = monitor()
    if not pyautogui.confirm(text='請確認HyRead視窗是否開啟，並且已經登入', title='確認視窗', buttons=['開始截圖', '取消']):
        sys.exit(0)
    folder_path = './screenshots'
    if not exists(folder_path):
        mkdir(folder_path)
    if not capture_window("HyRead",folder_path,x,y):
        print("Error capturing window.")
        exit(1)
    PngToPdf(folder_path,"output.pdf")
    if exists(folder_path):
        rmdir(folder_path)
Main()