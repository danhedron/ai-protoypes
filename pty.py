# coding=utf-8
Te = 0
Tr = 1
Tw = 2

def gen_row(size, row = 0):
	return [Te] * (size-1 if row%2 else size)

def gen_board(size):
	f = lambda x: gen_row(size, x)
	return [f(x) for x in range((size*2)-1)]

def dup_board(board):
	b = []
	for r in board:
		n = []
		for c in r:
			n.append(c)
		b.append(n)
	return b

def make_move(board, move, token):
	board[move[0]][move[1]] = token
	return board

def row_color(r):
	return Tw if r%2 else Tr

def token_glyph(x, r):
	if x == Te:
		return ' '
	return '-' if x == row_color(r) else '|'

def print_board(board):
	def gf(y):
		return lambda x: token_glyph(x, y)
	for r in board:
		c = row_color(len(r))
		p = '· ' if len(r)%2 else ''
		e = ' ·' if len(r)%2 else ''
		print("%s %s%s%s" % (c, p, ' · '.join(map(gf(len(r)), r)), e))

def move_value(board, move, token):
	bc = dup_board(board)
	nb = make_move(bc, move, token)
	score = 0
	if token == Tr:
		for r in range(1, len(bc), 2):
			if Tr in bc[r]:
				score += 1
	elif token == Tw:
		for r in range(1, len(bc), 2):
			score = max(score, bc[r].count(Tw))
	return score

# operations (row, index, 1)
def available_operations(board, token):
	ops = []
	for y in range(len(board)):
		for x in range(len(board[y])):
			if x == 0 and y == 0:
				continue
			if x == 0 and y == len(board)-1:
				continue
			if x == len(board[y])-1 and y == 0:
				continue
			if x == len(board[y])-1 and len(board)-1:
				continue
			if board[y][x] == Te:
				v = move_value(board, (y, x), token)
				ops.append((y, x, v))
	return ops

def best_move(board, moves, token):
	score = 0
	move = None
	for m in moves:
		if m[2] > score:
			print(m)
			score = m[2]
			move = m
	return move

board = gen_board(6)
print_board(board)
for i in range(1):
	avail = available_operations(board, Tr)
	print(avail)
	best = best_move(board, avail, Tr)
	print(best)
	make_move(board, best, Tr)
	print_board(board)

