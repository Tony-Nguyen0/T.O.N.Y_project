# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 12:17:57 2019

@author: Tony Nguyen
"""

#The Only Necessary Yeeter is a code which is used for the purpose of quick and simple image editing to remove the background or a selected colour of an image.
#It will operate inside a GUI for ease of use for user and clearer visualisation of process and progress.

#Refer to 'The Only Necessary Yeeter Documentation' for documentation on how to use the program.

#All the modules which will need to be imported for code to work 
from tkinter import *
from tkinter.colorchooser import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image 
import PIL.ImageGrab
import pyautogui
import os

#A little easter egg that's not really an easter egg and a more like a silly and redundant 
#function that will print out the the lines "Fish" and "Jingle Bells" 4 times
#over when called. 
def death():
    for i  in range(1,5):  
        print('Fish')
        print('Jingle Bells')

#A function that brings up tkinter's colour selection panel.       
def replaceColour():
    #Global scope used by function.
    global fileLocation
    global pictureLabel
    global pixelColour
    global image
    global toleranceEntry
    
    #askcolor() is the tkinter function which brings up the colour selection panel gui.
    colourReplace = askcolor() 
    #outpus the colour in the console in RGB format and hexcode.
    print(colourReplace)
    
    #splits the RGB variables from colourReplace to 3 different variables in respective to the values it contains.
    RGB, HexColours = colourReplace
    replaceR, replaceG, replaceB = RGB
    
    #gets the value in toleranceEntry that user has inputted and if user has not inputted a number toleranceLevel is by default set to 0.
    toleranceLevel = toleranceEntry.get()
    if toleranceLevel == "Tolerance Level":
        toleranceLevel = 0
    else:
        toleranceLevel = int(toleranceEntry.get())
    
    #Assigns the RBG values from pixelColour to 3 different variables 'R' (red value), 'G' (green value) and 'B' (blue value).
    R,G,B = pixelColour
    
    #Opens the image that user has selected and assigns it to to variable img in order to manipulate.
    img = Image.open(fileLocation)
    
    #If the image has already been opened and manipualted by user, the 'img' variable becomes that instead.
    if image == None:
        pass
    else:
        img = image
    
    #converts the image details to RGBA values (red green blue alpha).
    img = img.convert("RGBA")
    
    #gets the RGBA values of each pixel in image and returns it as a list which is assinged to variable 'datas'.
    datas = img.getdata()
    
    #Identifies the RGB values selected by user in image's data with a range decided by user's tolerance level inputted
    #and replaces it with a white colour with zero trasparency RGBA value.
    newData = []
    for item in datas:
        if item[0] in range(R - toleranceLevel, R + toleranceLevel+1) and item[1] in range(G - toleranceLevel, G + toleranceLevel+1) and item[2] in range(B - toleranceLevel, B + toleranceLevel+1):
#        if item[0] == range(R, R+100) and item[1] == range(G, G+100) and item[2] == range(B, B+100):
            newData.append((int(replaceR), int(replaceG), int(replaceB), 255))
        else:
            newData.append(item)
    
    #replaces image data with modified one.
    img.putdata(newData)    
#    img.show()
    
    
    image = img
    #Turns modified image into a displayable entity and displays it in 'pictureLabel', replacing the one before.
    updatedImage = ImageTk.PhotoImage(img)
    pictureLabel.forget()
    pictureLabel = Label(root, bg = defaultColour, image = updatedImage)
    #keeps the content in variable so that it will not be erased due to being a local variable in function.
    pictureLabel.image = updatedImage
    #sets label position in window.
    pictureLabel.pack(side = LEFT)
    

#The function makes the colour selected by user by right clicking on the program after toggling the 'Select Colour' button to show in a square box
#in order ot let user know what colour they hace clicked on. It takes in the arguement of the colour of pixel selected by user in RBG format.   
def identifiedColourBox(coordinateColour):
    #brings in the global scope variable colourLabel to update its content.
    global colourLabel
    #Gets the 3 values of the RGB colour format from arguement and separetes it for use in function.
    R,G,B = coordinateColour
    print(coordinateColour)
    #Turns the RBG colour variables into hex code for tkinter use.
    colour = '#%02x%02x%02x' % (R,G,B)
    print(colour)
    #Deletes previous colourLabel to replace it with the updated one
    canvas.delete(colourLabel)
    #This codes creates the square which will be filled in with the colour selected by user.
    colourLabel = canvas.create_rectangle(0, 0, 50, 50, fill = colour)

#This function identifies the colour of the pixel at the coordinate of mouse.
#Takes in the the 'x' and 'y' arguements which is the x-coordinate and y-coordinate of mouse position.
def getPixelColour(x, y):
    #Takes a screenshot of the screen and saves in temporarily.
    image = PIL.ImageGrab.grab(bbox = None)
    #Gets the image's pixel details, specifically its RBG variables for each pixels. This code uses the 'x' and 'y' coordinate of mouse to get the 
    #colour variable detail of the specific pixel at the coordinate.
    coordinateColour = image.load()[x,y]
    #Calls the identifiedColourBox(coordinateColour) function so that it will update the colour inside the colour box simultaneously when this function is runned.
    identifiedColourBox(coordinateColour)
    #the function imageSelectionTest(x,y) can be called here in order to check if the spot clicked on screen is the right image location that is being checked for 
    #pixel colour. This test is done by the function showing you an image of the location you clicked, if the square image has its center where you clicked
    #then the function can be considered to be checking the correct spot.
    
    #returns the RBG value of pixel from this function to be used in other functions.
    return coordinateColour

#Used to test what pixel is being used. Takes in the arguement 'x' and 'y' coordinate of mouse click location.
def imageSelectionTest(x,y):
    #takes a snapshot with an area of 50 pixels by 50 with the center being the spot clicked by user.
    imageTest= PIL.ImageGrab.grab(bbox = (x-50,y-50,x+50,y+50))
    #brings up your default photo software to display the image snapshotted in the line before.
    imageTest.show()
    #Used to test if the entire screen is available to be 
    showImageOfScreenTest()

#This functions takes a snapshot of the entire area used by PIL.ImageGrab.grab() function.
def showImageOfScreenTest():
    #code used to snapshot entire screen.
    image = PIL.ImageGrab.grab(bbox = None)
    #display snapshot from code in the line bfore.
    image.show(image)

#function that lets the user choose the image file from their directory.
def fileNavigation():
    #uses fileLocation global scope to be used as variable for other functions.
    global fileLocation
    global image
    #Opens file dialog to let user select the image file to be displayed and edited, it gets the file directory. Title of file dialog is set to "Select Image" and its default open location is 
    #users local disk. File filter is by default set to png files but can be changed to all files in order to find non-png image files such as jpg files.
    fileLocation =  filedialog.askopenfilename(initialdir = "/", title = "Select Image",filetypes = (("png files","*.png"),("all files","*.*")))
    #Using the image directory, turns the image into a displayable entity.
    picture = ImageTk.PhotoImage(file = str(fileLocation))
    #gives the directory of the image for testing purposes.
    print(fileLocation)
    
    #Resets the image global variable so that previous picture is completely removed
    image = None
    #returns the image as a displayable entity to be used in other functions to display it in application
    return picture

#Function used to display image selected by user in fileNavigation() function to a label in tkinter.
def viewImage():
    #Gets the global scope pictureLabel to update its content.
    global pictureLabel
    #global variable defaultColour that will be used in function.
    global defaultColour
    #calls the fileNavigation() function and assign its return variable to 'picture' (it's return variable is the image file selected by user as a displayable entity).
    picture = fileNavigation()
    #Gets rid of previous pictureLabel so that there is no duplicate.
    pictureLabel.forget()
    #creates a Label that contains the image specified by user in fileNavigation() function.
    pictureLabel = Label(root, bg = defaultColour, image = picture)
    #used to store the image in a variable so that it doesn't get cleared by being in a function.
    pictureLabel.image = picture
    #sticks the image to the left side of the screen.
    pictureLabel.pack(side = LEFT)
    
#function that scales the image down.    
def resizeImage():
    global pictureLabel
    resizedPicture = pictureLabel.configure(height = 120, width = 80)

#a function that allows a tkinter button to have a toggle functionality
def toggleColourSelect(tog=[0]):
    #gets the colourSelectButton that contains the tkinter button widget.
    global colourSelectButton
    #Allows for the button to change its name and functionality each time it is initiated.
    tog[0] = not tog[0]
    if tog[0]:
        #Sets the text shown on button to 'Selecting Colour'.
        colourSelectButton.config(text='Selecting Colour')
        #Sets the functionality of user's 'Right-Click' to callback function().
        root.bind("<Button-3>", callback)
    else:
        #Sets the text shown on button to 'Select Colour'.
        colourSelectButton.config(text='Select Colour')
        #Removes any function binded to user's 'Right-Click'.
        root.unbind("<Button-3>")

#Function used to all the primary button of application in one place. 
def homeButtons(buttonLayOut):
    #brings in global scope of empty variable that will be assigned to a button widget in order ot be manipulated by other functions.
    global colourSelectButton
    global toleranceEntry
    
    #all buttons are packed inside a set frame widget (buttonsLayOut) in order to keep it neat and made 
    #to fill both x and y axis of frame and anchored to the left side of application. They also all have their respective text shown on them
    #all in Jokerman font.
    
    #Title above button for application.
    Label(buttonLayOut, text = '➕ The Only Necessary Yeeter (T.O.N.Y) ➖', font = 'Jokerman', bg = defaultColour, fg = 'white').pack()
    
    #Button with its on click command set to death() function (an easter egg button but not really), displayed with text: 'Die!'.
    Button(buttonLayOut, text = 'Die!', font = 'Jokerman', command = death).pack(anchor = W, fill = BOTH)
    
    #Button with its on click command set to viewImage() function, shown with text: 'Import Image'.
    Button(buttonLayOut, text='Import Image', font = 'Jokerman', command=viewImage).pack(anchor = W, fill = BOTH)
    
    #Button with its on click command set to replaceColour() function, shown with text: 'Replace Colour'. 
    Button(buttonLayOut, text='Replace Colour', font = 'Jokerman', command=replaceColour).pack(anchor = W, fill = BOTH)
    
    #Button with its on click command set to resizeImage() function, shown with text: 'Resize Image'.
#    Button(buttonLayOut, text='Resize Image', font = 'Jokerman', command=resizeImage).pack(anchor = W, fill = BOTH)
    
    #Button with its on click command set to colourRemove() function, shown with text: 'Remove Colour'.
    Button(buttonLayOut, text = 'Remove Colour', font = 'Jokerman', command=colourRemove).pack(anchor = W, fill = BOTH)

    #Button with its on click command set to toggleColourSelect(tog=[0]) function, shown with text: "Select Colour", assigned to variable
    #colourSelectButton.
    colourSelectButton = Button(buttonLayOut, text = 'Select Colour', font = 'Jokerman', command=toggleColourSelect)
    colourSelectButton.pack(anchor = W, fill = BOTH)
    
    #Button with its on click command set to saveImage() function, shown with text: "Save file".
    Button(buttonLayOut, text = 'Save file', font = 'Jokerman', command=saveImage).pack(anchor = W, fill = BOTH)
    
    #Entry slot for user to input tolerance of colour removal.
    toleranceEntry = Entry(buttonLayOut, font = 'Jokerman', fg = '#%02x%02x%02x' % (128,128,128), justify = 'center')
    toleranceEntry.pack()
    
    #Puts a temporary text stating 'Tolerance level' for user to identify button functionality.
    toleranceEntry.insert(0, "Tolerance Level")
    
#Function used to remove specfic colours from an image.    
def colourRemove(): 
    #Global scope used by function.
    global fileLocation
    global pictureLabel
    global pixelColour
    global image
    global toleranceEntry
    
    #gets the value in toleranceEntry that user has inputted and if user has not inputted a number toleranceLevel is by default set to 0.
    toleranceLevel = toleranceEntry.get()
    if toleranceLevel == "Tolerance Level":
        toleranceLevel = 0
    else:
        toleranceLevel = int(toleranceEntry.get())
    
    #Assigns the RBG values from pixelColour to 3 different variables 'R' (red value), 'G' (green value) and 'B' (blue value).
    R,G,B = pixelColour
    
    #Opens the image that user has selected and assigns it to to variable img in order to manipulate.
    img = Image.open(fileLocation)
    
    #If the image has already been opened and manipualted by user, the 'img' variable becomes that instead.
    if image == None:
        pass
    else:
        img = image
    
    #converts the image details to RGBA values (red green blue alpha).
    img = img.convert("RGBA")
    
    #gets the RGBA values of each pixel in image and returns it as a list which is assinged to variable 'datas'.
    datas = img.getdata()
    
    #Identifies the RGB values selected by user in image's data with a range decided by user's tolerance level inputted
    #and replaces it with a white colour with zero trasparency RGBA value.
    newData = []
    for item in datas:
        if item[0] in range(R - toleranceLevel, R + toleranceLevel+1) and item[1] in range(G - toleranceLevel, G + toleranceLevel+1) and item[2] in range(B - toleranceLevel, B + toleranceLevel+1):
#        if item[0] == range(R, R+100) and item[1] == range(G, G+100) and item[2] == range(B, B+100):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    #replaces image data with modified one.
    img.putdata(newData)    
#    img.show()
    
    image = img
    #Turns modified image into a displayable entity and displays it in 'pictureLabel', replacing the one before.
    updatedImage = ImageTk.PhotoImage(img)
    pictureLabel.forget()
    pictureLabel = Label(root, bg = defaultColour, image = updatedImage)
    #keeps the content in variable so that it will not be erased due to being a local variable in function.
    pictureLabel.image = updatedImage
    #sets label position in window.
    pictureLabel.pack(side = LEFT)

def getEntry():
    #global variables manipualted in function.
    global fileNameEntry
    global fileName
    global root2
    #gets the string in entry slot typed by user.
    fileName = fileNameEntry.get()
    
    #prints user's entry text for testing.
    print(fileName)
    
    #Terminate second window.
    root2.quit()
    
def askFileName():
    #global variables which will be used and manipulated in function.
    global defaultColour
    global fileNameEntry
    global fileName
    global root2
    
    #creates a second window above the originaly parent window 'root'.
    root2 = Toplevel()
    
    #specific details of window such as title, size, colour, disabled resizing and icon.
    root2.title('Enter file name')
    root2.geometry('350x100')
    root2.configure(bg = defaultColour)
    root2.resizable(False, False)
    root2.iconbitmap('White_face_and_blue_moon.ico')
    root2.overrideredirect(True)
    
    #creates label next to entry slot that has text: 'Save File name as:'
    Label(root2, bg = defaultColour, fg = 'white', font = 'Jokerman', text = 'Save File name as:').grid(column = 1, row = 1)
    
    #creates entry slot for user.
    fileNameEntry = Entry(root2)
    #entry slot position
    fileNameEntry.grid(column = 2, row = 1)
#    fileNameEntry.focus_set()
    
    #confirmation button with function getEntry().
    Button(root2, text = 'Confirm', font = 'Jokerman', command = getEntry).grid(column = 2, row = 2)
    
    #keeps second window active.
    root2.mainloop()

#Function used which enables for user to save modified image in a diretory chosen by them.
def saveImage():
    #global variables used in function.
    global image
    global fileName
    
    #calls askFileName() function.
    askFileName()
    
    #after function ends, file dialog will come up for user to locate save directory that they want file to be saved in.
    location = filedialog.askdirectory(title = "Select save file location")
    print(location)
    
    #saves file to the location given by user, and makes it as a png extension.
    image.save(os.path.join(location, fileName +'.png'))
    
    #a messagebox that comes up to confirm to user that file has been saved.
    messagebox.showinfo("File confirmation", "File saved :)")
    

#function that checks mouse position and pixelColour of pixel at mouse position on mouse click 
#as well as initiates gives the mouse position for the getPixelColour function.     
def callback(event):
    #gets empty gobal scope variable 'pixelColour' which will be assigned a new value in this function in order for it to be used by other functions.
    global pixelColour
    
    #gets the x and y coordinate of mouse position
    x,y= pyautogui.position()
    
    #displays in console the x and y coordinate of mouse
    print(x,y)
    
    #assigns the previously empty variable 'pixelColour' with the return value of getPixelColour(x,y) which is the RBG values of the pixel at mouse position.
    pixelColour = getPixelColour(x,y)
    
    #displays in console the RGB value of pixel at mouse position.
    print(pixelColour)

#root = Tk() 
#frame = Frame(root, width=1920, height=1080)
#frame.bind("<Button-1>", callback)
#frame.pack()
#root.mainloop()
 
#Initiates the application window of tkinter.
root = Tk()

#assigns defaultColour with a hex value
defaultColour = '#%02x%02x%02x' % (106,107,108)

#sets tkinter application window background to the hex code in defaultColour variable.
root.configure(background = defaultColour)

#sets a specified corner icon for application window.
root.iconbitmap('White_face_and_blue_moon.ico')

#sets title of application window.
root.title("➕ The Only Necessary Yeeter (T.O.N.Y) ➖")

#disables the ability to resize tkinter application window.
root.resizable(False, False)

#sets the cursor when hovering over application window to a 'dotbox' cursor.
root.config(cursor = 'dotbox')

#Empty strings that need to exist for other function to manipualte as global scope.
fileLocation = None
pixelColour = None
colourSelectButton = None
image = None
fileNameEntry = None
fileName = None
root2 = None
toleranceEntry = None
#root.attributes('-fullscreen', True)
#root.state('zoomed')

#Frame inside application window to allow for neater catogorisation of widgets, anchored to the top left of application window with it's background also
#set to defaultColour variable colour.
buttonLayOut = Frame(root, bg = defaultColour)
#The buttonLayout frame is set to stay on the top left of the application.
buttonLayOut.pack(side =LEFT, anchor = N)

#Empty Label to be manipulated by functions and updated when in use
pictureLabel = Label(root, text = '')

#calls the homeButtons function
homeButtons(buttonLayOut)

#Creates an empty canvas which will be updated and manipulated by functions in program.
canvas = Canvas(buttonLayOut, width = 40, height = 40) 
canvas.pack()
colourLabel = canvas.create_rectangle(0,0,50,50, fill = None)

#Keeps tkinter window active.  
root.mainloop()  




