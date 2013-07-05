# pysnake.py - This is a CLI snake game written in Python 2.7.
# Inspired by Skylersun <git@github.com:Skylersun/PyMineSweeper.git>
# Copyright (c) 2013-2013, Weiwei Hu <huww06@gmail.com>
# All rights reserved.
import random
from time import gmtime, strftime
import urwid

__version__ = '0.0.1'
__author__ = 'Weiwei Hu <huww06@gmail.com>'


palette = [
    ('default_color', 'default', 'default'),
    ('snake_color', 'dark red', 'default'),
    ('bean_color', 'dark blue', 'default')]
"""
         (-1, 0)
(0, -1)    c    (0, 1)
         (1, 0)
"""
move_dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
turn_dir = {
    (-1, 0): [(0, 1), (0, -1), (1, 0)],
    (1, 0): [(0, -1), (0, 1), (-1, 0)],
    (0, -1): [(-1, 0), (1, 0), (0, 1)],
    (0, 1): [(1, 0), (-1, 0), (0, -1)]
}


class PySnake():
    """
    The pysnake class.
    """
    def __init__(self, display):
        self.display = display
        self.started = False
        self.stopped = False
        self.start_time = None
        self.cols = 30
        self.rows = 30
        self.mmap = []
        self.queue = []
        self.head = None
        self.tail = None
        self.length = 8
        self.score = 0
        # start to build the mmap
        for x in range(self.rows):
            line = []
            for y in range(self.cols):
                line.append('*')
            self.mmap.append(line)
        # randomize the header
        hx = random.randrange(0, self.cols)
        hy = random.randrange(0, self.rows)
        self.head = (hx, hy)
        self.queue.append((hx, hy))
        self.mmap[hx][hy] = 'h'
        length = self.length - 1
        while 1:
            if length == 0:
                break
            if hx > 0:
                hx -= 1
            else:
                hy += 1
            self.mmap[hx][hy] = 'x'
            self.queue.append((hx, hy))
            length -= 1
        self.tail = (hx, hy)
        # randomize the bean
        self._random_bean()

    def _draw(self):
        """
        Convert the mmap array to displayed text.
        """
        text = []
        for l in self.mmap:
            line = []
            for c in l:
                if c == '*':
                    line.append(('default_color', ' ' + c + ' '))
                elif c == 'x' or c == 'h':
                    line.append(('snake_color', ' ' + c + ' '))
                elif c == 'b':
                    line.append(('bean_color', ' ' + c + ' '))
            line.append('\n')
            text.append(line)
        text.append(['Score: ' + str(self.score) + '\n'])
        return text

    def move(self, straight='s', move_tail=True):
        """
        Move one step.
        """
        if straight == 's':
            _turn = 2
        elif straight == 'l':
            _turn = 0
        elif straight == 'r':
            _turn = 1
        hx, hy = self.head
        dx, dy = self._sub(self.queue[1], self.queue[0])
        ndx, ndy = turn_dir[(dx, dy)][_turn]
        nx, ny = self._add(self.head, (ndx, ndy))
        if self._used((nx, ny)):
            return
        self.mmap[hx][hy] = 'x'
        self.head = (nx, ny)
        self.queue.insert(0, (nx, ny))
        if self.mmap[nx][ny] == 'b':
            self.score += 1
            self._random_bean()
            move_tail = False
        self.mmap[nx][ny] = 'h'
        if move_tail:
            self.mmap[self.tail[0]][self.tail[1]] = '*'
            self.tail = self.queue[-2]
            self.queue.pop()
        else:
            self.length += 1
        text = self._draw()
        self.display.set_text(text)

    def _random_bean(self):
        # randomize the bean
        while 1:
            hx = random.randrange(0, self.cols)
            hy = random.randrange(0, self.rows)
            if self._used((hx, hy)) is False:
                self.mmap[hx][hy] = 'b'
                break
            if self.length == self.cols * self.rows:
                break

    def _used(self, p):
        if p[0] < 0 or p[0] >= self.rows or p[1] < 0 or p[1] >= self.cols:
            return True
        elif self.mmap[p[0]][p[1]] == 'x' or self.mmap[p[0]][p[1]] == 'h':
            return True
        else:
            return False

    def _add(self, l, r):
        return (l[0] + r[0], l[1] + r[1])

    def _sub(self, l, r):
        return (l[0] - r[0], l[1] - r[1])

    def start(self):
        self.started = True
        self.start_time = strftime("%d %b %Y %X", gmtime())
        text = '   * *   * *\n'
        text += ' *   *     *\n'
        text += '*             *\n'
        text += '*             *\n'
        text += ' *           *\n'
        text += '  *       *\n'
        text += '   *   *\n'
        text += '     * \n'
        self.display.set_text(self._draw())

    def key_press(self, key):
        if key == 'h':
            self.move('l')
        elif key == 'l':
            self.move('r')
        elif key == 's':
            self.move('s')


if __name__ == "__main__":
    display = urwid.Text(u"Hello World", align="center")
    fill = urwid.Filler(display, 'middle')
    pysnake = PySnake(display)
    pysnake.start()
    loop = urwid.MainLoop(fill, palette, unhandled_input=pysnake.key_press)
    loop.run()
