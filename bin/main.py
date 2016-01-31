import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from src.file_reader import FileReader
from src.file_writer import FileWriter
from src.run_info import RunInfo
from src.sudoku_solver import SudokuSolver
from src.input_information import InputInformation

if __name__ == '__main__':
    info = RunInfo()
    info.total_start = time.time()
    info.preprocessing_start = time.time()
    info.preprocessing_done = time.time()
    if(len(sys.argv) != 4):
        print('Only parameters for simple backtracking accepted right now')
        quit()
    else:
        input_info = InputInformation(sys.argv)

    try:
        input_file = open(input_info.input_file, 'r')
        output_file = open(input_info.output_file, 'w')
    except:
        print('Error opening file')
        quit()

    file_reader = FileReader(input_file)
    file_writer = FileWriter(output_file)
    N, P, Q,  = file_reader.get_params()
    board = file_reader.get_board()
    sudoku_board =  SudokuSolver(N, P, Q, board)
    info.search_start = time.time()
    sudoku_board.start_time = info.search_start
    sudoku_board.time_out_limit = float(input_info.timeout_limit)
    solved_board = sudoku_board.solve_board()
    info.search_done = time.time()
    if solved_board is not None:
        if solved_board.solved:
            info.status = info.status_types["s"]
            info.solution = solved_board.board_to_output()
        else:
            info.status = info.status_types["t"]
            info.count_nodes = solved_board.nodes_created
            info.count_deadends = solved_board.times_backtracked
            info.solution = info.generate_empty_board(N)
    else:
        info.status = info.status_types["e"]
        info.solution = info.generate_empty_board(N)

    file_writer.write_to_output(info)