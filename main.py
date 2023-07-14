import pygame as pg
import pygame.display
import sys
import math

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
        return None

    def render(self, display, walls):
        global last_closest_point

        closest = 100000
        closest_point = None
        for wall in walls:
            intersect_point = self.check_collision(wall)
            if intersect_point is not None:
                # Get distance between ray source and intersect point
                ray_dx = self.pos.x - intersect_point[0]
                ray_dy = self.pos.y - intersect_point[1]

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

        self.walls = self.generateWalls()
        self.walls.append(Wall(self.display, (0, 0), (800, 600), 'white'))

        self.rays = self.generate_rays()

    def generateWalls(self):
        walls = []
        walls.append(Wall(self.display, (0, 0), (WINDOW_SIZE[0], 0)))
        walls.append(Wall(self.display, (0, 0), (0, WINDOW_SIZE[1])))
        walls.append(Wall(self.display, (WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
        walls.append(Wall(self.display, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))

        return walls


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
