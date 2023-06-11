from pygame import *
from random import randint
from PIL import Image


class GameSprite():
    def __init__(self, x, y, w, h, color):
        self.rect = Rect(x, y, w, h)
        self.color = color
    def draw(self):
        draw.rect(window, self.color, self.rect)
    def collide(self,other):
        return abs(self.rect.x - other.rect.x) < 20 and abs(self.rect.y - other.rect.y) < 20

class Player(GameSprite):
    def __init__(self, x, y, color):
        super().__init__(x,y,20,20,color)
        self.speed = 2
    def move(self, left, right, up, down):
        keys_pressed = key.get_pressed()
        dx = 0
        dy = 0
        collision = False
        if keys_pressed[up]:
            dy -= self.speed
        if keys_pressed[down]:
            dy += self.speed
        if keys_pressed[left]:
            dx -= self.speed
        if keys_pressed[right]:
            dx += self.speed
        self.rect.x += dx
        self.rect.y += dy
        for w in walls:
            if self.rect.colliderect(w.rect):
                collision = True
                break
        if collision:
            self.rect.x -= dx
            self.rect.y -= dy
        for g in goals:
            if self.rect.colliderect(g.rect):
                goals.remove(g)
                if len(goals) == 0:
                    window.blit(my_label, (250,250))


font.init()
font1 = font.SysFont('Consolas', 80)
my_label = font1.render("YOU WIN", True, (255,255,255))


window = display.set_mode((700, 500))
display.set_caption("catch")

p1 = Player(100,100,(0,255,0))
p2 = Player(100,400,(0,0,255))

# walls = []
# for i in range(5):
#     w, l = 0, 0
#     length = 300
#     coin = randint(0,1)
#     if coin == 0:
#         w = 20
#         l = length
#     else:
#         w = length
#         l = 20
#     wall = GameSprite(randint(100,600), randint(100,400), w, l, (0,0,255))
#     walls.append(wall)

walls = []
goals = []

# # if we use a Python file
# for r in wall_data.level1:
#     walls.append(GameSprite(r.x, r.y, r.w, r.h, (255,255,255)))

# # if we use JSON
# with open('walls.json', 'r') as f:
#     data = json.load(f)
#     print(data)
#     for w in data["walls"]:
#         walls.append(GameSprite(w["x"], w["y"], w["w"], w["h"], (255,255,255)))

with open('walls.txt', 'r') as f:
    line = f.readline()
    while line:
        splitline = line.split(',')
        for i in range(len(splitline)):
            splitline[i] = int(splitline[i].strip(' ,()\n'))
        walls.append(GameSprite(splitline[0], splitline[1], splitline[2], splitline[3], (255,255,255)))
        line = f.readline()

with Image.open('walls2.png') as im:
    clrs = im.getpalette()
    print(im)
    
    width = im.width
    height = im.height

    window = display.set_mode((width*25, height*25))

    for x in range(width):
        for y in range(height):
            print(im.getpixel((x,y)))
            if im.getpixel((x,y)) == 1:
                walls.append(GameSprite(x*25, y*25, 25, 25, (255,255,255)))
            if im.getpixel((x,y)) == 2:
                goals.append(GameSprite(x*25, y*25, 15, 15, (0,255,0)))
#game loop
run = True
clock = time.Clock()
FPS = 30

while run:
    window.fill((0,0,0))

    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            # print(e.unicode)
            if e.unicode.isnumeric():
                frames_input.value += e.unicode

    p1.move(K_LEFT, K_RIGHT, K_UP, K_DOWN)
    p2.move(K_a,K_d,K_w,K_s)

    p1.draw()
    p2.draw()

    for w in walls:
        w.draw()

    for g in goals:
        g.draw()
    if len(goals) == 0:
        window.blit(my_label, (250,250))

    display.update()
    clock.tick(FPS)
