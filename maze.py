class Node():
	def __init__(self, state, parent, action, cost=0):
		self.state = state
		self.parent = parent
		self.action = action
		self.cost = cost

class StackFrontier():
	def __init__(self):
		self.frontier = []

	def add(self, node):
		self.frontier.append(node)

	def contains_state(self, state):
		return any(node.state == state for node in self.frontier)

	def empty(self):
		return len(self.frontier) == 0

	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[-1]
			self.frontier = self.frontier[:-1]
			return node

class QueueFrontier(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[0]
			self.frontier = self.frontier[1:]
			return node

class GreedyBestFirst(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			lowestnode = self.frontier[0]
			for node in self.frontier:
				if node.cost < lowestnode.cost:
					lowestnode = node
			self.frontier.pop(self.frontier.index(lowestnode))
			return lowestnode

class Astar(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			lowestnode = self.frontier[0]
			for node in self.frontier:
				if node.cost < lowestnode.cost:
					lowestnode = node
			self.frontier.pop(self.frontier.index(lowestnode))
			return lowestnode

class DFSMaze:
	def __init__(self, filename):
		with open(filename) as f:
			contents = f.read()

		if contents.count("A") != 1:
			raise Exception("Maze must have a start point")
		if contents.count("B") != 1:
			raise Exception("Maze must have a goal")

		contents = contents.splitlines()
		self.height = len(contents)
		self.width = max(len(line) for line in contents)

		self.walls = []
		for i in range(self.height):
			row = []
			for j in range(self.width):
				try:
					if contents[i][j] == "A":
						self.start = (i, j)
						row.append(False)
					elif contents[i][j] == "B":
						self.goal = (i, j)
						row.append(False)
					elif contents[i][j] == " ":
						row.append(False)
					else:
						row.append(True)
				except IndexError:
					row.append(False)
			self.walls.append(row)

		self.solution = None

		f.close()
		
	def neighbors(self, state):
		row, col = state

		candidates = [
			("up", (row - 1, col)),
			("down", (row + 1, col)),
			("left", (row, col - 1)),
			("right", (row, col + 1))
		]

		result = []

		for action, (r, c) in candidates:
			if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
				result.append((action, (r, c)))
		return result

	def solve(self):

		self.num_explored = 0

		start = Node(state = self.start, parent = None, action = None)
		frontier = StackFrontier()
		frontier.add(start)

		self.explored = []

		while True:

			if frontier.empty():
				raise Exception ("No solution")

			node = frontier.remove()

			self.num_explored += 1

			if node.state == self.goal:
				self.explored.append(node.state)
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions, cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and state not in self.explored:
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)

class BFSMaze(DFSMaze):
	def solve(self):
		self.num_explored = 0

		start = Node(state = self.start, parent = None, action = None)
		frontier = QueueFrontier()
		frontier.add(start)

		self.explored = []

		while True:

			if frontier.empty():
				raise Exception ("No solution")

			node = frontier.remove()

			self.num_explored += 1

			if node.state == self.goal:
				self.explored.append(node.state)
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions, cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and state not in self.explored:
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)

class GreedyBestFirstMaze(DFSMaze):

	def determineCost(self, node):
		#heuristic function
		node.cost = abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1])
		
	def solve(self):
		self.num_explored = 0

		start = Node(state = self.start, parent = None, action = None)
		frontier = GreedyBestFirst()
		frontier.add(start)

		self.explored = []

		while True:

			if frontier.empty():
				raise Exception ("No solution")

			for node in frontier.frontier:
				self.determineCost(node)

			node = frontier.remove()

			self.num_explored += 1

			if node.state == self.goal:
				self.explored.append(node.state)
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions, cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and state not in self.explored:
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)

class AstarMaze(DFSMaze):

	def determineCost(self, node):
		#heuristic function
		h = abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1])

		#cost to reach node
		g = 0
		parent = node.parent
		while parent is not None:
			parent = parent.parent
			g += 1

		node.cost = h + g 
		
	def solve(self):
		self.num_explored = 0

		start = Node(state = self.start, parent = None, action = None)
		frontier = Astar()
		frontier.add(start)

		self.explored = []

		while True:

			if frontier.empty():
				raise Exception ("No solution")

			for node in frontier.frontier:
				self.determineCost(node)

			node = frontier.remove()

			self.num_explored += 1

			if node.state == self.goal:
				self.explored.append(node.state)
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions, cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and state not in self.explored:
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)