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

    def sortFunction(self, move: list, gameState: SlidingTileBoard):
        source = move[0]
        destination = move[1]
        actual_coordinates = gameState.actual_xy[gameState.board[source[0]][source[1]]]
        oldHeuristic = gameState.manhattanDistance(source, [actual_coordinates[0], actual_coordinates[1]])
        newHeuristic = gameState.manhattanDistance(destination, [actual_coordinates[0], actual_coordinates[1]])
        return newHeuristic - oldHeuristic

    def search(self, gameState: SlidingTileBoard, path_cost: int, bound: int, visited: dict, path: list):

        if gameState.isSolved():
            path.append(gameState.serializeBoardToString())
            return True

        validMoves = gameState.generateValidMoves()
        validMoves = sorted(validMoves, key=lambda m: self.sortFunction(m, gameState))

        g_cost = path_cost + gameState.gCost()

        for move in validMoves:
            moved = gameState.move(move)

            if gameState.isSolved():
                path.append(gameState.serializeBoardToString())
                gameState.undoMove(move, moved)
                return True

            boundExceeded = False
            found = False
            f = g_cost + gameState.heuristic
            if f > bound:
                if f < self.nextBound:
                    self.nextBound = f
                boundExceeded = True

            else:
                if (gameState.hashValue not in visited) or (g_cost < visited[gameState.hashValue]):
                    visited[gameState.hashValue] = g_cost
                    found = self.search(gameState, g_cost, bound, visited, path)
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
            visited[gameState.hashValue] = 0
            self.nextBound = self.INFINITY

            found = self.search(gameState, 0, bound, visited, path)
            if found:
                path.append(gameState.serializeBoardToString())

            print(found)

            bound = self.nextBound

            visited.clear()

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
