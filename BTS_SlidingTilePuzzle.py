from SlidingTileBoard import SlidingTileBoard
import time


class BTS_SlidingTilePuzzle:

    def __init__(self):
        self.games = []
        self.fetchAllGames()
        self.INFINITY = 1000000
        self.solutionCost = self.INFINITY
        self.nodeBudget = 0
        self.nodes = 0
        self.fCostBound = []
        self.solutionLowerBound = self.INFINITY
        self.f_above = self.INFINITY
        self.f_below = 0
        self.c1 = 2
        self.c2 = 8

    def fetchAllGames(self):
        korfInstancesFilename = "korf100.txt"
        with open(korfInstancesFilename) as file:
            for line in file:
                game = line.rstrip().split()
                if len(game) == 0:
                    continue
                game.pop(0)
                gameTiles = [eval(i) for i in game]
                self.games.append(gameTiles)

    def sortFunction(self, move: list, gameState: SlidingTileBoard):
        source = move[0]
        destination = move[1]
        actual_coordinates = gameState.actual_xy[gameState.board[source[0]][source[1]]]
        oldHeuristic = gameState.manhattanDistance(source, [actual_coordinates[0], actual_coordinates[1]])
        newHeuristic = gameState.manhattanDistance(destination, [actual_coordinates[0], actual_coordinates[1]])
        return newHeuristic - oldHeuristic

    def limitedDfs(self, gameState: SlidingTileBoard, pathCost: int, costLimit: int, nodesLimit: int,
                   path: list, parent_move_destination: list):
        g_cost = pathCost + gameState.gCost()
        f = g_cost + gameState.heuristic
        if self.solutionCost == self.solutionLowerBound:
            return False
        elif f > costLimit:
            self.f_above = min(self.f_above, f)
            return False
        elif f >= self.solutionCost:
            self.f_below = self.solutionCost
            return False
        else:
            self.f_below = max(f, self.f_below)

        if self.nodes >= nodesLimit:
            return False

        if gameState.isSolved():
            self.solutionCost = f
            path.append(gameState.serializeBoardToString())
            return True

        validMoves = gameState.generateValidMoves(parent_move_destination)
        validMoves = sorted(validMoves, key=lambda m: self.sortFunction(m, gameState))

        for move in validMoves:
            moved = gameState.move(move)

            found = self.limitedDfs(gameState, g_cost, costLimit, nodesLimit, path, move[1])
            if found:
                path.append(gameState.serializeBoardToString())
            gameState.undoMove(move, moved)

            if found:
                return found

        return False

    def search(self, gameState: SlidingTileBoard, costLimit: int, nodeLimit: int, path: list):
        self.f_below = 0
        self.f_above = self.INFINITY
        self.nodes = 0
        self.limitedDfs(gameState, 0, costLimit, nodeLimit, path, [-1, -1])
        if self.nodes >= nodeLimit:
            return [0, self.f_below]
        elif self.f_below >= self.solutionCost:
            return [self.solutionCost, self.solutionCost]
        else:
            return [self.f_above, self.INFINITY]

    def solveWithBts(self, gameState: SlidingTileBoard, path: list):
        self.fCostBound = [gameState.heuristic, self.INFINITY]
        self.solutionCost = self.INFINITY
        self.nodeBudget = 0

        while self.solutionCost > self.fCostBound[0]:
            self.solutionLowerBound = self.fCostBound[0]
            self.fCostBound[1] = self.INFINITY

            '''
            Regular IDA*
            '''
            self.fCostBound = self.search(gameState, self.fCostBound[0], self.INFINITY, path)
            if self.nodes >= (self.c1 * self.nodeBudget):
                self.nodeBudget = self.nodes
                continue

            '''
            Exponential Search
            '''
            delta = 0
            while self.fCostBound[0] != self.fCostBound[1] and self.nodes < (self.c1 * self.nodeBudget):
                nextCost = self.fCostBound[0] + 2 ** delta
                delta = delta + 1
                self.solutionLowerBound = self.fCostBound[0]
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget))

            '''
            Binary Search
            '''
            while self.fCostBound[0] != self.fCostBound[1] and (
                    self.nodes < (self.c1 * self.nodeBudget) or self.nodes > (self.c2 * self.nodeBudget)):
                nextCost = (self.fCostBound[0] + self.fCostBound[1]) / 2
                self.solutionLowerBound = self.fCostBound[0]
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget))

            self.nodeBudget = max(self.nodes, (self.c1 * self.nodeBudget))

            if self.solutionCost == self.fCostBound[0]:
                return

    def solveAllGamesWithBTS(self):
        start_time = time.time()
        game = SlidingTileBoard(self.games[0])
        path = []
        self.solveWithBts(game, path)
        duration = time.time() - start_time
        print("--- %s s ---" % duration)
        if self.solutionCost < self.INFINITY:
            print('Solution Cost ', self.solutionCost)
            self.printSolution(path)

    def printSolution(self, path):
        path.reverse()
        print()
        for tileBoard in path:
            tileBoard = tileBoard.strip('|').split('|')
            gameTiles = [eval(i) for i in tileBoard]
            slidingTileBoardInstance = SlidingTileBoard(gameTiles)
            slidingTileBoardInstance.printBoard()

        print('Total moves ', len(path))
