import turtle
import random
import time
import sys
import math
from datetime import datetime


wn = turtle.Screen()
wn.mode("standard")
wn.colormode(255)
wn.bgcolor(255, 255, 255)
wn.title("Fly in a Jar")


duration = 9000
left = 45.0
right = 45.0
units = 30.0

sam = turtle.Turtle()
sam.pencolor(187, 187, 187)
sam.speed(0)
sam.ht()
sam.pensize(1)

joe = turtle.Turtle()
joe.pencolor(20, 20, 20)
joe.speed(0)
joe.ht()
joe.pensize(1)

x_high = 1000.0
x_low = -1000.0
y_high = 350.0
y_low = -350.0

boundary = (
            (x_low, y_high),
            (x_high, y_high),
            (x_high, y_low),
            (x_low, y_low))

dt_string = datetime.now().strftime("%d-%m-%Y_%H%M%S")



def get_random():
    """
    Returns either 0 or 1 to determine whether turtle makes
    a left or right turn.
    """
    m = random.randint(1,101)%2
    return m


def reverse_heading(z):
    """
    Reverse direction by 180 degrees to keep turtle within
    boundary.
    """
    return (z + 180) % 360


def color_choice(count):
    """
    Changes rgb values to change pen color
    """
    #color1 = (45, 45, 46)
    #color2 = (57, 57, 64)
    color3 = (57, 57, 74)
    color4 = (62, 62, 118)
    color5 = (93, 62, 118)
    color1 = (187, 187, 187)
    color2 = (0, 115, 177)

    if 0 <= count <= 2000:
        color = color1
    elif 2001 <= count <= 4000:
         color = color2
    elif 4001 <= count <= 6000:
         color = color1
    elif 6001 <= count <= 8000:
         color = color2
    elif 8001 <= count <= 9000:
         color = color1
    return color


def redirect_to_file(log):
    """
    Redirect coordinates to a log
    """
    original = sys.stdout
    sys.stdout = open('log.txt', 'a')
    print(log)
    sys.stdout = original


def next_coordinates(distance, heading, position):
    """
    Return next coordinates based on given distance,
    current heading, and current x, y
    new_x = cosine(degree in radians) * distance + original x coordinates
    """
    x = math.cos(math.radians(heading)) * distance + position[0]
    y = math.sin(math.radians(heading)) * distance + position[1]
    return x, y


def create_obstacles():
    circle = (-600, 0, 150)
    return circle


def check_obstacle(x, y):
    """
    take next expected coordinates and check if they are within a circle
    """
    circle = create_obstacles()
    num = ((x - circle[0])**2) + ((y - circle[1])**2)
    if num <= circle[2]**2:
        return circle

def find_distance(a_xy, b_xy):
    """
    Requires two pairs of coordinates. Find and return distance 
    between two points.
    """
    x1 = a_xy[0]
    y1 = a_xy[1]
    x2 = b_xy[0]
    y2 = b_xy[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def heading_360(heading):
    """
    Returns a heading within 0-360 degrees
    """
    if heading >= 360:
        heading -= 360
    if heading < 0:
        heading += 360
    return heading


def cosine_o_angle(hypotenuse, adjacent, opposite):
    """
    Returns all angles of a triangle where length of all three sides is know. 
    We only need angle opposite of radius (cos_o) for setting the heading to tangent point on circle. 
    """
    h = hypotenuse
    o = opposite
    a = adjacent
    cos_o = math.degrees(math.acos((h**2 + a**2 - o**2) / (2*h*a)))
    cos_a = math.degrees(math.acos((h**2 + o**2 - a**2) / (2*h*o)))
    cos_h = math.degrees(math.acos((o**2 + a**2 - h**2) / (2*o*a)))
    return (cos_o, cos_a, cos_h)


def find_leg(distance, radius):
    """
    Find leg of right angle to get point of tangent
    """
    leg = 0
    if distance >= radius:
        leg = math.sqrt(distance**2 - radius**2)
    return leg


def main():
    last_pos = sam.pos()
    n = 1
    while n <= duration:
        m = get_random()
        pos = sam.pos()
        x = pos[0]
        y = pos[1]
        z = int(sam.heading())
        sam.pencolor(color_choice(n))
        if m == 0:
            sam.left(left)
        elif m == 1:
            sam.right(right)
        next_x, next_y = next_coordinates(units, sam.heading(), sam.pos())
        obstacle = check_obstacle(next_x, next_y)
        if (
            (x_low+units) <= x <= (x_high-units) and
            (y_low+units) <= y <= (y_high-units)
        ):
                if obstacle:
                    distance = find_distance((sam.xcor(), sam.ycor()), obstacle)
                    adjacent = find_leg(distance, obstacle[2])
                    if adjacent > 0:
                        cos_angles = cosine_o_angle(distance, adjacent, obstacle[2])
                        cos_o = cos_angles[0]
                        center_heading = sam.towards(obstacle[0], obstacle[1])
                        heading_right = heading_360(center_heading - cos_o)
                        heading_left = heading_360(center_heading + cos_o)
                        pos = sam.pos()
                        l_pos = next_coordinates(adjacent, heading_left, pos)
                        r_pos = next_coordinates(adjacent, heading_right, pos)
                        l_length = find_distance(last_pos, l_pos)
                        r_length = find_distance(last_pos, r_pos)
                        if r_length > l_length:
                            heading = heading_right
                        else:
                            heading = heading_left
                        sam.setheading(heading)
                        sam.forward(adjacent)
                else:
                    sam.forward(units)
        else:
            sam.setheading(reverse_heading(z))
            sam.forward(units)
        n += 1
        last_pos = pos
        # redirect_to_file(x,y,z)

    wn.getcanvas().postscript(file='%s.eps' % dt_string)
    wn.exitonclick()



if __name__ == "__main__":
    main()
