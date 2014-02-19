# coding=utf-8
import sys

Te = 0
Tr = 1
Tw = 2

def gen_row(size, row = 0):
	print(row, size)
	return [Te] * (size if row%2 else (size-1))

def gen_board(size):
	f = lambda x: gen_row(size, x)
	return [f(x) for x in range((size*2)+1)]

def dup_board(board):
	b = []
	for r in board:
		n = []
		for c in r:
			n.append(c)
		b.append(n)
	return b

def make_move(board, move, token):
	board = dup_board(board)
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

def print_board(board, pre = ''):
	def gf(y):
		return lambda x: token_glyph(x, y)
	for y in range(len(board)):
		r = board[y]
		c = row_color(y)
		dot = '%s·' % col_esc(c)
		p = '%s%s%s ' % (pre, '' if y%2 else '  ', dot)
		e = ' %s' % dot
		print("%s%s%s\033[0m" % (p, (' %s ' %dot).join(map(gf(y), r)), e))

# operations (row, index, 1)
def avail_moves(board):
	ops = []
	for y in range(len(board)):
		for x in range(len(board[y])):
			if x == 0 and y == 0:
				continue
			if x == 0 and y == len(board):
				continue
			if x == len(board[y]) and y == 0:
				continue
			if x == len(board[y]) and y == len(board):
				continue
			if board[y][x] == Te:
				ops.append((y, x))
	return ops

# for red rows:
#  red: <=>, V> ^> V ^
#  wht : V2 ^2 V V> ^ ^>
# for white rows:
#  ^< ^
#  red: V2 ^2 V V> ^ ^>
#  wht: <=> V> ^> V ^
def adjacent_points(p, board):
	ps = []
	tc = board[p[0]][p[1]]
	if row_color(p[0]) == Tr:
		if p[0] > 0:
			ps.append((p[0]-1, p[1]))
			ps.append((p[0]-1, p[1]+1))
		if p[0] < len(board)-1:
			ps.append((p[0]+1, p[1]))
			ps.append((p[0]+1, p[1]+1))
		if tc == Tr:
			if p[1] > 0:
				ps.append((p[0], p[1]-1))
			if p[1] < len(board[p[0]])-1:
				ps.append((p[0], p[1]+1))
		elif tc == Tw:
			if p[0] > 3:
				ps.append((p[0]-2, p[1]))
			if p[0] < len(board)-3:
				ps.append((p[0]+2, p[1]))
	if row_color(p[0]) == Tw:
		if p[1] > 0:
			ps.append((p[0]-1, p[1]-1))
			ps.append((p[0]+1, p[1]-1))
		if p[1] < len(board[p[0]])-1:
			ps.append((p[0]-1, p[1]))
			ps.append((p[0]+1, p[1]))
		if tc == Tr:
			if p[0] > 2:
				ps.append((p[0]-2, p[1]))
			if p[0] < len(board)-2:
				ps.append((p[0]+2, p[1]))
		elif tc == Tw:
			if p[1] > 0:
				ps.append((p[0], p[1]-1))
			if p[1] < len(board[p[0]])-1:
				ps.append((p[0], p[1]+1))
	return ps

def point_in_set(point, sett):
	for p in sett:
		if point[0] == p[0] and point[1] == p[1]:
			return True
	return False

def find_winner(board):
	for c in range(len(board[1])):
		if board[1][c] != Tr:
			continue
		sopen = [(1, c)]
		sclosed = []
		while len(sopen) > 0:
			toppe = sopen.pop(0)
			if toppe[0] == len(board)-2:
				return Tr
			sclosed.append(toppe)
			adj = adjacent_points(toppe, board)
			for a in adj:
				if a in sclosed:
					continue
				if board[a[0]][a[1]] != Tr:
					continue
				sopen.append(a)
	for c in range(1, len(board), 2):
		if board[c][0] != Tw:
			continue
		sopen = [(c, 0)]
		sclosed = []
		while len(sopen) > 0:
			toppe = sopen.pop(0)
			if toppe[1] == len(board[1])-1:
				return Tw
			sclosed.append(toppe)
			adj = adjacent_points(toppe, board)
			for a in adj:
				if a in sclosed:
					continue
				if board[a[0]][a[1]] != Tw:
					continue
				sopen.append(a)
	for r in board:
		for x in r:
			if x == Te:
				return None
	return False

count = 0
lcount = 0
def move_value(board, move, player, plymax, plymin, d = 1):
	global count
	global lcount
	nb = make_move(board, move, player)
	w = find_winner(nb)
	count+=1
	if count - lcount >= 100:
		print(count)
		lcount = count
	if w != None:
		if w == plymax:
			return 1
		elif w == plymin:
			return -1
		else:
			return 0
	avail = avail_moves(nb)
	v = None
	if player == plymax:
		v = -1000
		for a in avail:
			v = max(v, move_value(nb, a, plymin, plymax, plymin, d+1))
	else:
		v =  1000
		for a in avail:
			v = min(v, move_value(nb, a, plymax, plymax, plymin, d+1))
	return v

def best_move(board, moves, player, plymin):
	score = 0
	move = None
	for m in moves:
		s = move_value(board, m, player, player, plymin)
		print(m, s)
		if s > score:
			score = s
			move = m
	return move

board = gen_board(2)
print_board(board)
won = False
while not won:
	print('#')
	for t in [Tr, Tw]:
		print('-')
		if won == True:
			continue
		avail = avail_moves(board)
		best = best_move(board, avail, t, Tw if t == Tr else Tr)
		board = make_move(board, best, t)
		print_board(board)
		if find_winner(board) != None:
			won = True
winner = find_winner(board)
if winner == Tr:
	print('Red wins')
elif winner == Tw:
	print('White wins')
else:
	print('Nobody wins')
