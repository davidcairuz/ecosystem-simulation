#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import Canvas, Tk
import time
import numpy as np

WIDTH = 500
HEIGHT = 400
FOOD_SIZE = 10

class Food:

	all_food = {}
	current_generation = 0

	def __init__(self, canvas):
		(x1, y1, x2, y2) = self.get_random_coordinates()
		self.canvas = canvas

		self.shape = self.canvas.create_oval(x1, y1, x2, y2, fill='green')
		self.food = np.random.randint(100, 1001)

		Food.all_food[self.shape] = self

	def get_random_coordinates(self):
		x1 = np.random.randint(0, WIDTH - FOOD_SIZE)
		y1 = np.random.randint(0, HEIGHT - FOOD_SIZE)
		x2 = x1 + FOOD_SIZE
		y2 = y1 + FOOD_SIZE

		return (x1, y1, x2, y2)