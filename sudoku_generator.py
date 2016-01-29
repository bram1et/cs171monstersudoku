#!/usr/bin/python
import sys
import copy
import random

from sudoku_pieces import Row
from sudoku_pieces import Column
from sudoku_pieces import Block
from sudoku_pieces import Cell
from file_reader import FileReader

class SudokuBoardGenerator:
    def __init__(self, M, N, P, Q):
        self.m = M
        self.n = N
        self.p = P
        self.q = Q
        self.rows = []
        self.columns = []
        self.blocks = []
        self.domain = self.get_domain()
        print(self.domain)
        self.check_board_params()

    def get_domain(self):
        domain = []
        for i in range(self.n):
            if i < 9:
                domain.append(i + 1)
            else:
                domain.append(chr((i - 9) + 65))
        return domain

    def check_board_params(self):
        if self.n > 35:
            raise ValueError('Number of tokens cannot excede 35')
        if self.p <= 0 or self.q <= 0 or self.n <= 0:
            raise ValueError('All values must be greater than 0')
        if self.p * self.q != self.n:
            raise ValueError('N must equal P * Q')
        if self.m > self.n**2:
            raise ValueError('M must less than N^2')
#        if len(board) != self.n:
#            raise ValueError('Number of rows in board must equal N')
        return True

    def get_block_num(self, row, col):
        return (int(row/self.p) + int(col/self.q)) + (row//self.p)

    def create_empty_board(self):
        self.rows = []
        self.columns = []
        self.blocks = []

        for count in range(self.n):
            self.rows.append(Row(self.n))
            self.columns.append(Column(self.n))
            self.blocks.append(Block(self.p, self.q))

        for row in range(self.n):
            for col in range(self.n):
                new_cell = Cell(copy.copy(self.domain), 0)
                self.rows[row].add_to_row(new_cell)
                self.columns[col].add_to_column(new_cell)
                block_num = self.get_block_num(row, col)
                self.blocks[block_num].add_to_block(new_cell)


    def generate_board(self):
        self.create_empty_board()
        count = 0
        while(count < self.m):
#            print(count)
#            self.print_board()
#            print()
            for i in range(self.n**2):
                row = i // self.n
                col = i % self.n
                percent_Filled = self.m / float(self.n ** 2)
                if random.random() < percent_Filled:
                    domain = self.rows[row].cells[col].domain
                    if len(domain) > 0 and not self.rows[row].cells[col].set:
                        count += 1
                        self.rows[row].cells[col].value = random.choice(domain)
                        self.rows[row].cells[col].set = True

                        self.rows[row].update_domains()
                        self.columns[col].update_domains()
                        self.blocks[self.get_block_num(row, col)].update_domains()

                        self.rows[row].check_row(row)
                        self.columns[col].check_column(col)
                        self.blocks[self.get_block_num(row, col)].check_block(self.get_block_num(row, col))

                        if count == self.m:
                            break
                    elif len(domain) == 0:
                        self.print_board()
                        print(count)
                        count = 0
                        self.create_empty_board()

#        print(count)

    def print_board(self):
        for row in self.rows:
            row.print_row()

if __name__ == '__main__':

    sudoku_board =  SudokuBoardGenerator(14, 12, 4, 3)
    sudoku_board.generate_board()
    sudoku_board.print_board()


