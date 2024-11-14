from picture import Picture
screen_height=720
screen_width=1280
class Player(Picture):
    def __init__(self, image_path, image_sizing, start_x, start_y):
        super().__init__(image_path, image_sizing, start_x, start_y)
        self.score = 0
        self.velocity_y = 0
        self.gravity = 500
        self.on_ground = False
        self.jump_frame_counter = 0
        self.isOutOfScreen1=False
        self.isOutOfScreen2=False
        self.relative_position=0

    def update(self, dt, screen_height,ground_level):
        

        if not self.on_ground:
            self.velocity_y += self.gravity * dt
            self.pos.y += self.velocity_y * dt

        if self.pos.y + self.image.get_height() >= screen_height - ground_level:
            self.pos.y = screen_height - self.image.get_height() - ground_level
            self.velocity_y = 0  
            self.on_ground = True
            
        else:
            self.on_ground = False

        
        if not self.on_ground:
            self.jump_frame_counter += 1

    def jump(self):
            self.velocity_y = -300  
            self.on_ground = False
    def isOutOfScreen(self):
        if(self.pos.y + self.image.get_height() > screen_height):
            self.isOutOfScreen1=True
        if(self.pos.y<0):
            self.isOutOfScreen2=True
            