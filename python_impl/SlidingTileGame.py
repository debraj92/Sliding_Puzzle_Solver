from SlidingTileBoard import SlidingTileBoard
import time


class SlidingTileGame:

    def __init__(self):
        self.games = []
        self.fetchAllGames()
        self.INFINITY = 1000000
        self.nextBound = self.INFINITY
        self.NodesExpanded = 0
        self.NodesGenerated = 0
        self.pathLength = 0
        self.visited = {}
        self.gameState = None

    def fetchAllGames(self):
        korfInstancesFilename = "korf100_run.txt"
        with open(korfInstancesFilename) as file:
            for line in file:
                game = line.rstrip().split()
                if len(game) == 0:
                    continue
                game.pop(0)
                gameTiles = [eval(i) for i in game]
                self.games.append(gameTiles)

    def printAllGames(self):
        for game in self.games:
            gameState = SlidingTileBoard(game)
            gameState.printBoard()
            print('\n')

    def search(self, path_cost: int, bound: int, parent_move: tuple):

        if self.gameState.isSolved():
            return True

        validMoves = self.gameState.generateValidMoves(parent_move)
        self.NodesExpanded += 1
        self.NodesGenerated += len(validMoves)
        for move in validMoves:
            moved = self.gameState.move(move)

            found = False

            g_cost = path_cost + self.gameState.gCost()
            f = g_cost + self.gameState.heuristic

            if f > bound:
                if f < self.nextBound:
                    self.nextBound = f

            else:
                cached = self.visited.get(self.gameState.hashValue)
                if cached is not None:
                    isCurrentNodeBetterThanCached = (g_cost < cached[0]) or (g_cost == cached[0] and cached[1] < bound)
                    if isCurrentNodeBetterThanCached:
                        cached[0] = g_cost
                        cached[1] = bound
                else:
                    isCurrentNodeBetterThanCached = True
                    self.visited[self.gameState.hashValue] = [g_cost, bound]

                if isCurrentNodeBetterThanCached:
                    found = self.search(g_cost, bound, move)
                    if found:
                        self.pathLength += 1

            self.gameState.undoMove(move, moved)

            if found:
                return found

        return False

    def solveAllGamesWithIDA_Star(self):
        for game in self.games:
            self.nextBound = self.INFINITY
            self.NodesExpanded = 0
            self.NodesGenerated = 0
            self.pathLength = 0
            self.visited = {}
            start_time = time.time()
            self.gameState = SlidingTileBoard(game, False)
            print('Start From ', self.gameState.serializeBoardToString())
            pathFound = self.solveWithIDA_Star()
            duration = round(time.time() - start_time, 3)
            if pathFound:
                print(
                    f'IDA*: {duration}s elapsed; {self.NodesExpanded} expanded; {self.NodesGenerated} generated; Solution Length {self.pathLength}')
                print()

    def solveWithIDA_Star(self):
        bound = self.gameState.heuristic
        if self.gameState.isSolved():
            return True

        found = False
        while bound < self.INFINITY and not found:
            print(
                f'Starting iteration with bound {bound}; {self.NodesExpanded} expanded  {self.NodesGenerated} generated')
            self.visited[self.gameState.hashValue] = [0, bound]
            self.nextBound = self.INFINITY
            found = self.search(0, bound, ((-1, -1), ()))
            bound = self.nextBound

        return found

    def printSolution(self, path):
        path.reverse()
        print()
        for tileBoard in path:
            tileBoard = tileBoard.strip('|').split('|')
            gameTiles = [eval(i) for i in tileBoard]
            slidingTileBoardInstance = SlidingTileBoard(gameTiles, False)
            slidingTileBoardInstance.printBoard()

        print('Total moves ', len(path))
