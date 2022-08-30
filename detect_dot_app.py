# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from unittest import result
import cv2
import numpy as np
import tkinter as tk
from pyparsing import col
from requests import delete


# create txt file with blob/dot corners
def cedric_function():
    global n
    global label
    global button_albus
    global button_bellatrix
    global button_cedric
    global button_disp
    global input_image
    global filename
    global root

    label.grid_forget()
    # Load image
    input_image = cv2.imread(filename)
    # get circle info and center details
    cir_info, xcnts = blob_detector(input_image)

    # prepare table 
    fields = ['Label', 'Pixel Coordinates'] 
        
    rows=[fields]
    counter = 1
    for iter in xcnts:
        row_val1 = str(iter)
        row_val2 = row_val1.replace("\n\n ","\t")
        row=[counter,row_val2]
        
        counter +=1
        rows.append(row)

    # using the savetxt 
    np.savetxt("cedric.txt", 
        rows,
        # delimiter ="", 
        fmt ='% s')


# create csv file with circle details (center and radius in mils)
def bellatrix_function():
    global n
    global label
    global button_albus
    global button_bellatrix
    global button_cedric
    global button_disp
    global input_image
    # global cir_info
    # global xcnts
    global filename
    global root

    label.grid_forget()
    # Load image
    input_image = cv2.imread(filename)
    # get circle info and center details
    cir_info, xcnts = blob_detector(input_image)

    # create table (1 pixel ~= 10.24 mils) 
    fields = ['Label', 'CenterX(mils) from left corner', 'CenterY(mils) from left corner', 'Radius(mils)','Suitable for Bellatrix team?'] 
        
    rows=[fields]
    counter = 1
    for iter in cir_info:
        if (iter[2]*2)>49.8 and (iter[2]*2)<50.1:
            row=[counter,iter[0]*10.24,iter[1]*10.24,iter[2]*10.24,'Yes']
        else:
            row=[counter,iter[0]*10.24,iter[1]*10.24,iter[2]*10.24,'No']

        counter +=1
        rows.append(row)

    # using the savetxt to create csv files
    np.savetxt("bellatrix.csv", 
            rows,
            delimiter =", ", 
            fmt ='% s')


# display(if any) blob/dot is  is 2 pixels with 0.02 margin of error
def albus_function():
    global n
    global label
    global button_albus
    global button_bellatrix
    global button_cedric
    global button_disp
    global input_image
    global filename
    global root

    label.grid_forget()
    # Load image
    input_image = cv2.imread(filename)
    # get circle info and center details
    cir_info, xcnts = blob_detector(input_image)
    
    lv_counter = 0
    
    # filter with diameter in between 1.98 to 2.02 (with 0.02 tolerance)
    xcnts_temp1 = xcnts
    i=0
    for iter1 in cir_info:
        val1 = iter1[2]*2 
        if val1 > 2.02 or val1<1.98:
            xcnts_temp1[i]=[0,0]
        i=i+1      

    xcnts_temp = [x for x in xcnts_temp1 if len(x) == 1]

    # if data exist plot it
    if len(xcnts_temp) > 0:
        cv2.drawContours(input_image, xcnts_temp, -1, (0, 255, 0), 1)

    
    # display image
    image_no_1 = ImageTk.PhotoImage(image=Image.fromarray(input_image))
    label = Label(image=image_no_1)
    label.grid(row=1, column=0, columnspan=3)

    # display NIL text
    lv_counter = "-"
    lv_xcnts = "-----------------------------------"
    
    # to erase old blob info label if exist
    try:
        disp_xcnt.config(text="")
        disp_xcnt_mm.config(text="")
    except:
        pass

    # display new blobl info label
    disp_text = "Label,CenterX,centerY,Radius in pixels: " + lv_counter +  lv_xcnts
    disp_xcnt = tk.Label(root, text=disp_text)

    disp_text_mm = "Label,CenterX,centerY,Radius in pixels: " + lv_counter +  lv_xcnts
    disp_xcnt_mm = tk.Label(root, text=disp_text_mm)
 
    # grid function is for placing the buttons in the frame
    button_albus.grid(row=5, column=0)
    button_bellatrix.grid(row=5, column=1)
    button_cedric.grid(row=5, column=2)
    # button_reset.grid(row=5,column=3)
    blob_number.grid(row = 6,column=1)
    button_disp.grid(row=6,column=3)
    disp_xcnt.grid(row=7,column=0,columnspan=3)
    disp_xcnt_mm.grid(row=8,column=0,columnspan=3)

    root.mainloop()  

# highlight specific blob and its information on the screen 
def dropdown_function():
    global n
    global label
    global button_albus
    global button_bellatrix
    global button_cedric
    global button_disp
    global input_image
    global filename
    global root

    label.grid_forget()
    # Load image
    input_image = cv2.imread(filename)
    # get circle info and center details
    cir_info, xcnts = blob_detector(input_image)

    # highlight specific blob
    lv_counter = 0
    val = n.get()
    if val.isdigit():
        int_val = int(val)-1
        temp_image = input_image
        temp_xcnts = xcnts
        cv2.drawContours(temp_image, xcnts, int_val, (0, 255, 0), 1)
        image_no_1 = ImageTk.PhotoImage(image=Image.fromarray(temp_image))
        lv_counter = str(int_val+1)
        lv_xcnts = str(cir_info[int_val-1])
        lv_xcnts_mm = str([cir_info[int_val-1][0]*0.26,cir_info[int_val-1][1]*0.26,cir_info[int_val-1][2]*0.26])
    else:
        cv2.drawContours(input_image, xcnts, -1, (0, 255, 0), 1)
        image_no_1 = ImageTk.PhotoImage(image=Image.fromarray(input_image))
        label = Label(image=image_no_1)
        lv_counter = "-"
        lv_xcnts = "------------------------------------------------------"

    label = Label(image=image_no_1)
    # We have to show the box so this below line is needed
    label.grid(row=1, column=0, columnspan=3)

    # display specific blob information    
    try:
        disp_xcnt.config(text="")
        disp_xcnt_mm.config(text="")
    except:
        pass

    disp_text = "Label,CenterX,centerY,Radius in pixels: " + lv_counter +  lv_xcnts
    disp_xcnt = tk.Label(root, text=disp_text)
    if val.isdigit():
        disp_text_mm = "Label,CenterX,centerY,Radius in mm from left corner " + lv_counter +  lv_xcnts_mm
    else:
        disp_text_mm = "Label,CenterX,centerY,Radius in mm from left corner " + lv_counter +  lv_xcnts

    disp_xcnt_mm = tk.Label(root, text=disp_text_mm)

    # grid function is for placing the buttons in the frame
    button_albus.grid(row=5, column=0)
    button_bellatrix.grid(row=5, column=1)
    button_cedric.grid(row=5, column=2)
    blob_number.grid(row = 6,column=1)
    button_disp.grid(row=6,column=3)
    disp_xcnt.grid(row=7,column=0,columnspan=3)
    disp_xcnt_mm.grid(row=8,column=0,columnspan=3)

    root.mainloop()

        
# detect blob 
def blob_detector(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # normalize the image and get the gray image of the normalized image
    norm_img = np.zeros(np.size(gray))
    norm_image = cv2.normalize(image,  norm_img, 0, 255, cv2.NORM_MINMAX)
    gray_n = cv2.cvtColor(norm_image, cv2.COLOR_BGR2GRAY)

    # do a simple thresholding
    ret, thresh1 = cv2.threshold(gray_n, 120, 255, cv2.THRESH_BINARY)

    #applying erode() to enlarget the blob which will be used to filter background
    kernelmatrix = np.ones((7, 7), np.uint8)
    resultimage = cv2.erode(thresh1, kernelmatrix)

    # findcontours of the enlarged blobs
    cnts = cv2.findContours(resultimage, cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]


    xcnts = []
    cir_info = []

    # for each contour: 
    # 1. get bounding box, it's area and number of corners in the polygon
    # 2. find a new/actual contour inside the bounding box
    # 3. get's the new contour area

    for cnt in cnts:
        # find approx edge of polygons
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        # find area of bounding box
        x,y,w,h = cv2.boundingRect(cnt)
        area = w*h
        if area < 150 and len(approx)>7:
            new_cnts = cv2.findContours(thresh1[y:y+h,x:x+w], cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
            for new_cnt in new_cnts[0]:
                new_cnt[0][0] = new_cnt[0][0] + x
                new_cnt[0][1] = new_cnt[0][1] + y
            
            xcnts.append(new_cnts[0])

            (cenX, cenY), rad = cv2.minEnclosingCircle(new_cnts[0])
            
            cir_info.append([cenX,cenY,rad])

    return cir_info,xcnts


###########################################################################
######################## Start of the Program #############################
###########################################################################

# Calling the Tk (The initial constructor of tkinter)
root = Tk()

# We will make the title of our app as Image Viewer
root.title("Dot Detector")

# The geometry of the box which will be displayed
# on the screen
root.geometry("700x600")

filename = 'test1.jpg'
# Load image
input_image = cv2.imread(filename)
# get circle info and center details
cir_info, xcnts = blob_detector(input_image)

# draw contours based on the extract blob corners
temp_image = input_image
temp_xcnts = xcnts
cv2.drawContours(temp_image, temp_xcnts, -1, (0, 255, 0), 1)
image_no_1 = ImageTk.PhotoImage(image=Image.fromarray(temp_image))

# display image on the app
label = Label(image=image_no_1)

# We have to show the box so this below line is needed
label.grid(row=1, column=0, columnspan=3)

# 3 buttons for 3 different team
button_albus = Button(root, text="Albus (display)", command=albus_function)

button_bellatrix = Button(root, text="Bellatrix (download)",
						command=bellatrix_function)

button_cedric = Button(root, text="Cedric (download)",
						command=cedric_function)


# label
ttk.Label(root, text = "Choose specific blob :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 6, padx = 10, pady = 25)
  
# Combobox creation
n = tk.StringVar()
blob_number = ttk.Combobox(root, width = 27, textvariable = n)

# display all the blob counters/numbers
trim_xcnts = xcnts
val = range(1,len(cir_info)+1,1)
# Adding combobox drop down list
blob_number['values'] = tuple(val)+tuple(str('A'))
# prevent typing a value
blob_number['state'] = 'readonly'

button_disp = Button(root, text="Display specific blob",
						command=dropdown_function)


# grid function is for placing the buttons in the frame
button_albus.grid(row=5, column=0)
button_bellatrix.grid(row=5, column=1)
button_cedric.grid(row=5, column=2)
blob_number.grid(row = 6,column=1)
button_disp.grid(row=6,column=3)

root.mainloop()
