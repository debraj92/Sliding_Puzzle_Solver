import math


class SlidingTileBoard:

    def __init__(self, tile_board: list, costType: bool):
        self.board = []
        self.hashValue = 0
        self.EmptyCellCoordinates = tuple()
        self.heuristic = 0
        self.pathLength = 0
        self.actual_xy = {}
        self.manhattanDistanceCache = {}
        self.NON_UNIFORM_COST = costType

        k = 0
        for r in range(4):
            row = []
            for c in range(4):
                row.append(tile_board[k])
                self.actual_xy[k] = (r, c)
                if tile_board[k] == 0:
                    self.EmptyCellCoordinates = (r, c)
                k += 1
            self.board.append(row)

        for r in range(4):
            for c in range(4):
                tileValue = self.getTile([r, c])
                if tileValue == 0:
                    continue
                self.hashValue ^= (r * 4 + c) << (tileValue * 4)
                actual_coordinates = self.actual_xy[self.board[r][c]]
                if self.NON_UNIFORM_COST:
                    self.heuristic += self.manhattanDistance((r, c), actual_coordinates) * self.gCostWeighted((r, c))
                else:
                    self.heuristic += self.manhattanDistance((r, c), actual_coordinates) * self.gCost()

        for i in range(1, 16):
            actual_coordinates = self.actual_xy[i]
            for r in range(4):
                for c in range(4):
                    self.manhattanDistanceCache[(r, c, actual_coordinates[0], actual_coordinates[1])] = self.manhattanDistance((r, c), actual_coordinates)

    def printBoard(self):
        for r in range(4):
            for c in range(4):
                if self.board[r][c] >= 10:
                    print("  " + str(self.board[r][c]), end='')
                else:
                    print("   " + str(self.board[r][c]), end='')

            print()
        print()

    def getX(self, coordinates: list) -> int:
        return coordinates[0]

    def getY(self, coordinates: list) -> int:
        return coordinates[1]

    def manhattanDistance(self, source: tuple, destination: tuple):
        return abs(source[0] - destination[0]) + abs(source[1] - destination[1])

    def getTile(self, coordinates: list) -> int:
        return self.board[coordinates[0]][coordinates[1]]

    def setTile(self, coordinates, tile_value) -> int:
        self.board[self.getX(coordinates)][self.getY(coordinates)] = tile_value

    def move(self, move_object: tuple) -> int:
        source = move_object[0]
        destination = move_object[1]

        # Enable when debugging
        '''
        if self.manhattanDistance(source, destination) > 1:
            print('ERROR: Cannot move to non-adjacent position')
            return -1

        if self.getTile(destination) != 0:
            print('ERROR: Cannot move to non-empty position')
            return -1
        '''

        # update heuristic
        actual_coordinates = self.actual_xy[self.board[source[0]][source[1]]]
        if self.NON_UNIFORM_COST:
            self.heuristic += (self.manhattanDistanceCache[destination + actual_coordinates] - self.manhattanDistanceCache[
                source + actual_coordinates]) * self.gCostWeighted(source)
        else:
            self.heuristic += self.manhattanDistanceCache[destination + actual_coordinates] - self.manhattanDistanceCache[
                    source + actual_coordinates]

        # remove old hash
        self.hashValue ^= (source[0] * 4 + source[1]) << (self.board[source[0]][source[1]] * 4)

        # actual move
        self.board[destination[0]][destination[1]] = self.board[source[0]][source[1]]
        self.board[source[0]][source[1]] = 0
        self.EmptyCellCoordinates = source

        # add new hash
        self.hashValue ^= (destination[0] * 4 + destination[1]) << (self.board[destination[0]][destination[1]] * 4)

        return 1

    def undoMove(self, move_object: tuple, move_err):
        # Enable when debugging
        '''
        if move_err == -1:
            print('ERROR: Cannot undo move, since move was unsuccessful')
            return move_err
        '''

        return self.move((move_object[1], move_object[0]))

    def isSolved(self):
        return round(self.heuristic) == 0

    def gCost(self):
        return 1

    def gCostWeighted(self, tileCoordinate: tuple):
        tileValue = self.board[tileCoordinate[0]][tileCoordinate[1]]
        return round((tileValue + 2) / (tileValue + 1), 3)

    def generateValidMoves(self, parent_move: tuple):
        listOfValidMoves = []
        # Enable for debugging
        # assert len(self.EmptyCellCoordinates) > 0
        destination = self.EmptyCellCoordinates
        x = self.EmptyCellCoordinates[0]
        y = self.EmptyCellCoordinates[1]
        if x > 0 and parent_move[1] != (x - 1, y):
            listOfValidMoves.append(((x - 1, y), destination))
        if x < 3 and parent_move[1] != (x + 1, y):
            listOfValidMoves.append(((x + 1, y), destination))

        if y > 0 and parent_move[1] != (x, y - 1):
            listOfValidMoves.append(((x, y - 1), destination))
        if y < 3 and parent_move[1] != (x, y + 1):
            listOfValidMoves.append(((x, y + 1), destination))

        return tuple(listOfValidMoves)

    def serializeBoardToString(self):
        result = ""
        for r in range(4):
            for c in range(4):
                result += str(self.getTile([r, c])) + " "

        return result
