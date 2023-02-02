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

    def printAllGames(self):
        for game in self.games:
            gameState = SlidingTileBoard(game)
            gameState.printBoard()
            print('\n')

    def sortFunction(self, move: tuple, gameState: SlidingTileBoard):
        source = move[0]
        destination = move[1]
        actual_coordinates = gameState.actual_xy[gameState.board[source[0]][source[1]]]
        return (gameState.manhattanDistanceCache[destination + actual_coordinates] -
                gameState.manhattanDistanceCache[
                    source + actual_coordinates])

    def search(self, gameState: SlidingTileBoard, path_cost: int, bound: int, visited: dict, parent_move: tuple):

        if gameState.isSolved():
            return True

        validMoves = gameState.generateValidMoves(parent_move)
        validMoves = sorted(validMoves, key=lambda m: self.sortFunction(m, gameState))
        self.NodesExpanded += 1
        self.NodesGenerated += len(validMoves)
        for move in validMoves:
            moved = gameState.move(move)

            boundExceeded = False
            found = False

            g_cost = path_cost + gameState.gCost()
            f = g_cost + gameState.heuristic

            if f > bound:
                if f < self.nextBound:
                    self.nextBound = f
                boundExceeded = True

            else:
                cached = visited.get(gameState.hashValue)
                if cached is not None:
                    isCurrentNodeBetterThanCached = (g_cost < cached[0]) or (cached[1] < bound and (g_cost == cached[0]))
                    if isCurrentNodeBetterThanCached:
                        cached[0] = g_cost
                        cached[1] = bound
                else:
                    isCurrentNodeBetterThanCached = True
                    visited[gameState.hashValue] = [g_cost, bound]

                if isCurrentNodeBetterThanCached:
                    found = self.search(gameState, g_cost, bound, visited, move)
                    if found:
                        self.pathLength += 1

            gameState.undoMove(move, moved)

            if found:
                return found

            if boundExceeded:
                break

        return False

    def solveAllGamesWithIDA_Star(self):
        self.nextBound = self.INFINITY
        start_time = time.time()
        game = SlidingTileBoard(self.games[0], False)
        pathFound = self.solveWithIDA_Star(game)
        duration = round(time.time() - start_time, 3)
        if pathFound:
            print(f'IDA*: {duration}s elapsed; {self.NodesExpanded} expanded; {self.NodesGenerated} generated; Solution Length {self.pathLength}')

    def solveWithIDA_Star(self, gameState: SlidingTileBoard):
        bound = gameState.heuristic
        if gameState.isSolved():
            return True

        visited = {}
        found = False
        while bound < self.INFINITY and not found:
            print(f'Starting iteration with bound {bound}; {self.NodesExpanded} expanded  {self.NodesGenerated} generated')
            visited[gameState.hashValue] = [0, bound]
            self.nextBound = self.INFINITY
            found = self.search(gameState, 0, bound, visited, ((-1, -1), ()))
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
