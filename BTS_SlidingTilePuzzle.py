from SlidingTileBoard import SlidingTileBoard
import time


class BTS_SlidingTilePuzzle:

    def __init__(self):
        self.games = []
        self.fetchAllGames()
        self.INFINITY = 100000000000000000000000
        self.solutionCost = self.INFINITY
        self.nodeBudget = 0
        self.nodes = 0
        self.fCostBound = []
        self.solutionLowerBound = self.INFINITY
        self.f_above = self.INFINITY
        self.f_below = 0
        self.c1 = 2
        self.c2 = 9.5
        self.visited = {}
        self.dontUpdateCache = False

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

    def sortFunction(self, move: tuple, gameState: SlidingTileBoard):
        source = move[0]
        destination = move[1]
        actual_coordinates = gameState.actual_xy[gameState.board[source[0]][source[1]]]

        if gameState.NON_UNIFORM_COST:
            return (1 + gameState.manhattanDistanceCache[destination + actual_coordinates] -
                    gameState.manhattanDistanceCache[
                        source + actual_coordinates]) * gameState.gCostWeighted(source)

        return gameState.manhattanDistanceCache[destination + actual_coordinates] - gameState.manhattanDistanceCache[
            source + actual_coordinates]

    def limitedDfs(self, gameState: SlidingTileBoard, pathCost: int, costLimit: float, nodesLimit: int,
                   path: list, parent_move: tuple):

        if self.solutionCost == self.solutionLowerBound:
            return False

        f = pathCost + gameState.heuristic

        self.f_below = max(f, self.f_below)

        if self.nodes >= nodesLimit:
            return False

        validMoves = gameState.generateValidMoves(parent_move)
        validMoves = sorted(validMoves, key=lambda m: self.sortFunction(m, gameState))

        self.nodes += 1
        for move in validMoves:
            moved = gameState.move(move)
            if gameState.NON_UNIFORM_COST:
                g_cost = pathCost + gameState.gCostWeighted(move[1])
            else:
                g_cost = pathCost + gameState.gCost()
            f = g_cost + gameState.heuristic

            if gameState.isSolved():
                self.solutionCost = f
                path.append(gameState.serializeBoardToString())
                gameState.undoMove(move, moved)
                return True

            found = False
            boundExceeded = False

            if f > costLimit:
                self.f_above = min(self.f_above, f)
                boundExceeded = True
            elif f >= self.solutionCost:
                self.f_below = self.solutionCost
                boundExceeded = True
            else:
                cached = self.visited.get(gameState.hashValue)
                nodeWidth = nodesLimit - self.nodes
                isCurrentNodeBetterThanCached = False
                if cached is not None:
                    isCurrentNodeBetterThanCached = (g_cost < cached[0]) or (
                            (g_cost == cached[0]) and ((cached[1] < costLimit) or (cached[2] < nodeWidth)))
                    if (not self.dontUpdateCache) and isCurrentNodeBetterThanCached:
                        cached[0] = g_cost
                        cached[1] = costLimit
                        cached[2] = nodeWidth
                else:
                    isCurrentNodeBetterThanCached = True
                    self.visited[gameState.hashValue] = [g_cost, costLimit, nodeWidth]

                if isCurrentNodeBetterThanCached:
                    found = self.limitedDfs(gameState, g_cost, costLimit, nodesLimit, path, move)
                    if found:
                        path.append(gameState.serializeBoardToString())

            gameState.undoMove(move, moved)

            if found:
                return found

            if boundExceeded:
                break

        return False

    def search(self, gameState: SlidingTileBoard, costLimit: float, nodeLimit: int, path: list):
        self.f_below = 0
        self.f_above = self.INFINITY
        self.nodes = 0
        self.limitedDfs(gameState, 0, costLimit, nodeLimit, path, ((-1, -1), ()))
        if self.nodes >= nodeLimit:
            # For Bin Search
            if self.fCostBound[0] < self.f_below:
                return [self.fCostBound[0], self.f_below]
            return [0, self.f_below]
        elif self.f_below >= self.solutionCost:
            # Solved
            return [self.solutionCost, self.solutionCost]
        else:
            # For next IDA*
            if self.fCostBound[1] > self.f_above:
                return [self.f_above, self.fCostBound[1]]
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
            self.dontUpdateCache = False
            print('IDA* bound ', self.fCostBound[0])
            self.fCostBound = self.search(gameState, self.fCostBound[0], self.INFINITY, path)
            if self.nodes >= (self.c1 * self.nodeBudget):
                self.nodeBudget = self.nodes
                continue

            '''
            Exponential Search
            '''
            delta = 1
            while self.fCostBound[0] != self.fCostBound[1] and self.nodes < (self.c1 * self.nodeBudget):
                nextCost = self.fCostBound[0] + 2 ** delta
                delta = delta + 1
                self.solutionLowerBound = self.fCostBound[0]
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget), path)

            '''
            Binary Search
            '''
            self.dontUpdateCache = True
            binSearchCount = 0
            while self.fCostBound[0] != self.fCostBound[1] and (
                    self.nodes < (self.c1 * self.nodeBudget) or self.nodes >= (self.c2 * self.nodeBudget)):
                nextCost = (self.fCostBound[0] + self.fCostBound[1]) / 2
                self.solutionLowerBound = self.fCostBound[0]
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget), path)
                binSearchCount += 1
                if binSearchCount >= 2:
                    break

            self.nodeBudget = max(self.nodes, (self.c1 * self.nodeBudget))

            if self.solutionCost == self.fCostBound[0]:
                return

    def solveAllGamesWithBTS(self):
        start_time = time.time()
        game = SlidingTileBoard(self.games[0], True)
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
            slidingTileBoardInstance = SlidingTileBoard(gameTiles, True)
            slidingTileBoardInstance.printBoard()

        print('Total moves ', len(path))
