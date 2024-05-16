import pygame as pg
import sys

class RigidBody:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.velocity = [0, 0]
        self.mass = width * height
        self.momentum = [self.velocity[0] * self.mass, self.velocity[1] * self.mass]

    def update(self):
        self.rect.move_ip(self.velocity)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)



def trdde_velocities(rect1, rect2):
    temp_x = rect1.velocity[0]
    temp_y = rect1.velocity[1]

    try:
        rect1.velocity[0] = rect2.velocity[0] - rect1.velocity[0]
        rect1.velocity[1] = rect2.velocity[1] - rect1.velocity[1]
        rect2.velocity[0] = temp_x - rect2.velocity[0]
        rect2.velocity[1] = temp_y - rect2.velocity[1]
    except Exception as e:
        print("Error: ", e)


def velocity_calc(m1, m2, u1, u2):
    out = ((m1 - COR * m2) * u1) + ((1 + COR) * m2 * u2)
    out = out / (m1 + m2)
    return out

#Coefficient of Restitution
COR = 1
def elastic_collision(rect1, rect2):
    rect1_x = rect1.velocity[0]
    rect1_y = rect1.velocity[1]
    rect2_x = rect2.velocity[0]
    rect2_y = rect2.velocity[1]
    rect1_mass = rect1.mass
    rect2_mass = rect2.mass
    rect1.velocity[0] = velocity_calc(rect1_mass, rect2_mass, rect1_x, rect2_x)
    rect1.velocity[1] = velocity_calc(rect1_mass, rect2_mass, rect1_y, rect2_y)
    rect2.velocity[0] = velocity_calc(rect2_mass, rect1_mass, rect2_x, rect1_x)
    rect2.velocity[1] = velocity_calc(rect2_mass, rect1_mass, rect2_y, rect1_y)


def collision(rect1, rect2):
    elastic_collision(rect1, rect2)


# Initialize Pygame
pg.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Rigid Body Physics")

# # Define colors
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)

# Dark mode palette
BACKGROUND_COLOR = (30, 30, 30)
RECT1_COLOR = (255, 100, 100)
RECT2_COLOR = (100, 100, 255)


# Create rigid bodies
rect1 = RigidBody(100, 200, 100, 100, RECT1_COLOR)
rect2 = RigidBody(400, 300, 20, 20, RECT2_COLOR)




#Friction
FRICTION_COEFFICIENT = 0.1

def apply_friction(self):
    if self.velocity[0] != 0:
        self.velocity[0] -= FRICTION_COEFFICIENT * (self.velocity[0] / abs(self.velocity[0]))
    if self.velocity[1] != 0:
        self.velocity[1] -= FRICTION_COEFFICIENT * (self.velocity[1] / abs(self.velocity[1]))


#Gravity
GRAVITY = 1

def apply_gravity(self):
    self.velocity[1] += GRAVITY

def collide_border(rect):
    if rect.rect.left <= 0 or rect.rect.right >= screen_width:
        rect.velocity[0] *= -1
    if rect.rect.top <= 0:
        rect.velocity[1] *= -1
    if rect.rect.bottom >= screen_height:
        print(rect.velocity[1])
        if rect.velocity[1] <= 5:
            rect.velocity[1] = 0
        else:
            rect.velocity[1] *= -1


#Move Speed
MOVE_SPEED = 2

# Main loop
clock = pg.time.Clock()
running = True
frame_count = 0
while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    #Apply Friction
    apply_friction(rect1)
    apply_friction(rect2)

    apply_gravity(rect1)
    apply_gravity(rect2)
    
    # Check for key presses to change velocity of rect1
    if(frame_count == 10):
        keys = pg.key.get_pressed()
        rect1.velocity[1] += MOVE_SPEED * (keys[pg.K_DOWN] - keys[pg.K_UP])
        rect1.velocity[0] += MOVE_SPEED * (keys[pg.K_RIGHT] - keys[pg.K_LEFT])
        frame_count = 0
    # keys = pg.key.get_pressed()
    # if keys[pg.K_DOWN] - keys[pg.K_UP] != 0:
    #     rect1.velocity[1] = MOVE_SPEED * (keys[pg.K_DOWN] - keys[pg.K_UP])
    # if keys[pg.K_RIGHT] - keys[pg.K_LEFT] != 0:
    #     rect1.velocity[0] = MOVE_SPEED * (keys[pg.K_RIGHT] - keys[pg.K_LEFT])

    # Check for collision
    if rect1.rect.colliderect(rect2.rect):
        collision(rect1, rect2)
        
        # Move rect1 outside of rect2 to prevent overlap
        # if rect1.rect.colliderect(rect2.rect):
        #     rect1.rect.move_ip(rect1.velocity[0], rect1.velocity[1])
        #     rect2.rect.move_ip(rect1.velocity[0], rect1.velocity[1])

    collide_border(rect1)
    collide_border(rect2)


    # Update positions
    rect1.update()
    rect2.update()



    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw rigid bodies
    rect1.draw(screen)
    rect2.draw(screen)
    # pg.draw.ellipse(screen, RECT2_COLOR, rect1)


    # Update the display
    pg.display.flip()

    frame_count += 1

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()
sys.exit()