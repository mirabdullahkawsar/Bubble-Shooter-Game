from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

shooter_x = 400
shooter_y = 50
shooter_radius = 20
fire_radius = 10
fire_speed = 5
lives = 3
score = 0
miss_fire = 0
paused = False
game_over = False
misfires = 0 
fires = []
falling_circles = []
shooter_color = (1.0, 1.0, 0.0)
reset_button = (10, 680, 100, 710) 
pause_button = (120, 680, 200, 710)
exit_button = (210, 680, 300, 710)

def draw_points(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy < 0:
            return 7
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx >= 0 and dy < 0:
            return 6
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5

def convert_to_zone_0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone_0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone_0(zone, x1, y1)
    x2, y2 = convert_to_zone_0(zone, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x, y = x1, y1
    while x <= x2:
        px, py = convert_from_zone_0(zone, x, y)
        draw_points(px, py)
        if d > 0:
            y += 1
            d += dNE
        else:
            d += dE
        x += 1

def midpoint_circle(cx, cy, r):
    x = 0
    y = r
    d = 1 - r
    draw_circle_points(cx, cy, x, y)

    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        draw_circle_points(cx, cy, x, y)

def draw_circle_points(cx, cy, x, y):
    draw_points(cx + x, cy + y)
    draw_points(cx - x, cy + y)
    draw_points(cx + x, cy - y)
    draw_points(cx - x, cy - y)
    draw_points(cx + y, cy + x)
    draw_points(cx - y, cy + x)
    draw_points(cx + y, cy - x)
    draw_points(cx - y, cy - x)


def shooter():
    glColor3f(*shooter_color)   
    midpoint_line(shooter_x - 10, shooter_y - 20, shooter_x - 10, shooter_y + 20) 
    midpoint_line(shooter_x + 10, shooter_y - 20, shooter_x + 10, shooter_y + 20)  
    midpoint_line(shooter_x - 10, shooter_y + 20, shooter_x + 10, shooter_y + 20)  
    midpoint_line(shooter_x - 10, shooter_y - 20, shooter_x + 10, shooter_y - 20)     
    midpoint_line(shooter_x - 10, shooter_y + 20, shooter_x, shooter_y + 40)  
    midpoint_line(shooter_x + 10, shooter_y + 20, shooter_x, shooter_y + 40)    
    glColor3f(1.0, 0.0, 0.0)  
    midpoint_line(shooter_x - 10, shooter_y - 20, shooter_x - 20, shooter_y - 30) 
    midpoint_line(shooter_x - 20, shooter_y - 30, shooter_x - 10, shooter_y - 30)  
    midpoint_line(shooter_x + 10, shooter_y - 20, shooter_x + 20, shooter_y - 30)  
    midpoint_line(shooter_x + 20, shooter_y - 30, shooter_x + 10, shooter_y - 30)  

def draw_fire(fire_x, fire_y):
    glColor3f(1.0, 0.0, 0.0)
    midpoint_circle(fire_x, fire_y, fire_radius)

def draw_falling_circle(circle):
    x, y, r, color = circle
    glColor3f(*color)
    midpoint_circle(x, y, r)

def draw_buttons():  
    draw_button(reset_button, "<", (.6, 0.4, 1.0))
    draw_button(pause_button, "| |", (0., 1.0, 0.0))
    draw_button(exit_button, "X", (1.0, 0.0, 0.0))

def draw_button(button, text, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(button[0], button[1])
    glVertex2f(button[2], button[1])
    glVertex2f(button[2], button[3])
    glVertex2f(button[0], button[3])
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(button[0] + 5, button[1] + 15) 
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def check_button_click(x, y):
    global paused, score, lives, fires, falling_circles, game_over
    if reset_button[0] <= x <= reset_button[2] and reset_button[1] <= y <= reset_button[3]:
        score = 0
        lives = 3
        fires.clear()
        falling_circles.clear()
        game_over = False
        paused = False
        return True
    if pause_button[0] <= x <= pause_button[2] and pause_button[1] <= y <= pause_button[3]:
        paused = not paused
        return True
    if exit_button[0] <= x <= exit_button[2] and exit_button[1] <= y <= exit_button[3]:
        glutLeaveMainLoop()  
        return True

    return False

def mouse(button, state, x, y):
    if state == GLUT_DOWN:
        check_button_click(x, 750 - y)  
    glutPostRedisplay()

def update_game(value):
    global fires, falling_circles, score, lives, game_over, misfires

    if paused or game_over:
        glutTimerFunc(16, update_game, 0)
        return

    for fire in fires:
        fire['y'] += fire_speed
    missed_fires = [fire for fire in fires if fire['y'] - fire_radius > 800]
    fires = [fire for fire in fires if fire['y'] - fire_radius <= 800]

    misfires += len(missed_fires)

    if misfires >= 3:
        game_over = True
        print(f"G a m e O v e r! You missed 3 shots! Focus on aim Fighter. Final Score: {score}")

    for circle in falling_circles:
        circle[1] -= 2

    for fire in fires:
        fx, fy = fire['x'], fire['y']
        for circle in falling_circles:
            cx, cy, cr, _ = circle
            if (fx - cx) ** 2 + (fy - cy) ** 2 <= (fire_radius + cr) ** 2:
                score += 1
                fires.remove(fire)
                falling_circles.remove(circle)
                break

    for circle in falling_circles:
        if circle[1] - circle[2] <= 0:
            lives -= 1
            falling_circles.remove(circle)
            if lives == 0:
                game_over = True
                print(f"G a m e  O v e r! Final Score: {score}")

    glutPostRedisplay()
    glutTimerFunc(16, update_game, 0)


def add_falling_circle(value):
    if not paused and not game_over:
        x = random.randint(20, 780)
        y = 750
        r = random.randint(15, 40)
        color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
        falling_circles.append([x, y, r, color])

    glutTimerFunc(1500, add_falling_circle, 0)

def keyboard(key, x, y):
    global shooter_x, fires

    if game_over or paused:
        return

    if key == b'a':
        shooter_x = max(shooter_radius, shooter_x - 15)
    elif key == b'd':
        shooter_x = min(800 - shooter_radius, shooter_x + 15)
    elif key == b' ':
        fires.append({'x': shooter_x, 'y': shooter_y + shooter_radius})

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    shooter()

    for fire in fires:
        draw_fire(fire['x'], fire['y'])

    for circle in falling_circles:
        draw_falling_circle(circle)

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, 730)
    for char in f"Score: {score} Lives: {lives}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    if game_over:
        glRasterPos2f(350, 375)
        for char in "G A M E  O V E R !":
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    draw_buttons() 

    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glOrtho(0, 800, 0, 750, -1, 1)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(800, 750)
glutCreateWindow(b"HIT THE BALL")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse) 
glutTimerFunc(0, update_game, 0)
glutTimerFunc(0, add_falling_circle, 0)
glutMainLoop()
