import pygame
import random
import sys
pygame.init()
# colors for the game \ constants
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]  # colors and other great stuff
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]
screen_size = (700, 400)  # x, y coordinates
window_size = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Asteroid Shooter")
icon_window = pygame.image.load("Images/icon.png").convert_alpha()  # load an image for the icon brother # noqa E501 # this here ignores long line linter issues
pygame.display.set_icon(icon_window)
# loading images
try:
    backgroundImage = pygame.image.load("Images/bg.png")
    playerImage = pygame.image.load("Images/ship.png")
    asteroidImage = pygame.image.load("Images/asteroid4.png")
    bulletImage = pygame.image.load("Images/bullet.png")
except Exception as imageError:
    print("Error: " + imageError)

# loading sounds + music 
try:
    shootingSound = pygame.mixer.Sound("Sounds/fire_2.ogg")
    backgroundMusic = pygame.mixer.music.load("Sounds/background_music.ogg")
except Exception as soundError:
    print("Error: " +soundError)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = asteroidImage.convert_alpha()  # load an image
        #  self.set_colorkey(BLACK)  old way to convert image
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = playerImage.convert_alpha()
        #  pygame.Surface.set_colorkey() old shit way to remove background 
        self.rect = self.image.get_rect()

    def controls(self):
        """ keyboard controls are needed here! """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bulletImage.convert_alpha() # load the image for the bullet
        #pygame.Surface.set_colorkey() disabled due to shit error wtf
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
all_sprites_list = pygame.sprite.Group()
asteroid_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
for i in range(50):
    asteroid = Asteroid(BLACK)
    asteroid.rect.x = random.randrange(SCREEN_WIDTH)
    asteroid.rect.y = random.randrange(250)
    asteroid_list.add(asteroid)
    all_sprites_list.add(asteroid)
player = Player()
all_sprites_list.add(player)
done = False
clock = pygame.time.Clock()
score = 0
x_player_pos = 350
y_player_pos = 200
pygame.mixer.music.play(-1) # plays the background music outside of main loop to avoid continous playback
keys = pygame.key.get_pressed()
player.rect.x = 200  # change this to the variables created above
player.rect.y = 350
speedOfPlayer = 0  # only y coord.
f4keyExit = False # alt f4 exit 
altkeyExit = False
# setup for the score:
""" font = pygame.font.Font(None, 36)
text = font.render(score, 1, WHITE)
textpos = text.get_rect(background.get_width()/2)
background.blit(text, textpos) """
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                altkeyExit = True
            if event.key == pygame.K_F4:
                f4keyExit = True
            if event.key == pygame.K_SPACE:
                bullet = Bullet()
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
                shootingSound.play()
            # actual controls for the player:
            if event.key == pygame.K_a:
                speedOfPlayer = -3
            if event.key == pygame.K_d:
                speedOfPlayer = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                speedOfPlayer = 0
            if event.key == pygame.K_d:
                speedOfPlayer = 0
    if player.rect.x <= 0:
        speedOfPlayer *= -1
    if player.rect.x >= 646:
        speedOfPlayer *= -1
    if f4keyExit and altkeyExit:
        done = True
    all_sprites_list.update()
    for bullet in bullet_list:  # see if the asteroids are hit
        asteroid_hit_list = pygame.sprite.spritecollide(bullet, asteroid_list, True)

        for asteroid in asteroid_hit_list:  # add the score thing here
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)  # prints score to the console, add one that prints the score out onto the GUI 
        if asteroid.rect.y < -10:
            asteroid_list.remove(bullet)
            all_sprites_list.remove(bullet)
    
    screen.fill(WHITE)
    screen.blit(backgroundImage, [0, 0])  # fills it with background image
    all_sprites_list.draw(screen)  # puts stuff on the screen
    player.rect.x += speedOfPlayer

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
