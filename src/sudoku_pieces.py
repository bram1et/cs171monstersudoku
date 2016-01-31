from __future__ import print_function
import copy

class Row:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def add_to_row(self, cell):
        self.cells.append(cell)

    def print_row(self):
        for cell in range(len(self.cells)):
            print(self.cells[cell].value, end=' ')
        print()

    def check_row(self, row_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_row()
#            raise ValueError('There is an error in row {}'.format(row_num))
            return False
        return True

    def update_domains(self):
        values_to_remove = []
        changes = dict()
        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)
        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, value):
        for cell in self.cells:
            if value not in cell.domain:
                cell.domain.append(value)

class Column:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def add_to_column(self, cell):
        self.cells.append(cell)

    def print_column(self):
        for cell in self.cells:
            print(cell.value, end='\n')

    def check_column(self, col_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_column()
#            raise ValueError('There is an error in column {}'.format(col_num))
            return False
        return True

    def update_domains(self):
        changes = dict()
        values_to_remove = []
        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)
        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, value):
        for cell in self.cells:
            if value not in cell.domain:
                cell.domain.append(value)

class Block:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []

    def add_to_block(self, cell):
        self.cells.append(cell)

    def print_block(self):
        break_point = self.cols
        for num_cells in range(len(self.cells)):
            print(self.cells[num_cells].value, end=' ')
            break_point -= 1
            if break_point == 0:
                print()
                break_point = self.cols

    def check_block(self, block_num):
        cell_values = []
        for cell in self.cells:
            if cell.value != 0:
                cell_values.append(cell.value)
        if len(set(cell_values)) != len(cell_values):
#            self.print_block()
#            raise ValueError('There is an error in block {}'.format(block_num))
            return False
        return True

    def update_domains(self):
        values_to_remove = []
        changes = dict()

        for this_cell in self.cells:
            if this_cell.value != 0:
                values_to_remove.append(this_cell.value)

        for this_cell in self.cells:
            changes[self.cells.index(this_cell)] = []
            if not this_cell.set:
                for value_to_remove in values_to_remove:
                    if this_cell.check_if_in_domain(value_to_remove):
                        this_cell.remove_from_domain(value_to_remove)
                        changes[self.cells.index(this_cell)].append(value_to_remove)
        return changes

    def add_to_domains(self, value):
        for cell in self.cells:
            if value not in cell.domain:
                cell.domain.append(value)



class Cell:
    def __init__(self, domain, value=0):
        self.value = value
        self.domain = [value] if value != 0 else domain
        self.set = True if value != 0 else False

    def remove_from_domain(self, value):
        self.domain.remove(value)

    def check_if_in_domain(self, value):
        return value in self.domain


class Sudoku:
    def __init__(self, N, P, Q, board_values):
        self.n = N
        self.p = P
        self.q = Q
        self.rows = []
        self.columns = []
        self.blocks = []
        self.board_values = board_values
        self.domain = self.get_domain()
        self.check_board_params()
        self.initialize_board()

    def get_block_num(self, row, col):
        return (int(row/self.p) + int(col/self.q)) + (row//self.p)

    def initialize_board(self):
        for count in range(self.n):
            self.rows.append(Row(self.n))
            self.columns.append(Column(self.n))
            self.blocks.append(Block(self.p, self.q))

        for row in range(self.n):
            for col in range(self.n):
                cell_value = self.board_values[row][col]
                new_cell = Cell(copy.copy(self.domain), cell_value)
                self.rows[row].add_to_row(new_cell)
                self.columns[col].add_to_column(new_cell)
                block_num = self.get_block_num(row, col)
                self.blocks[block_num].add_to_block(new_cell)

        for index in range(self.n):
            self.rows[index].check_row(index)
            self.columns[index].check_column(index)
            self.blocks[index].check_block(index)

            self.rows[index].update_domains()
            self.columns[index].update_domains()
            self.blocks[index].update_domains()

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
            print('Number of tokens cannot excede 35')
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




