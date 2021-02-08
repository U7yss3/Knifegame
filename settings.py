#settings
import os
import pygame as pg
vec = pg.math.Vector2


Title = "Knife game"
screen_width = 900
screen_height = 600
FPS = 60
game_font = "arial"

#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.10
PLAYER_GRAV = 0.5
JUMP_HEIGHT = -10

#knifes
KNIFE_RATE = 150
KNIFE_GRAV = 0.2
KNIFE_SPEED = 10
knifesdict = {"1": "knife.png", "2": "knife2.png"}
knifespositions = [(720, 40), (750, 40), (780, 40), (690, 40), (660, 40), (630, 40)]     #for knife counter
lifepositions =  [(820, 40), (850, 40), (880, 40)]


h = 25 #platform height

#colors
sky_blue = (0,128,255)
black = (0,0,0)
bg_color = black
red = (255,0,0)
grey = (30,30,30)
blue = (0,0,255)
light_blue = (100, 100, 255)
white = (255, 255, 255)
darkmagenta = (139,0,139)
black = (0,0,0)
light_grey = (100, 100, 100)
dark_grey = (20, 20, 20)
less_white = (160, 160, 160)
green = (0, 255, 0)

#set up assets folders (sprite image)
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "png")
map_folder = os.path.join(game_folder, "Maps")
menu_folder = os.path.join(game_folder, "Menu_bg")
Main_menubg = pg.image.load(os.path.join(menu_folder, "Main_menu.jpg"))
celldoor_folder = os.path.join(img_folder, "laporte")

# LEVELS
levelmapsdict = {"Level1":"Map1.txt", "Level2":"Map2.txt", "Level3":"Map3.txt", "Multi":"Multiplayer.txt"}
levelbakcroundict = {"Level1":"level1.jpg", "Multi":"level1.jpg", "Level2":"Level2.jpg"}
celldict = {"1": "1.jpg", "2": "2.jpg", "3": "3.jpg", "4": "4.jpg", "5": "5.jpg", "6": "6.jpg", "7": "7.jpg", "8": "8.jpg", "9": "9.jpg", "10": "10.jpg", "11": "11.jpg", "12": "12.jpg", "13": "13.jpg"}


#main menu
TILESIZE = 30
GRIDWIDTH = screen_width / TILESIZE
GRIDHEIGHT = screen_height / TILESIZE

