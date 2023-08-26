#created by mng48301

import cv2
import pytesseract
import threading
import customtkinter as ctk
from customtkinter import filedialog
import time

pytesseract.pytesseract.tesseract_cmd = r"" # path to pytesseract installer

#definitions of window for gui
window = ctk.CTk()
window.title("VIDText")
window.geometry("500x500+700+100")
window.iconbitmap(r"") # path to window icon for gui
mode = "dark"
window._set_appearance_mode(f"{mode}")
imported = False 
clicked = False


def click_pic():
    global clicked
    clicked = True

def get_feed(path):
    if imported:
        video = cv2.VideoCapture(f"{path}")
    else:
        video = cv2.VideoCapture(0)
    start = 0
    end = 0
    while True:
        success, frame = video.read()
        if not success:
            break
        
        start = time.time()
        fps = str(int(1/(start - end)))
        end = start
        
        cv2.putText(frame, f"FPS: {fps}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        
        #processing text from image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed_frame = cv2.GaussianBlur(gray, (5, 5), 0)
        extracted_text = pytesseract.image_to_string(processed_frame)
        print(extracted_text)
        

        cv2.imshow("Video Feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

def quit_all(): 
    cv2.destroyAllWindows()
  

def run_vid(): 
    global imported
    imported = False
    runner_vid = threading.Thread(target=get_feed, args= (0,))
    runner_vid.start()

def run_pic():
    runner_pic = threading.Thread(target=take_pic)
    runner_pic.start()

def take_pic(): 
    
    video = cv2.VideoCapture(0)
    start = 0
    end = 0
    while True:
        success, frame = video.read()
        if clicked:
            break
        if not success:
            break
        start = time.time()
        fps = str(int(1/(start - end)))
        end = start
        cv2.putText(frame, f"FPS: {fps}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("Video Feed", frame)
    cv2.imwrite("frame.jpg", frame)

    print("File saved as frame.jpg") # saves file to dir
  
    video.release()
    cv2.destroyAllWindows()

    #processing text from image
    image = cv2.imread("frame.jpg") #file is saved as a .jpg file
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_frame = cv2.GaussianBlur(gray, (5, 5), 0)
    extracted_text = pytesseract.image_to_string(processed_frame)
    print(extracted_text)


def get_import():
    global imported
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4, *.avi")])
    imported = True
    if video_path:
        get_feed(video_path)


#styling declarations

title_font = ctk.CTkFont(
    family= "Helvetica", 
    size= 90, 
    weight= "bold", 
    slant= "roman", 
    underline= True, 
    overstrike= False
    )


#mainframe
spacer = ctk.CTkLabel(window, text= "0000000", text_color= "#242424", bg_color="#242424", font =("Helvetica", 25))
spacer.grid(row= 1, columns= 1)


title_label = ctk.CTkLabel(window, text= "VIDText", text_color= "#a2afb8", bg_color="#242424", font = title_font)
title_label.grid(row= 1, column= 2, columnspan= 4, pady= 25)

import_button = ctk.CTkButton(window, text="Import Video", corner_radius= 10, hover_color= "#34b7eb", fg_color="#3474eb", bg_color="#242424", font = ("Helvetica", 20), command= lambda: get_import())
import_button.grid(row= 2, column= 2, columnspan= 4, pady= 25)

use_video_button = ctk.CTkButton(window, text="Use Current Video", corner_radius= 10, hover_color= "#34b7eb", fg_color="#3474eb", bg_color="#242424", font = ("Helvetica", 20), command= lambda: run_vid())
use_video_button.grid(row= 3, column= 2, pady= 25, columnspan= 4)

picture_select_button = ctk.CTkButton(window, text="Take Picture", corner_radius= 10, hover_color= "#34b7eb", fg_color="#3474eb", bg_color="#242424", font = ("Helvetica", 20), command= lambda: run_pic())
picture_select_button.grid(row= 4, column= 3, columnspan= 2, pady= 25, ipadx= 15)

picture_button = ctk.CTkButton(master=window, text="📷", width= 7, height= 10, corner_radius= 10, hover_color= "#34b7eb", fg_color="#3474eb", bg_color="#242424", font = ("Helvetica", 20), command= lambda: click_pic())
picture_button.grid(row=4, column= 5, columnspan= 3)

quit_button = ctk.CTkButton(window, text="Quit (q)", corner_radius= 10, hover_color= "#34b7eb", fg_color="#3474eb", bg_color="#242424", font = ("Helvetica", 20), command= quit_all)
quit_button.grid(row=5, column= 2, columnspan= 4, pady= 25)


window.mainloop()
