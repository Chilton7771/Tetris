# this tetris game was created by Chilton Cai

import copy
import keyboard
import random
import time


# decides the colour of pixels tetrimoes on the board
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

# makes a new bag
def new_bag():
	global tetrimoes
	global bag

	bag = []
	for shape in list(tetrimoes.values()):
		bag.append(shape)
	random.shuffle(bag)

# picks out a new tetrimo from the bag 
def new_tetrimo():
	global tetrimoes
	global bag

	try:
		tetrimo = bag.pop(0) # pop will remove first item and assign it to return thing
	except: # in case bag has run out
		new_bag()
		tetrimo = bag.pop(0)

	return tetrimo

# resets the value of lock delay
def reset_lock_delay(ground_touch='none'):
	global lock_delay

	if ground_touch == 'none' or ground_touch == True:
		lock_delay = 0.5

# this function allows us to specify text colour with 24 bit colours
def colored(text, rgb):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(rgb[0], rgb[1], rgb[2], text)

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

bag = []
new_bag()
tetrimo = new_tetrimo() # pick random tetrimo from tetrimoes
colour = colour_in(tetrimo) 

grid_permanent = copy.deepcopy(empty_grid) # copy off empty/default grid
grid = copy.deepcopy(grid_permanent)
shape_origin_x = 4
shape_origin_y = 1
ghost_origin_y = shape_origin_y

score = 0
level = 1
lines_cleared = 0
fps_start = time.time()
fps = 1
fps_count = 0

gravity_timer = time.time()
default_gravity = (0.8-((level-1)*0.007))**level # this equation gives us the time in between each fall of the piece
gravity = default_gravity
lock_delay = 0.5 # delay before blocks lock onto the ground in seconds
gameover = False

hold_piece = 'none'
hold = False
move = False
right = False
left = False
hard_drop = False
clockwise = False
anti_clockwise = False
das_start = 0
arr_start = 0
lock_delay_start = 0
ground_touch = False

# player settings
das = 0.12 # delay before repeating in seconds
arr = 0.04 # delay before each repeat in seconds
sdf = 20 # multiplication of the speed of gravity


# very disorganised spaghetti loop
while True:
	# GAME

	# gameover
	for pixel in grid_permanent[0]:
		if pixel != 0:
			gameover = True

	# ending the game
	if gameover == True: # losing the game		
		grid_permanent = copy.deepcopy(empty_grid)
		score = 0
		level = 0
		lines_cleared = 0
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

	if (lines_cleared / 10) >= level:
		level += 1
		default_gravity = (0.8-((level-1)*0.007))**level

	# setup for what the player sees
	next = False
	previous_frame = copy.deepcopy(grid) # previous grid, later it will compare with new grid to make sure something happened
	grid = copy.deepcopy(grid_permanent) # update new blank grid with what has happened so far

	if (time.time()-gravity_timer) > gravity and ground_touch == False:
		shape_origin_y += 1 # move tetrimo down
		gravity_timer = time.time()

	# making/updating the grids		
	for name, shape in tetrimo.items():
		# updating the grid display
		if name == tetrimo["state"]:
			for piece in shape:

				# checking if tetrimo has touched anything
				if (shape_origin_y+piece[0] == 19 or grid_permanent[shape_origin_y+piece[0]+1][shape_origin_x+piece[1]] != 0) and ground_touch == False:
					ground_touch = True
					lock_delay_start = time.time()
				else:
					grid[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour

			if ground_touch == True:
				lock_delay -= time.time() - lock_delay_start
				lock_delay_start = time.time()

				if lock_delay < 0:
					next = True
					ground_touch = False
					reset_lock_delay()

			# keeping the piece in place after it has touched the floor
			if next == True:
				for piece in shape: # updating the permanent grid
					grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour
				# restarting the shape for the next time it comes up again
				tetrimo['state'] = 'a_flat'
				tetrimo = new_tetrimo() # pick random tetrimo from bag
				shape_origin_x = 4
				shape_origin_y = 1
				colour = colour_in(tetrimo) 
				hold = False # this allows for holding again

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
	ghost_colour = colour_in(tetrimo, True)
	for name, shape in tetrimo.items():
		if name == tetrimo['state']:
			for piece in shape:
				if grid[ghost_origin_y+piece[0]][shape_origin_x+piece[1]] == 0: # lets the real piece have priority
					grid[ghost_origin_y+piece[0]][shape_origin_x+piece[1]] = ghost_colour

	# hold pieces
	hold_grid = [
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]
	]
	if hold_piece != 'none':
		if hold == False:
			hold_colour = colour_in(hold_piece)
		else:
			hold_colour = 8 # 8 means no colour
		for name, shape in hold_piece.items():
			if name == 'a_flat': # comparing it to "a_flat" keeps it in default position
				for piece in shape: # updating the permanent grid
					hold_grid[2+piece[0]][1+piece[1]] = hold_colour
		colour = colour_in(tetrimo)

	row_number = 0
	display = [
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]
	]
	for row in hold_grid:
		pixel_number = 0
		for pixel in row:
			if pixel == 0:
				display[row_number][pixel_number] = '·'
			elif pixel == 1:
				display[row_number][pixel_number] = colored('■', [0, 229, 255]) # cyan
			elif pixel == 2:
				display[row_number][pixel_number] = colored('■', [0, 34, 255]) # blue
			elif pixel == 3:
				display[row_number][pixel_number] = colored('■', [255, 128, 0]) # orange
			elif pixel == 4:
				display[row_number][pixel_number] = colored('■', [255, 255, 0]) # yellow
			elif pixel == 5:
				display[row_number][pixel_number] = colored('■', [0, 255, 0]) # green
			elif pixel == 6:
				display[row_number][pixel_number] = colored('■', [140, 0, 200]) # purple
			elif pixel == 7:
				display[row_number][pixel_number] = colored('■', [255, 0, 0]) # red
			elif pixel == 8:
				display[row_number][pixel_number] = colored('■', [171, 171, 171]) # grey
			
			pixel_number += 1
		row_number += 1
	hold_grid = display

	if grid != previous_frame: # if nothing has changed, no point in printing new one
		display = '' # top of box
		row_number = 0

		for row in grid:
			row_number += 1
			for pixel in row:
				if pixel == 0:
					display += '· '
				
				# colours!
				elif pixel == 1:
					display += colored('■ ', [0, 229, 255]) # cyan
				elif pixel == 2:
					display += colored('■ ', [0, 34, 255]) # blue
				elif pixel == 3:
					display += colored('■ ', [255, 128, 0]) # orange
				elif pixel == 4:
					display += colored('■ ', [255, 255, 0]) # yellow
				elif pixel == 5:
					display += colored('■ ', [0, 255, 0]) # green
				elif pixel == 6:
					display += colored('■ ', [140, 0, 200]) # purple
				elif pixel == 7:
					display += colored('■ ', [255, 0, 0]) # red
				
				elif pixel == 8:
					display += colored('▢ ', [0, 229, 255]) # cyan
				elif pixel == 9:
					display += colored('▢ ', [0, 34, 255]) # blue
				elif pixel == 10:
					display += colored('▢ ', [255, 128, 0]) # orange
				elif pixel == 11:
					display += colored('▢ ', [255, 255, 0]) # yellow
				elif pixel == 12:
					display += colored('▢ ', [0, 255, 0]) # green
				elif pixel == 13:
					display += colored('▢ ', [140, 0, 200]) # purple
				elif pixel == 14:
					display += colored('▢ ', [255, 0, 0]) # red
			
			if row_number == 1:
				display += f'│ LEVEL: {level}\n│ {hold_grid[1][0]} {hold_grid[1][1]} {hold_grid[1][2]} {hold_grid[1][3]} ││ '
			elif row_number == 2:
				display += f'│ LINES: {lines_cleared}\n│ {hold_grid[2][0]} {hold_grid[2][1]} {hold_grid[2][2]} {hold_grid[2][3]} ││ '
			elif row_number == 3:
				display += f'│ SCORE: {score}\n│ {hold_grid[3][0]} {hold_grid[3][1]} {hold_grid[3][2]} {hold_grid[3][3]} ││ '
			elif row_number == 4:
				display += f'│\n└─────────┘│ '
			elif row_number == 5:
				display += f'│ {fps} FPS\n           │ '
			elif row_number == 20:
				display += '│\n'	
			else:
				display += '│\n           │ '	
		
		display = f'┌─────────┐┌─────────────────────┐\n│ {hold_grid[0][0]} {hold_grid[0][1]} {hold_grid[0][2]} {hold_grid[0][3]} ││ ' + display # top of box
		display += '           └─────────────────────┘\n          ' # bottom of box
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
			
			# this code checks if the piece will go through walls because of the rotation
			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] < 0:
							shape_origin_x += 1 # moves piece to the right, out of wall
						elif shape_origin_x+piece[1] > 9: # second bit because pieces can still clip with the opposite rotation
							shape_origin_x -= 1 # moves piece to the left, out of wall

						# immediately rotating back if pieces go into others when rotating
						if grid_permanent[shape_origin_y+piece[0]+1][shape_origin_x+piece[1]] > 0:
							if tetrimo["state"] == "a_flat":
								tetrimo["state"] = "a_upright"
							elif tetrimo["state"] == "a_upright":
								tetrimo["state"] = "b_flat"
							elif tetrimo["state"] == "b_flat":
								tetrimo["state"] = "b_upright"
							elif tetrimo["state"] == "b_upright":
								tetrimo["state"] = "a_flat"

			reset_lock_delay(ground_touch)
		
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
			
			# this code checks if the piece will go through walls because of the rotation
			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] > 9:
							shape_origin_x -= 1 # moves piece to the left, out of wall

						elif shape_origin_x+piece[1] < 0: # second bit because pieces can still clip with the opposite rotation
							shape_origin_x += 1 # moves piece to the right, out of wall
						
						# immediately rotating back if pieces go into others when rotating [TEMPORARY SOLUTION]
						if grid_permanent[shape_origin_y+piece[0]+1][shape_origin_x+piece[1]] > 0:
							if tetrimo["state"] == "a_flat":
								tetrimo["state"] = "b_upright"
							elif tetrimo["state"] == "b_upright":
								tetrimo["state"] = "b_flat"
							elif tetrimo["state"] == "b_flat":
								tetrimo["state"] = "a_upright"
							elif tetrimo["state"] == "a_upright":
								tetrimo["state"] = "a_flat"


			reset_lock_delay(ground_touch)
		
		clockwise = True
	else:
		clockwise = False

	# moving left
	if keyboard.is_pressed('left'):
		
		# check if left was the previous keypress, if not then restart DAS and do 
		# initial move
		if left == False:
			das_start = time.time()
			move = True

			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] == 0 or grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]-1] > 0:
							move = False
			

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and left == True:
			if time.time()-arr_start > arr:
				move = True
				arr_start = time.time()

				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape:
							if shape_origin_x+piece[1] == 0 or grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]-1] > 0:
								move = False
		
		if move == True:
			move = False
			shape_origin_x -= 1
			reset_lock_delay(ground_touch)

		left = True # state that the previous key is left
	else:
		left = False


	# moving right
	if keyboard.is_pressed('right'):

		# check if right was the previous keypress, if not then restart DAS and do 
		# initial move
		if right == False:
			das_start = time.time()
			move = True

			# this code checks if any piece is on the border of grid
			for name, shape in tetrimo.items():
				if name == tetrimo['state']:
					for piece in shape:
						if shape_origin_x+piece[1] == 9 or grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]+1] > 0:
							move = False

		# check if DAS timer has finished, if DAS filled then do ARR
		if (time.time()-das_start) > das and right == True:
			if time.time()-arr_start > arr:
				arr_start = time.time()
				move = True

				# this code checks if any piece is on the border of grid, might turn 
				# into function later
				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape:
							if shape_origin_x+piece[1] == 9 or grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]+1] > 0:
								move = False

		if move == True:
			move = False
			shape_origin_x += 1
			reset_lock_delay(ground_touch)

		right = True # state that the previous key is right
	else:
		right = False

	# flipping the tetrimo
	if keyboard.is_pressed('backspace'):
		if flipped == False:
			if tetrimo["state"] == "a_flat":
				tetrimo["state"] = "b_flat"
			elif tetrimo["state"] == "b_flat":
				tetrimo["state"] = "a_flat"
			
			elif tetrimo["state"] == "a_upright":
				tetrimo["state"] = "b_upright"
			elif tetrimo["state"] == "b_upright":
				tetrimo["state"] = "a_upright"

			reset_lock_delay(ground_touch)
		flipped = True
	
	else:
		flipped = False

	# soft drop
	if keyboard.is_pressed('down'):
		# the if statement below checks if we have already sped up the gravity so
		# that we dont divide the gravity multiple times
		if gravity != (default_gravity / sdf):
			gravity /= sdf # divides the time it takes to go to the next cell

	else:
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
								# first one is checking for floor, second one is 
								# checking for other tetrimo

								next = True
								hard_drop_loop = False
				shape_origin_y += 1

			if next == True:
				shape_origin_y -= 1 # this makes it so that Y does not end up being 
				                    #20 which is out of index range

				for name, shape in tetrimo.items():
					if name == tetrimo['state']:
						for piece in shape: # updating the permanent grid
							grid_permanent[shape_origin_y+piece[0]][shape_origin_x+piece[1]] = colour
				# restarting the shape for the next time it comes up again
				tetrimo['state'] = 'a_flat'
				tetrimo = new_tetrimo() # pick random tetrimo from tetrimoes
				shape_origin_x = 4
				shape_origin_y = 1
				colour = colour_in(tetrimo) 
				next = False
				hold = False # allows player to hold again
		
		hard_drop = True
	else:
		hard_drop = False
	
	if keyboard.is_pressed('shift'):
		if hold == False:
			if hold_piece != 'none':
				# this code switches the hold piece and tetrimo
				placeholder = hold_piece
				hold_piece = tetrimo
				tetrimo = placeholder
				colour_in(tetrimo)

				hold_piece["state"] = 'a_flat'
				shape_origin_y = 1
				shape_origin_x = 4

			else:
				print(tetrimo)
				hold_piece = copy.deepcopy(tetrimo) # fill hold with current tetrimo

				# get new tetrimo
				tetrimo['state'] = 'a_flat'
				tetrimo = new_tetrimo() # pick random tetrimo from tetrimoes

				hold_piece["state"] = 'a_flat'
				shape_origin_x = 4
				shape_origin_y = 1
				next = False
			hold = True
	
	# reset the game
	if keyboard.is_pressed('p'):
		grid_permanent = copy.deepcopy(empty_grid)
		score = 0
		level = 0
		lines_cleared = 0
		
		# resetting the current tetrimo
		tetrimo['state'] = 'a_flat'
		tetrimo = new_tetrimo() # pick random tetrimo from tetrimoes
		shape_origin_x = 4
		shape_origin_y = 1
		colour = colour_in(tetrimo) 
		next = False
		hold = False # allows player to hold again
		hold_piece = 'none'
	
	# fps counting
	try:
		fps = round((1 / (time.time()-fps_start) / fps_count)) # calculates the fps
		fps_start = time.time() # resets the fps start time
		fps_count = 0 # this variable is for taking into account the amount of 
		              # frames we have skipped because of the zero division error

	except:
		pass
	fps_count += 1

