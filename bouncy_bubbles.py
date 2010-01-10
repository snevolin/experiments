#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

"""
 * Bouncy Bubbles. 
 * Based on code from Keith Peters (www.bit-101.com). 
 * 
 * Multiple-object collision.
  
 Ported from processing (http://processing.org/).
 Also added mass to the ball that is equal to the radius.
"""
 
import gtk
from lib import graphics
from lib.pytweener import Easing

import math
from random import randint


SPRING = 0.05;
GRAVITY = 0.03;
FRICTION = -0.9;


class Ball(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius

        # just for kicks add mass, so bigger balls would not bounce as easy as little ones
        self.mass = float(self.radius) * 2  
        self.color = color
        
        # velocity
        self.vx = 0
        self.vy = 0
    
    def draw(self, area):
        area.set_color(self.color, 0.8)
        area.context.arc(self.x, self.y, self.radius, 0, 2.0 * math.pi)
        area.context.fill()
        
    def move(self, area_dimensions):
        width, height = area_dimensions
        
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        
        radius = self.radius
        
        # bounce of the walls
        if self.x - radius < 0 or self.x + radius > width:
            self.vx = self.vx * FRICTION
            
        if self.y - radius < 0 or self.y + radius > height:
            self.vy = self.vy * FRICTION

        self.x = max(radius, min(self.x, width - radius))
        self.y = max(radius, min(self.y, height - radius))
        

    def colide(self, others):
        for ball in others:
            if ball == self:
                continue
            
            dx = ball.x - self.x
            dy = ball.y - self.y
            
            # we are using square as root is bit expensive
            min_distance = (self.radius + ball.radius) ** 2
            
            if (dx ** 2 + dy ** 2) < min_distance:
                min_distance = self.radius + ball.radius
                angle = math.atan2(dy, dx)
                target_x = self.x + math.cos(angle) * min_distance
                target_y = self.y + math.sin(angle) * min_distance
                
                ax = (target_x - ball.x) * SPRING
                ay = (target_y - ball.y) * SPRING

                mass_ratio = self.mass / ball.mass
                
                self.vx -= ax / mass_ratio
                self.vy -= ay / mass_ratio
                
                # repulse
                ball.vx += ax * mass_ratio
                ball.vy += ay * mass_ratio
            

class Canvas(graphics.Area):
    def __init__(self):
        graphics.Area.__init__(self)
        self.balls = []
        self.window_pos = None
    
        
    def on_expose(self):
        if not self.balls:
            for i in range(15):
                radius = randint(10, 30)
                self.balls.append(Ball(randint(radius, self.width - radius),
                                       randint(radius, self.height - radius),
                                       radius,
                                       "#aaaaaa"))
        
        # on expose is called when we are ready to draw
        for ball in self.balls:
            ball.move((self.width, self.height))
            ball.colide(self.balls)
            ball.draw(self)

        window_pos = self.get_toplevel().get_position()
        if self.window_pos and window_pos != self.window_pos:
            dx = window_pos[0] - self.window_pos[0]
            dy = window_pos[1] - self.window_pos[1]
            for ball in self.balls:
                ball.x -= dx
                ball.y -= dy
        self.window_pos = window_pos
            
        self.redraw_canvas()


class BasicWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Graphics Module")
        window.set_size_request(600, 200)
        window.connect("delete_event", lambda *args: gtk.main_quit())
    
        canvas = Canvas()
        
        box = gtk.VBox()
        box.pack_start(canvas)
        
    
        window.add(box)
        window.show_all()
        
        
if __name__ == "__main__":
    example = BasicWindow()
    gtk.main()
