from SlidingTileBoard import SlidingTileBoard
import time


class SlidingTileGame:

    def __init__(self):
        self.games = []
        self.fetchAllGames()
        self.INFINITY = 1000000
        self.nextBound = self.INFINITY

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
        oldHeuristic = gameState.manhattanDistance(source, [actual_coordinates[0], actual_coordinates[1]])
        newHeuristic = gameState.manhattanDistance(destination, [actual_coordinates[0], actual_coordinates[1]])
        return newHeuristic - oldHeuristic

    def search(self, gameState: SlidingTileBoard, path_cost: int, bound: int, visited: dict, path: list, parent_move: tuple):

        if gameState.isSolved():
            path.append(gameState.serializeBoardToString())
            return True

        validMoves = gameState.generateValidMoves(parent_move)
        validMoves = sorted(validMoves, key=lambda m: self.sortFunction(m, gameState))

        for move in validMoves:
            moved = gameState.move(move)

            if gameState.isSolved():
                path.append(gameState.serializeBoardToString())
                gameState.undoMove(move, moved)
                return True

            boundExceeded = False
            found = False

            #g_cost = path_cost + gameState.gCostWeighted(move[1])
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
                    found = self.search(gameState, g_cost, bound, visited, path, move)
                    if found:
                        path.append(gameState.serializeBoardToString())

            gameState.undoMove(move, moved)

            if found:
                return found

            if boundExceeded:
                break

        return False

    def solveAllGamesWithIDA_Star(self):
        self.nextBound = self.INFINITY
        start_time = time.time()
        game = SlidingTileBoard(self.games[0])
        path = []
        pathFound = self.solveWithIDA_Star(game, path)
        duration = time.time() - start_time
        print("--- %s s ---" % duration)
        if pathFound:
            self.printSolution(path)

    def solveWithIDA_Star(self, gameState: SlidingTileBoard, path: list):
        bound = gameState.heuristic
        if gameState.isSolved():
            path.append(gameState.serializeBoardToString())
            return True

        visited = {}
        found = False
        while bound < self.INFINITY and not found:
            print("Bound", bound)
            visited[gameState.hashValue] = [0, bound]
            self.nextBound = self.INFINITY

            found = self.search(gameState, 0, bound, visited, path, ((-1, -1), ()))
            if found:
                path.append(gameState.serializeBoardToString())

            print(found)

            bound = self.nextBound

        return found

    def printSolution(self, path):
        path.reverse()
        print()
        for tileBoard in path:
            tileBoard = tileBoard.strip('|').split('|')
            gameTiles = [eval(i) for i in tileBoard]
            slidingTileBoardInstance = SlidingTileBoard(gameTiles)
            slidingTileBoardInstance.printBoard()

        print('Total moves ', len(path))
