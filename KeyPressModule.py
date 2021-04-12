# getting commands from the keyboard
# use pygame to get keyboard commands
import pygame


# initialise a window for pygame
# keypress needs to be within a game window

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


# need to get the keypress
# if key is pressed - True else False
def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans


def main():
    if getKey("LEFT"):
        print("left key pressed")
    if getKey("RIGHT"):
        print("right key pressed")


if __name__ == "__main__":
    init()
    while True:
        main()
