#include <iostream>
#include <string>
#include "SlidingTilePuzzleIDA_Star.h"
#include "BTS_SlidingTilePuzzleSolver.h"
#include "CostType.h"

int main(int argc, char *argv[]) {
    if (argc > 1) {
        string gameBoard = argv[1];
#ifdef UNIFORM_COST
        SlidingTilePuzzleIDA_Star solver;
#else
        BTS_SlidingTilePuzzleSolver solver;
#endif
        solver.playGame(gameBoard);
        return 0;
    }
    // Uncomment this line if IDA* should be run. Comment the BTS solver initialization line.
    //SlidingTilePuzzleIDA_Star solver;

    BTS_SlidingTilePuzzleSolver solver;

    solver.fetchAllGames();
    solver.playAllGames();
    return 0;
}
