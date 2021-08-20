import random, math, string
from cmu_112_graphics import *
import numpy as np
from terrainMode import *
from colorMode import *
from interface import *

# This file is the main file that contains runApp along with all screen modes

##########################################
# Starting Screen Mode
##########################################
# Terrain selection: flat or randomly generated

def startButtons(app):
    buttonList = []
    terrainMode = Button(app.width//5 - 150, 7*app.height//8 - 50,
                            app.width//5 + 150, 7*app.height//8 + 50, "terrainMode")
    terrainMode.aes("Random Terrain", "Avenir 35", "black", "lightgreen")
    buttonList.append(terrainMode)
    flatMode = Button(4*app.width//5 - 150, 7*app.height//8 - 50,
                            4*app.width//5 + 150, 7*app.height//8 + 50, "flatMode")
    flatMode.aes("Flat Map", "Avenir 35", "black", "lightblue")
    buttonList.append(flatMode)
    uploadButton = Button(app.width//2 - 100, 8*app.height//9 - 30,
                            app.width//2 + 100, 8*app.height//9 + 30, 'upload')
    uploadButton.aes("Upload Map", "Avenir 27", "black", "SlateGray3")
    buttonList.append(uploadButton)
    return buttonList

def startMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 75, 
                    text="""SANDBOX MAP CREATOR""", font = 'Avenir 80')
    font = 'Avenir 30'
    canvas.create_text(app.width/2, 160, 
                    text="""Customize your 3D map terrains and colors in this sanbox tool 
                        where your imagination is the limit!""", font = font, fill = 'SpringGreen3')
    canvas.create_text(app.width/2, 225, 
                    text='To begin, select a flat or randomly generated terrain.', 
                        font = font, fill = 'firebrick1')
    canvas.create_text(app.width/2, 270, text="Press 'h' for help and instructions!", 
                       font = font, fill = 'dodger blue')
    # Draw image
    canvas.create_image(app.width//2, 460, image = ImageTk.PhotoImage(app.startImage))
    # Draw buttons
    for button in app.startButtons:
        text = button.text
        font = button.font
        textCol = button.textCol
        boxCol = button.boxCol
        x0, y0, x1, y1 = button.coords
        textX, textY = (x0 + x1)/2, (y0 + y1)/2
        canvas.create_rectangle(button.coords, fill = boxCol, width = 3)
        canvas.create_text(textX, textY, text = text, font = font, fill = textCol)
    drawHelpScreen(app, canvas)

def startMode_keyPressed(app, event):
    if event.key == 'h': app.helpScreen = not app.helpScreen

def startMode_mousePressed(app, event):
    x, y = event.x, event.y
    for button in app.startButtons:
        if button.inButton(x, y) == True:
            if button.name != 'upload':
                app.lastMode = app.mode
                app.mode = button.name
            elif button.name == 'upload': 
                name = app.getUserInput("Enter name of terrain file (ending in .txt):")
                if name[-4:len(name)] != '.txt':
                    app.showMessage('Invalid file name, please try again!')
                    return
                if len(fileToPoints(app, name)) > 6:
                    app.showMessage('Uploaded file named ' + '"' + name + '"!')
                    app.terrainPoints = fileToPoints(app, name)
                    app.mode = 'terrainMode'
                elif len(fileToPoints(app, name)) == 6:
                    app.showMessage('No file with such name, please try again!')
                    appStarted(app)

##########################################
# Flat Mode
##########################################

def flatButtons(app):
    buttonList = []
    startMode = Button(50, app.height-100, 250, app.height-50, 'startMode')
    startMode.aes("Back to Start", "Avenir 30", "black", "lightgreen")
    buttonList.append(startMode)
    colorMode = Button(app.width - 250, app.height-100, 
                        app.width - 50, app.height-50, "colorMode")
    colorMode.aes("Add Color", "Avenir 30", "black", "lightblue")
    buttonList.append(colorMode)
    return buttonList

def flatMode_keyPressed(app, event):
    # navigational key press commands in ALL MODES adapted from 3DGraphicsDemo
    if event.key == 'h': app.helpScreen = not app.helpScreen
    elif event.key == 'q': app.helpScreen2 = not app.helpScreen2
    elif event.key == 'p': # toggles pause (for rotation animation)
        app.isPaused = not app.isPaused
    elif event.key == 'r': # rotates points clockwise 
        app.flatPoints = rotate(app, app.flatPoints, 10)
    elif event.key == 't': # rotates points counterclockwise
        app.flatPoints = rotate(app, app.flatPoints, -10)
    elif event.key == 'Up': # moves cube +z
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([0,0,20])
    elif event.key == 'Down': # moves cube -z
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([0,0,-20]) 
    elif event.key == 'Left': # moves cube +x
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([20,0,0])
    elif event.key == 'Right': # moves cube -x
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([-20,0,0])
    elif event.key == 'z': # moves cube -y
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([0,-20,0])
    elif event.key == 'x': # moves cube +y
        for i in range(len(app.flatPoints)):
            app.flatPoints[i] += np.array([0,20,0])
    elif event.key == 'Space':
        appStarted(app)
        app.mode = 'flatMode'
    elif event.key == 'Tab':
        app.multiselect = not app.multiselect

def flatMode_mousePressed(app, event):
    point = (event.x, event.y)
    index = nearestPoint(app.flatVectorXY, point)
    x1, y1 = app.flatVectorXY[index]
    if dist(event.x, event.y, x1, y1) <= 6:
        app.selectedVertex = index
    x, y = event.x, event.y
    for button in app.flatButtons:
        if button.inButton(x, y) == True:
            app.lastMode = app.mode
            app.mode = button.name
            app.isPaused = True
            if button.name == "colorMode":
                createDisplay(app)
                app.colorButtons = colorButtons(app)
                app.panelButtons = panelButtons(app)
                # for colorList, use actual level index (start from 1, not 0)
                app.colorList = [None for i in range(0, app.numColors)]
            
def flatMode_mouseMoved(app, event):
    app.mouseX, app.mouseY = point = event.x, event.y
    index = nearestPoint(app.flatVectorXY, point)
    x1, y1 = app.flatVectorXY[index]
    if dist(event.x, event.y, x1, y1) <= 6:
            app.highlightedVertex = index

def flatMode_mouseDragged(app, event):
    index = app.selectedVertex
    if index == None: return
    x, newY = app.flatVectorXY[index][0], event.y
    # manually calculate new z value
    pointX, pointY = app.flatPoints[index][0], app.flatPoints[index][1]
    angleX, angleY = math.sin(app.xAxisAngle), math.sin(app.yAxisAngle)
    originY = app.origin[1]
    newZ = originY - pointX*angleX - pointY*angleY - newY
    app.flatPoints[index][2] = newZ
    if app.multiselect != False:
        nearbyPoints = [index + 1, index - 1, index - app.n, index + app.n, 
                  index - app.n - 1, index - app.n + 1,
                  index + app.n - 1, index + app.n + 1]
        for elem in nearbyPoints:
            app.flatPoints[elem][2] = 0.95*newZ

def flatMode_timerFired(app):
    if not app.isPaused:
        app.flatPoints = rotate(app, app.flatPoints, 10)
    app.flatVectorXY = vecs2Graph(app, app.flatPoints)
    app.flatPolygons = createPolygons(app, app.flatVectorXY)

def flatMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,1280,755, fill = 'light yellow')
    printText(app, canvas)
    drawButtons(app, canvas, app.flatButtons)
    drawMultiselectToggle(app, canvas)
    drawPolygons(app, canvas, app.flatPolygons, app.flatPoints)
    highlightVertex(app, canvas, app.flatVectorXY)
    drawHelpScreen(app, canvas)
    drawHelpScreen2(app, canvas)

##########################################
# Terrain Mode
##########################################
# Adjust screen altitudes by dragging vertices

def terrainMode_keyPressed(app, event):
    if event.key == 'h': app.helpScreen = not app.helpScreen
    elif event.key == 'q': app.helpScreen2 = not app.helpScreen2
    elif event.key == 'p': # toggles pause (for rotation animation)
        app.isPaused = not app.isPaused
    elif event.key == 'r': # rotates points clockwise 
        app.terrainPoints = rotate(app, app.terrainPoints, 10)
    elif event.key == 't': # rotates points counterclockwise
        app.terrainPoints = rotate(app, app.terrainPoints, -10)
    elif event.key == 'Up': # moves cube +z
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([0,0,20])
    elif event.key == 'Down': # moves cube -z
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([0,0,-20]) 
    elif event.key == 'Left': # moves cube +x
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([20,0,0])
    elif event.key == 'Right': # moves cube -x
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([-20,0,0])
    elif event.key == 'z': # moves cube -y
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([0,-20,0])
    elif event.key == 'x': # moves cube +y
        for i in range(len(app.terrainPoints)):
            app.terrainPoints[i] += np.array([0,20,0])
    elif event.key == 'Space':
        appStarted(app)
        app.mode = 'terrainMode'
    elif event.key == 'Tab':
        app.multiselect = not app.multiselect

def terrainMode_mousePressed(app, event):
    point = (event.x, event.y)
    index = nearestPoint(app.vectorXY, point)
    x1, y1 = app.vectorXY[index]
    '''
    if dist(event.x, event.y, x1, y1) <= 6:
        app.selectedVertex = index
    '''
    x, y = event.x, event.y
    for button in app.terrainButtons:
        if button.inButton(x, y) == True:
            app.lastMode = app.mode
            app.mode = button.name
            app.isPaused = True
            if button.name == "colorMode":
                createDisplay(app)
                app.colorButtons = colorButtons(app)
                app.panelButtons = panelButtons(app)
                # for colorList, use actual level index (start from 1, not 0)
                app.colorList = [None for i in range(0, app.numColors)] 

def terrainMode_mouseMoved(app, event):
    app.mouseX, app.mouseY = point = event.x, event.y
    index = nearestPoint(app.vectorXY, point)
    x1, y1 = app.vectorXY[index]
    if dist(event.x, event.y, x1, y1) <= 6:
            app.selectedVertex = index
            app.highlightedVertex = index

def terrainMode_mouseDragged(app, event):
    index = app.selectedVertex
    if index == None: return
    x, newY = app.vectorXY[index][0], event.y
    # manually calculate new z value
    pointX, pointY = app.terrainPoints[index][0], app.terrainPoints[index][1]
    angleX, angleY = math.sin(app.xAxisAngle), math.sin(app.yAxisAngle)
    originY = app.origin[1]
    newZ = originY - pointX*angleX - pointY*angleY - newY
    app.terrainPoints[index][2] = newZ
    if app.multiselect != False:
        nearbyPoints = [index + 1, index - 1, index - app.n, index + app.n, 
                  index - app.n - 1, index - app.n + 1,
                  index + app.n - 1, index + app.n + 1]
        for elem in nearbyPoints:
            app.terrainPoints[elem][2] = 0.9*newZ
    
def terrainMode_timerFired(app):
    if not app.isPaused:
        app.terrainPoints = rotate(app, app.terrainPoints, 10)
    app.vectorXY = vecs2Graph(app, app.terrainPoints)
    app.polygons = createPolygons(app, app.vectorXY)

def terrainMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,1280,755, fill = 'light yellow')
    printText(app, canvas)
    drawButtons(app, canvas, app.terrainButtons)
    drawMultiselectToggle(app, canvas)
    drawPolygons(app, canvas, app.polygons, app.terrainPoints)
    highlightVertex(app, canvas, app.vectorXY)
    drawHelpScreen(app, canvas)
    drawHelpScreen2(app, canvas)

##########################################
# Color Selection / Terrain Addition Mode
##########################################
# Select colors for various altitudes or choose from existing palettes
# Add various textures to canvas with cursor (or selecting polygons)

def colorMode_keyPressed(app, event):
    if app.inputBox == False:
        if event.key == 'h': app.helpScreen = not app.helpScreen
        elif event.key == 'q': app.helpScreen2 = not app.helpScreen2
        elif event.key == 'p': # toggles pause (for rotation animation)
            app.isPaused = not app.isPaused
        elif event.key == 'r': # rotates points clockwise 
            app.displayPoints = rotate(app, app.displayPoints, 10)
        elif event.key == 't': # rotates points counterclockwise
            app.displayPoints = rotate(app, app.displayPoints, -10)
        elif event.key == 'Up': # moves points +z
            for i in range(len(app.displayPoints)):
                app.displayPoints[i] += np.array([0,0,20])
        elif event.key == 'Down': # moves points -z
            for i in range(len(app.displayPoints)):
                app.displayPoints[i] += np.array([0,0,-20]) 
        elif event.key == 'Left': # moves points +x
            for i in range(len(app.displayPoints)):
                app.displayPoints[i] += np.array([20,0,0])
        elif event.key == 'Right': # moves points -x
            for i in range(len(app.displayPoints)):
                app.displayPoints[i] += np.array([-20,0,0])
        elif event.key == 'c':
            app.showReference = not app.showReference
    elif app.inputBox == True:
        if event.key in string.ascii_letters or event.key in string.digits:
            app.inputString += event.key
        elif event.key == 'Space':
            app.inputString += ' '
        elif event.key == "#":
            app.inputString += event.key
        elif event.key == 'Delete' and len(app.inputString) > 0:
            app.inputString = app.inputString.rstrip(app.inputString[-1])
        elif event.key == 'Enter':
            assignAltitude(app, app.displayPolygons, app.displayPoints)
            assignLevels(app, app.displayPolygons)
            assignColors(app, app.displayPolygons, app.inputString, app.selectedLevel)
            app.inputBox = False
            app.selectedLevel = None
            app.inputString = ''


def colorMode_mousePressed(app, event):
    x, y = event.x, event.y
    for button in app.colorButtons:
        if button.inButton(x, y) == True:
                app.lastMode = app.mode
                app.mode = button.name
                app.isPaused = True
                if button.name == 'finishMode':
                    app.finishButtons = finishButtons(app) 
                    app.displayPoints += np.array([0, 0, 100])
                    app.isPaused = False
    for button in app.panelButtons: 
        if button.inButton(x, y) == True and button.name != 'hexButton':
            app.selectedLevel = int(button.name)
            app.inputBox = True

def colorMode_timerFired(app):
    if not app.isPaused:
        app.displayPoints = rotate(app, app.displayPoints, 10)
    app.panelButtons = panelButtons(app)
    app.displayVectorXY = vecs2Graph(app, app.displayPoints)
    app.displayPolygons = createPolygons(app, app.displayVectorXY)
    assignAltitude(app, app.displayPolygons, app.displayPoints)
    assignLevels(app, app.displayPolygons)
    refreshColors(app, app.displayPolygons, app.colorList)

def colorMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,1280,755, fill = 'light yellow')
    drawButtons(app, canvas, app.colorButtons)
    drawPanelButtons(app, canvas)
    drawBlankBoxes(app, canvas)
    drawBoxBorders(app, canvas)
    printText(app, canvas)
    drawPolygons(app, canvas, app.displayPolygons, app.displayPoints)
    drawHelpScreen(app, canvas)
    drawHelpScreen2(app, canvas)
    if app.showReference == True:
        canvas.create_image(app.width//2, app.height//2, 
                            image = ImageTk.PhotoImage(app.colorReference))
    
##########################################
# Display and Save Mode
##########################################
# Rotate completed map, option to save to computer

def finishMode_timerFired(app):
    if not app.isPaused:
        app.displayPoints = rotate(app, app.displayPoints, 10)
    app.displayVectorXY = vecs2Graph(app, app.displayPoints)
    app.displayPolygons = createPolygons(app, app.displayVectorXY)
    assignAltitude(app, app.displayPolygons, app.displayPoints)
    assignLevels(app, app.displayPolygons)
    refreshColors(app, app.displayPolygons, app.colorList)

def finishMode_keyPressed(app, event):
    if event.key == 'p': # toggles pause (for rotation animation)
        app.isPaused = not app.isPaused
    elif event.key == 'Up': # moves points +z
            for i in range(len(app.displayPoints)):
                app.displayPoints[i] += np.array([0,0,20])
    elif event.key == 'Down': # moves points -z
        for i in range(len(app.displayPoints)):
            app.displayPoints[i] += np.array([0,0,-20]) 
    elif event.key == 'Left': # moves points +x
        for i in range(len(app.displayPoints)):
            app.displayPoints[i] += np.array([20,0,0])
    elif event.key == 'Right': # moves points -x
        for i in range(len(app.displayPoints)):
            app.displayPoints[i] += np.array([-20,0,0])

def finishMode_mousePressed(app, event):
    x, y = event.x, event.y
    for button in app.finishButtons:
        if button.inButton(x, y) == True:
            if button.name != 'save':
                app.lastMode = app.mode
                app.mode = button.name
                if button.name == 'colorMode':
                    app.displayPoints += np.array([0, 0, -100])
                    app.isPaused = True
                elif button.name == 'startMode':
                    appStarted(app)
            elif button.name == 'save':
                name = app.getUserInput('Enter a name for your file (ending in .txt):')
                pointsToFile(app, name, app.displayPoints)

def finishMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,1280,755, fill = 'light yellow')
    printText(app, canvas)
    drawPolygons(app, canvas, app.displayPolygons, app.displayPoints)
    drawButtons(app, canvas, app.finishButtons)
    drawHelpScreen(app, canvas)
    drawHelpScreen2(app, canvas)


##########################################
# Run App
##########################################

def appStarted(app): 
    app.mode = 'startMode'
    app.lastMode = None
    app.helpScreen = False
    app.helpScreen2 = False
    app.upload = False

    # GENERAL MODEL
    # center of our 3D coordinate system
    app.origin = app.width//2, 2*app.height//3
    # x axis is the left hand side axis
    app.xAxisAngle = deg2Rad(200) 
    # y axis is the right hand side axis 
    app.yAxisAngle = deg2Rad(340)
    app.axesVecs = np.array([[150,0,0], [0,150,0], [0,0,150]])
    app.axesPoints = vecs2Graph(app, app.axesVecs)
    app.n = 23  # max is (value inside generateHeights**2) // 2
    app.scale = 120
    app.isPaused = True
    app.mouseX, app.mouseY = (0, 0)
    app.selectedVertex = None
    app.highlightedVertex = None

    # START MODE
    app.image = app.loadImage('splash_screen.png')
    app.startImage = app.scaleImage(app.image, 0.45)

    # TERRAIN MODE
    app.heights = generateHeights(6, scale = 1)
    app.terrainPoints = createPoints(app, (0, 0, app.height//4))
    app.vectorXY = vecs2Graph(app, app.terrainPoints)
    app.polygons = createPolygons(app, app.vectorXY)

    app.multiselect = False # also used for Flat Mode
 
    # FLAT MODE
    app.flatPoints = createFlatPoints(app, (0, 0, app.height//4))
    app.flatVectorXY = vecs2Graph(app, app.flatPoints)
    app.flatPolygons = createPolygons(app, app.flatVectorXY)

    # BUTTONS
    app.startButtons = startButtons(app)
    app.terrainButtons = flatButtons(app) # same buttons for flat and terrain
    app.flatButtons = flatButtons(app)
    app.colorButtons = None
    app.panelButtons = None
    app.finishButtons = None

    # COLOR MODE
    app.displayPoints = []
    app.displayVectorXY = None
    app.displayPolygons = None
    app.altitudeList = None
    app.inputBox = False
    app.inputString = ''
    app.numColors = 6
    app.colorList = []
    app.selectedLevel = None
    # color list from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    # color reference pop-up also from above link
    app.image2 = app.loadImage('color_reference.png')
    app.colorReference = app.scaleImage(app.image2, 0.5)
    app.showReference = False
    app.allColors = ['snow', 'white', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99', 'black']


runApp(width = 1280, height = 755) # full screen