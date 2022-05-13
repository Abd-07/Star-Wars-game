import arcade
import random

# устанавливаем константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Star Wars"

class Space_ship(arcade.Sprite):
    def update(self):
        if self.right > SCREEN_WIDTH:
            self.right=SCREEN_WIDTH
        if self.left < 0 :
            self.left = 0

class Bullet(arcade.Sprite):
    def __init__(self):
     super().__init__("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/laser.png",0.8)
     self.change_y=5
     self.laser_sound=arcade.load_sound("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/laser.wav")
    def update(self):
         self.center_y += self.change_y
         if self.center_y > SCREEN_HEIGHT:
             self.kill()

class Enemy(arcade.AnimatedTimeSprite):
    def __init__(self):
        super(). __init__()
        self.textures.append(arcade.load_texture("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/tie fighter.png"))
        self.textures.append(arcade.load_texture("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/tie fighter2.png"))
        self.change_y=1
    def update(self):
        self.center_y -=self.change_y

# class with the game
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background=arcade.load_texture("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/space_background.png")
        self.space_ship=Space_ship("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Star Wars/x-wing.png")
        self.set_mouse_visible(False)
        self.red_line=Red_line("/Users/abdulazizsuleymanov/Desktop/Python/Arcade/Car Race/red_line_v2.png",0.4)

        self.bullets=arcade.SpriteList()
        self.enemies=arcade.SpriteList()

    def on_mouse_motion(self,x,y,dx,dy):
        self.space_ship.center_x=x
    
    def on_mouse_press(self,x,y,button,modifiers):
        bullet=Bullet()
        bullet.center_x=self.space_ship.center_x
        bullet.bottom=self.space_ship.top
        self.bullets.append(bullet)
        arcade.play_sound(bullet.laser_sound)

    # initial values
    def setup(self):
        self.space_ship.center_x=SCREEN_WIDTH/2
        self.space_ship.center_y=70
        for i in range(1000):
            enemy=Enemy()
            enemy.center_x=random.randint(20,SCREEN_WIDTH-20)
            enemy.center_y = 50*i + SCREEN_HEIGHT
            self.enemies.append(enemy)
        self.ships_killed=0
        
        self.red_line.center_x=400
        self.red_line.center_y=570
        self.red_line.change_x=0
        self.red_line.change_y=0
   
    # rendering
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.space_ship.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.red_line.draw()
        arcade.draw_text(f"Ships killed: {self.ships_killed}",280,550,arcade.color.BLACK,30)

    # logic
    def update(self, delta_time):
        self.space_ship.update()
        self.bullets.update()
        self.enemies.update_animation()
        self.enemies.update()
        for bullet in self.bullets:
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.kill()
        for bullet in self.bullets: 
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)
            if len(hit_list) > 0: 
                bullet.kill()
                self.ships_killed+=1
                for enemy in hit_list:
                    enemy.kill()
        self.red_line.update()

class Red_line(arcade.Sprite):
    def update(self):
        pass

window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
