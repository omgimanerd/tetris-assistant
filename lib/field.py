#!/usr/bin/python

from tetromino import Tetromino

import numpy as np

class Field():

    WIDTH = 10
    HEIGHT = 22

    def __init__(self, state=None):
        """
        Initialize a Tetris Field.
        X increases to the right and Y increases downward (as normal).
        """
        if state is not None:
            self.state = np.array(state, dtype=np.uint8, copy=True)
        else:
            self.state = np.full((Field.HEIGHT, Field.WIDTH), 0, dtype=np.uint8)

    def __str__(self):
        bar = '   |' + ' '.join(map(str, range(Field.WIDTH))) + '|\n'
        mapped_field = np.vectorize(Tetromino.TYPES.__getitem__)(self.state)
        field = '\n'.join(['{:2d} |'.format(i) +
            ' '.join(row) + '|' for i, row in enumerate(mapped_field)])
        return bar + field + '\n' + bar

    def _test_tetromino(self, tetromino, r_end, c_start):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the bottom left corner of the
        tetromino at the specified row and column.
        """
        r_start, c_end = r_end - tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end >= Field.HEIGHT:
            return False
        test_area = self.state[r_start:r_end, c_start:c_end]
        for s, t in zip(test_area.flat, tetromino.flat()):
            if s != 0 and t != 0:
                return False
        return True

    def _place_tetromino(self, tetromino, r_end, c_start):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        r_start, c_end = r_end - tetromino.height(), c_start + tetromino.width()
        if c_start < 0 or c_end > Field.WIDTH:
            return False
        if r_start < 0 or r_end >= Field.HEIGHT:
            return False
        for tr, sr in enumerate(range(r_start, r_end)):
            for tc, sc, in enumerate(range(c_start, c_end)):
                if tetromino[tr][tc] != 0:
                    self.state[sr][sc] = tetromino[tr][tc]

    def _get_tetromino_drop_row(self, tetromino, column):
        """
        Given a tetromino and a column, return the row that the tetromino
        would end up in if it were dropped in that column.
        Assumes the leftmost column of the tetromino will be aligned with the
        specified column.
        """
        if column < 0 or column + tetromino.width() > Field.WIDTH:
            return -1
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def _line_clear(self):
        """
        Checks and removes all filled lines.
        """
        non_filled = np.array(
            [not row.all() and row.any() for row in self.state])
        if non_filled.any():
            tmp = self.state[non_filled]
            self.state.fill(0)
            self.state[Field.HEIGHT - tmp.shape[0]:] = tmp

    def copy(self):
        """
        Returns a shallow copy of the field.
        """
        return Field(self.state)

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column.
        The leftmost column of the tetromino will be aligned with the specified
        column.
        Returns the row it was dropped in for computations.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH

        row = self._get_tetromino_drop_row(tetromino, column)
        assert row != -1
        print(row, column)
        self._place_tetromino(tetromino, row, column)
        self._line_clear()
        return row

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        gaps = 0
        for col in self.state.T:
            begin = False
            for space in col:
                if space != Tetromino.TYPES_D[' ']:
                    begin = True
                elif begin:
                    gaps += 1
            begin = False
        return gaps

    def heights(self):
        h = Field.HEIGHT - 1
        return np.array([h - np.min(np.nonzero(col)) for col in self.state.T])

if __name__ == '__main__':
    f = Field()
    f._place_tetromino(Tetromino.ITetromino(), 21, 6)
    f._place_tetromino(Tetromino.ITetromino(), 21, 2)
    # f.drop(Tetromino.ITetromino(), 6)
    # f.drop(Tetromino.ITetromino(), 2)
    # f.drop(Tetromino.OTetromino(), 3)
    # f.drop(Tetromino.JTetromino().rotate_left(), 0)
    # f.drop(Tetromino.JTetromino().rotate_left(), 2)
    # f.drop(Tetromino.OTetromino(), 5)
    # f.drop(Tetromino.OTetromino(), 7)
    # f.drop(Tetromino.ITetromino(), 6)
    # f.drop(Tetromino.OTetromino(), 5)
    print(f)