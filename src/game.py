import pygame
import random

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()


class Display:
    display_width = 800
    display_height = 600


class Cactus:
    cactus_height = 70
    cactus_size = [(69, 449), (37, 410), (40, 420)]

    @staticmethod
    def create_cactus_arr():
        array = []
        for i in 20, 300, 600:
            choice = random.randrange(0, 3)
            img = Image.cactus_img[choice]
            width, height = Cactus.cactus_size[choice]
            array.append(Object(Display.display_width + i, height, width, img, 4))
        return array


class Player:
    def __init__(self):
        self.health = 3
        self.make_jump = False
        self.jump_counter = 30
        self.max_above = 0
        self.above_cactus = False
        self.run_count = 0
        self.img_counter = 0

    def draw_dino(self):
        if self.img_counter == 25:
            self.img_counter = 0

        display.blit(Image.dino_img[self.img_counter // 5], (Player.player_x, Player.player_y))
        self.img_counter += 1

    def check_health(self):
        self.health -= 1
        if self.health == 0:
            pygame.mixer_music.stop()
            pygame.mixer.Sound.play(Musician.game_over_sound)
            return False
        else:
            return True

    def show_health(self):
        show = 0
        x = 20
        while show != self.health:
            display.blit(Image.health_img, (x, 20))
            x += 40
            show += 1

    def check_collision(self, barriers):
        def check_res(player, barrier, barriers):
            if player.check_health:
                radius = find_radius(barriers)
                barrier.set_to_object(radius)
                return False
            return True

        for barrier in barriers:
            if barrier.y == 449:  # it is a little cactus
                if not self.make_jump:
                    if barrier.x <= Player.player_x + Player.player_width - 35 <= barrier.x + barrier.width:
                        if self.check_health:
                            return check_res(self, barrier, barriers)

                elif self.jump_counter >= 0:
                    if Player.player_y + Player.player_heigth - 5 >= barrier.y:
                        if barrier.x <= Player.player_x + Player.player_width - 40 <= barrier.x + barrier.width:
                            return check_res(self, barrier, barriers)

                else:
                    if Player.player_y + Player.player_heigth - 10 >= barrier.y:
                        if barrier.x <= Player.player_x <= barrier.x + barrier.width:
                            return check_res(self, barrier, barriers)

            else:
                if not self.make_jump:
                    if barrier.x <= Player.player_x + Player.player_width - 5 <= barrier.x + barrier.width:
                        return check_res(self, barrier, barriers)

                    elif self.jump_counter == 10:
                        if Player.player_y + Player.player_heigth - 5 >= barrier.y:
                            if barrier.x <= Player.player_x + Player.player_width - 5 <= barrier.x + barrier.width:
                                return check_res(self, barrier, barriers)

                    elif self.jump_counter >= -1:
                        if Player.player_y + Player.player_heigth - 5 >= barrier.y:
                            if barrier.x <= Player.player_x + Player.player_width - 35 <= barrier.x + barrier.width:
                                return check_res(self, barrier, barriers)

                        else:
                            if Player.player_y + Player.player_heigth - 10 >= barrier.y:
                                if barrier.x <= Player.player_x + 5 <= barrier.x + barrier.width:
                                    return check_res(self, barrier, barriers)
        return False

    player_width = 60
    player_heigth = 100
    player_x = Display.display_width // 3
    player_y = Display.display_height - player_heigth - 100
    clock = pygame.time.Clock()

    def jump(self):
        if self.jump_counter >= -30:
            if self.jump_counter == 30:
                pygame.mixer.Sound.play(Musician.jump_sound)

            Player.player_y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False


class Musician:
    background_sound = pygame.mixer.Sound('textures/background.wav')
    jump_sound = pygame.mixer.Sound('textures/jump.wav')
    game_over_sound = pygame.mixer.Sound('textures/game_over.wav')
    heart_plus_sound = pygame.mixer.Sound('textures/score.wav')
    magic_sound = pygame.mixer.Sound('textures/magic.wav')
    button_sound = pygame.mixer.Sound('textures/button.wav')

    jump_sound.set_volume(0.15)
    game_over_sound.set_volume(0.2)

    @staticmethod
    def load_backgroung_song(name):
        pygame.mixer_music.load('textures/{}.wav'.format(name))
        pygame.mixer_music.set_volume(0.3)


class Button:
    def __init__(self, width, height, x, y, message, font_size):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 50)
        self.active_color = (23, 204, 50)
        self.x = x
        self.message = message
        self.font_size = font_size
        self.y = y

    def draw(self, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(display, self.active_color, (self.x, self.y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(Musician.button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_color, (self.x, self.y, self.width, self.height))

        print_text(message=self.message, x=self.x + 25, y=self.y - 5, font_size=self.font_size)


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

    def set_to_object(self, radius):
        choice = random.randrange(0, 3)
        img = Image.cactus_img[choice]
        width, height = Cactus.cactus_size[choice]
        self.return_self(radius, height, width, img)

    @staticmethod
    def open_random_object():
        choice = random.randrange(0, 2)
        img_of_stone = Image.stone_img[choice]

        choice = random.randrange(0, 2)
        img_of_cloud = Image.cloud_img[choice]

        stone = Object(Display.display_width, Display.display_height - 80, 10, img_of_stone, 4)
        cloud = Object(Display.display_width, 80, 70, img_of_cloud, 2)

        return stone, cloud


class Health(Object):
    def __init__(self, x, y, width, image, speed):
        super().__init__(x, y, width, image, speed)
        self.hearts = 0


class Image:
    stone_img = [pygame.image.load("textures/Objects/Stone{}.png".format(i)) for i in range(2)]
    cloud_img = [pygame.image.load("textures/Objects/Cloud{}.png".format(i)) for i in range(2)]
    cactus_img = [pygame.image.load("textures/Objects/Cactus{}.png".format(i)) for i in range(3)]
    health_img = pygame.image.load('textures/Effects/heart.png')
    background_img = pygame.image.load('textures/Backgrounds/bg (1).png')
    land_img = pygame.image.load('textures/Backgrounds/Land.jpg')

    dino_img = [pygame.image.load('textures/Dino/Dino{}.png'.format(i)) for i in range(5)]
    health_img = pygame.transform.scale(health_img, (30, 30))


class Scores:
    scores = 0
    max_scores = 0


def start_game():
    player = Player()
    Musician.load_backgroung_song("background")
    while game_cycle(player):
        Scores.scores = 0
        player.make_jump = False
        player.jump_counter = 30
        Player.clock = pygame.time.Clock()
        player.health = 2
        player.run_count = 1


def show_menu():
    background = Image.background_img

    start_button = Button(270, 70, 270, 200, 'start game', 60)
    quit_button = Button(270, 70, 270, 300, '        exit', 50)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(background, (0, 0))
        start_button.draw(start_game)
        quit_button.draw(quit)

        pygame.display.update()
        Player.clock.tick(60)


def game_cycle(player):
    pygame.mixer_music.play(-1)
    game = True
    cactus_arr = Cactus.create_cactus_arr()
    land = Image.land_img

    stone, cloud = Object.open_random_object()
    heart = Health(Display.display_width, 280, 30, Image.health_img, 4)

    if player.run_count != 0:
        pygame.mixer.Sound.play(Musician.magic_sound)
    player.run_count += 1

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if player.make_jump:
            player.jump()

        count_scores(cactus_arr, player)

        display.blit(land, (0, 0))
        print_text('Scores: ' + str(Scores.scores), 600, 10)

        draw_array(cactus_arr)
        move_objects(stone, cloud)
        player.draw_dino()

        if player.check_collision(cactus_arr):
            game = False

        heart.move()
        display.blit(heart.image, (heart.x, heart.y))
        hearts_plus(heart, player)
        player.show_health()

        pygame.display.update()
        Player.clock.tick(60)

    return game_over()


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < Display.display_width:
        radius = Display.display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        display.blit(cactus.image, (cactus.x, cactus.y))
        if not check:
            radius = find_radius(array)
            cactus.set_to_object(radius)


def move_objects(stone, cloud):
    check = stone.move()
    display.blit(stone.image, (stone.x, stone.y))
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = Image.stone_img[choice]
        stone.return_self(Display.display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    display.blit(cloud.image, (cloud.x, cloud.y))
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = Image.cloud_img[choice]
        cloud.return_self(Display.display_width, random.randrange(10, 200), stone.width, img_of_cloud)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='textures/text_style.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer_music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press Enter to continue', 200, 250)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        Player.clock.tick(15)

    pygame.mixer_music.unpause()


def count_scores(barriers, player):
    above = 0

    if -20 <= player.jump_counter < 25:
        for barrier in barriers:
            if Player.player_y + Player.player_heigth - 5 <= barrier.y:
                if barrier.x <= Player.player_x <= barrier.x + barrier.width \
                        or barrier.x <= Player.player_x + Player.player_width <= barrier.x + barrier.width:
                    above += 1

        player.max_above = max(player.max_above, above)
    else:
        if player.jump_counter == -30:
            Scores.scores += player.max_above
            max_above = 0


def game_over():
    if Scores.scores > Scores.max_scores:
        Scores.max_scores = Scores.scores
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Game over. Press Enter to play again. Press Esc to exit", 50, 200)
        print_text('Max scores: ' + str(Scores.max_scores), 300, 300)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return True

        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        Player.clock.tick(15)


def hearts_plus(heart, player):
    if Player.player_x <= heart.x <= Player.player_x + Player.player_width:
        if Player.player_y <= heart.y <= Player.player_y + Player.player_heigth:
            pygame.mixer.Sound.play(Musician.heart_plus_sound)
            if player.health < 5:
                player.health += 1

            radius = Display.display_width + random.randrange(500, 1500)
            heart.return_self(radius, heart.y, heart.width, heart.image)


display = pygame.display.set_mode((Display.display_width, Display.display_height))
pygame.display.set_caption('404 NotFound')

show_menu()
pygame.quit()
quit()

