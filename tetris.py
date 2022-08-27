import copy
import keyboard
import random
import time
from termcolor import colored


def colour_in(tetrimo, highlight=False):

	if highlight == False:
		if tetrimo['name'] == "I":
			number = 1
		elif tetrimo['name'] == "J":
			number = 2
		elif tetrimo['name'] == "L":
			number = 3
		elif tetrimo['name'] == "O":
			number = 4
		elif tetrimo['name'] == "S":
			number = 5
		elif tetrimo['name'] == "T":
			number = 6
		elif tetrimo['name'] == "Z":
			number = 7
			
	elif highlight == True:
		if tetrimo['name'] == "I":
			number = 8
		elif tetrimo['name'] == "J":
			number = 9
		elif tetrimo['name'] == "L":
			number = 10
		elif tetrimo['name'] == "O":
			number = 11
		elif tetrimo['name'] == "S":
			number = 12
		elif tetrimo['name'] == "T":
			number = 13
		elif tetrimo['name'] == "Z":
			number = 14
	
	return number

# hard coded each piece's position cos it was easier than the other methods
tetrimoes = {
	"I": {
		"a_flat": [[0, 0], [0, -1], [0, 1], [0, 2]],
		"b_flat": [[1, 0], [1, -1], [1, 1], [1, 2]],
		"a_upright": [[0, 1], [-1, 1], [1, 1], [2, 1]],
		"b_upright": [[0, 0], [-1, 0], [1, 0], [2, 0]],
		"state": "a_flat", 
		"name": "I"
	},
	"J": {
		"a_flat": [[0, 0], [-1, -1], [0, -1], [0, 1]],
		"b_flat": [[0, 0], [0, -1], [0, 1], [1, 1]],
		"a_upright": [[0, 0], [-1, 0], [-1, 1], [1, 0]],
		"b_upright": [[0, 0], [-1, 0], [1, -1], [1, 0]],
		"state": "a_flat",
		"name": "J"
	},
	"L": {
		"a_flat": [[0, 0], [-1, 1], [0, -1], [0, 1]],
		"b_flat": [[0, 0], [0, -1], [0, 1], [1, -1]],
		"a_upright": [[0, 0], [-1, 0], [1, 0], [1, 1]],
		"b_upright": [[0, 0], [-1, -1], [-1, 0], [1, 0]],
		"state": "a_flat",
		"name": "L"
	},
	"O": {
		"a_flat": [[0, 0], [-1, 0], [-1, 1], [0, 1]],
		"b_flat": [[0, 0], [-1, 0], [-1, 1], [0, 1]], 
		"a_upright": [[0, 0], [-1, 0], [-1, 1], [0, 1]], 
		"b_upright": [[0, 0], [-1, 0], [-1, 1], [0, 1]],
		"state": "a_flat",
		"name": "O"
	},
	"S": {
		"a_flat": [[0, 0], [-1, 0], [-1, 1], [0, -1]],
		"b_flat": [[0, 0], [0, 1], [1, -1], [1, 0]],
		"a_upright": [[0, 0], [-1, 0], [0, 1], [1, 1]],
		"b_upright": [[0, 0], [-1, -1], [0, -1], [1, 0]],
		"state": "a_flat",
		"name": "S"
	},
	"T": {
		"a_flat": [[0, 0], [-1, 0], [0, -1], [0, 1]],
		"b_flat": [[0, 0], [0, -1], [0, 1], [1, 0]],
		"a_upright": [[0, 0], [-1, 0], [0, 1], [1, 0]],
		"b_upright": [[0, 0], [-1, 0], [0, -1], [1, 0]],
		"state": "a_flat",
		"name": "T"
	},
	"Z": {
		"a_flat": [[0, 0], [-1, -1], [-1, 0], [0, 1]],
		"b_flat": [[0, 0], [0, -1], [1, 0], [1, 1]],
		"a_upright": [[0, 0], [-1, 1], [0, 1], [1, 0]],
		"b_upright": [[0, 0], [-1, 0], [0, -1], [1, -1]],
		"state": "a_flat",
		"name": "Z"
	}
}

empty_grid = [
	# 10x20
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

tetrimo = random.choice(list(tetrimoes.values())) # pick random tetrimo from tetrimoes
colour = colour_in(tetrimo) 

grid_permanent = copy.deepcopy(empty_grid) # copy off empty/default grid
grid = copy.deepcopy(grid_permanent)
shape_origin_x = 4
shape_origin_y = 1
ghost_origin_y = shape_origin_y

score = 0
level = 1
level_lines = 10
lines_cleared = 0

gravity_timer = time.time()
default_gravity = (0.8-((level-1)*0.007))**level
gravity = default_gravity
gameover = False

move = False
right = False
left = False
hard_drop = False
soft_drop = False
clockwise = False
anti_clockwise = False
das_start = 0
arr_start = 0

# player settings
das = 0.12 # delay before repeating in seconds
arr = 0.04 # delay before each repeat in seconds
sdf = 0.05 # percentage of gravity time


# very disorganised spaghetti loop
while True:


	# GAME

	# gameover
	for pixel in grid_permanent[0]:
		if pixel != 0:
			gameover = True

	if gameover == True:		
		grid_permanent = copy.deepcopy(empty_grid)
		score = 0
		print('gameover')
		input('>>> ')
		gameover = False
		
	# line clearing
	n = -1 # keep track of current index
	for row in grid_permanent:
		n += 1
		if 0 not in row: # if there is no gap
			grid_permanent.pop(n) # remove row from grid_permanent
			new_line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
			grid_permanent.insert(0, new_line) # add new row at the top
			# the 3 lines above will make pieces for down after a line clear

			score += 100*level
			lines_cleared += 1
			level_lines -= 1

	if level < 15 and level_lines == 0:
		level += 1
		default_gravity = (0.8-((level-1)*0.007))**level
		level_lines = 10

	# setup for what the player sees
	next = False
	previous_frame = copy.deepcopy(grid) # previous grid, later it will compare with new grid to make sure something happened
	grid = copy.deepcopy(grid_permanent) # update new blank grid with what has happened so far

	if (time.time()-gravity_timer) > gravity:
		shape_origin_y += 1 # move tetrimo down
		gravity_timer = time.time()


	# making/updating the grids		
	for name, shape in tetrimo.items():
		# updating the grid display
		if name == tetrimo["state"]:
			for piece in shape:

				# checking if tetrimo has touched anything
				if shape_origin_y+piece[0] == 19 or grid_permanent[shape_origin_y+piece[0]+1][shape_origin_x+piece[1]] != 0:
					# first one is checking for floor, second one is checking for other tetrimo

					next = True
				else:
					grid[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour

			# keeping the piece in place after it has touched the floor
			if next == True:
				for piece in shape: # updating the permanent grid
					grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour
				# restarting the shape for the next time it comes up again
				tetrimo['state'] = 'a_flat'
				tetrimo = random.choice(list(tetrimoes.values())) # pick random tetrimo from tetrimoes
				shape_origin_x = 4
				shape_origin_y = 1
				colour = colour_in(tetrimo) 

	# putting the ghost piece into the grid
	loop = True
	ghost_origin_y = shape_origin_y
	while loop:
		for name, shape in tetrimo.items():
			if name == tetrimo['state']:
				for piece in shape:
					if ghost_origin_y+piece[0] == 19 or grid_permanent[ghost_origin_y+piece[0]+1][shape_origin_x+piece[1]] != 0:
						# first one is checking for floor, second one is checking for other tetrimo
						loop = False
		ghost_origin_y += 1
	
	ghost_origin_y -= 1
	colour = colour_in(tetrimo, True)
	for name, shape in tetrimo.items():
		if name == tetrimo['state']:
			for piece in shape:
				grid[ghost_origin_y+piece[0]][shape_origin_x+piece[1]] = colour
	colour = colour_in(tetrimo) # reverting colour just in case

	if grid != previous_frame: # if nothing has changed, no point in printing new one
		display = ' _____________________\n| '
		row_number = 0

		for row in grid:
			row_number += 1
			for pixel in row:
				if pixel == 0:
					display += '. '
				
				# colours!
				elif pixel == 1:
					display += colored('■ ', 'cyan')
				elif pixel == 2:
					display += colored('■ ', 'blue')
				elif pixel == 3:
					display += '■ '
				elif pixel == 4:
					display += colored('■ ', 'yellow')
				elif pixel == 5:
					display += colored('■ ', 'green')
				elif pixel == 6:
					display += colored('■ ', 'magenta')
				elif pixel == 7:
					display += colored('■ ', 'red')
				
				elif pixel == 8:
					display += colored('▢ ', 'cyan')
				elif pixel == 9:
					display += colored('▢ ', 'blue')
				elif pixel == 10:
					display += colored('▢ ', 'white')
				elif pixel == 11:
					display += colored('▢ ', 'yellow')
				elif pixel == 12:
					display += colored('▢ ', 'green')
				elif pixel == 13:
					display += colored('▢ ', 'magenta')
				elif pixel == 14:
					display += colored('▢ ', 'red')
					
					
			if row_number == 1:
				display += f'| LEVEL: {level}\n| '
			elif row_number == 2:
				display += f'| LINES: {lines_cleared}\n| '
			elif row_number == 3:
				display += f'| SCORE: {score}\n| '
				
			else:
				display += '|\n| '	
		print(display)

	# INPUT

	# anti-clockwise
	if keyboard.is_pressed('a'): # threading stops here for some reason
		if anti_clockwise  == False:

			if tetrimo["state"] == "a_flat":
				tetrimo["state"] = "b_upright"
			elif tetrimo["state"] == "b_upright":
				tetrimo["state"] = "b_flat"
			elif tetrimo["state"] == "b_flat":
				tetrimo["state"] = "a_upright"
			elif tetrimo["state"] == "a_upright":
				tetrimo["state"] = "a_flat"
		
		anti_clockwise = True
	else:
		anti_clockwise = False

	# clockwise
	if keyboard.is_pressed('r'):
		if clockwise == False:
			if tetrimo["state"] == "a_flat":
				tetrimo["state"] = "a_upright"
			elif tetrimo["state"] == "a_upright":
				tetrimo["state"] = "b_flat"
			elif tetrimo["state"] == "b_flat":
				tetrimo["state"] = "b_upright"
			elif tetrimo["state"] == "b_upright":
				tetrimo["state"] = "a_flat"
		
		clockwise = True
	else:
		clockwise = False

	# moving left
	if keyboard.is_pressed('left'):
		
		# check if left was the previous keypress, if not then restart DAS and do initial move
		if left == False:
			das_start = time.time()

			move = True

			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] == 0:
							move = False
			

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and left == True:

			if time.time()-arr_start > arr:
				move = True
				arr_start = time.time()

				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape:
							if shape_origin_x+piece[1] == 0:
								move = False
		
		if move == True:
			move = False
			shape_origin_x -= 1

		left = True # state that the previous key is left
	else:
		left = False


	# moving right
	if keyboard.is_pressed('right'):

		# check if right was the previous keypress, if not then restart DAS and do initial move
		if right == False:
			das_start = time.time()
			move = True

			# this code checks if any piece is on the border of grid, might turn into function later
			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] == 9:
							move = False

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and right == True:
			if time.time()-arr_start > arr:
				arr_start = time.time()
				move = True

				# this code checks if any piece is on the border of grid, might turn into function later
				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape:
							if shape_origin_x+piece[1] == 9:
								move = False

		if move == True:
			move = False
			shape_origin_x += 1

		right = True # state that the previous key is right
	else:
		right = False

	# flipping the tetrimo
	if keyboard.is_pressed('backspace'):
		if flip == False:
			if tetrimo["state"] == "a_flat":
				tetrimo["state"] = "b_flat"
			elif tetrimo["state"] == "b_flat":
				tetrimo["state"] = "a_flat"
			
			elif tetrimo["state"] == "a_upright":
				tetrimo["state"] = "b_upright"
			elif tetrimo["state"] == "b_upright":
				tetrimo["state"] = "a_upright"
		flip = True
	
	else:
		flip = False

	# soft drop
	if keyboard.is_pressed('down'):
		gravity = sdf
	else:
		soft_drop == False
		gravity = default_gravity
	
	# hard drop
	if keyboard.is_pressed('up'):
		if hard_drop == False:
			hard_drop_loop = True
			while hard_drop_loop:
				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape:
							if shape_origin_y+piece[0] == 19 or grid_permanent[shape_origin_y+piece[0]+1][shape_origin_x+piece[1]] != 0:
								# first one is checking for floor, second one is checking for other tetrimo

								next = True
								hard_drop_loop = False
				shape_origin_y += 1

			if next == True:
				shape_origin_y -= 1 # this makes it so that Y does not end up being 20 which is out of index range

				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape: # updating the permanent grid
							grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour
				# restarting the shape for the next time it comes up again
				tetrimo['state'] = 'a_flat'
				tetrimo = random.choice(list(tetrimoes.values())) # pick random tetrimo from tetrimoes
				shape_origin_x = 4
				shape_origin_y = 1
				colour = colour_in(tetrimo) 
				next = False
		
		hard_drop = True
	else:
		hard_drop = False
		
		