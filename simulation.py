#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import Canvas, Tk
import time
import numpy as np
from individual import Individual
from food import Food

WIDTH = 500
HEIGHT = 400

master = Tk()
canvas = Canvas(master, width=WIDTH, height=HEIGHT)
master.title('Simulation')
canvas.pack()

# Creating individuals
for i in range(30):
	newind = Individual(canvas)

# Creating food
for i in range(15):
	newind = Food(canvas)

# Main loop
while True:
	Individual.current_generation += 1

	for ind in list(Individual.all_individuals.values()):
		ind.step()

	master.update()
	time.sleep(0.015)

	if len(Food.all_food) == 0:
		print('End of simulation')
		break

master.mainloop()