import os
import random
add_library('minim')


path = os.getcwd()
#set up ground level, width and height
RESOLUTION_W = 720
RESOLUTION_H = 720
GROUND = 585
player = Minim(this)

#parent class for all creatures
class Creature:
    def __init__(self, x, y, r, img, img_w, img_h, num_slices):
        self.x = x # x coordinate of center
        self.y = y # y coordinate of center
        self.r = r # radius
        self.vy = 0 #vertical velocity (initially set to 0)
        self.vx = 5 #horizontal velocity
        self.img = loadImage(path + "/images/" + img) #load the sprite image
        self.img_w = img_w # Width of the sprite image
        self.img_h = img_h # height of the sprite image
        self.num_slices = num_slices
        self.slice = 0 #initial sprite
        self.dir = RIGHT  
        self.g = GROUND
        
    def gravity(self):
        #if the creature is on the ground the vertical velocity is 0
        if self.y + self.r >= self.g: 
            self.vy = 0
        else:
            self.vy += 0.4 #increase vertical velocity to create effect of acceleration
            if self.y + self.r + self.vy > self.g: #adapt coordinates to display creature exactly on the ground
                self.vy = self.g - (self.y+self.r)
        #self.g = 585        
        for platform in game.platforms: #if creature lands on a platform set the ground level to platform's top surface
            if self.y + self.r <= platform.y and self.x >= platform.x and self.x <= platform.x + platform.platform_w:
                self.g = platform.y
                
    def change_direction(self): #function to get the opposite direction
        if self.dir == LEFT:
            self.dir = RIGHT
        elif self.dir == RIGHT:
            self.dir = LEFT
    
    
    def check_platform_collision(self):
    # Handle collisions with platforms
        for platform in game.platforms:
            # check horizontal collisions
            if (self.y + self.r > platform.y and
                self.y - self.r < platform.y + platform.platform_h):
                # Right edge collision
                if (self.x + self.r >= platform.x + platform.platform_w and
                    self.x - self.r < platform.x + platform.platform_w):
                    self.x = platform.x + platform.platform_w + self.r
                    self.change_direction()

                # Left edge collision
                elif (self.x + self.r >= platform.x and self.x < platform.x):
                    self.x = platform.x - self.r
                    self.change_direction()
                
            
            # Vertical collisions
            if (self.x + self.r >= platform.x and
                self.x - self.r < platform.x + platform.platform_w):
                # Top collision
                if (self.y + self.r >= platform.y and
                    self.y < platform.y and self.vy >= 0):
                    self.y = platform.y - self.r
                    self.vy = 0
                    self.jump_count = 0
                
                # Bottom collision
                elif (self.y - self.r <= platform.y + platform.platform_h and
                    self.y > platform.y + platform.platform_h and self.vy <= 0):
                    self.y = platform.y + platform.platform_h + self.r
                    self.vy = 0

class Enemy(Creature): #enemy class inherits from creature
    def __init__(self, x, y, r, x_lim_left, x_lim_right):
        # Initialize enemy attributes
        Creature.__init__(self, x, y, r, "worm.png", 30, 30, 5)
        self.x_lim_left = x_lim_left # Left boundary for enemy movement
        self.x_lim_right = x_lim_right # Right boundary for enemy movement
        self.vx = 1 # Speed of the enemy
        self.alive = True # attribute to keep track if enemy's alive
        self.slice = 0  # Current sprite 
    
    def update(self): #function for enemy's movement
        self.gravity()
        self.check_platform_collision() #check if enemy bumps into edges of platforms
        if frameCount % 10 == 0: # cycle through sprites
            self.slice = (self.slice + 1) % self.num_slices
         #move based on direction   
        if self.dir == RIGHT: 
            if self.x + self.r >= self.x_lim_right: # if enemy moves right the right boarder is reached turn away
                self.dir = LEFT #and change direction
            else:
                self.x += self.vx #increase x coordinate for moving right

        elif self.dir == LEFT:
            if self.x - self.r <= self.x_lim_left: #if enemy moves left and the left border reached turn away 
                self.dir = RIGHT # and change direction
            else:
                self.x -= self.vx #decrease x coordinate for moving left


        
    def display(self):
        if self.alive == True:
            dWidth = self.r * 2  # Adjust width based on radius
            dHeight = self.r * 2 # Adjust height based on radius
    
            dx = self.x - self.r  # Adjust x to center
            dy = self.y - self.r # Adjust x to center
            if self.dir == RIGHT: #display the image based on direction and cycle through sprites to create the animation of moving
                image(self.img, dx, dy + game.y_shift, dWidth, dHeight, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img, dx, dy + game.y_shift, dWidth, dHeight, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            

class Egg:
    def __init__(self, x, y, r, dir):
        # Initialize egg attributes for position, size, and movement direction
        self.x = x # x coordinate of the center
        self.y = y # y coordinate of the center
        self.r = r # radius
        self.vx = 15 #speed of the egg
        self.dir = dir #Direction of the egg's movement
    
    def display(self): #draw an egg
        fill(255, 255, 255)
        noStroke()
        ellipse(self.x, self.y + game.y_shift, self.r * 2, self.r * 2)
          
        
    def update(self): #move based on direction
        if self.dir == RIGHT: # if moving right increase x
            self.x += self.vx
        elif self.dir == LEFT: # if moving left decrease x
            self.x -= self.vx
        


class Chicken(Creature):
    def __init__(self, x, y, r):
        Creature.__init__(self, x, y, r, "chick.png", 83, 80, 1) #inherit from parent class
        self.key_handler = {UP: False} # key handler for jumping
        self.jump_count = 0 # attribute that keeps track of jumps
        self.shoot = False # attribute to signal when to shoot
        self.egg = None  # Store the egg object
        self.egg_active = False  # Flag to track if an egg is moving
        self.shoot = False  # Track when to shoot
        self.dir = LEFT
        self.alive = True # keep track if the chicken is alive
        self.jump_sound = player.loadFile(path + "/images/jump.wav")

    def shoot_the_egg(self):
        # Shoot an egg only if no egg is active and shoot flag is True
        if self.shoot == True and self.egg_active == False:
            if self.dir == RIGHT: # shoot an egg according to the chickens direction in the moment of shooting
                self.egg = Egg(self.x + self.r + 10, self.y, 10, self.dir)
            else:
                self.egg = Egg(self.x - self.r - 10, self.y, 10, self.dir)
            self.egg_active = True  # Mark egg as active
            self.shoot = False  # Reset shoot flag after shooting
    #this is new
    def update_egg(self):
        # Update egg's position only if it is active
        if self.egg_active == True: # if there is an active egg we display and move it
            self.egg.display()
            self.egg.update()
            # Deactivate egg if it moves off-screen
            if self.egg.x + self.egg.r < 0 or self.egg.x - self.egg.r > RESOLUTION_W:
                self.egg_active = False # if the egg is off screen we mark that there is no more active egg
                self.shoot = False
            for platform in game.platforms: # iterate through all platforms and check if the egg collides with any of them
                if (self.egg.x + self.egg.r > platform.x and
                self.egg.x < platform.x + platform.platform_w and
                self.egg.y > platform.y and
                self.egg.y < platform.y + platform.platform_h):
                    self.shoot = False
                    self.egg_active = False # if it does the egg is no longer active
                    break #collision found, stops checking
        
    
    def display(self): # display the chicken image based on its direction
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2, self.y + game.y_shift - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2, self.y + game.y_shift - self.img_h//2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
        
            
            
    def update(self):
        self.gravity() # apply gravity to chicken
        #if the chicken is on the ground the jump count gets reset
        if self.y + self.r == self.g:
            self.jump_count = 0 
         # move vertically   
        self.y += self.vy
        
        #if the chicken reaches the edges of the frame it should change the direction and move the other way
        if self.dir == RIGHT: #check if right wall is reached
            if self.x + self.r >= RESOLUTION_W:
                self.dir = LEFT
            else: # if the chicken is inside the frame
                self.x += self.vx # the x increases to move right

        elif self.dir == LEFT:  #check if left wall is reached
            if self.x - self.r <= 0:
                self.dir = RIGHT
            else: # if the chicken is inside the frame
                self.x -= self.vx # the x decreses to move left
         
                        
        if self.key_handler[UP] == True: #if jump is pressed
            if self.jump_count < 2: #if the player didnt already press jump more than twice
                self.vy = -18 # set vertical velocity
                self.y += self.vy # update y coordinate
                self.jump_count += 1 # increase jump count
                self.jump_sound.rewind()
                self.jump_sound.play()
                
        if self.y <= game.h//2: #calculate y_shift if the chicken goes higher than the middle of the screen for creating parallex effect
            game.y_shift = game.h//2 - self.y
            # self.g = self.g - game.y_shift
        
        else: # if chicken is in the lower half shift is 0
            game.y_shift = 0  


class Platform():
    def __init__(self, x, y, platform_w, platform_h, img_name):
        #set attributes for platforms
        self.img_name = img_name
        self.img = loadImage(path + '/images/' + str(self.img_name) + ".png")
        self.x = x # x of the upper left corner
        self.y = y # y of the upper left corner
        self.platform_w = platform_w # width
        self.platform_h = platform_h # height
    
    def display(self): # display the platform image
        fill(100)
        image(self.img, self.x, self.y + game.y_shift, self.platform_w, self.platform_h)
       
        

        
class Fruit():
    def __init__(self, name, x, y, r):
        #set the attributes for the fruit class
        self.name = name
        self.x = x # x coordinate of the center
        self.y = y # y coordinate of the center
        self.r = r # radius
        self.img = loadImage(path + "/images/" + str(self.name) + ".png")  # Load fruit image
        self.visible = True # Set visibility of fruit to true initially
    
    def display(self):
        if self.visible == True: # if fruit is visible display the image according to shift
            image(self.img, self.x - self.r, self.y + game.y_shift - self.r, self.r * 2, self.r * 2)
        
    
    
class Game():
    def __init__(self):
        #set up game attributes
        self.w = RESOLUTION_W
        self.h = RESOLUTION_H
        self.y_shift = 0 # set y shift to 0 initially
        self.chicken = Chicken(50, 545, 40) # instantiate chicken
        self.g = 585
        self.fruit_sound = player.loadFile(path + "/images/collect_fruit.wav")
        self.lose_sound = player.loadFile(path + "/images/lose.wav")
        self.flag_img = loadImage(path + '/images/'+ "flag.png")
        self.game_over = loadImage(path + '/images/'+ "game_over.png")
        self.you_won = loadImage(path + '/images/'+ "you_won.png")
        self.game_won = False # attribute to keep track if player wins the game, intially false
        self.platforms = [] # list of all platforms
        # #create all the platforms
        self.platforms.append(Platform(0, self.g, self.w, self.h - self.g, "ground1"))
        self.platforms.append(Platform(500, 385, 220, 200, "tile1"))
        self.platforms.append(Platform(0, 300, 350, 70, "tile2"))
        self.platforms.append(Platform(0, 140, 150, 160, "tile3"))
        self.platforms.append(Platform(330, -80, 390, 100, "tile4"))
        self.platforms.append(Platform(450, -270, 300, 200, "tile9"))
        self.platforms.append(Platform(0, -320, 300, 150, "tile5"))
        self.platforms.append(Platform(0, -480, 150, 150, "tile6"))
        self.platforms.append(Platform(330, -660, 150, 100, "tile7"))
        self.platforms.append(Platform(0, -800, 120, 100, "tile8"))
        self.platforms.append(Platform(580, -850, 150, 100, "tile7"))
        self.platforms.append(Platform(300, -1020, 250, 30, "250x30 tile"))
        self.platforms.append(Platform(300, -1210, 120, 100, "120x100 tile"))
        self.platforms.append(Platform(180, -1330, 120, 100, "120x100 tile"))
        self.platforms.append(Platform(0, -1450, 180, 100, "180x100 tile"))
        self.platforms.append(Platform(340, -1600, 180, 100, "180x100 tile"))
        self.platforms.append(Platform(190, -1800, 150, 100, "tile7"))        
        #list of enemies
        self.enemies = []
        self.start = False # attribute to pass in when to start
        self.score = 0 # attribute to count the score, initially 0
        self.fruits = [] # list of fruits
        
        
        #randomly generate fruits and enemies 
        for platform in self.platforms[1:len(self.platforms)-1]:
            if platform.platform_w > 120:
                if random.choice([True, False]): # chose if enemy will be generated on that platform
                    x = self.get_valid_coordinates(platform, 30) # get random x
                    if x != None:
                        self.enemies.append(Enemy(x, platform.y - 30, 30, platform.x + 30, platform.x + platform.platform_w - 30))
                
            else:
                if random.choice([True, False]): # chose if fruit will be generated on that platform
                    x = self.get_valid_coordinates(platform, 15)
                    if x != None:
                        self.fruits.append(Fruit(random.choice(["apple", "banana"]), x, platform.y - 15, 15))

    


    
    
    
    
    def get_valid_coordinates(self, platform, r): # function to generate coordinates that will not crash with any of the platforms
        next_platform = self.platforms[self.platforms.index(platform)+1] # get the next platform
        if next_platform.y + next_platform.platform_h >= platform.y and next_platform.x in range(platform.x, platform.x+platform.platform_w+1): # check if there is another platform on top of the platform we are about display enemy/fruit
            # determine from which side the platforms are stacked and generate coordinates on the area of the platform that is not overlaping with the area of another platform
            if next_platform.x <= platform.x:
                x = random.randint(platform.x + next_platform.platform_w + r, platform.x + platform.platform_w - r)
            else:
                x = random.randint(platform.x + r, next_platform.x - r)
        else: # if there is no platform stacked, generate random coordinate within the platform
            x = random.randint(platform.x + r, platform.x + platform.platform_w - r)
        return x
            
            
   
        
    def get_distance(self,first, other): # function to calculate distance between two objects
        return ((first.x - other.x)**2 + (first.y - other.y)**2)**0.5  
        
        
    def eat_fruit(self): # function for eating fruit
        for fruit in self.fruits:  # iterate through all the fruits
            if fruit.visible == True and self.get_distance(self.chicken, fruit) <= self.chicken.r + fruit.r: # if the fruit is not already eaten and the chicken matches its coordinates eat the fruit
                fruit.visible = False # stop displaying fruit after eaten
                self.score += 1 # increase score
                self.fruit_sound.play()
                self.fruit_sound.rewind()


    def kill_enemy(self): # function for killing enemies
        if self.chicken.egg != None: # check if an egg is shot
            for enemy in self.enemies: #iterate through all enemies
                
                # if the enemy is alive and the egg nails the enemy
                if enemy.alive == True and self.get_distance(self.chicken.egg, enemy) <= self.chicken.egg.r + enemy.r:
                    enemy.alive = False # enemy dies
                    self.chicken.egg_active = False # egg becomes inactive
                    
  
    def check_collision_with_enemy(self): # function to check if chicken bumps into enemy
        for enemy in self.enemies: # iterate through all enemies
            #if chicken bumps it dies
            if enemy.alive == True and self.get_distance(self.chicken, enemy) <= self.chicken.r + enemy.r:
                self.chicken.alive = False     

    def display(self):
        self.determine_win() # check if the game is won
        if self.game_won == True: # display the winning message and stop the game in the current frame
            self.chicken.display()
            for platform in self.platforms:
                platform.display() # display all the platforms
            for enemy in self.enemies:
                enemy.display() # display all the enemies
            for fruit in self.fruits:
                fruit.display() # display all the fruits
            fill(0, 255, 0)  # Green text
            textSize(32)
            textAlign(CENTER)
            
            image(self.you_won, 0, 100)
            textSize(20)
            text("Click anywhere to restart", self.w // 2, self.h // 2 + 30)

        elif self.chicken.alive == True:

            self.check_collision_with_enemy() # call function to check if chicken collides with enemy
            self.chicken.check_platform_collision() # control position regarding bumping to platforms
            self.chicken.gravity() # call the gravity
            self.chicken.display() # display chicken
            if self.start == True: # whenever player starts the game
                self.chicken.update() # the chicken starts moving
                self.chicken.shoot_the_egg()  # Handle egg shooting
                self.chicken.update_egg() # egg moves
                self.eat_fruit() 
                self.kill_enemy()
            
            for fruit in self.fruits:
                fruit.display() # display all the fruits
            for platform in self.platforms:
                platform.display() # display all the platforms
            for enemy in self.enemies:
                enemy.display() # display all the enemies
                enemy.update() # move enemies
            
            image(self.flag_img, 170, -1850 + game.y_shift, 60, 50)
            
            fill(255, 255, 255)
            textSize(20)
            text("Press key 'UP' to jump", 270, 500 + game.y_shift)
            
            fill(255, 255, 255)
            textSize(20)
            text("Press 'ENTER' to shoot", 500, 350 + game.y_shift)
            
            fill(255, 255, 255)
            textSize(20)
            text("Press 'SPACE' to change direction", 300, 130 + game.y_shift)
            
            fill(255, 0, 0)  # Set text color to black
            textSize(17)  # Set text size
            text("Score: " + str(game.score), 630, 20) # display score
        
        else: # if chicken dies the game stops in the current frame and displays platforms enemies and fruits
            self.chicken.display()
            for platform in self.platforms:
                platform.display()
            for enemy in self.enemies:
                enemy.display()
            for fruit in self.fruits:
                fruit.display()
            image(self.flag_img, 170, -1850 + game.y_shift, 60, 50)
            self.lose_sound.play()

            fill(255, 0, 0)  # Red text
            textSize(32)
            textAlign(CENTER)
            # display messages
            
            image(self.game_over, 120, 150)
            textSize(20)
            text("Score: " + str(self.score), self.w // 2 , self.h // 2 + 30)
            text("Click anywhere to restart", self.w // 2, self.h // 2 + 50)
            
    def determine_win(self):
        # Check if the chicken meets the winning condition
        chicken = self.chicken
        # if the chicken reaches the last platform it wins
        if (chicken.y == self.platforms[-1].y - chicken.r and
            chicken.x - chicken.r >= self.platforms[-1].x and
            chicken.x + chicken.r <= self.platforms[-1].x + self.platforms[-1].platform_w):
            self.game_won = True

    def reset(self): # function to reset the game whenever clicked
        self.__init__()
game = Game() # instantiate game

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    background(0,0,0)
    
def draw(): 
    background(0,0,0)
    
    game.display() 

    
  
def keyPressed():
    if game.chicken.alive == True and game.game_won == False:
        if keyCode == 32: # if space is pressed the chicken changes direction
            game.start = True 
            game.chicken.change_direction()
        elif keyCode == UP: # if up is pressed chicken jumps
            game.chicken.key_handler[UP] = True
        elif key == ENTER: # if enter is pressed chicken shoots
            game.chicken.shoot = True
        else:
            return

def mouseClicked():
    if game.chicken.alive == False:  # Highlighted: Restart the game when clicked
        game.reset()

def keyReleased(): # set back environment after key is released
    if keyCode == UP:
        game.chicken.key_handler[UP] = False
        # game.chicken.jump_pressed = False
    elif key == ENTER:
        game.chicken.shoot = False
