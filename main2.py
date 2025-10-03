import pygame
import math
import os
import imageio

pygame.init()

# Display
WIDTH, HEIGHT = 800, 600 
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slingshot Rocket Simulation")

# Constants
PLANET_MASS = 100
SHIP_MASS = 5
g = 3
FPS = 60
PLANET_RADIUS = 50 
OBJ_RADIUS = 5
VEL_SCALE = 100

# Load assets
BG = pygame.transform.scale(pygame.image.load("back3.jpg"),(WIDTH,HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("mars.png"),(PLANET_RADIUS*2,PLANET_RADIUS*2))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Frame capture setup
os.makedirs("frames", exist_ok=True)
captured_frames = []
frame_count = 0

class Planet: 
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        window.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

class Spacecraft: 
    def __init__(self, x, y, velx, vely, mass):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.mass = mass
    
    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force  = (g * self.mass * planet.mass) / distance**2
        
        accel = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        accel_x = accel * math.cos(angle)
        accel_y = accel * math.sin(angle)

        self.velx += accel_x
        self.vely += accel_y

        self.x += self.velx
        self.y += self.vely

    def draw(self):
        pygame.draw.line(window, ORANGE, (int(self.x), int(self.y)),
                 (int(self.x + self.velx * 10), int(self.y + self.vely * 10)), 1)
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), OBJ_RADIUS)

def create_ship(Location, mouse):
    t_x, t_y = Location
    m_x, m_y = mouse
    velx = (m_x - t_x) / VEL_SCALE
    vely = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, velx, vely, SHIP_MASS)
    return obj
    
# Main loop 
def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    global frame_count, captured_frames

    while running: 
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        window.blit(BG, (0, 0))
        
        if temp_obj_pos:
            pygame.draw.line(window, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(window, RED, temp_obj_pos, OBJ_RADIUS)
            
        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_RADIUS
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()

        # Save each frame as image
        frame_path = f"frames/frame_{frame_count:04d}.png"
        pygame.image.save(window, frame_path)
        captured_frames.append(frame_path)
        frame_count += 1

    pygame.quit()

    # Create GIF from captured frames
    print("Creating GIF...")
    images = [imageio.v2.imread(f) for f in captured_frames]
    imageio.mimsave("simulation.gif", images, duration=1 / FPS)  # ~60 FPS

    # Clean up frame images
    for f in captured_frames:
        os.remove(f)
    os.rmdir("frames")

    print("GIF saved as simulation.gif")

if __name__ == "__main__":
    main()
