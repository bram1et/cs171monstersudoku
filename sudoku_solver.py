from __future__ import print_function
import sys
import copy
import time
import random

from sudoku_pieces import Row
from sudoku_pieces import Column
from sudoku_pieces import Block
from sudoku_pieces import Cell
from file_reader import FileReader

class SudokuSolver:
    def __init__(self, N, P, Q, board_values):
        self.n = N
        self.p = P
        self.q = Q
        self.rows = []
        self.columns = []
        self.blocks = []
        self.board_values = board_values
        self.num_cells = self.n * self. n
        self.cells_solved = 0
        self.solved = False
        self.start_time = None
        self.time_out_limit = None
        self.nodes_created = 0
        self.times_backtracked = 0
        self.domain = self.get_domain()
        self.check_board_params()
        self.initialize_board()


    def get_block_num(self, row, col):
        return (int(row/self.p) + int(col/self.q)) + (row//self.p)

    def check_update(self, row_num, column_num, block_num):
        row_check = self.rows[row_num].check_row(row_num)
        column_check = self.columns[column_num].check_column(column_num)
        block_check = self.blocks[block_num].check_block(block_num)
        return row_check, column_check, block_check
#        row_changes = self.rows[row_num].update_domains()
#        col_changes = self.columns[column_num].update_domains()
#        block_changes = self.blocks[block_num].update_domains()
#        print('Row Changes', end=" ")
#        print(row_changes)
#        print('Column Changes', end=" ")
#        print(col_changes)
#        print('Block Changes', end=" ")
#        print(block_changes)

#    def add_back_to_domain(self, row_num, column_num, block_num, value):
#        self.rows[row_num].add_to_domains(value)
#        self.columns[column_num].add_to_domains(value)
#        self.blocks[block_num].add_to_domains(value)

    def initialize_board(self):
        for count in range(self.n):
            self.rows.append(Row(self.n))
            self.columns.append(Column(self.n))
            self.blocks.append(Block(self.p, self.q))

        for row in range(self.n):
            for col in range(self.n):
                cell_value = self.board_values[row][col]
                if cell_value != 0:
                    self.cells_solved += 1
                new_cell = Cell(copy.copy(self.domain), cell_value)
                self.rows[row].add_to_row(new_cell)
                self.columns[col].add_to_column(new_cell)
                block_num = self.get_block_num(row, col)
                self.blocks[block_num].add_to_block(new_cell)

        for index in range(self.n):
            self.check_update(index, index, index)

    def print_board(self):
        for row in self.rows:
            row.print_row()

    def get_domain(self):
        domain = []
        for i in range(self.n):
            if i < 10:
                domain.append(i + 1)
            else:
                domain.append(chr((i - 10) + 65))
        return domain

    def check_board_params(self):
        if self.n > 35:
            raise ValueError('Number of tokens cannot excede 35')
        if self.p <= 0 or self.q <= 0 or self.n <= 0:
            raise ValueError('All values must be greater than 0')
        if self.p * self.q != self.n:
            raise ValueError('N must equal P * Q')
        # if len(board) != self.n:
        #     raise ValueError('Number of rows in board must equal N')
        for row in self.board_values:
            if len(row) != self.n:
                raise ValueError('Number of columns in board must equal N')
            for cell in row:
                if cell not in self.domain and cell != 0:
                    raise ValueError('Value of a cell is not in domain')
        return True

    def print_domains(self):
        for row in self.rows:
            for col in range(self.n):
                print(row.cells[col].domain, end=" ")
            print()

    def solve_board(self, start_row=0, start_col=0):

        self.nodes_created += 1
        time_elapsed = time.time() - self.start_time
        if time_elapsed > self.time_out_limit:
            return self

        if self.cells_solved == (self.n * self.n):
            self.solved = True
            return self
        else:
            for row_num in range(start_row, self.n):
                for col_num in range(start_col, self.n):
                    this_cell = self.rows[row_num].cells[col_num]
                    if not this_cell.set:
                        for value in self.domain:
                            this_cell.value = value
#                            print(value, row_num, col_num, self.cells_solved)
#                             print("Trying {0} at location ({0}, {0}). {0} Solved".format(value, row_num, col_num, self.cells_solved))
#                            self.print_board()
                            row_ok, col_ok, block_ok = self.check_update(row_num, col_num, self.get_block_num(row_num, col_num))
                            if row_ok and col_ok and block_ok:
                                self.cells_solved += 1
                                this_cell.set = True
                                if col_num == self.n - 1:
                                    next_row = row_num + 1
                                    next_col = 0
                                else:
                                    next_row = row_num
                                    next_col = col_num + 1
                                solved_board = self.solve_board(next_row, next_col)
                                if solved_board != None:
                                    return solved_board
                                else:
                                    self.times_backtracked += 1
                                    self.cells_solved -= 1
                            else:
                                this_cell.value = 0
                                this_cell.set = False
#                                self.cells_solved -= 1
                        this_cell.value = 0
                        this_cell.set = False
                        return None
                    else:
                        if col_num == self.n - 1:
                            row_num = row_num + 1
                            col_num = 0
                start_row = 0
                start_col = 0
        return None

    def board_to_output(self):
        output_string = "("
        for row in self.rows:
            for col in range(self.n):
                output_string += str(row.cells[col].value)
                output_string += ","
        output_string = output_string[:-1]
        output_string += ")"
        return output_string


