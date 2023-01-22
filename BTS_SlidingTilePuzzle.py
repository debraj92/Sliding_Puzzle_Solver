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
        self.c2 = 8
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

    def limitedDfs(self, gameState: SlidingTileBoard, pathCost: int, costLimit: float, nodesLimit: int,
                   path: list, parent_move: tuple):

        if self.solutionCost == self.solutionLowerBound:
            return False

        f = pathCost + gameState.heuristic

        self.f_below = max(f, self.f_below)

        if self.nodes >= nodesLimit:
            return False

        validMoves = gameState.generateValidMoves(parent_move)
        self.nodes += 1
        for move in validMoves:
            moved = gameState.move(move)

            g_cost = pathCost + gameState.gCostWeighted(move[1])
            #g_cost = pathCost + gameState.gCost()
            f = g_cost + gameState.heuristic

            if gameState.isSolved():
                self.solutionCost = f
                path.append(gameState.serializeBoardToString())
                gameState.undoMove(move, moved)
                return True

            found = False
            if f > costLimit:
                self.f_above = min(self.f_above, f)
            elif f >= self.solutionCost:
                self.f_below = self.solutionCost
                costExceeded = True
            else:
                cached = self.visited.get(gameState.hashValue)
                nodeWidth = nodesLimit - self.nodes
                if cached is not None:
                    isCurrentNodeBetterThanCached = (g_cost < cached[0]) or (
                        (g_cost == cached[0]) and ((cached[1] < costLimit) or (cached[2] < nodeWidth)))
                    if not self.dontUpdateCache and isCurrentNodeBetterThanCached:
                        cached[0] = g_cost
                        cached[1] = costLimit
                        cached[2] = nodeWidth
                else:
                    isCurrentNodeBetterThanCached = True
                    if not self.dontUpdateCache:
                        self.visited[gameState.hashValue] = [g_cost, costLimit, nodeWidth]

                if isCurrentNodeBetterThanCached:
                    found = self.limitedDfs(gameState, g_cost, costLimit, nodesLimit, path, move)
                    if found:
                        path.append(gameState.serializeBoardToString())

            gameState.undoMove(move, moved)

            if found:
                return found

        return False

    def search(self, gameState: SlidingTileBoard, costLimit: float, nodeLimit: int, path: list):
        self.f_below = 0
        self.f_above = self.INFINITY
        self.nodes = 0
        self.limitedDfs(gameState, 0, costLimit, nodeLimit, path, ((-1, -1), ()))
        if self.nodes >= nodeLimit:
            if self.fCostBound[0] < self.f_below:
                return [self.fCostBound[0], self.f_below]
            return [0, self.f_below]
        elif self.f_below >= self.solutionCost:
            return [self.solutionCost, self.solutionCost]
        else:
            if self.fCostBound[1] > self.f_above:
                return [self.f_above, self.fCostBound[1]]
            return [self.f_above, self.INFINITY]

    def solveWithBts(self, gameState: SlidingTileBoard, path: list):
        self.fCostBound = [gameState.heuristic, self.INFINITY]
        self.solutionCost = self.INFINITY
        self.nodeBudget = 0

        t1 = 0
        t2 = 0
        t3 = 0

        while self.solutionCost > self.fCostBound[0]:
            self.solutionLowerBound = self.fCostBound[0]
            self.fCostBound[1] = self.INFINITY

            print('bound ', self.solutionLowerBound)
            '''
            Regular IDA*
            '''
            t1_s = time.time()
            self.dontUpdateCache = False
            self.fCostBound = self.search(gameState, self.fCostBound[0], self.INFINITY, path)
            if self.nodes >= (self.c1 * self.nodeBudget):
                self.nodeBudget = self.nodes
                continue
            t1 += time.time() - t1_s

            '''
            Exponential Search
            '''
            t2_s = time.time()
            delta = 0
            while self.fCostBound[0] != self.fCostBound[1] and self.nodes < (self.c1 * self.nodeBudget):
                nextCost = self.fCostBound[0] + 2 ** delta
                delta = delta + 1
                self.solutionLowerBound = self.fCostBound[0]
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget), path)

            t2 += time.time() - t2_s
            '''
            Binary Search
            '''
            t3_s = time.time()
            self.dontUpdateCache = True
            while self.fCostBound[0] != self.fCostBound[1] and (
                    self.nodes < (self.c1 * self.nodeBudget) or self.nodes >= (self.c2 * self.nodeBudget)):
                nextCost = (self.fCostBound[0] + self.fCostBound[1]) / 2
                self.solutionLowerBound = self.fCostBound[0]
                #self.visited.clear()
                self.fCostBound = self.search(gameState, nextCost, (self.c2 * self.nodeBudget), path)

            t3 += time.time() - t3_s
            self.nodeBudget = max(self.nodes, (self.c1 * self.nodeBudget))

            if self.solutionCost == self.fCostBound[0]:
                print('Time IDA* ', t1)
                print('Exp Search ', t2)
                print('Bin Search ', t3)
                return

        print('Time IDA* ', t1)
        print('Exp Search ', t2)
        print('Bin Search ', t3)

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
