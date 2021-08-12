import tk as tk
from selenium import webdriver
import threading
import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
driver = webdriver.Chrome("./chromedriver")
driver.get("https://popcat.click/")
button = None
isCancel = False


def set_interval(func, sec):
    def func_wrapper():
        if not isCancel:
            set_interval(func, sec)
            func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def check_button_exists():
    if len(driver.find_elements_by_class_name("cat-img")) != 0:
        global button
        button = driver.find_element_by_class_name("cat-img")


def set_check_button_interval(sec):
    def func_wrapper():
        if button is not None:
            check_button_timer.cancel()
            t.cancel()
        else:
            set_check_button_interval(sec)
            check_button_exists()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def call():
    if button is not None:
        button.click()
        click_timer.cancel()


def stop_interval():
    check_button_timer.cancel()
    global isCancel
    isCancel = True


def start_click():
    global isCancel
    isCancel = False
    global click_timer
    click_timer = set_interval(call, 0.04)


check_button_timer = set_check_button_interval(0.5)
click_timer = None


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            driver.close()
        except Exception as e:
            print(e)
        win.destroy()


def main():
    win.geometry('300x200')
    win.resizable(False, False)
    win.title('洗貓')

    tk.Button(win, text="開始洗貓", command=start_click, pady=5).grid(row=0, column=0, pady=10)
    tk.Button(win, text="停止洗貓", command=stop_interval, pady=5).grid(row=1, column=0, pady=10)

    win.protocol("WM_DELETE_WINDOW", on_closing)
    # 啟動主視窗
    win.mainloop()


if __name__ == "__main__":
    main()
