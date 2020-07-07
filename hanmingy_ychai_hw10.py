#Albert Yang, Lynn Chai, Assignment 10, November 26th

'''
Cool Stuff Done:
1. Add a restart. Typing a certain key or clicking the mouse resets everything. [1 pt]
2. Detect when the board has been cleared and do something celebratory (messages, sounds, graphics, etc…). [2 pts]
3. Keep score and display the score somewhere on screen. [2 pts]
4. Vary the velocity when bouncing off of anything. Maybe even add some small random factor. [1 pts]
5. Add sound for the hits (dig around in the source code for middsound to see how you could do that). [3 pts]
6. Vary the ball velocity when bouncing off the paddle. This could be based on where on the paddle the ball strikes or you could impart some velocity if the paddle is moving. [2 pts]
'''

#################################################################################################################################
####  I changed the play function in middsound so that "player.wait_done()" does not get called in play(self) anymore       #####
#################################################################################################################################
####  sound playing may lag on the very first collision, but after the first collision the sound plays without lag at all   #####
#################################################################################################################################


import middsound #Using sound
import turtle  # Using Turtle and Screen classes
import random  # Using randint
import time #Using Sleep 
import math


def append_tone(snd, frq, duration):
    """
    from lab 7, play sounds
    """
    
    num_samples = int(duration * snd.framerate)
    for i in range(0, num_samples):
        sample = int(math.sin(2*math.pi*frq*(i/snd.framerate))*middsound.MAXVALUE)
        snd.append(sample)
    return snd

sound = middsound.new()
append_tone(sound, 420, 0.05)


class Ball:
    
    """
    A class representing a ball on the screen
    
    Attributes
    ----------
    t : turtle
        A turtle type object from the module turtle
    radius : float
        The radius of the ball
    x : float
        The x coordinate of the ball
    y : float
        The y coordinate of the ball
    vx : float
        The x component of the ball velocity
    vy : float
        The y component of the ball velocity
    velocity : list
        The x and y components of the velocity of the ball
    color : string
        The color of the ball
    
    Methods
    -------
    update()
        Update the ball location and check if the ball should bounce off the window edges
    collide_with_rect()
        Check if this ball is colliding with another ball
    draw()
        Draw the ball on the screen
    """
    
    def __init__(self, t, x , y , radius, vx, vy, color):
        
        """
        Parameters
        ----------
        t : turtle
            A turtle type object from the module turtle
        radius : float
            The radius of the ball
        x : float
            The x coordinate of the ball
        y : float
            The y coordinate of the ball
        vx : float
            The x component of the ball velocity
        vy : float
            The y component of the ball velocity
        velocity : list
            The x and y components of the velocity of the ball
        color : string
            The color of the ball
        """
        
        self.turtle = t
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = [vx, vy]
        self.color = color
    
    
    def draw(self):
        
        """
        Draw the ball on the screen
        """
        
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.dot(self.radius * 2, self.color)
        
        
    def update(self, bricklist, paddle_x, paddle_width):
        
        """
        Update the ball status:
        - Check if the ball should bounce off the window edges
        - Update position using the velocity
        """
        
        # Acquire the screen instance from the turtle
        screen = turtle.Screen()
        
        # Store current screen properties
        width = screen.window_width() 
        height = screen.window_height()
        
        # Check for screen boundaries
        if (self.x - self.radius <= -width//2) or(self.x + self.radius >= width//2):
            sound.play()
            self.velocity[0] *= -1 - (random.randint(0, 5)/400)
        if (self.y + self.radius >= height//2):
            sound.play()
            self.velocity[1] *= -1 - (random.randint(0, 5)/400)
        
        #the ball responds to the sides that were hit. side was returned by collide_with_rect() call in run()
        if self.touched != []:
            sound.play()
            if 't' in self.touched:
                self.velocity[1] *= -1 -(random.randint(0, 5)/400)
                #the player is rewarded for catching the ball with the middle of the paddle
                self.velocity[0] *= 1 + 0.1*(abs((self.x - (paddle_x + paddle_width//2)))/(paddle_width//2))
                self.velocity[1] *= 1 + 0.1*(abs((self.x - (paddle_x + paddle_width//2)))/(paddle_width//2))
            if 'b' in self.touched:
                self.velocity[1] *= -1 -(random.randint(0, 5)/400)
            if 'l' in self.touched:
                self.velocity[0] *= -1 -(random.randint(0, 5)/400)
            if 'r' in self.touched:
                self.velocity[0] *= -1 -(random.randint(0, 5)/400)
        
        #master list that stores the collisions of all bricks with ball
        self.masterList = []
        
        #adds all collisions in one frame into masterList[]
        for i in bricklist:
            if i.visible == True:
                self.collide_with_rect(i)
                if self.touched != []:
                    sound.play()
                    self.masterList.extend(self.touched)
                    i.visible = False

        #checks what sides are hit and makes the ball respond
        if 't' in self.masterList or 'b' in self.masterList:
            self.velocity[1] *= -1 -(random.randint(0, 5)/400)
        if 'l' in self.masterList or 'r' in self.masterList:
            self.velocity[0] *= -1 -(random.randint(0, 5)/400)
                           
        # Update position with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        

                        
                        
    def collide_with_rect(self, rect):
        
        """
        Check if this ball is colliding with another ball
        
        Parameters
        ----------
        other : ball
            Another ball to be checked for collision
        """
        
        #list that stores what sides the ball has touched in the rect
        self.touched = []
        
        #used to determine wether a side was hit
        before = [self.x - self.velocity[0], self.y - self.velocity[1]]
        now = [self.x, self.y]
        
        #determines wether each side was hit. self.radius//2 was added or subtracted to make determination more accurate
        if before[1] >= rect.y + self.radius//2 >= now[1]: 
            if rect.x - self.radius//2 < self.x <rect.x+ rect.width + self.radius//2: 
                self.touched.append('t')
        
        if now[1] >= rect.y - rect.height - self.radius//2>= before[1]:
            if rect.x - self.radius//2 < self.x <rect.x+ rect.width + self.radius//2: 
                self.touched.append('b')
        
        if now[0] >= rect.x - self.radius//2 >= before[0]: 
            if rect.y - rect.height - self.radius//2< self.y <rect.y+self.radius//2: 
                self.touched.append('l')
                
        if before[0] >= rect.x + rect.width + self.radius//2 >= now[0]: 
            if rect.y - rect.height - self.radius//2 < self.y <rect.y + self.radius//2: 
                self.touched.append('r')
        
class Paddle:
    
    """
    A class representing a paddle on the screen
    
    Attributes
    ----------
    turtle : Turtle 
        A Turtle type object from the module turtle
    width: float
        The width of the paddle
    height: float
        The height of the paddle
    color : string
        The color of the paddle
        
    Methods
    ----------
    update()
        Update the paddle location based on the mouse location 
    draw()
        Draw the ball on the screen
    """
    
    def __init__(self, t, width, height, color):
        
        """
        Parameters
        ----------
        t : turtle
            A turtle type object from the module turtle
        width: float
            The width of the paddle
        height: float
            The height of the paddle
        color : string
            The color of the paddle
        """
        
        self.turtle = t
        self.width = width
        self.height = height
        self.color = color
        self.x = 0
        self.y = 0
    
    def update(self):
        
        """
        Update the position of the paddle based on the mouse location
        
        """
        
        # Acquire the screen instance from the turtle
        screen = turtle.Screen()
        
        # Store current screen properties
        width = screen.window_width() 
        height = screen.window_height()
        
        #x follows cursor, y is fixed
        self.x = turtle.getcanvas().winfo_pointerx() - turtle.getcanvas().winfo_rootx() -580
        self.y = -height//2 + 50
    
    
    def draw(self):
        
        """
        draw the paddle on the screen
        """
        
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.fillcolor(self.color)
        self.turtle.begin_fill()
        self.turtle.setheading(0)
        self.turtle.forward(self.width)
        self.turtle.right(90)
        self.turtle.forward(self.height)
        self.turtle.right(90)
        self.turtle.forward(self.width)
        self.turtle.right(90)
        self.turtle.forward(self.height)
        self.turtle.end_fill()
    
    

class Brick:
    
    """
    A class representing the bricks on the screen
    
    Attributes
    ----------
    turtle : Turtle 
        A Turtle type object from the module turtle
    width : float
        The width of the brick
    height : float
        The height of the brick
    color : string
        The color of the brick
    visible : boolean
        Whether the brick is visible or not, brick disappers after the ball touches
    x: float
        The x coordinate of the brick
    y: float
        The y coordinate of the brick
        
    Methods
    ----------
    draw()
        Draw the bricks on the screen
    """
    
    def __init__(self, t, width, height, color):
        
        """storing Brick attributes"""
        
        self.turtle = t
        self.width = width
        self. height = height
        self.color = color
        self.visible = True
        self.x = 0
        self.y = 0
    
    
    def draw(self):
        
        """draws brick only when visible"""
        
        if self.visible == True:
            self.turtle.pendown()
            self.turtle.fillcolor(self.color)
            self.turtle.begin_fill()
            self.turtle.setheading(0)
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.right(90)
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.end_fill()
            self.turtle.penup()
                


class Game:
    
    """
    A class implementing the game
    
    Attributes
    ----------
    screen : Screen
        A Screen type object from the module turtle
    turtle : Turtle
        A Turtle type object from the module turtle
        
    
    Methods
    -------
    initialize_objs()
        Create the gamefield by adding the paddle, the bricks, and the ball
    run()
        Determines the game dynamic frame by frame (one frame for each call)
    done()
        Exit the program
        
    """
    
    def __init__(self):
        
        """
        Attributes
        ----------
        screen : Screen
            A Screen type object from the module turtle
        turtle : Turtle
            A Turtle type object from the module turtle
        """
        
        # Create a screen object (singleton) and set it up
        self.screen = turtle.Screen()
        self.screen.setup(0.5, 0.5)  # Use half with and half height of your current screen
        self.screen.tracer(False)
        self.screen.colormode(255)
        
        # Create an invisible turtle object
        self.turtle = turtle.Turtle(visible=False)
        
        # Initialize the scene
        self.initialize_objs()
    
        # Defines users' interactions we should listen for
        self.screen.onkey(self.done, 'q') # Check if user pushed 'q'
        self.screen.onkey(self.run and self.initialize_objs, 'r')
        
        # As soon as the event loop is running, set up to call the self.run() method
        self.screen.ontimer(self.run, 0)
    
        # Tell the turtle screen to listen to the users' interactions
        self.screen.listen()
        
        # Start the event loop
        self.screen.mainloop()
        
    def initialize_objs(self):
        """
        Initializes the scene
        """

        # Defines the size of the game field       
        width = self.screen.window_width() - 100
        height = self.screen.window_height()
        
        #variables used to initailize rows of bricks
        x = -width//2
        y = height//2 - 50
        
        #list of Brick objects
        self.bricks = []
        
        #customize bricks
        b_in_row = 3
        h_of_b = 10
        rows_of_b = 4
        
        #initializes bricks with their coordinates
        for u in range(rows_of_b):
            
            for _ in range(b_in_row):
                brick = Brick(self.turtle, width//b_in_row, height//h_of_b, (random.randint(0, 255), random.randint(0, 255),  random.randint(0, 255)))
                brick.x = x
                brick.y = y
                x += brick.width
                self.bricks.append(brick)
            x = -width//2
            y -= height//10
            
            
        #initializes paddle
        self.paddle = Paddle(self.turtle, 200, 30, (random.randint(0, 255), random.randint(0, 255),  random.randint(0, 255)))
        #initializes ball
        self.pong = Ball(self.turtle, 0, -50 , 10, 4, -1, (random.randint(0, 100), random.randint(0, 100),  random.randint(0, 100)))               # color: blue
        
        
    def run(self):
        """
        Determines the game dynamic frame by frame (one frame for each call)
        """
        # Acquire the screen instance from the turtle
        screen = turtle.Screen()
        
        # Store current screen properties
        width = screen.window_width() 
        height = screen.window_height()
        # Clear the screen
        self.turtle.clear()
        
        #draws bricks
        for i in self.bricks:
            self.turtle.penup()
            self.turtle.goto(i.x, i.y)
            self.turtle.pendown()
            i.draw()
        
        #cool stuff 3, celebrates when all bricks are invisible
        if all(brick.visible == False for brick in self.bricks):
            self.turtle.penup()
            self.turtle.goto(-265,-30)
            self.turtle.pendown()
            self.turtle.write('(= !YOU WIN! =)', font= ("Consolas", 40, "normal"))
            time.sleep(2)
            self.done()

        #procedures of actual game
            
        self.paddle.update()
        self.paddle.draw()
    
        self.pong.collide_with_rect(self.paddle)
        
        self.pong.draw()
        self.pong.update(self.bricks, self.paddle.x, self.paddle.width)
        
        score= sum(1 for i in self.bricks if i.visible == False)
        
        self.turtle.penup()
        self.turtle.goto(width//2 -90,-height//2+50)
        self.turtle.pendown()
        self.turtle.write(score, font= ("Consolas", 40, "normal"))
        

        # Update the overall screen
        self.screen.update()
        
        # Call the self.run() method when the ball isnt at the bottom
        if (-self.pong.y + self.pong.radius < height//2):
            self.screen.ontimer(self.run, 0)
        else:
            self.turtle.penup()
            self.turtle.goto(-290,-30)
            self.turtle.pendown()
            self.turtle.write('(= !Nice Try! =)', font= ("Consolas", 40, "normal"))
            time.sleep(2)
            self.done()
        
    def done(self):
        """
        Exit the program
        """
        self.screen.bye()


# Runs the Game
scene = Game()



