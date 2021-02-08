#sprites classes
from settings import *



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.players.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "idle.png")).convert()
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (45, 70))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.is_dead = False
        self.knife_counter = 3
        self.health = 3
        self.last_shot = 0
        self.can_jump = False
        ### move after animated
        self.mask = pg.mask.from_surface(self.image)
        self.rect.midbottom = self.pos

    def update(self):
        self.can_jump = False
        self.acc = vec(0, PLAYER_GRAV)
        self.check_plat_collision()
        self.check_key_pressed()
        self.apply_motion_eq()
        self.block_player_on_sides()
        self.wall_collision()

        if abs(self.vel.x) < 0.3:
            self.vel.x = 0

            #death
        if self.health == 0 or self.pos.y > screen_height:
            self.is_dead = True
            self.kill()


        self.rect.midbottom = self.pos

    def wall_collision(self):
        #TODO better wall collision
        ''' # check collision if coming from bottom
        self.rect.y -= 10
        hit = pg.sprite.spritecollideany(self, self.game.walls)
        self.rect.y += 10
        if hit:
            if self.rect.y > hit.rect.y + hit.rect.h:
                self.rect.y = hit.rect.y + hit.rect.h
                self.vel.y = 0'''

        # check collision if coming from left
        self.rect.x += 10
        hit = pg.sprite.spritecollideany(self, self.game.walls)
        self.rect.x -= 10
        if hit:
            if self.rect.x + self.rect.w > hit.rect.x:
                self.pos.x = hit.rect.x - self.rect.w/2
                self.vel.x = 0

        #check collision if coming from right
        self.rect.x -= 10
        hit = pg.sprite.spritecollideany(self, self.game.walls)
        self.rect.x += 10
        if hit:
            if self.rect.x < hit.rect.w+hit.rect.x:
                self.pos.x = hit.rect.x+hit.rect.w + self.rect.w / 2
                self.vel.x = 0

    def check_plat_collision(self):
        self.rect.y += 1
        for plat in self.game.platforms:
            if pg.sprite.collide_rect(self, plat) and plat.rect.y + 10 > self.rect.bottom and self.vel.y > 0:# and plat.rect.y<self.pos.y<plat.rect.y+plat.rect.w:
                self.pos.y = plat.rect.y
                self.vel.y = 0
                self.can_jump = True
        self.rect.y -= 1

    def check_key_pressed(self):
        # keys pressed ?
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = +PLAYER_ACC
        if keys[pg.K_UP] and self.can_jump:
            self.jump()

        if self.game.level != "Level1" and self.game.level != "Level2":
            mouse = pg.mouse.get_pressed()
            if mouse[0]:
                now = pg.time.get_ticks()
                if now - self.last_shot > KNIFE_RATE and self.knife_counter > 0:
                    mouse_pos = pg.mouse.get_pos()
                    self.throw_knife((self.pos.x, self.pos.y - self.rect.height / 2),
                                     vec(mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y + self.rect.height / 2))

    def apply_motion_eq(self):
        #if self.check_for_wall():
        self.acc.x += self.vel.x * PLAYER_FRICTION  # friction
        self.vel += self.acc  # motion equations
        self.pos += self.vel + 0.5 * self.acc

    def block_player_on_sides(self):
        if self.pos.x + (self.rect.width / 2) > screen_width:
            self.pos.x = screen_width - (self.rect.width / 2)
        if self.game.level[-1:] == "1" and 330 < self.rect.y < 420:
            pass
        elif self.pos.x - (self.rect.width / 2) < 0:
            self.pos.x = (self.rect.width / 2)

    def throw_knife(self, pos, dir):
        self.knife_counter -= 1
        self.last_shot = pg.time.get_ticks()
        Knife(self.game, pos, dir, self)

    def jump(self):
        #jump only if standing on smth
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = JUMP_HEIGHT


class Opponent_multi(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "idle.png")).convert()
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (45, 66))
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.is_dead = False
        self.mask = pg.mask.from_surface(self.image)
        #TODO animation

    def update(self):
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.platforms.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.Surface([TILESIZE, TILESIZE])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        #self.rect = pg.rect.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.walls.add(self)
        self.rect = pg.rect.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Knife(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, player):
        pg.sprite.Sprite.__init__(self)
        self.dir = dir
        self.player = player
        self.game = game
        self.game.knifes.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "knife2.png")).convert()
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.knifeimage = self.image
        self.pos = pos
        self.rect.center = self.pos
        self.vel = vec(dir).normalize()*KNIFE_SPEED
        self.throw_time = pg.time.get_ticks()
        self.angle = -(vec(1, 0).angle_to(self.vel))
        """la trajectoire du couteau doit suivre """

    def update(self):
        self.now = pg.time.get_ticks()
        self.collision_with_platforms_and_rotation_update()
        self.collision_with_walls()
        self.collision_with_opponent()
        self.collision_with_self()

        # update position and angle of knife
        self.image = pg.transform.rotate(self.knifeimage, self.angle)
        self.pos += self.vel
        self.rect.center = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def collision_with_platforms_and_rotation_update(self):
        if not pg.sprite.spritecollideany(self, self.game.platforms) and not self.collision_with_walls():
            if (self.now - self.throw_time) % 7 == 0:
                self.angle = -(vec(1, 0).angle_to(self.vel))
            self.vel.y += KNIFE_GRAV
        else:
            for plat in self.game.platforms:
                hits = pg.sprite.collide_rect(self, plat)
                if hits:
                    if self.vel != (0, 0):
                        self.stop_rotation = self.vel
                    self.angle = -(vec(1, 0).angle_to(self.stop_rotation))
                    self.vel = vec(0, 0)

    def collision_with_opponent(self):
        # if the player's knife hits ennemy
        try:
            hits = pg.sprite.collide_rect(self, self.game.p2)
            if hits:
                self.kill()
        except:
            pass

    def collision_with_self(self):
        if self.now - self.throw_time > 200:
            hits = pg.sprite.collide_rect(self, self.game.player)
            if hits:
                if self.vel != [0, 0]:
                    self.game.player.health -= 1
                self.kill()
                self.game.player.knife_counter += 1

    def collision_with_walls(self):
        # not really ressource efficient this one
        for wall in self.game.walls:
            hits = pg.sprite.collide_rect(self, wall)
            if hits:
                if self.vel != (0, 0):
                    self.stop_rotation = self.vel
                    self.angle = -(vec(1, 0).angle_to(self.stop_rotation))
                self.vel = vec(0, 0)
                return True


class Ennemy_Knife(pg.sprite.Sprite):
    def __init__(self, game, pos, angle):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.opp_knifes.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "knife2.png")).convert()
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.knifeimage = self.image
        self.pos = pos
        self.rect.center = self.pos
        self.throw_time = pg.time.get_ticks()
        self.angle = angle

    def update(self):
        self.now = pg.time.get_ticks()
        self.image = pg.transform.rotate(self.knifeimage, self.angle)
        self.rect.center = self.pos
        self.collision_with_player()

    def collision_with_player(self):
        hitsplat = pg.sprite.spritecollideany(self, self.game.platforms)
        hits = pg.sprite.spritecollideany(self, self.game.players)
        if hits:
            if not hitsplat:
                self.game.player.health -= 1
            self.game.player.knife_counter += 1


class Cell(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.load_images()
        self.game.all_sprites.add(self)
        self.image = self.doors[0]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        self.current_frame = 0
        self.last_update = 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_images(self):
        self.doors = []
        for i in range(13):
            i += 1
            self.doors.append(pg.image.load(os.path.join(celldoor_folder, celldict[str(i)])).convert())

    def open(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            center = self.rect.center
            if self.current_frame < 12:
                self.current_frame = self.current_frame+1
            self.image = self.doors[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        hits = pg.sprite.spritecollideany(self, self.game.players)
        if hits:
            now = pg.time.get_ticks()
            self.open()


class Knifenumber(pg.sprite.Sprite):
    def __init__(self, game, i):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.knifes_for_counter.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "knife2.png")).convert()
        self.image.set_colorkey(black)
        self.image = pg.transform.scale(self.image, (70, 35))
        self.image = pg.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.center = knifespositions[i]


class Life(pg.sprite.Sprite):
    def __init__(self, game, i):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.health_hearts.add(self)
        self.game.all_sprites.add(self)
        self.image = pg.image.load(os.path.join(img_folder, "heart.jpg")).convert()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = lifepositions[i]


class Friend(pg.sprite.Sprite):
    pass