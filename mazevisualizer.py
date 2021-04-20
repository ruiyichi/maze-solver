import pygame
from maze import *
import tkinter as tk
import sys

def setup():

	if len(sys.argv) != 3:
	    sys.exit("Usage: python3 mazesolvervisualizer.py maze.txt BFS|DFS|GBFS|A*")

	if sys.argv[2] == "BFS":
		m = BFSMaze(sys.argv[1])

	if sys.argv[2] == "DFS":
		m = DFSMaze(sys.argv[1])

	if sys.argv[2] == "GBFS":
		m = GreedyBestFirstMaze(sys.argv[1])
	
	if sys.argv[2] == "A*":
		m = AstarMaze(sys.argv[1])

	m.solve()

	explored = m.explored
	colorexplored = []

	root = tk.Tk()

	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight() - 100

	pygame.init()
	
	square_size = 0
	while square_size*m.width <= screen_width and square_size*m.height <= screen_height:
		square_size += 1
	square_size -= 1
	
	border_size = square_size/100*3

	width = square_size*m.width
	height = square_size*m.height

	win = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Maze solver")
	FPS = 8
	clock = pygame.time.Clock()
	run = True

	while run:
		clock.tick(FPS)
		
		for row in range(m.width):
			for col in range(m.height):
				#draw border
				pygame.draw.rect(win, (0, 0, 0), pygame.Rect(width/m.width*row, height/m.height*col, square_size, square_size))
				
				#draw walls
				if m.walls[col][row]:
					pygame.draw.rect(win, (60, 60, 60), pygame.Rect(width/m.width*row, height/m.height*col, square_size-border_size, square_size-border_size))
				#draw valid path
				else:
					pygame.draw.rect(win, (255, 255, 255), pygame.Rect(width/m.width*row, height/m.height*col, square_size-border_size, square_size-border_size))
		
		for cell in colorexplored:
			if cell != m.goal:
				pygame.draw.rect(win, (255, 255, 0), pygame.Rect(width/m.width*cell[1], height/m.height*cell[0], square_size-border_size, square_size-border_size))

		if len(explored) > 0:
			cell = explored[0]
			pygame.draw.rect(win, (0, 255, 0), pygame.Rect(width/m.width*cell[1], height/m.height*cell[0], square_size-border_size, square_size-border_size))
			colorexplored.append(explored.pop(0))
			
		if m.goal in colorexplored:
			for cell in m.solution[1]:
				pygame.draw.rect(win, (200, 69, 0), pygame.Rect(width/m.width*cell[1], height/m.height*cell[0], square_size-border_size, square_size-border_size))

		#draw start
		pygame.draw.rect(win, (255, 0, 0), pygame.Rect(width/m.width*m.start[1], height/m.height*m.start[0], square_size-border_size, square_size-border_size))
		
		#draw goal
		pygame.draw.rect(win, (0, 0, 255), pygame.Rect(width/m.width*m.goal[1], height/m.height*m.goal[0], square_size-border_size, square_size-border_size))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False

		pygame.display.update()

if __name__ == "__main__":
	setup()