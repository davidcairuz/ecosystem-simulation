#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import Canvas, Tk
import time
import numpy as np
from individual import Individual
from food import Food
import math

WIDTH = 1280
HEIGHT = 720
FOOD_RATE = 100
INDIVIDUAL_QNT = 30

def create_food(canvas):
	quantity = math.ceil((np.random.randint(30, 101)/100) * INDIVIDUAL_QNT)
	for i in range(quantity):
		Food(canvas)

master = Tk()
canvas = Canvas(master, width=WIDTH, height=HEIGHT)
master.title('Simulation')
canvas.pack()

# Creating individuals
for i in range(100):
	Individual(canvas)

# Creating food
create_food(canvas)

# Main loop
while True:
	Individual.current_generation += 1

	for ind in list(Individual.all_individuals.values()):
		ind.step()

	if Individual.current_generation % FOOD_RATE == 0 and len(Food.all_food) < 1.5 * INDIVIDUAL_QNT:
		create_food(canvas)

	master.update()
	time.sleep(0.015)

	if len(Food.all_food) == 0 or len(Individual.all_individuals) == 0:
		print('End of simulation')
		break

master.mainloop()