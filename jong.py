#Credits to Tech with Tim for their tutorial. Hoping to learn something from this.

import pygame
pygame.init()
pygame_icon = pygame.image.load('resources/icon.ico')
pygame.display.set_icon(pygame_icon)


boopsound = pygame.mixer.Sound("sounds/boop.ogg")
winsound = pygame.mixer.Sound("sounds/win.ogg")

#Window size
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption("Jong")

#Max framerate
FPS = 60

#RGB Coloring
WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5


class Paddle: #Controls how paddles render and control
    COLOR = WHITE
    VEL = 12

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    
    def move(self, up=True): #Moves paddles up and down
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        
class Ball: #Defines the ball.
    MAX_VEL = 8
    COLOR = WHITE

    def __init__(self, x, y, radius): #Ball size and max speed
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win): #Draws the ball
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self): 
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x 
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1



def draw(win, paddles, ball, left_score, right_score): #Determines how shit's drawn
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH// 4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * 3/4 - right_score_text.get_width()//2, 20))





    for paddle in paddles: #Updates the paddles
        paddle.draw(win)

    for i in range (10, HEIGHT, HEIGHT//20): #Dashed line in the center
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle): #Collision math oh dear fucking god
    #Makes ball bounce off floor and celing
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
        pygame.mixer.Sound.play(boopsound)
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        pygame.mixer.Sound.play(boopsound)

    #Makes ball bounce off paddles
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                pygame.mixer.Sound.play(boopsound)


    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
                pygame.mixer.Sound.play(boopsound)
        

def handle_paddle_movement(keys, left_paddle, right_paddle): #Handles paddle movements
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:     #LeftPaddleMovement
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:  #RightPaddleMovement
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)



def main():
    run = True
    clock = pygame.time.Clock()  #Locks FPS 

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) #Left paddle size
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) #Right paddle size

    left_score = 0
    right_score = 0

    while run: #Updates every frame
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) #Draws everything

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed() 
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0: #Resets ball position and adds to score when balls go off sides
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score +=1
            ball.reset()

        won = False #Checks to see whoever gets the winning score first
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left wins!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right wins!"

        if won: #Resets game when someone wins.
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.mixer.Sound.play(winsound)
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
    