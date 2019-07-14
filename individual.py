#!/usr/bin/python
# -*- coding: utf-8 -*-
from food import Food
from tkinter import Canvas, Tk
import time
import numpy as np
import random

WIDTH = 1280
HEIGHT = 720
IND_SIZE = 12
START_GEN = 200
VIEW_RADIUS = 100

class Individual:

	all_individuals = {}
	current_generation = 0

	def __init__(self, canvas):
		(x1, y1, x2, y2) = self.get_random_coordinates()
		self.canvas = canvas
		self.shape = self.canvas.create_oval(x1, y1, x2, y2, fill='red')
		self.xspeed = 1
		self.yspeed = 1

		self.on_course = False
		self.food_position_x = 0
		self.food_position_y = 0

		self.food = 0
		self.max_hunger = np.random.randint(500, 1001)

		self.randomly_change_direction(low=-1, high=1, chance=100)
		Individual.all_individuals[self.shape] = self

	def get_random_coordinates(self):
		x1 = np.random.randint(0, WIDTH - IND_SIZE)
		y1 = np.random.randint(0, HEIGHT - IND_SIZE)
		x2 = x1 + IND_SIZE
		y2 = y1 + IND_SIZE

		return (x1, y1, x2, y2)

	def step(self):
		if self.is_dead():
			return

		self.reached_border()
		self.canvas.move(self.shape, self.xspeed, self.yspeed)

		focus_group = self.decide_next_action()

		self.eat()
		if self.food == 0:
			self.randomly_change_direction(low=-1, high=1, chance=2)
			self.on_course = False
		
		self.reached_food()

		self.food += 1
		
		if not self.on_course:
			self.move_to(focus_group)
		
		if not self.on_course:
			self.randomly_change_direction(low=-1, high=1, chance=2)

	def reached_food(self):
		(x1, y1, x2, y2) = self.canvas.coords(self.shape)
		
		if x1 == self.food_position_x and y1 == self.food_position_y:
			self.randomly_change_direction(low=-1, high=1, chance=2)
			self.on_course = False
	
	def decide_next_action(self):
		if self.food > 200:	
			return Food.all_food
		else:
			return None
	
	def move_to(self, group):
		if group == None:
			self.randomly_change_direction(low=-1, high=1, chance=2)
			self.on_course = False
			return

		(x1, y1, x2, y2) = self.canvas.coords(self.shape)

		x1 -= VIEW_RADIUS
		y1 -= VIEW_RADIUS
		x2 += VIEW_RADIUS
		y2 += VIEW_RADIUS

		currently_seeing = self.canvas.find_overlapping(x1, y1, x2, y2)
		currently_seeing = [obj for obj in currently_seeing if obj in group]

		if len(currently_seeing) == 0:
			self.randomly_change_direction(low=-1, high=1, chance=2)
			self.on_course = False
			return

		target = currently_seeing[0]

		targ_x1, targ_y1, targ_x2, targ_y2 = self.canvas.coords(target)
		
		self.xspeed = ((targ_x1 + targ_x2)/2 - x1)/100
		self.yspeed = ((targ_y1 + targ_y2)/2 - y1)/100

		self.food_position_x = (targ_x1 + targ_x2)/2 
		self.food_position_y = (targ_y1 + targ_y2)/2

		self.on_course = True

	def is_dead(self):
		if self.food >= self.max_hunger:
			self.canvas.delete(self.shape)
			try:
				del Individual.all_individuals[self.shape]
			except KeyError:
				pass

		return self.shape not in Individual.all_individuals

	def reached_border(self):
		pos = self.canvas.coords(self.shape)

		if pos[3] >= HEIGHT or pos[1] <= 0:
			self.yspeed = -self.yspeed

		if pos[2] >= WIDTH or pos[0] <= 0:
			self.xspeed = -self.xspeed
		
		self.on_course = False
		self.randomly_change_direction(low=-1, high=1, chance=2)

	def eat(self):
		currently_overlapping = self.detect_resource_collision(Food.all_food)
		
		if len(currently_overlapping) == 0:
			return

		for food in currently_overlapping:
			self.canvas.delete(food)
			try:
				del Food.all_food[food]
			except KeyError:
				pass

		self.food = 0

	def detect_resource_collision(self, group):
		(x1, y1, x2, y2) = self.canvas.coords(self.shape)
		currently_overlapping = self.canvas.find_overlapping(x1, y1, x2, y2)

		currently_overlapping = [ind for ind in currently_overlapping if ind in group]

		return currently_overlapping

	def randomly_change_direction(self, low, high, chance):
		if np.random.randint(0, 101) > 100 - chance:
			self.xspeed = np.random.randint(low, high + 1)
		if np.random.randint(0, 101) > 100 - chance:	
			self.yspeed = np.random.randint(low, high + 1)