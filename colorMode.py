import random, math, copy, string
from cmu_112_graphics import *
import numpy as np
from terrainMode import *
from interface import *

# This file contains all functions used in color selection and assignment

def createDisplay(app):
    if app.lastMode == 'terrainMode':
        app.displayPoints = copy.deepcopy(app.terrainPoints) # in [x, y, z] format
        app.displayVectorXY =  copy.deepcopy(app.vectorXY) # in [x, y] format
    elif app.lastMode == 'flatMode':
        app.displayPoints = copy.deepcopy(app.flatPoints)
        app.displayVectorXY = copy.deepcopy(app.flatVectorXY)
    app.displayPoints += np.array([0,0,-100]) 
    app.displayPolygons = createPolygons(app, app.displayVectorXY)
    assignAltitude(app, app.displayPolygons, app.displayPoints)
    assignLevels(app, app.displayPolygons)
    app.colorList = [None for i in range(0, app.numColors)] 

def assignAltitude(app, polygonList, pointsList):
    app.altitudeList = np.zeros((len(polygonList), 1))
    for i in range(len(polygonList)):
        polygon = polygonList[i]
        index1, index2, index3, index4 = polygon.indexes
        coord1 = pointsList[index1]
        coord2 = pointsList[index2]
        coord3 = pointsList[index3]
        coord4 = pointsList[index4]
        zVal = (coord1[2] + coord2[2] + coord3[2] + coord4[2])/4
        polygon.setAltitude(zVal)
        app.altitudeList[i] = zVal

def assignLevels(app, polygonList):
    # find max, min of all altitudes
    # for each polygon, assign by altitude
    maxAlt, minAlt = max(app.altitudeList), min(app.altitudeList)
    section = (maxAlt - minAlt)/app.numColors
    for i in range(len(polygonList)):
        polygon = polygonList[i]
        alt = polygon.altitude
        diff = alt - minAlt
        if diff == 0:
            level = 1
        else:
            level = int((diff // section) + 1)
        polygon.setLevel(level)

def isHexValue(string):
    hexVals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    if string[0] != "#" or len(string) != 7: return False
    for c in string[1:]:
        if c not in hexVals: return False
    return True

def assignColors(app, polygonList, string, selectedLevel):
    level = selectedLevel
    if len(string) == 0: return
    if isHexValue(string) == False and (string not in app.allColors): return
    for polygon in polygonList:
        if polygon.level == level:
            polygon.setColor(string)
    app.colorList[selectedLevel - 1] = string

def refreshColors(app, polygonList, colorList):
    for polygon in polygonList:
        level = polygon.level
        if level > 6: level = 6
        if colorList[level - 1] != None: # need level - 1 since app.colorList indexed from 0
            polygon.setColor(colorList[level - 1]) 

def colorButtons(app):
    if app.lastMode == None: return
    buttonList = []
    lastMode = Button(50, app.height-100, 250, app.height-50, app.lastMode)
    lastMode.aes("Back to Terrain Edit", "Avenir 20", "black", "lightgreen")
    buttonList.append(lastMode)
    finishMode = Button(app.width - 250, app.height-100, 
                        app.width - 50, app.height-50, "finishMode")
    finishMode.aes("Finish!", "Avenir 30", "black", "lightblue")
    buttonList.append(finishMode)
    return buttonList

def panelButtons(app):
    buttonList = []
    # Create color buttons
    width, height = 125, 50
    startX, startY = 100, 30
    color1 = Button(startX + 1*width, startY,
                    startX + (1+1)*width, startY + height, name = '1')
    buttonList.append(color1)
    color2 = Button(startX + 2*width, startY,
                    startX + (2+1)*width, startY + height, name = '2')
    buttonList.append(color2)
    color3 = Button(startX + 3*width, startY,
                    startX + (3+1)*width, startY + height, name = '3')
    buttonList.append(color3)
    color4 = Button(startX + 4*width, startY,
                    startX + (4+1)*width, startY + height, name = '4')
    buttonList.append(color4)
    color5 = Button(startX + 5*width, startY,
                    startX + (5+1)*width, startY + height, name = '5')
    buttonList.append(color5)
    color6 = Button(startX + 6*width, startY,
                    startX + (6+1)*width, startY + height, name = '6')
    buttonList.append(color6)
    for button in buttonList:
        index = int(button.name)
        if app.colorList[index - 1] != None:
            button.setColor(app.colorList[index - 1])
    # hexadecimal button
    hexButton = Button(20, 100, 215, 150, 'hexButton')
    hexButton.setColor('papaya whip')
    hexButton.setText(app.inputString)
    buttonList.append(hexButton)
    return (buttonList)

def drawPanelButtons(app, canvas):
    for button in app.panelButtons:
        if button.boxCol == None: color = 'white'
        else: color = button.boxCol
        x0, y0, x1, y1 = button.coords
        if button.text == None:
            canvas.create_rectangle(x0, y0, x1, y1, fill = color)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill = color)
            canvas.create_text((x0 + x1)/2, (y0 + y1)/2,
                                text = str(button.text), font = 'Avenir 23')
    
def drawBlankBoxes(app, canvas):
    width, height = 125, 30
    startX, startY = 100, 50
    for i in range(1, app.numColors + 1):
        canvas.create_text(startX + (i+0.5)*width, startY + 1.5*height,
                            text = i, font = "Avenir 25")
    canvas.create_text(1.2*startX, startY+height/2 - 10, text = "Altitude Colors", font = "Avenir 25")

def drawBoxBorders(app, canvas):
    border = 'firebrick2'
    if app.inputBox == True:
        canvas.create_rectangle(20, 100, 215, 150, outline = border, width = 3)
    if app.selectedLevel != None:
        for button in app.panelButtons[:len(app.panelButtons) - 1]:
            if int(button.name) == app.selectedLevel:
                x0, y0, x1, y1 = button.coords
                canvas.create_rectangle(x0, y0, x1, y1, outline = border, width = 3)

##########################################
# Finish Mode 
##########################################

def finishButtons(app):
    if app.lastMode == None: return
    buttonList = []
    lastMode = Button(50, app.height-100, 250, app.height-50, app.lastMode)
    lastMode.aes("Back to Color Edit", "Arial 20", "black", "lightgreen")
    buttonList.append(lastMode)
    startMode = Button(app.width//2 - 100, app.height-100, app.width//2 + 100, app.height-50, 'startMode')
    startMode.aes("Start Again", "Arial 20", "black", "lightblue")
    buttonList.append(startMode)
    saveButton = Button(app.width - 250, app.height-100, 
                        app.width - 50, app.height-50, 'save')
    saveButton.aes("Save Elevation!", "Arial 20", "black", "plum1")
    buttonList.append(saveButton)
    return buttonList
        