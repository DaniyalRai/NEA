from config import SCREEN_WIDTH, SCREEN_HEIGHT

import pygame

class Container:
    def __init__(self, x, y, width, height, backgroundColour, borderColour, borderThickness):
        self.rect = pygame.Rect(SCREEN_WIDTH * x, SCREEN_HEIGHT * y, SCREEN_WIDTH * width, SCREEN_HEIGHT * height)

        self.backgroundColour = backgroundColour
        
        self.borderColour = borderColour
        self.borderThickness = borderThickness

    def draw(self, screen):
        pygame.draw.rect(screen, self.backgroundColour, self.rect)
        pygame.draw.rect(screen, self.borderColour, self.rect, self.borderThickness)

class Button:
    def __init__(self, x, y, width, height, text, font, textColour, backgroundColour, borderColour, borderThickness, hoverBorderThickness=0, selectedBackgroundColour=(0,0,0)):
        self.font = font
        self.textColour = textColour

        self.text = font.render(text, True, textColour)
        self.rect = pygame.Rect(SCREEN_WIDTH * x, SCREEN_HEIGHT * y, SCREEN_WIDTH * width, SCREEN_HEIGHT * height)

        self.backgroundColour = backgroundColour
        self.normalBackgroundColour = backgroundColour
        self.selectedBackgroundColour = selectedBackgroundColour

        self.borderColour = borderColour
        self.borderThickness = borderThickness
        self.normalBorderThickness = borderThickness
        self.hoverBorderThickness = hoverBorderThickness

    def draw(self, screen):
        pygame.draw.rect(screen, self.backgroundColour, self.rect)
        pygame.draw.rect(screen, self.borderColour, self.rect, self.borderThickness)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))

    def moveButton(self, x, y):
        self.rect.x = SCREEN_WIDTH * x
        self.rect.y = SCREEN_HEIGHT * y

    def updateHovered(self, mousePosition):
        if self.rect.collidepoint(mousePosition):
            self.borderThickness = self.hoverBorderThickness
            return True
        else:
            self.borderThickness = self.normalBorderThickness

    def setSelected(self, selected):
        if selected:
            self.backgroundColour = self.selectedBackgroundColour
        else:
            self.backgroundColour = self.normalBackgroundColour

class TextInputBox(Button):
    def __init__(self, x, y, width, height, text, font, textColour, backgroundColour, borderColour, borderThickness, hoverBorderThickness=0, selectedBackgroundColour=(0,0,0)):
        self.textContent = text
        super().__init__(x, y, width, height, text, font, textColour, backgroundColour, borderColour, borderThickness, hoverBorderThickness, selectedBackgroundColour)

    def update(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.textContent = self.textContent[:-1]
        elif event.unicode.isalnum():
            self.textContent += event.unicode

        self.text = self.font.render(self.textContent, True, self.textColour)

    def getText(self):
        return self.textContent