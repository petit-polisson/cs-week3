import pygame
screen_height=720
screen_width=1280
class Picture:
    def __init__(self, image_path, image_sizing, start_x, start_y):
        self.image = pygame.image.load(image_path)
        original_width, original_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (original_width // image_sizing, original_height // image_sizing))
        self.pos = pygame.Vector2(start_x, start_y)

    def update(self, dt, screen_width, speed, direction):
        if direction=="l":
            self.pos.x-=speed*dt
        elif direction=="r":
            self.pos.x += speed * dt
        elif direction=="u":
            self.pos.y -= speed * dt
        elif direction=="d":
            self.pos.y += speed * dt  

        if self.pos.x > screen_width:
            self.pos.x = -self.image.get_width() * 40
            self.pos.y = self.pos.y - 10

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))
    def position(self):
        return self.pos.y
    def rel_position(self,moon_position):
        return int(moon_position-self.pos.y +591)