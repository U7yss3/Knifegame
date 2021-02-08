# game
from Menu import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.game_font = pg.font.match_font(game_font)
        #self.game_font = "/System/Library/Fonts/Supplemental/Arial.ttf"
        pg.display.set_caption(Title)
        self.running = True
        self.next_action = False
        self.clock = pg.time.Clock()

    # primary functions  /  Game LOOP
    def new(self, n_players, player_number):
        #start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.knifes = pg.sprite.Group()
        self.opp_knifes = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.knifes_for_counter = pg.sprite.Group()
        self.health_hearts = pg.sprite.Group()
        self.player_n = player_number
        self.number_of_players = n_players
        self.old_n_knifes = 0
        self.old_n_lives = 0
        self.level_ended = False
        self.previous_data = [[0, 0], [0, 0], 0, [0, 0], 0, [0, 0], 0]
        self.opponent_knives_list = [0, Ennemy_Knife, 0, Ennemy_Knife, 0, Ennemy_Knife]
        if self.number_of_players > 1:
            self.multiplayer = True
            self.level = "Multi"
            self.create_map()
            self.n.send(self.encode(self.player.pos))
            self.p2 = Opponent_multi(self, 0, 0, )
        else:
            self.multiplayer = False
            self.create_map()

        print("Player number : ", player_number)
        self.run()

    def run(self):
        #game loop
        '''if not self.running:
            return'''
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.specific_level_actions()
            self.draw()

    def update(self):
        if self.multiplayer:
            self.server_communication()
        self.all_sprites.update()

    def events(self):
        #game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):     #game loop - dra<
        try:
            self.screen.blit(self.image, (0,0))
        except:
            self.screen.fill(bg_color)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_info()
        pg.display.flip()

    # screens
    def menu(self):
        self.m = Menu(self)
        run = True
        if not self.next_action:
            self.next_action = "Start"
        while run:
            if self.next_action == "Start":
                self.next_action = self.m.Start_screen(self.screen)
            if self.next_action == "Campaign":
                self.next_action = self.m.Campaign(self.screen)
            try:
                if self.next_action[:-1] == "Level":
                    self.level = self.next_action
                    return 0, 1
            finally:
                if self.next_action == "Multiplayer":
                    self.next_action = self.m.Multiplayer(self.screen)
                if type(self.next_action) == int:
                    return (2, self.next_action)
                if self.next_action == "STOP":
                    self.running = False
                    run = False

    # secondary
    def specific_level_actions(self):
        if self.level == "Level1":
            if self.player.pos.x < 0:
                self.level_ended = True
        if self.level == "Level2":
            self.player.knife_counter=0

    def server_communication(self):
        if not self.player.is_dead:
            send = self.encode(self.player.pos)
        else:
            send = "DEAD"
        reply = self.n.send(send)
        if reply and reply != "connected":
            if reply == "DEAD":
                self.p2.is_dead = True
                self.p2.kill()
            else:
                data = self.decode(reply)
                self.p2.pos = data[0]
                i=1         #update pos opponent
                while i < 7:
                    if self.previous_data[i][0] == 0 and data[i][0] != 0:     # create knife sprite if it was not there before
                        k = Ennemy_Knife(self, data[i], data[i+1])
                        self.opponent_knives_list[i] = k    # add knive in knife list
                    elif self.previous_data[i][0] != 0 and data[i][0] == 0:
                        self.opponent_knives_list[i].kill()
                    else:
                        self.opponent_knives_list[i].pos = data[i]
                        self.opponent_knives_list[i].angle = data[i+1]
                    i += 2
                self.previous_data = data

    def connect_to_server(self):
        self.n = Network()

    def draw_info(self):
        # draw knife counter
        if self.level != "Level1":
            n_knives = self.player.knife_counter
            if n_knives != self.old_n_knifes:
                for knife in self.knifes_for_counter:
                    knife.kill()
                for i in range(n_knives):
                    Knifenumber(self, i)
            self.old_n_knifes = n_knives

        # draw life counter:
        n_lives = self.player.health
        if n_lives != self.old_n_lives:
            for life in self.health_hearts:
                life.kill()
            for i in range(n_lives):
                Life(self, i)
        self.old_n_lives = n_lives

        if self.player.is_dead:
            self.draw_text("You Died !", 50, red, screen_width / 2, screen_height / 2)
            pg.display.flip()
            time.sleep(1)
            self.playing = False
        if self.level_ended:
            self.draw_text("Well Done, you beated "+ self.level + " !", 50, blue, screen_width / 2, screen_height / 2)
            pg.display.flip()
            time.sleep(1)
            self.playing = False
            self.next_action = "Campaign"
        try:
            if self.p2.is_dead:
                self.draw_text("Well Done, you won !", 50, blue, screen_width / 2, screen_height / 2)
                pg.display.flip()
                time.sleep(1)
                self.playing = False
        except:
            pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.game_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def create_map(self):
        # make the map data into a list
        if self.level != "Level3":
            self.image = pg.image.load(os.path.join(img_folder, levelbakcroundict[self.level])).convert()
        mapfile = levelmapsdict[self.level]
        self.map_data = []
        if self.level == "Level1":
            Platform(self, -30, 420)
            Platform(self, -60, 420)
            Platform(self, -90, 420)

        file = open(os.path.join(map_folder, mapfile), "r")
        for line in file:
            self.map_data.append(line.strip())

        # check for correct size
        if len(self.map_data) == 20:
            for i in range(20):
                if len(self.map_data[i]) != 30:
                    print("Map Size Error")
        else:
            print("Map Size Error")

        # create platforms
        y = 0
        for row in self.map_data:
            i=0
            while i < len(row):
                if row[i] == "-":
                    Platform(self, i, y)
                if row[i] == str(self.player_n):
                    self.player = Player(self, i * TILESIZE, y * TILESIZE)
                if row[i] == 'c':
                    Cell(self, i, y)
                if row[i] == 'i':
                    Wall(self, i, y)
                i += 1
            y += 1
        time.sleep(1)

    def draw_grid(self):
        for x in range(0, screen_width, TILESIZE):
            pg.draw.line(self.screen, light_blue, (x, 0), (x, screen_height))
        for y in range(0, screen_height, TILESIZE):
            pg.draw.line(self.screen, light_blue, (0, y), (screen_width, y))

    def decode(self, data):
        data = data.split(";")
        knifes = False
        output = []
        playerpos = data[0].split(",")
        for i in range(2):
            playerpos[i] = float(playerpos[i])
        output.append(playerpos)
        if len(data)>1:
            knifes = True
        if knifes:
            for i in range(len(data)-1):
                i+=1
                knifepos = data[i].split(',')[:-1]
                knifeangle = float(data[i].split(',')[-1:][0])
                for i in range(2):
                    knifepos[i] = float(knifepos[i])
                output.append(knifepos)
                output.append(knifeangle)
        return output

    def encode(self, player_pos):
        output = str(round(player_pos[0], 3)) + "," + str(round(player_pos[1], 3))
        for knife in self.knifes:
            output += ";" + self.encode_knife(knife.pos, knife.angle)
        i = len(self.knifes)
        for knife in range(3-i):
            output += ";0,0,0"
        return output

    def encode_knife(self, knifepos, knifeangle):
         return str(round(knifepos[0], 2)) + "," + str(round(knifepos[1], 2)) + "," + str(round(knifeangle, 2))




g = Game()
g.connect_to_server()
while g.running:
    n_players, player = g.menu()
    g.new(n_players, player)


pg.quit()
