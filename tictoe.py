def make_board():
	return [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]

def copy_board(board):
	nb = []
	for y in range(len(board)):
		rb = []
		for x in range(len(board)):
			rb.append(board[y][x])
		nb.append(rb)
	return nb

def avail_moves(board):
	m = []
	for y in range(len(board)):
		for x in range(len(board)):
			if board[y][x] == ' ':
				m.append((y, x))
	return m

def print_board(board):
	f = lambda l: '|'.join(l)
	print('\n------\n'.join(map(f, board)))

def find_line(board, x, y, dx, dy):
	ttype = board[y][x]
	if ttype == ' ':
		return False
	if board[y+dy][x+dx] != ttype:
		return False
	if board[y+(dy*2)][x+(dx*2)] != ttype:
		return False
	return True

def apply_move(board, move, ply):
	board = copy_board(board)
	board[move[0]][move[1]] = ply
	return board

def is_terminal(board):
	for y in range(len(board)):
		if find_line(board, 0, y, 1, 0):
			return board[y][0]
	for x in range(len(board)):
		if find_line(board, x, 0, 0, 1):
			return board[0][x]
	if find_line(board, 0, 0, 1, 1):
		return board[0][0]
	if find_line(board, 0, 2, 1, -1):
		return board[2][0]
	for r in board:
		for c in r:
			if c == ' ':
				return False
	return ' '

def utility(ply, board):
	t = is_terminal(board)
	if t == False or t == ' ':
		return 0
	elif t == ply:
		return 1
	else:
		return -1

def move_value(board, move, player, maxplayer, otherplayer):
	nb = apply_move(board, move, player)
	t = is_terminal(nb)
	if t != False:
		return utility(maxplayer, nb)
	av = avail_moves(nb)
	v = None
	if player == maxplayer:
		v = -1000
		for m in av:
			v = max(v, move_value(nb, m, otherplayer, maxplayer, otherplayer))
	else:
		v =  1000
		for m in av:
			v = min(v, move_value(nb, m, maxplayer, maxplayer, otherplayer))
	if v != None and False:
		print(v)
	return v

def determine_move(board, currentplayer, otherplayer):
	avail = avail_moves(board)
	best_move = None
	best_value = 0
	for m in avail:
		val = move_value(board, m, currentplayer, currentplayer, otherplayer)
		if val > best_value:
			best_move = m
	return m

board = make_board()
for i in range(100):
	for player,op in [('x','o'),('o', 'x')]:
		if is_terminal(board):
			break
		board = apply_move(board, determine_move(board, player, op), player)
		print_board(board)
		print(is_terminal(board))

