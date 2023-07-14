import pygame as pg
import pygame.display
import sys
import math
import random

WINDOW_SIZE = (1200, 800)
NUM_RAYS = 180


class Wall:
    def __init__(self, display, start_pos, end_pos, color='white'):
        self.display = display
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color

    def render(self):
        pg.draw.line(self.display, self.color, self.start_pos, self.end_pos, 3)


class Ray:
    def __init__(self, angle, pos=(0, 0), color='yellow'):
        self.pos = pos
        self.angle = angle
        self.color = color
        self.direction = (math.cos(angle), math.sin(angle))

    def update(self, pos):
        self.pos = pos
        print(pos)

    def check_collision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.direction[0]
        y4 = self.pos[1] + self.direction[1]

        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None

        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collide_position = [x, y]
            return collide_position

    def render(self, display, walls):
        closest = 100000
        closest_point = None
        for wall in walls:
            intersect_point = self.check_collision(wall)
            if intersect_point is not None:
                # Get distance between ray source and intersect point
                ray_dx = self.pos[0] - intersect_point[0]
                ray_dy = self.pos[1] - intersect_point[1]

                distance = math.sqrt(ray_dx ** 2 + ray_dy ** 2)
                if distance < closest:
                    closest = distance
                    closest_point = intersect_point

        if closest_point is not None:
            pygame.draw.line(display, self.color, self.pos, closest_point)


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.display = pygame.Surface(WINDOW_SIZE)

        self.walls = []

        self.generate_walls()
        self.generate_random_walls(4)

        self.rays = self.generate_rays()

    def generate_walls(self):
        self.walls.append(Wall(self.display, (0, 0), (WINDOW_SIZE[0], 0)))
        self.walls.append(Wall(self.display, (0, 0), (0, WINDOW_SIZE[1])))
        self.walls.append(Wall(self.display, (WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
        self.walls.append(Wall(self.display, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))

    def generate_random_walls(self, random_walls_count):
        for i in range(random_walls_count):
            start_x = random.randint(0, WINDOW_SIZE[0])
            start_y = random.randint(0, WINDOW_SIZE[1])
            end_x = random.randint(0, WINDOW_SIZE[0])
            end_y = random.randint(0, WINDOW_SIZE[1])

            self.walls.append(Wall(self.display, (start_x, start_y), (end_x, end_y)))


    def generate_rays(self):
        rays = []
        for i in range(0, 360, int(360 / NUM_RAYS)):
            print(i)
            rays.append(Ray(angle=math.radians(i)))

        return rays

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for ray in self.rays:
            ray.update(mouse_pos)

    def render(self):
        self.display.fill('black')

        for wall in self.walls:
            wall.render()

        for ray in self.rays:
            ray.render(self.display, self.walls)

        self.screen.blit(self.display, (0, 0))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

            self.update()
            self.render()
            pg.display.flip()
            self.clock.tick()


if __name__ == '__main__':
    game = Game()
    game.run()
