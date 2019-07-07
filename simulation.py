from tkinter import Canvas, Tk
import time
import numpy as np 

WIDTH = 500
HEIGHT = 400
GENERATION_GAP = 200

class Individual:

    all_individuals = {}
    current_generation = 0
    
    def __init__(self):
        self.shape = canvas.create_oval(10, 10, 20, 20, fill='red')
        self.xspeed = 1
        self.yspeed = 1
        
        Individual.all_individuals[self.shape] = self
            
    def walk(self):
        if self.is_dead():
            return

        self.check_if_reached_border()
        canvas.move(self.shape, self.xspeed, self.yspeed)

        self.kill_by_contact(starting_gen=GENERATION_GAP)
        self.change_direction(low=-1, high=1, chance=95)
        

    def is_dead(self):
        return self.shape not in Individual.all_individuals
	
    def check_if_reached_border(self):
        pos = canvas.coords(self.shape)
        
        if pos[3] >= HEIGHT or pos[1] <= 0:
            self.yspeed = -self.yspeed

        if pos[2] >= WIDTH or pos[0] <= 0:
            self.xspeed = -self.xspeed
    
    def kill_by_contact(self, starting_gen):
        if Individual.current_generation < starting_gen:
            return

        currently_overlapping = self.detect_collision()

        for individual in currently_overlapping:
            canvas.delete(individual) 
            try:
                del Individual.all_individuals[individual]
            except KeyError:
                pass
    
    def detect_collision(self):
        x1, y1, x2, y2 = canvas.coords(self.shape)
        currently_overlapping = canvas.find_overlapping(x1, y1, x2, y2)
        
        if len(currently_overlapping) == 1:
            currently_overlapping = {}

        return currently_overlapping
    
    def change_direction(self, low, high, chance):
        # 95% chance of keep going in the same direction
        if np.random.randint(0, 101) > chance:
            self.xspeed = np.random.randint(low, high+1)
            self.yspeed = np.random.randint(low, high+1)

master = Tk()
canvas = Canvas(master, width=WIDTH, height=HEIGHT)
master.title("Simulation")
canvas.pack()

# Creating individuals
for i in range(20):
	newind = Individual()

# Main loop
while(True):
    Individual.current_generation += 1
    
    for ind in list(Individual.all_individuals.values()):
        ind.walk()
        
    master.update()
    time.sleep(0.015)

master.mainloop()
