from tkinter import *
import time
import numpy as np 

WIDTH = 500
HEIGHT = 400

def kill_by_contact(individuals):
	overlapping_individuals = detect_all_overlapping(individuals)
	for ind in overlapping_individuals:
		canvas.delete(ind)

def detect_all_overlapping(individuals):
	overlapping_individuals = set()
	
	for ind in individuals:
		detect_individual_overlapping(ind, overlapping_individuals)

	return overlapping_individuals

def detect_individual_overlapping(ind, overlapping_individuals):
	try:
		x1, y1, x2, y2 = canvas.coords(ind.shape)
	except:
		return

	currently_overlapping = canvas.find_overlapping(x1, y1, x2, y2)
	
	if len(currently_overlapping) == 1:
		return

	for ind in currently_overlapping:
		overlapping_individuals.add(ind)
	

class Individual:
	def __init__(self):
		self.shape = canvas.create_oval(10, 10, 20, 20, fill='red')
		self.xspeed = 1
		self.yspeed = 1

	def walk(self):
		canvas.move(self.shape, self.xspeed, self.yspeed)
		pos = canvas.coords(self.shape)

		if pos[3] >= HEIGHT or pos[1] <= 0:
			self.yspeed = -self.yspeed
			return

		if pos[2] >= WIDTH or pos[0] <= 0:
			self.xspeed = -self.xspeed
			return

		# 80% chance of keep going in the same direction
		if np.random.randint(0, 101) > 95:
			self.xspeed = np.random.randint(-1, 2)
			self.yspeed = np.random.randint(-1, 2)
	
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title("Simulation")
canvas.pack()

# Creating individuals
individuals = []
for i in range(20):
	newind = Individual()
	individuals.append(newind)

generation = 0

# Main loop
while(True):
	generation += 1

	for ind in individuals:
		try:
			ind.walk()
		except:
			individuals.remove(ind)

	tk.update()
	time.sleep(0.015)

	if generation > 1000:
		kill_by_contact(individuals)

tk.mainloop()
