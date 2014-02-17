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

def col_esc(t):
	return "\033[31m" if t == Tr else "\033[97m"

def token_glyph(x, r):
	if x == Te:
		return ' '
	col = row_color(r)
	isrow = x == col
	glyph = '-' if isrow else '|'
	colour = col_esc(col) if isrow else col_esc(Tw if col == Tr else Tr)
	return "%s%s" % (colour, glyph)

def print_board(board):
	def gf(y):
		return lambda x: token_glyph(x, y)
	for r in board:
		c = row_color(len(r))
		dot = '%s·' % col_esc(c)
		p = '%s ' % dot if len(r)%2 else ''
		e = ' %s' % dot if len(r)%2 else ''
		print("%s%s%s\033[0m" % (p, (' %s ' %dot).join(map(gf(len(r)), r)), e))

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
			if bc[r][0] == Tw:
				score = 2
			else:
				rowscore = 0
				for l in range(len(bc[r])):
					if bc[r][l] == Tw:
						rowscore += 1
				score = max(score, rowscore)
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

def determine_win(board):
	winner = None
	reds = [True] * len(board[1])
	for r in range(1, len(board), 2):
		for x in range(0, len(board[r])):
			if board[r][x] != Tr:
				reds[x] = False
	if True in reds:
		return Tr

board = gen_board(6)
print_board(board)
for i in range(2):
	for t in [Tr, Tw]:
		avail = available_operations(board, t)
		best = best_move(board, avail, t)
		print(avail)
		make_move(board, best, t)
		print_board(board)
		print(determine_win(board))

