import random

class Board:
    
    __letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, rows = 1, cols = 1):
        self.__rows = rows
        self.__cols = cols
        self.__tiles = "_" * (rows * cols)
        
    @property
    def rows(self):
        return self.__rows
    
    @rows.setter
    def rows(self, rows):
        self.__rows = rows

    @property
    def cols(self):
        return self.__cols
    
    @cols.setter
    def cols(self, cols):
        self.__cols = cols

    def axis_to_pos(self, row, col):
        assert self.inside(row, col)
        return row * (self.__cols) + col

    def pos_to_axis(self, pos):
        c = pos % self.__cols
        r = pos // self.__cols
        return r, c

    def get_tile(self, row, col):
        assert self.inside(row, col)
        return self.__tiles[self.axis_to_pos(row, col)]

    def set_tile(self, row, col, letter):
        assert self.inside(row, col)
        p = self.axis_to_pos(row, col)
        self.__tiles = self.__tiles[:p] + letter + self.__tiles[p+1:]

    def get_tiles(self):
        return self.__tiles

    def set_tiles(self, tiles):
        self.__tiles = tiles
        padding = self.__rows * self.__cols - len(tiles)
        self.__tiles = self.__tiles + ("-" * padding) 

    def show(self):
        for r in range(self.__rows):
            for c in range(self.__cols):
                self.draw_tile(r, c)
            print("")

    def inside(self, row, col):
        return row >= 0 and col >= 0 and row < self.__rows and col < self.__cols

    def inside_pos(self, pos):
        return pos >= 0 and pos < self.__rows * self.__cols

    def draw_tile(self, row, col):
        pass

    def fill_random(self):
        self.__tiles = ''
        for _ in range(self.__rows * self.__cols - 1):
            letter  = random.choice(self.__letters)
            self.__tiles += letter
        self.__tiles += '_'

    def fixed(self, r, c):
        return False

    def empty(self, r, c):
        return self.get_tile(r, c) == '_'

    def moved_position(self, r, c, d):
        dr = {0: -1, 1: 0, 2: 1, 3:  0}
        dc = {0:  0, 1: 1, 2: 0, 3: -1}
        return r + dr[d], c + dc[d]

    def get_random_postion(self):
        r = random.choice(range(self.__rows))
        c = random.choice(range(self.__cols))
        return r, c

    def find_path_at(self, word, row, col, depth, path):
        adjacent_rc = [(r,c) for (r,c) in [self.moved_position(row, col, d) for d in [0, 1, 2, 3]] if self.inside(r,c) and not self.empty(r,c) and not (r,c) in path]
        random.shuffle(adjacent_rc)
        for r,c in adjacent_rc:
            if(depth < len(word)-1):
                return self.find_path_at(word, r,c, depth + 1, path + [(row,col)])
            else:
                # full word path found, so, set letters now
                path.append((row, col))
                for i in range(len(word)):
                    self.set_tile(path[i][0], path[i][1], word[i])
                return True
        return False

    def set_word(self, word):
        # select start position
        r, c = self.get_random_postion()        
        while self.fixed(r, c) or self.empty(r,c):
            r, c = self.get_random_postion()
        
        # set letters
        self.find_path_at(word, r, c, 0, [])
         

    def solved_at(self, word, row, col, depth = 0):
        #if depth > len(word):
        #    return False
        
        adjacent_rc = [self.moved_position(row, col, d) for d in [0, 1, 2, 3]]
        adjacent_rc_inside = [(r,c) for (r,c) in adjacent_rc if self.inside(r,c)]
        neighbors= [self.get_tile(r,c) for r,c in adjacent_rc_inside]

        for i in range(len(neighbors)):
            if neighbors[i] == word[depth + 1]:
                if depth + 1 == len(word) - 1:
                    return True
                else:
                    return self.solved_at(word, adjacent_rc_inside[i][0], adjacent_rc_inside[i][1], depth + 1)

        return False

    def solved(self, word):
        # get postions of first letter
        p = 0
        s = 0
        lp = []
        while(p >= 0):
            p = self.__tiles.find(word[0], s)
            if p >= 0:
                s = p + 1       
                lp.append(self.pos_to_axis(p))
        
        # check solved in every found position
        for r,c in lp:
            if self.solved_at(word, r, c):
                return True
        
        return False
    
    def swap_tiles(self, row, col, new_row, new_col):
        t = self.get_tile(row, col)
        self.set_tile(row, col, self.get_tile(new_row, new_col))
        self.set_tile(new_row, new_col, t)

    def mess(self, level):
        # find empty tile
        r, c = self.pos_to_axis(self.__tiles.find("_"))
        prev_r, prev_c = -1, -1

        # random moves
        for _ in range(level) :
            adjacent_rc = [self.moved_position(r, c, d) for d in [0, 1, 2, 3]]
            adjacent_rc_inside = [(r, c) for (r, c) in adjacent_rc if self.inside(r, c) and (r, c) != (prev_r, prev_c)]
            nr, nc = random.choice(adjacent_rc_inside)
            self.swap_tiles(r, c, nr, nc)
            prev_r, prev_c = r, c
            r, c = nr, nc

    def touch(self, row, col):
        adjacent_rc = [self.moved_position(row, col, d) for d in [0, 1, 2, 3]]
        adjacent_rc_inside = [(r,c) for (r,c) in adjacent_rc if self.inside(r,c)]
        neighbors= [self.get_tile(r,c) for r,c in adjacent_rc_inside]
        if '_' in neighbors:
            i = neighbors.index('_')
            r, c = adjacent_rc_inside[i]
            self.swap_tiles(row, col, r, c)










        
                