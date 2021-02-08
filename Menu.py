from sprites import *
import time
from network import Network

class Menu():
    def __init__(self, game):
        self.clock = pg.time.Clock()
        self.game = game

    def Start_screen(self, screen):
        #   Start screen, returns what next action is to be executed
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        run = True
        while run:
            campaign = self.button(screen, "Campaign", black, white, GRIDWIDTH/2, 7, 10, 2)
            multi = self.button(screen, "Multiplayer", black, white, GRIDWIDTH/2, 12, 10, 2)
            if campaign:
                return campaign
            if multi:
                return multi
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "STOP"

    def Campaign(self, screen):
        time.sleep(0.3)
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        run = True
        while run:
            self.level_y = 7
            self.draw_text(screen, "You have to escape the prison", 30, white, GRIDWIDTH/2, 4)
            for level in levelmapsdict:
                if level != "Multi":
                    self.L = self.button(screen, level, red, white, GRIDWIDTH/2, self.level_y, 10, 2)
                    self.level_y += 3
                    if self.L:
                        return self.L

            back = self.return_to_menu(screen)
            if back:
                return "Start"
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "STOP"

    def Multiplayer(self, screen):
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        self.game.connect_to_server()
        player_n = self.game.n.get_player_number()

        screen.blit(self.image, (0, 0))
        run = True
        while run:
            back = self.return_to_menu(screen)
            self.draw_text(screen, "Connecting to server", 40, white, GRIDWIDTH/2, (GRIDHEIGHT/2)-3)
            if player_n:
                self.draw_text(screen, "Connected", 40, green, GRIDWIDTH / 2, GRIDHEIGHT / 2)
                self.draw_text(screen, "Player number: ", 40, white, GRIDWIDTH / 2, (GRIDHEIGHT / 2) + 2)
                self.draw_text(screen, player_n, 40, white, GRIDWIDTH / 2, (GRIDHEIGHT / 2) + 4)
                self.draw_text(screen, "Waiting for opponent connection", 40, white, GRIDWIDTH / 2, (GRIDHEIGHT / 2) + 5)
                answer = self.game.n.send("connected")
                pg.display.flip()
                if answer == "connected":
                    time.sleep(1)
                    return int(player_n)
            else:
                self.draw_text(screen, "Not connecting to server", 40, red, GRIDWIDTH / 2, GRIDHEIGHT / 2)
                tryagain = self.button(self.game.screen, "Try again ?", blue, white, 20, 22, 1, 10)
                if tryagain:
                    return "Multiplayer"
            if back:
                return "Start"
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "STOP"

    ###################################################

    def button(self, screen, text, button_color, text_color, x, y, w, h):
        # This function creates a button on screen
        # it returns the text of the button if it is pressed, and none otherwise
        # changes the color of box when mouse is hovering over it
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
            button_color = grey
            pg.event.get()
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                return text
        pg.draw.rect(screen, button_color, rect)
        self.draw_text(screen, text, 30, text_color, x, 5 + y, True)

    def draw_text(self, screen, text, size, color, x, y, nogrid=False, midtop=True):
        # This function draws text on screen, and dosen't return anything
        font = pg.font.Font(pg.font.match_font(game_font), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if midtop:
            if not nogrid:
                text_rect.midtop = (x * TILESIZE, y * TILESIZE)
            if nogrid:
                text_rect.midtop = (x, y)
        else:
            if not nogrid:
                text_rect.topright = (x * TILESIZE, y * TILESIZE)
            if nogrid:
                text_rect.topright = (x, y)
        screen.blit(text_surface, text_rect)

    def return_to_menu(self, screen):
        # This function creates a button for returning to menu,
        # returns next action if button is pressed
        restart = self.button(screen, "Return to menu", black, less_white, GRIDWIDTH/2, 18, 13, 2)
        if restart == "Return to menu":
            return restart

    def text_box(self, screen, text, x, y, w, h, time):
        # creates a text box with inputted text
        # makes box grow as text is growing
        # creates a vertical white bar to animate a bit
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        font = pg.font.Font('freesansbold.ttf', 25)
        text_surface = font.render(text, True, white)
        text_box.text_width = text_surface.get_width()
        text_box.text_rect = text_surface.get_rect()
        text_box.text_rect.midtop = (x, 5 + y)

        if text_box.text_width + 40 > w:
            w = 40 + text_box.text_width
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        pg.draw.rect(screen, black, rect)
        if (pg.time.get_ticks() - time) % 500 < 250:
            pg.draw.line(screen, white, (x + text_box.text_width / 2, y), (x + text_box.text_width / 2, y + 40), 3)

        screen.blit(text_surface, text_box.text_rect)

