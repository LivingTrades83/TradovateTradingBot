import pyautogui as pag
import time
import keyboard
import cv2
import numpy as np
from itertools import zip_longest
import datetime

time.sleep(5.0)

counter = 0
while keyboard.is_pressed('q') == False:

    now = datetime.datetime.now()
    minute = (now.minute + 1) / 3
    second = now.second
    one = pag.locateOnScreen('Images\\USD.PNG')

    if minute.is_integer() or now.minute == 0:
        if second == 55:
            print("heard")
            open_cv_image = screenshot_me()
            img, red_rectangles, green_rectangles, rec_list, highest_y, lowest_y = determine_candles(open_cv_image)
            if one == None:
                print('nothing')
                
            if one != None:
                resultGreen = green_engulfing(rec_list)
                resultRed = red_engulfing(rec_list)
                print(resultGreen, resultRed)
                if resultGreen == True:
                    stop_loss_long(highest_y, lowest_y)
                else: pass

                if resultRed == True:
                    stop_loss_short(highest_y, lowest_y)
                else: pass
                print(counter)
                counter += 1

def press_buy():
    coords = pag.center(pag.locateOnScreen('Images\MarketBuy.PNG'))
    time.sleep(0.1)
    pag.click(coords)
    
def press_sell():
    coords = pag.center(pag.locateOnScreen('Images\MarketSell.PNG'))
    time.sleep(0.1)
    pag.click(coords)

def press_exit_all():
    coords = pag.center(pag.locateOnScreen('Images\ExitAll.PNG'))
    time.sleep(0.1)
    print(coords)
    #pag.click(coords)

def stop_loss_long(highest_y, lowest_y):
    
    time.sleep(0.1)

    stop_one, stop_two = pag.locateAllOnScreen('Images\RedXSmall.png')

    if stop_one[1] < stop_two[1]:
        take_profit = stop_one
        stop_loss = stop_two
    else:
        take_profit = stop_two
        stop_loss = stop_one

    print(stop_loss)
    print(take_profit)

    entry_point_y = ((stop_loss[1] + take_profit[1]) / 2) + 8
    profit_y = ((233 + lowest_y) - entry_point_y)
    print("entry_point_y: ",entry_point_y)
    print("profit_y: ",profit_y)
    print("highest_y: ",highest_y + 233)
    print("lowest_y: ",lowest_y + 233)

    pag.moveTo(take_profit[0] + 40, take_profit[1] + 10)
    pag.dragTo(540, (entry_point_y - profit_y), 1, button='left')

    time.sleep(0.1)

    pag.moveTo(stop_loss[0] + 40, stop_loss[1] + 10)
    pag.dragTo(540, (233 + lowest_y), 1, button='left')

    pag.moveTo(1300, 500)

def stop_loss_short(highest_y, lowest_y):

    time.sleep(0.1)
    stop_one, stop_two = pag.locateAllOnScreen('Images\GreenXSmallest.png')

    if stop_one[1] < stop_two[1]:
        stop_loss = stop_one
        take_profit = stop_two
    else:
        stop_loss = stop_two
        take_profit = stop_one 

    entry_point_y = ((stop_loss[1] + take_profit[1]) / 2) + 8
    profit_y = (entry_point_y - (233 + highest_y))

    pag.moveTo(take_profit[0] + 40, take_profit[1] + 10)
    pag.dragTo(540, profit_y + entry_point_y, 1, button='left')

    time.sleep(0.1)

    pag.moveTo(stop_loss[0] + 40, stop_loss[1] + 10)
    pag.dragTo(540, (233 + highest_y - 1), 1, button='left')

    pag.moveTo(1300, 500)
    #Moves to the top of wick or bottom
    #pag.moveTo(540, (233 + lowest_y))
    
def screenshot_me():
    im1 = pag.screenshot(region=(0,233,867,757))
    open_cv_image = np.array(im1) 
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    #Shows Image
    #cv2.imshow("test", open_cv_image)
    #cv2.waitKey(0)
    return open_cv_image

class Rectangle:
    def __init__(self, color, height, top, bottom, center_x, gray_top=None):
        self.color = color
        self.height = height
        self.top = top
        self.bottom = bottom
        self.center_x = center_x
        self.gray_top = gray_top

def determine_candles(cv_image):
    
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    lower_gray = np.array([0, 0, 100])
    upper_gray = np.array([180, 50, 255])

    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask_red = cv2.add(mask_red1, mask_red2)
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
    mask_gray = cv2.inRange(hsv_image, lower_gray, upper_gray)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_gray, _ = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_red = sorted(contours_red, key=lambda contour: cv2.boundingRect(contour)[0])
    contours_green = sorted(contours_green, key=lambda contour: cv2.boundingRect(contour)[0])
    contours_gray = sorted(contours_gray, key=lambda contour: cv2.boundingRect(contour)[0])

   
    red_rectangles = []
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        red_rectangle = Rectangle(color='Red', height=h, top=(y, x), bottom=(y + h, x + w), center_x = ((x + (x + w)) / 2))
        red_rectangles.append(red_rectangle)
        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #cv2.putText(cv_image, 'Red', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    green_rectangles = []
    for contour in contours_green:
        x, y, w, h = cv2.boundingRect(contour)
        green_rectangle = Rectangle(color='Green', height=h, top=(y, x), bottom=(y + h, x + w), center_x = ((x + (x + w)) / 2))
        green_rectangles.append(green_rectangle)
        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(cv_image, 'Green', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
   
    #cv_image.save(r"Images\\CurrentDisplay.PNG")
    cv2.imshow('Current Display', cv_image)
    cv2.waitKey(delay=1)

    rectangle_list = []
    for i in red_rectangles:
        rectangle_list.append(i)
    for i in green_rectangles:
        rectangle_list.append(i)

    rec_list = sorted(rectangle_list, key=lambda Rectangle: Rectangle.center_x, reverse=True)

    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    given_x = int(rec_list[0].center_x)
    column = gray_image[:, given_x]

    # Find the y-coordinate of the highest non-black pixel using NumPy
    indices = np.nonzero(column)
    highest_y = indices[0][0] if indices[0].size > 0 else None

    indices = np.nonzero(column)
    lowest_y = indices[0][-1] if indices[0].size > 0 else None

    return cv_image, red_rectangles, green_rectangles, rec_list, highest_y, lowest_y

def green_engulfing(rectangles):
    
    first_rectangle = rectangles[0]
    runner_rectangle = rectangles[1]
    
    if first_rectangle.color == "Green" and runner_rectangle.color == "Red":
        if first_rectangle.top[0] <= runner_rectangle.top[0] and first_rectangle.bottom[0] >= runner_rectangle.bottom[0]:
            print("Long Position")
            press_buy()
            return True
        else: return False
    else: return False

def red_engulfing(rectangles):
    first_rectangle = rectangles[0]
    runner_rectangle = rectangles[1]

    if first_rectangle.color == "Red" and runner_rectangle.color == "Green":
        if first_rectangle.top[0] <= runner_rectangle.top[0] and first_rectangle.bottom[0] >= runner_rectangle.bottom[0]:
            print("Short Position")
            press_sell()
            return True
        else: return False
    else: return False
