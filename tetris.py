# this version of tetris outputs frames even when not needed and uses multi-threading to do input# this version of tetris will only output frames when needed
import copy
import keyboard
import random
import time
from termcolor import colored


def colour_in(tetrimo):
	if tetrimo['name'] == "I":
		colour = 1
	elif tetrimo['name'] == "J":
		colour = 2
	elif tetrimo['name'] == "L":
		colour = 3
	elif tetrimo['name'] == "O":
		colour = 4
	elif tetrimo['name'] == "S":
		colour = 5
	elif tetrimo['name'] == "T":
		colour = 6
	elif tetrimo['name'] == "Z":
		colour = 7
	
	return colour

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


grid_permanent = copy.deepcopy(empty_grid) # copy off empty/default grid
grid = copy.deepcopy(grid_permanent)
tetrimo = random.choice(list(tetrimoes.values())) # pick random tetrimo from tetrimoes
colour = colour_in(tetrimo) 
shape_origin_x = 4
shape_origin_y = 1

gravity_timer = time.time()
default_gravity = 1
gravity = default_gravity
gameover = False

right = False
left = False
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
				
				

	if grid != previous_frame: # if nothing has changed, no point in printing new one
		display = '| '
		for row in grid:
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

			if shape_origin_x-1 != 0:
				shape_origin_x -= 1 # intial move before DAS and arr

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and left > 0:
			if time.time()-arr_start > arr:
				arr_start = time.time()

				if shape_origin_x-1 != 0:
					shape_origin_x -= 1	

		left = True # state that the previous key is left
	else:
		left = False


	# moving right
	if keyboard.is_pressed('right'):

		# check if right was the previous keypress, if not then restart DAS and do initial move
		if right == False:
			das_start = time.time()

			if shape_origin_x+1 != 9:
					shape_origin_x += 1 # intial move before DAS and arr

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and right > 0:
			if time.time()-arr_start > arr:
				arr_start = time.time()

				if shape_origin_x+1 != 9:
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

	if keyboard.is_pressed('down'):
		gravity = sdf
	else:
		soft_drop == False
		gravity = default_gravity