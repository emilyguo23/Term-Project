import random, math
from cmu_112_graphics import *
import numpy as np

# This file contains all functions for the user interface (help screens, buttons, etc)
# as well as reading / saving .txt files

##########################################
# Button Class
##########################################

class Button(object):
    def __init__(self, x0, y0, x1, y1, name):
        coords = (x0, y0, x1, y1)
        self.coords = coords
        self.name = name
        self.boxCol = None
        self.text = None
    
    def inButton(self, x, y):
        x0, y0, x1, y1 = self.coords
        if (x0 <= x <= x1) and (y0 <= y <= y1):
            return True
        return False
    
    def aes(self, text, font, textCol, boxCol):
        self.font = font
        self.text = text
        self.textCol = textCol
        self.boxCol = boxCol
    
    def setColor(self, color):
        self.boxCol = color

    def setText(self, text):
        self.text = text

def drawButtons(app, canvas, buttonList):
    for button in buttonList:
        text = button.text
        font = button.font
        textCol = button.textCol
        boxCol = button.boxCol
        x0, y0, x1, y1 = button.coords
        textX, textY = (x0 + x1)/2, (y0 + y1)/2
        canvas.create_rectangle(button.coords, fill = boxCol, width = 3)
        canvas.create_text(textX, textY, text = text, font = font, fill = textCol)

##########################################
# Help Boxes
##########################################

def drawHelpScreen(app, canvas):
    if app.helpScreen == False: return
    if app.helpScreen2 == True: return
    canvas.create_rectangle(188.75, 75, app.width - 188.75, app.height - 75, fill = 'burlywood1', width = 4)
    boldFont, font = "Avenir 30 bold underline", "Avenir 20"
    startMessages = ["Start Screen", 
    """On the start screen, you can choose between flat or randomly-generated
       terrains. You can some back to the start screen anytime to change your choice!
       Your edited maps will not be lost if you return to the start screen."""]
    canvas.create_text(640, 125, text = startMessages[0], font = boldFont)
    canvas.create_text(640, 185, text = startMessages[1], font = font)

    mapMessages = ["Map Editing",
    """In Map Editing mode, hover over vertices to select. Once the red circle appears over
       a vertex, that vertex is selected. Drag the vertex to a new height to edit.
       In Map Editing mode, press "q" to learn more about buttons for navigation."""]
    canvas.create_text(640, 305, text = mapMessages[0], font = boldFont)
    canvas.create_text(640, 365, text = mapMessages[1], font = font)

    colorMessages = ["Color Assignment",
    """Map Generator assigns color by altitude sections where Level 1 is the lowest altitude
       and Level 7 is the highest. Click on a rectangle in the "Altitude Colors" row, then
       type in a 6-digit hex value (starting with "#") or a valid Python color name. Hit Enter 
       to assign. In Color Assignment mode, press "q" to learn more about adding color. 
       Colors can be changed anytime!"""]
    canvas.create_text(640, 485, text = colorMessages[0], font = boldFont)
    canvas.create_text(640, 575, text = colorMessages[1], font = font)

# instructions on key presses, adding color
def drawHelpScreen2(app, canvas):
    if app.helpScreen2 == False: return
    if app.helpScreen == True: return
    boldFont, font = "Avenir 30 bold underline", "Avenir 20"

    if app.mode == 'terrainMode' or app.mode == 'flatMode':
        message = ["Map Editing",
    """In Map Editing mode, parts of the map may be off-screen due to the map's size and/or
       elevation. These keys can be used to nagivate the map:
       Up, Down: shifts map along z-axiz
       Left, Right: shifts map along x-axis
       "x", "z": shift map along y-axis
       "p": toggle auto-rotation feature
       "r", "t": rotates map manually, clockwise and counterclockwise respectively
       Additional commands:
       SPACE: (Flat mode) Resets map to flat terrain; (Terrain mode) Generates new map!
       * Caution: Pressing SPACE erases all progress! *
       Wireframe lines may overlap due to drawing pattern; rotate to view all angles."""]
        canvas.create_rectangle(188.75, 75, app.width - 188.75, 475, fill = 'burlywood1', width = 4)
        canvas.create_text(640, 120, text = message[0], font = boldFont)
        canvas.create_text(640, 290, text = message[1], font = font)

    if app.mode == 'colorMode':
        message = ["Color Addition",
    """    Click one of the numbered boxes next to "Altitude Colors", then start typing!
    Colors can be assigned using both hex values and color names. Some examples:
       Hex value: "#2d6a4f" (must include "#" as first character entry)
       Color name: "dodger blue"
       There is no need to include quotation marks around entries!
       Press "c" when no altitude is selected for color references."""]
        canvas.create_rectangle(188.75, 75, app.width - 188.75, 320, fill = 'burlywood1', width = 4)
        canvas.create_text(640, 115, text = message[0], font = boldFont)
        canvas.create_text(640, 215, text = message[1], font = font)
    
##########################################
# File Loading / Saving
# readFile and writeFile are from https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
##########################################

def fileToPoints(app, path):
    try:
        file = readFile(path)
        pointsList = file.splitlines()
        newPoints = []
        for point in pointsList:
            coord = point.split(',')
            x, y, z = float(coord[0]), float(coord[1]), float(coord[2])
            newPoints.append([x, y, z])
        newPoints = np.array(newPoints)
        return newPoints
    except:
        return 'Failed'

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def pointsToFile(app, path, pointsList):
    if path[-4:len(path)] != '.txt':
        app.showMessage('Invalid file name, please try again!')
        return
    pointsList = pointsList.tolist()
    content = ''
    for i in range(len(pointsList)):
        point = pointsList[i]
        x, y, z = str(point[0]), str(point[1]), str(point[2])
        content += x + ',' + y + ',' + z + ',' + '\n'
    writeFile(path, content)
    app.showMessage('Elevation saved to file' + '"' + path + '"!')

def writeFile(path, content):
    with open(path, "wt") as f:
            f.write(content)
