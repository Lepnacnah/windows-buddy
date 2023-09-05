import tkinter as tk
import desktop
from PIL import Image, ImageTk
from screeninfo import get_monitors
import random

SF = 3 #scale factor for the image


class character:
    def __init__(self, cycles, window, label):
        self.monitors = get_monitors()
        self.cycles = cycles
        self.window = window
        self.anim_delta = 0
        self.move_delta = 0
        self.label = label
        self.anim_speed = 125
        self.move_speed = 16
        self.dir = 1
        self.cycle = 1
        self.f_cycles = self.make_flipped()
        self.xv = 0
        self.yv = 0
        self.x = 2000
        self.x_accel = 0.2
        self.looking = False
        self.y = self.get_floor() - 500
        self.target = (-500, self.get_floor())
        self.max_velocity = (15, 50)

        self.setupWindow()
    
    def setupWindow(self):
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor','black')
        self.window.attributes('-topmost',True)
        self.window.geometry(f"{18*SF}x{18*SF}+{self.x}+{self.y}")
        self.label.configure(image=idle[0])
        self.label.pack()

        self.anim()
        self.move()
        self.window.mainloop()
    
    def make_flipped(self):
        f_cycles = []
        for cycle in self.cycles:
            f_cycle = []
            for frame in cycle:
                new_img = ImageTk.getimage(frame)
                flipped = new_img.transpose(Image.FLIP_LEFT_RIGHT)
                tk_image = ImageTk.PhotoImage(flipped)
                f_cycle.append(tk_image)
            f_cycles.append(f_cycle)
        return f_cycles
    
    def anim(self):
        self.anim_delta += 1
        if self.dir == 0:
            img = self.cycles[self.cycle][self.anim_delta%len(self.cycles[self.cycle])]
        else:
            img = self.f_cycles[self.cycle][self.anim_delta%len(self.f_cycles[self.cycle])]
        
        self.label.configure(image=img)
        self.label.photo = img
        self.window.after(self.anim_speed, self.anim)

    def move(self):
        self.move_delta += 1
        self.move_x()
        self.move_y()
        
        self.window.geometry(f"{18*SF}x{18*SF}+{int(self.x)}+{int(self.y)}")
        self.window.after(self.move_speed, self.move)
    
    def move_x(self):
        if abs(self.target[0] - self.x) > 10:
            #gotta speed
            self.cycle = 1
            if self.target[0] < self.x:
                self.xv = max(self.xv-self.x_accel, -self.max_velocity[0])
            else:
                self.xv =min(self.xv+self.x_accel, self.max_velocity[0])
            self.anim_speed = 125
        else:
            #we're chilling at our destination
            self.xv *= 0.7
            self.cycle = 0
            self.anim_speed = 150
            if not self.looking:
                self.looking = True
                self.new_target()
        self.dir = 0
        if self.xv < 0:
            self.dir = 1
        
        if abs(self.xv) > self.max_velocity[0] - self.max_velocity[0]/2:
            #Go super sayain
            self.cycle = 4
            self.anim_speed = 175
        self.x += self.xv

    def move_y(self):
        ground = self.get_floor()
        if self.y > ground:
            self.y = ground
            self.yv = 0
        elif self.y < ground:
            self.yv = min(self.yv + 0.3, self.max_velocity[1])
        self.y += self.yv

    def get_floor(self, x_pos = None):
        """get the floor height, the lowest point, 
        inc if multiple monitors are stacked on top of each other"""
        floors = []
        ref_x = self.x
        if x_pos != None:
            ref_x = x_pos
        for m in self.monitors:
            if ref_x > m.x and ref_x < m.x + m.width:
                floors.append(m.height + m.y)
        if len(floors) == 0:
            return self.y
        return min(floors) - (18*SF)
    
    def get_ceiling(self, y_pos = None):
        """get the height where the lil guy is still visible"""
        ceilings = []
        ref_x = self.x
        if y_pos != None:
            ref_x = y_pos
        for m in self.monitors:
            if ref_x > m.x and ref_x < m.x + m.width:
                ceilings.append(m.y)
        return max(ceilings) + (18*SF)
    
    def get_x_bounds(self, x_pos = None):
        """Get the edges of the screen(s) or when the lip is too high"""
        ground = self.get_floor(x_pos)
        lowest = 0
        highest = 0
        for m in self.monitors:
            if m.x < lowest and self.get_floor(m.x + 1) - ground < (SF * 16):
                lowest = m.x
            if m.x + m.width > highest and self.get_floor(m.x +1) - ground < (SF * 16):
                highest = m.x + m.width
        return (lowest + SF*18, highest - SF*18)
    
    def new_target(self, forced = False):
        """get a new target from the avaliable locations"""
        if random.randint(0, 30) == 1 or forced:
            b = self.get_x_bounds()
            point = random.randint(b[0], b[1])
            self.target = (point, self.get_floor(point))
            self.looking = False
        else:
            self.window.after(1000, self.new_target)
window = tk.Tk()
#initalize the gifs and the tk objects
idle = [tk.PhotoImage(file="assets\gifs\DinoSprites_tard.gif",format='gif -index %i' %(i)).zoom(SF,SF) for i in range(4)]
walk = [tk.PhotoImage(file="assets\gifs\DinoSprites_tard.gif",format='gif -index %i' %(i)).zoom(SF,SF) for i in range(4,10)]
kick = [tk.PhotoImage(file="assets\gifs\DinoSprites_tard.gif",format='gif -index %i' %(i)).zoom(SF,SF) for i in range(10,14)]
hurt = [tk.PhotoImage(file="assets\gifs\DinoSprites_tard.gif",format='gif -index %i' %(i)).zoom(SF,SF) for i in range(14,17)]
speed = [tk.PhotoImage(file="assets\gifs\DinoSprites_tard.gif",format='gif -index %i' %(i)).zoom(SF,SF) for i in range(17,23)]
cycles = [idle, walk, kick, hurt, speed]
label = tk.Label(window, bd=0,bg='black')

#run the program
char = character(cycles, window, label)
