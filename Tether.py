import turtle
import random
import math
import time

# Setup screen 
screen = turtle.Screen()
screen.title("Tether Probe Deorbit Simulation — Full Orbit View")
screen.bgcolor("black")
screen.setup(width=1000, height=900)
screen.tracer(0)

# Draw Earth 
earth = turtle.Turtle()
earth.penup()
earth.hideturtle()
earth.goto(0, -420)
earth.color("royalblue")
earth.begin_fill()
earth.circle(200)
earth.end_fill()

# Probe setup
probe = turtle.Turtle()
probe.shape("circle")
probe.color("deepskyblue")
probe.shapesize(1.5)
probe.penup()
probe.goto(0, 300) 

# Tether setup 
tether = turtle.Turtle()
tether.color("cyan")
tether.pensize(3)
tether.hideturtle()

# Debris setup 
debris_list = []
num_debris = 12

for _ in range(num_debris):
    d = turtle.Turtle()
    d.shape("circle")
    d.color("red")
    d.shapesize(0.6)
    d.penup()
  
    d.goto(-520, random.randint(-50, 380))
    d.dx = random.uniform(1.8, 2.4)
    d.dy = random.uniform(-0.15, 0.15)
    d.slowed = False
    d.falling = False
    d.fall_speed = 0
    debris_list.append(d)

# Text display
counter = turtle.Turtle()
counter.hideturtle()
counter.penup()
counter.color("white")
counter.goto(-470, 410)
collected = 0


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Main animation loop
while True:
    screen.update()
    counter.clear()
    counter.write(f"Debris Collected: {collected}", font=("Arial", 16, "bold"))

    tether.clear()
    tether.penup()
    tether.goto(probe.xcor(), probe.ycor())
    tether.pendown()
    tether.goto(probe.xcor(), probe.ycor() - 180)

    # Move debris
    for d in debris_list:
        if not d.isvisible():
            continue

        if d.falling:
            d.fall_speed += 0.02 
            d.sety(d.ycor() - d.fall_speed)
            d.setx(d.xcor() + 0.5 * math.sin(d.ycor() / 80))  
            if d.ycor() < -240:  
                d.hideturtle()
                collected += 1
            continue

        # Normal orbital flight
        d.setx(d.xcor() + d.dx)
        d.sety(d.ycor() + math.sin(d.xcor() / 100))  

        # Respawn when leaving right side
        if d.xcor() > 520:
            d.goto(-520, random.randint(-50, 380))
            d.dx = random.uniform(1.8, 2.4)
            d.dy = random.uniform(-0.15, 0.15)
            d.color("red")
            d.slowed = False
            d.falling = False
            d.fall_speed = 0

        # Check proximity to tether 
        px, py = probe.xcor(), probe.ycor()
        tx, ty = px, py - 180
        if px - 12 < d.xcor() < px + 12 and ty < d.ycor() < py:
            if not d.slowed:
                d.color("orange")
                d.dx *= 0.5
                d.dy *= 0.5
                d.slowed = True

        if d.slowed:
            d.dy -= 0.01 
            d.sety(d.ycor() + d.dy)
            if d.dy < -1.5 or random.random() < 0.005:
                d.falling = True
                d.fall_speed = 0.5

    time.sleep(0.02)
