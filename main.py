import pygame
import math
import os

pygame.init()

from config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_WIDTH, TRACK_HEIGHT, COLOUR_SCHEME, BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS, DEFAULT_TRACK_NAME, ASSETS_PATH, CAR_WIDTH, CAR_HEIGHT, TOTAL_LAPS
from gui import Container, TextInputBox, Button
from cars import Car, CarAgent
from track import Track

# Loading car images
blueCarImage = pygame.transform.scale(pygame.image.load(f"{ASSETS_PATH}/Cars/BlueCar.png"), (CAR_WIDTH, CAR_HEIGHT))
redCarImage = pygame.transform.scale(pygame.image.load(f"{ASSETS_PATH}/Cars/RedCar.png"), (CAR_WIDTH, CAR_HEIGHT))

# Initialising fonts
font16 = pygame.font.Font(f"{ASSETS_PATH}/Fonts/font.otf", 16)

class Game:
    def __init__(self):
        #Initialising screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Game")

        self.running = True
        self.clock = pygame.time.Clock()
        self.deltaTime = 1 / FPS

        self.displayMainMenu()

    def displayMainMenu(self):
        #Initialising menu buttons
        playButton = Button(0.1, 0.2, 0.2, 0.1, "Play", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1],COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        trackButton = Button(0.1, 0.35, 0.2, 0.1, "Create Track", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        trainButton = Button(0.1, 0.5, 0.2, 0.1, "Train an Agent", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        exitButton = Button(0.1, 0.65, 0.2, 0.1, "Exit", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)

        buttons = [playButton, trackButton, trainButton, exitButton]

        while self.running:
            # Checking if buttons are hovered
            hoveredButton = None
            for button in buttons:
                if button.updateHovered(pygame.mouse.get_pos()):
                    hoveredButton = button

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Button handling
                    if hoveredButton:
                        if hoveredButton == playButton:
                            trackSelected = self.trackSelection()
                            if trackSelected:
                                self.track.initialiseTrack()
                                self.gameLoop()
                        elif hoveredButton == trackButton:
                            while self.trackSelection(True):
                                self.trackEditor()
                        elif hoveredButton == trainButton:
                            pass
                        elif hoveredButton == exitButton:
                            self.running = False

            # Drawing main menu            
            self.screen.fill((8, 132, 28))

            for button in buttons:
                button.draw(self.screen)

            pygame.display.flip()

            # Getting time between frames
            self.deltaTime = self.clock.tick(FPS) / 1000
    
    def trackSelection(self, allowNewTrack=False):
        backButton = Button(0.02, 0.88, 0.1, 0.1, "Back", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        selectButton = Button(0.88, 0.88, 0.1, 0.1, "Select", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)

        buttons = [backButton, selectButton]

        # Creating the track selection scroll menu
        containerPosition = (0.25, 0.05)
        offScreenPosition = (2, 2)
        buttonLength = 0.48
        buttonHeight = 0.13
        buttonPadding = (0.01, 0.01 * (SCREEN_WIDTH / SCREEN_HEIGHT))
        tracksPerPage = 6
        scrollIndex = 0

        trackButtonsContainer = Container(containerPosition[0], containerPosition[1], buttonLength + buttonPadding[0] * 2, buttonHeight * (tracksPerPage) + buttonPadding[1] * (tracksPerPage + 1), COLOUR_SCHEME[3], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS)
        
        trackButtons = []

        # New track button
        if allowNewTrack:
            newTrackButton = Button(0, 0, buttonLength, buttonHeight, "New Track", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS, COLOUR_SCHEME[2])
            trackButtons.append(newTrackButton)

        # Creating track buttons from diirectory
        trackPaths = os.listdir(f"{ASSETS_PATH}/Tracks")
        for trackPath in trackPaths:
            strippedPath = trackPath[:-5]
            trackButton = Button(0, 0, buttonLength, buttonHeight, strippedPath, font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS, COLOUR_SCHEME[2])
            trackButtons.append(trackButton)

        selectedTrack = 0

        if len(trackButtons) > 0:
            trackButtons[selectedTrack].setSelected(True)

        updateButtons = True
        while self.running:
            hoveredButton = None
            for button in buttons:
                if button.updateHovered(pygame.mouse.get_pos()):
                    hoveredButton = button

            hoveredTrackIndex = None
            for index, button in enumerate(trackButtons):
                if button.updateHovered(pygame.mouse.get_pos()):
                    hoveredTrackIndex = index
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Button handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hoveredTrackIndex is not None:
                        trackButtons[selectedTrack].setSelected(False)
                        selectedTrack = hoveredTrackIndex
                        trackButtons[selectedTrack].setSelected(True)
                    elif hoveredButton == backButton:
                        return False
                    elif hoveredButton == selectButton:
                        if selectedTrack == 0 and allowNewTrack:
                            self.track = Track()
                        else:
                            if allowNewTrack:
                                selectedTrack -= 1

                            self.track = Track(trackPaths[selectedTrack][:-5])

                        return True

                # Handling scrolling up and down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        trackButtons[selectedTrack].setSelected(False)
                        selectedTrack = max(selectedTrack - 1, 0)
                        trackButtons[selectedTrack].setSelected(True)
                        
                        if selectedTrack < scrollIndex:
                            scrollIndex -= 1
                            updateButtons = True
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        trackButtons[selectedTrack].setSelected(False)
                        selectedTrack = min(selectedTrack + 1, len(trackButtons) - 1)
                        trackButtons[selectedTrack].setSelected(True)

                        if selectedTrack >= scrollIndex + tracksPerPage:
                            scrollIndex += 1  
                            updateButtons = True                  
            
            # Only updating the positions of buttons if the user scrolled
            if updateButtons:
                for index, button in enumerate(trackButtons):
                    if index in range(scrollIndex, scrollIndex + tracksPerPage):
                        relativeIndex = index - scrollIndex
                        button.moveButton(containerPosition[0] + buttonPadding[0], containerPosition[1] + buttonPadding[1] * (relativeIndex + 1) + buttonHeight * relativeIndex)
                    else:
                        button.moveButton(offScreenPosition[0], offScreenPosition[1])

            # Drawing buttons and scroll container
            self.screen.fill((8, 132, 28))

            trackButtonsContainer.draw(self.screen)

            for button in buttons:
                button.draw(self.screen)

            for button in trackButtons:
                button.draw(self.screen)

            pygame.display.flip()

            self.deltaTime = self.clock.tick(FPS) / 1000
            updateButtons = False

    def trackEditor(self):
        # Getting track name
        trackName = self.track.getFilePath()
        if trackName is None:
            trackName = DEFAULT_TRACK_NAME

        editingTrackName = False

        backButton = Button(0.02, 0.88, 0.1, 0.1, "Back", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        saveButton = Button(0.88, 0.88, 0.1, 0.1, "Save", font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS)
        trackNameBox = TextInputBox(0.88, 0.76, 0.1, 0.1, trackName, font16, COLOUR_SCHEME[0], COLOUR_SCHEME[1], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS, BUTTON_HOVER_THICKNESS, COLOUR_SCHEME[2])

        elements = [backButton, saveButton, trackNameBox]

        # Scaling down the track to fit on the screen
        zoom = int(TRACK_WIDTH / SCREEN_WIDTH)
        trackSurface = pygame.Surface((TRACK_WIDTH, TRACK_HEIGHT))
        selectedPoint = None

        firstDraw = True
        editorRunning = True
        while self.running and editorRunning:
            updateTrack = False
            hoveredElement = None
            for element in elements:
                if element.updateHovered(pygame.mouse.get_pos()):
                    hoveredElement = element

            # Scaling the mouse position so nodes are placed down accurately
            mousePosition = pygame.mouse.get_pos()
            scaledMousePosition = (mousePosition[0] * zoom, mousePosition[1] * zoom)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    editingTrackName = False
                    trackNameBox.setSelected(editingTrackName)

                    if event.button == 1:
                        updateTrack = True
                        if hoveredElement:
                            # Button handling
                            if hoveredElement == backButton:
                                editorRunning = False
                            elif hoveredElement == saveButton:
                                if selectedPoint is None:
                                    trackName = trackNameBox.getText()
                                    if trackName == "":
                                        trackName = DEFAULT_TRACK_NAME

                                    self.track.exportTrack(trackName)
                                    editorRunning = False

                            # User is editing the track name
                            elif hoveredElement == trackNameBox:
                                editingTrackName = True
                                trackNameBox.setSelected(editingTrackName)

                        elif selectedPoint is not None:
                            # Placing down a point that was being moved
                            selectedPoint = None
                        else:
                            # Point creation/selection (Left click)
                            if (hoveredPoint := self.track.getHoveredPoint(scaledMousePosition)) is not None:
                                # Selecting an existing point
                                selectedPoint = hoveredPoint
                            else:
                                # Adding a new point
                                self.track.addPoint(scaledMousePosition)

                    elif event.button == 3:
                        # Point deletion (Right click)
                        updateTrack = True
                        if (hoveredPoint := self.track.getHoveredPoint(scaledMousePosition)) is not None:
                            # Removing the hovered point
                            self.track.removePoint(hoveredPoint)
                        else:
                            # Removing the last point that was placed down
                            self.track.removePoint()

                elif event.type == pygame.KEYDOWN and editingTrackName:
                    # Updating the track name
                    trackNameBox.update(event)

            if selectedPoint is not None:
                # Moving the selected point with the mouse cursor
                updateTrack = True
                self.track.movePoint(selectedPoint, scaledMousePosition)
            
            # Making sure the track is always drawn on the first frame
            if firstDraw:
                updateTrack = True
                firstDraw = False

            # Only update the track if neccessary to save computing power
            if updateTrack:
                trackSurface.fill((8, 132, 28))
                self.track.drawEditor(trackSurface)

            # Scaling the track surface and drawing it
            scaledTrackSurface = pygame.transform.scale(trackSurface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaledTrackSurface, (0, 0))

            for element in elements:
                element.draw(self.screen)

            pygame.display.flip()

            self.deltaTime = self.clock.tick(FPS) / 1000

    def training(self):
        pass

    def gameLoop(self):
        containerPosition = (0.25, 0)
        gameInfoContainer = Container(containerPosition[0], containerPosition[1], 0.5, 0.1, COLOUR_SCHEME[3], COLOUR_SCHEME[0], BUTTON_BORDER_THICKNESS)

        spawnPoint, spawnAngle = self.track.getSpawnPosition()

        playerCar = Car(spawnPoint[0], spawnPoint[1], spawnAngle, blueCarImage)
        agentCar = CarAgent(spawnPoint[0], spawnPoint[1], spawnAngle, redCarImage)

        laps = 0
        cameraOffset = pygame.Vector2(0, 0)

        gameRunning = True
        while self.running and gameRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            acceleration = 0
            turnDirection = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                acceleration += 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                acceleration -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                turnDirection += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                turnDirection -= 1

            playerCar.update(self.deltaTime, acceleration, turnDirection, self.track)
            agentCar.update(self.deltaTime, self.track)

            # Check if game over
            laps = max(playerCar.laps, agentCar.laps)
            if laps >= TOTAL_LAPS:
                gameRunning = False

            cameraOffset = playerCar.getCameraOffset(cameraOffset)
            
            self.screen.fill((8, 132, 28))
            self.track.draw(self.screen, cameraOffset)

            playerCar.draw(self.screen, cameraOffset)
            agentCar.draw(self.screen, cameraOffset)

            pygame.display.flip()

            self.deltaTime = self.clock.tick(FPS) / 1000

if __name__ == "__main__":
    Game()