import os, random

path = os.getcwd()
NUM_ROWS = 20 # Number of rows in the grid
NUM_COLS = 20 # Number of columns in the grid
RESOLUTION = 600 # Window resolution
TILE_WIDTH = RESOLUTION / NUM_COLS # Width of each tile in the grid
TILE_HEIGHT = RESOLUTION / NUM_ROWS # Width of each tile in the grid


class Snake(list):
    def __init__(self, r, c):
        # Load images for the snake's head in different directions
        self.head_left = loadImage(path + "/images/" + "head_left" + ".png")
        self.head_up = loadImage(path + "/images/" + "head_up" + ".png")
        self.r = r # Row position of the snake's head
        self.c = c # Column position of the snake's head
        self.vx = 1  # Horizontal velocity
        self.vy = 1  # Vertical velocity
        self.allow_dir_change = True
        self.target_direction = RIGHT # Stores next desired direction. 
        self.direction = RIGHT  # Initial direction of the snake
        # Add two green elements to the snake body
        self.append(SnakeElement(self.r, self.c-1, "green"))
        self.append(SnakeElement(self.r, self.c-2, "green"))
        self.alive = True # Checks if the snake is alive(moving); initiaally set to True
    
    def display(self):
        if self.alive == True: # Check if the snake is alive
            # Display the snake's head based on its direction
            if self.target_direction != self.direction: # Check if thye target direction is the same as current direction
                self.direction = self.target_direction # If not the same this line updates target direction to match with current direction
            if self.direction == RIGHT: # Displays snake head in the right direction
                image(self.head_left, self.c*TILE_WIDTH, self.r*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 0, 0)
            elif self.direction == LEFT: # Displays snake head in the left direction reversing the image of snake's head in right direction
                image(self.head_left, self.c*TILE_WIDTH, self.r*TILE_HEIGHT)
            elif self.direction == UP: # Displays snake head in the right direction
                image(self.head_up, self.c*TILE_WIDTH, self.r*TILE_HEIGHT)
            elif self.direction == DOWN: # Displays snake head in the down direction reversing the image of snake's head in up direction
                image(self.head_up, self.c*TILE_WIDTH, self.r*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT, 0, 0)
            for part in self: # After displaying the head this loop goes over the snake body and displays all the elements
                part.display()
            
    def check_if_exists(self, c, r): # The function checks if there is a snake element in a certain cell
        for element in self:
            if element.r == r and element.c == c: # Check if any part of the snake occupies a given cell (c, r)
                return True
        return False
       
    def add_element(self, clr):
        # Add a new element to the snake's tail based on its current direction
        tail = self[-1] # Gets the last element of the snake body(tail)
        new_r = tail.r # Store the current row position of the tail
        new_c = tail.c # Store the current column position of the tail
        if self.direction == RIGHT: # If the snake is moving right
            new_c -= 1 # Move the new tail position one cell to the left (to extend in the right direction)
        elif self.direction == LEFT: # If the snake is moving left
            new_c += 1 # Move the new tail position one cell to the right (to extend in the left direction)
        elif self.direction == UP: # If the snake is moving up
            new_r += 1 # Move the new tail position one cell down (to extend upwards)
        elif self.direction == DOWN: # If the snake is moving down
            new_r -= 1 # Move the new tail position one cell up (to extend downwards)
        self.append(SnakeElement(new_r, new_c, clr)) # Append a new SnakeElement at the calculated position to extend the tail
        
    def move(self):
        
        # Check if the snake is within the grid bounds, otherwise end the game
        if not ((self.direction == RIGHT and self.c + self.vx < NUM_COLS) or (self.direction == LEFT and self.c - self.vx > -1) or (self.direction == UP and self.r - self.vy > -1) or (self.direction == DOWN and self.r + self.vy < NUM_ROWS)):
            self.vx = 0 # Stop horizontal movement
            self.vy = 0 # Stop Vertical movement
            self.alive = False # Snake is not alive any more
            self.display_score = False # Stops displaying score in the upper right corner
            noLoop()
            background(203)
            fill(0, 0, 0)  # Set text color to black
            textSize(30)  # Set text size
            text("Game's Over", 200, 300)
            textSize(20)
            text("Score: " + str(game.score), 260, 330)
            return
        
        stop_game = False # Check if the game should stop due to collision
        if self.direction == RIGHT and self.c + self.vx < NUM_COLS: # Check if the snake is in the frame
            if self.check_if_exists(self.c + self.vx, self.r) == True: # Check collision with itself on the right
                stop_game = True # If colision is detected the variable for checking if the game should stop becomes true
                       
        elif self.direction == LEFT and self.c - self.vx > -1: # Check if the snake is in the frame
            if self.check_if_exists(self.c - self.vx, self.r) == True: # Check collision with itself on the left
                stop_game = True # If colision is detected the variable for checking if the game should stop becomes true
                
                
        elif self.direction == UP and self.r - self.vy > -1:
            if self.check_if_exists(self.c, self.r - self.vy) == True: # Check collision with itself above
                stop_game = True # If colision is detected the variable for checking if the game should stop becomes true
                
        elif self.direction == DOWN and self.r + self.vy < NUM_ROWS:
            if self.check_if_exists(self.c, self.r + self.vy) == True: # Check collision with itself below
                stop_game = True # If colision is detected the variable for checking if the game should stop becomes true
        
        if stop_game == True: # If a collision occurs, stop the game
            self.vx = 0 # Stop horizontal movement
            self.vy = 0 # Stop Vertical movement
            self.alive = False # Snake is not alive any more
            self.display_score = False # Stops displaying score in the upper right corner
            noLoop()
            background(203)
            fill(0, 0, 0)  # Set text color to black
            textSize(30)  # Set text size
            text("Game's Over", 200, 300)
            textSize(20)
            text("Score: " + str(game.score), 260, 330)
            return    
    
            
        # This is for moving the elements of snake body
        for part in self[::-1]: # Goes over all elements starting from tail until head
            if self.index(part) != 0: # If the element is not the one that comes before the head its row and column updates to the row and column of the element in front of it
                part.r = self[self.index(part)-1].r 
                part.c = self[self.index(part)-1].c 
            else: # This case is for the element before head
                part.r = self.r # The element row and column updates to head's row and column
                part.c = self.c
    
    # Update the head position based on the current direction
        if self.direction == RIGHT and self.c + self.vx < NUM_COLS: # Move right if the snake wont go outside of the frame
                self.c += self.vx  
                       
        elif self.direction == LEFT and self.c - self.vx > -1:  # Move left if the snake wont go outside of the frame
                self.c -= self.vx
                
        elif self.direction == UP and self.r - self.vy > -1:  # Move up if the snake wont go outside of the frame
                self.r -= self.vy
                
        elif self.direction == DOWN and self.r + self.vy < NUM_ROWS:  # Move down if the snake wont go outside of the frame
                self.r += self.vy
        
            

    

        
    def set_direction(self, direction):
        # Prevent reversing the snake's direction
        if (direction == LEFT and self.direction == RIGHT) or (direction == RIGHT and self.direction == LEFT) or (direction == UP and self.direction == DOWN) or (direction == DOWN and self.direction == UP) :
            return # Exit if reverse direction is attempted
        if self.target_direction != self.direction:
            return
        if self.allow_dir_change == True: # Checks if changing direction is allowed
            self.direction = direction # Set new direction
            self.allow_dir_change = False  # Prevent immediate change again
            self.target_direction = direction # Set target direction
        else: # Set target direction if change not allowed yet
            self.target_direction = direction
        
            
    

class Fruit():
    def __init__(self, name, clr):
        self.name = name # Set fruit name
        self.img = loadImage(path + "/images/" + str(self.name) + ".png")  # Load fruit image
        self.visible = True # Set visibility of fruit to true initially
        self.clr = clr # Set color of the fruit
    
        
        
        
class SnakeElement():
    def __init__(self, r, c, clr):
        self.radius = TILE_WIDTH / 2 # Set radius based on tile width
        self.r = r # Set row position
        self.c = c # Set column position
        self.clr = clr # Set color
    
    
    
    def display(self): # Draws snake element as circle in different color
        if self.clr == "red":
            fill(172, 48, 32)
            noStroke()
            ellipse((self.c + 0.5)* TILE_WIDTH, (self.r + 0.5) * TILE_HEIGHT, self.radius * 2, self.radius * 2)
        elif self.clr == "yellow":
            fill(252, 226, 76)
            noStroke()
            ellipse((self.c + 0.5)* TILE_WIDTH, (self.r + 0.5) * TILE_HEIGHT, self.radius * 2, self.radius * 2)        
        elif self.clr == "green":
            fill(80, 152, 32)
            noStroke()
            ellipse((self.c + 0.5)* TILE_WIDTH, (self.r + 0.5) * TILE_HEIGHT, self.radius * 2, self.radius * 2)
            
            
        
            
        
        
class Game():
    def __init__(self):
        self.snake = Snake(NUM_COLS//2, NUM_ROWS//2) # Initialize snake in the center
        self.fruit_visible = True # Set fruit visibility to true initially
        self.score = 0 # score is 0 initially
        # Initialize row and column for fruit
        self.r = 0
        self.c = 0
        self.colors = {"apple": "red", "banana": "yellow"} # Set colors for fruits
        self.display_score = True
                
                
    def display_score(self):
        if self.display_score == True:
            fill(0, 0, 0)  # Set text color to black
            textSize(17)  # Set text size
            text("Score: " + str(game.score), 500, 20)
    
    def get_random_coordinates(self):
         # Get random coordinates for fruit while it is visible
        while self.fruit_visible == True: # fruit visible attribute ensures that only one fruit at a time is displayed when function is called
        
            self.r = random.randint(0, NUM_ROWS - 1) 
            self.c = random.randint(0, NUM_COLS - 1)
            # Check if fruit was generated on snake's head or body
            if self.r == self.snake.r and self.c == self.snake.c:
                self.get_random_coordinates() # Re-run for new coordinates
            else: # Check if the fruit was generated on any of the body elements
                for element in self.snake:
                    if self.r == element.r and self.c == element.c:
                        self.get_random_coordinates() # Re-run for new coordinates
            self.choice = random.choice(["apple", "banana"]) # Randomly choose which fruit to display and save it
            self.fruit = Fruit(self.choice, self.colors[self.choice])
            self.fruit_visible = False # Set fruit visibility to false to prevent function from running all over again
    
    def display_fruit(self):
        if self.snake.alive == True: # Check if the snake is "alive"
            self.get_random_coordinates() # Get randomly generated coordinates
            image(self.fruit.img, self.c * TILE_WIDTH, self.r * TILE_HEIGHT) # Display the image of the fruit
        
    def eat_fruit(self):
        if self.snake.r == self.r and self.snake.c == self.c: # WE check if snake head coordinates coincide with fruit coordinates
            self.score += 1 # Increases score by 1 
            clr = self.colors[self.choice] # Store the color of the fruit that was eaten
            self.snake.add_element(clr) # Snake increases in length by 1 
            self.fruit_visible = True # Ensures generating new coordinates for next fruit
            # New coordinates are generated and corrwsponding fruit is displayed
            self.get_random_coordinates() 
            self.display_fruit()
        
   
    
    def determine_win(self):
        if len(self.snake) == 399: # Checks if the snake becomes length of 399 because head is not included snake list 
            # Sets speed to zero, snake stops moving
            self.snake.vx = 0
            self.snake.vy = 0
            self.fruit_visible = False 
            self.snake.alive = False # Updates that snake no longer moves 
            noLoop() 
            background(203)
            fill(0, 0, 0)  # Set text color to black
            textSize(50)  # Set text size
            text("Congrats, You Won!", 70, 300)
            return    
        
    def reset_game(self):
        # Reset game to initial conditions
        self.snake = Snake(NUM_COLS // 2, NUM_ROWS //2)
        self.fruit_visible = True
        self.score = 0
        self.snake.vx = 1
        self.snake.vy = 1
        loop()
            
        
        
def setup():
    size(RESOLUTION, RESOLUTION) # Define canvas size
    background(203)


game = Game() # Initialize game instance


def draw():

    
    if frameCount <= 180:
        background(203)
        fill(0, 0, 0)  # Set text color to black
        textSize(17)  # Set text size
        text("Waiting to start... ", 240, 280)
        return
    fill(203)

    game.determine_win()
    if frameCount % 12 == 0:
        
        game.snake.allow_dir_change = True
        
        background(203)
    
        # for row in range(NUM_ROWS):
        #     for col in range(NUM_COLS):
        #         if (row + col) % 2 == 0:
        #             noStroke()
        #             fill(205, 205, 205)
        #         else:
        #             noStroke()
        #             fill(210, 210, 210)
        #         rect(col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    
        game.snake.move()
        game.eat_fruit()
        game.display_fruit()
        game.snake.display()
            
    
        




        
def keyPressed():
    # Update snake's direction based on arrow key presses
    if keyCode != LEFT and keyCode != RIGHT and keyCode != DOWN and keyCode != UP:
        return  # Ignore non-directional keys
    game.snake.set_direction(keyCode)
    
def mouseClicked(): # Restart game on mouse click if the game has ended
    if game.snake.alive == False:  # Check if game has stopped
        game.reset_game() 


    
    
