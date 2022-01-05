"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 30, 2021
"""

def is_empty(board):

    for y in range(len(board)):
      for x in board[y]:
        if x != " ":
          return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):

  if y_end + d_y == -1 or y_end + d_y == len(board) or x_end + d_x == -1 or x_end + d_x == len(board[0]):
    end = "capped"
  else:
    end = board[y_end + d_y][x_end + d_x]

  if y_end - (length * d_y) == -1 or y_end - (length * d_y) == len(board) or x_end - (length * d_x) == -1 or x_end - (length * d_x) == len(board[0]):
    start = "capped"
  else:
    start = board[y_end - (length * d_y)][x_end - (length * d_x)]

  if end == " " and start == " ":
    return "OPEN"
  elif end == " " or start == " ":
    return "SEMIOPEN"
  else:
    return "CLOSED"


def read(board, coord):
  return board[coord[0]][coord[1]]

def whole_row(board, y_start, x_start, d_y, d_x):
  #returns the coordinates of an entire row on the board in the specified direction
  row = []
  coord = [y_start, x_start]

  while coord[0] < len(board) and coord[1] < len(board[0]) and coord[0] > -1 and coord[1] > -1:
    box = coord[:]
    row.append(box)
    coord[0] += d_y
    coord[1] += d_x

  return row


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count = 0
  semi_open_seq_count = 0
  row = whole_row(board, y_start, x_start, d_y, d_x)
  elems = []
  run = 1

  for i in row:
    elems.append(read(board, i))
  elems.append("end")

  #row contains the coordinates of the entire row across the board
  #elems contains the elements in each square in the row

  for j in range(1, len(elems)):

    if elems[j] != elems[j - 1]:
      if run == length and elems[j - 1] == col:
        if is_bounded(board, row[j - 1][0], row[j - 1][1], length, d_y, d_x) == "OPEN":
            open_seq_count += 1
        elif is_bounded(board, row[j - 1][0], row[j - 1][1], length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1

      run = 1

    else:
      run += 1


  #return is_bounded(board, row[j-1][0], row[j-1][1],length, d_y, d_x), open_seq_count, semi_open_seq_count
  return open_seq_count, semi_open_seq_count



def detect_rows(board, col, length):
  open_seq_count, semi_open_seq_count = 0, 0

  rows_left = whole_row(board, 0, 0, 1, 0)
  columns = whole_row(board, 0, 0, 0, 1)
  rows_right = whole_row(board, 0, len(board[0])-1, 1, 0)
  diagonals_l = columns[:]
  diagonals_l.extend(rows_left[1:])
  diagonals_r = columns[:]
  diagonals_r.extend(rows_right[1:])

  #top to bottom (1,0)
  for c in columns:
    count = detect_row(board, col, c[0], c[1], length, 1, 0)
    open_seq_count += count[0]
    semi_open_seq_count += count[1]

  #left to right (0,1)
  for r in rows_left:
    count = detect_row(board, col, r[0], r[1], length, 0, 1)
    open_seq_count += count[0]
    semi_open_seq_count += count[1]

  #upper left to lower right (1,1)
  for d in diagonals_l:
    count = detect_row(board, col, d[0], d[1], length, 1, 1)
    open_seq_count += count[0]
    semi_open_seq_count += count[1]

  #upper right to lower left (1,-1)
  for e in diagonals_r:
    count = detect_row(board, col, e[0], e[1], length, 1, -1)
    open_seq_count += count[0]
    semi_open_seq_count += count[1]

  return open_seq_count, semi_open_seq_count



def search_max(board):
  scores = []

  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] != " ":
        #keeps track of every sqaure on the board, regardless of if its empty or not
        scores.append(-99999999999999)
      else:
        board[i][j] = "b"
        scores.append(score(board))
        board[i][j] = " "

  #max_score_index = scores.index(max(scores))

  move_y = scores.index(max(scores)) // len(board[0])
  move_x = scores.index(max(scores)) % len(board)
  return move_y, move_x



#dont modify
def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win_helper(board, row, col):
  run = 1
  for i in range(1, len(row)):
    if read(board, row[i]) == read(board, row[i-1]) and read(board, row[i]) == col:
      run += 1
    else:
      run = 1
    if run == 5:
      if i == len(row)-1:
        return True
      else:
        if read(board, row[i+1]) != col:
          return True

  return False


def is_win(board):
  rows_left = whole_row(board, 0, 0, 1, 0)
  columns = whole_row(board, 0, 0, 0, 1)
  rows_right = whole_row(board, 0, len(board[0])-1, 1, 0)
  diagonals_l = columns[:]
  diagonals_l.extend(rows_left[1:])
  diagonals_r = columns[:]
  diagonals_r.extend(rows_right[1:])

  full = True


    #up down win
  for r in rows_left:
      if is_win_helper(board, whole_row(board, r[0], r[1], 0, 1), 'b') == True:
        return "Black won"

      elif is_win_helper(board, whole_row(board, r[0], r[1], 0, 1), 'w') == True:
        return "White won"

    #left right win
  for c in columns:
      if is_win_helper(board, whole_row(board, c[0], c[1], 1, 0), 'b') == True:
        return "Black won"
      elif is_win_helper(board, whole_row(board, c[0], c[1], 1, 0), 'w') == True:
        return "White won"

    #upper left to lower right win
  for d in diagonals_l:
      if is_win_helper(board, whole_row(board, d[0], d[1], 1, 1), 'b') == True:
        return "Black won"
      elif is_win_helper(board, whole_row(board, d[0], d[1], 1, 1), 'w') == True:
        return "White won"

    #upper right to lower left win
  for e in diagonals_r:
      if is_win_helper(board, whole_row(board, e[0], e[1], 1, -1), 'b') == True:
        return "Black won"
      elif is_win_helper(board, whole_row(board, e[0], e[1], 1, -1), 'w') == True:
        return "White won"

  #check if board is full
  for i in range(len(board)):
      for j in range(len(board[0])):
        if board[i][j] == " ":
          full = False

  if full == True:
    return "Draw"
  else:
    return "Continue playing"





#dont modify
def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


#dont modify
def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


#dont modify
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


#dont modify
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


#tests
def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 7; y = 0; d_x = -1; d_y = 1; length = 4
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 4, 3, d_y, d_x, 1, "b")
    print_board(board)

    y_end = 3
    x_end = 4

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'CLOSED':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = -1; d_y = 1; length = 3
    #put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    put_seq_on_board(board, y, x, d_y, d_x, 3, "w")

    print_board(board)
    print(detect_row(board, "w", 0,6,length,d_y,d_x))
    if detect_row(board, "w", 0,6,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 0, 0, 1, 1, 4, "w")
    put_seq_on_board(board, 7, 0, 0, 1, 3, "b")
    print_board(board)
    print(detect_rows(board, col, length))
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    print(search_max(board))

    if search_max(board) == (4,6):
      print("TEST CASE for search_max PASSED")
    else:
      print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
  #play_gomoku(8)
  some_tests()
  easy_testset_for_main_functions()