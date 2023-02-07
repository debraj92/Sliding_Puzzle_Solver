#include <iostream>
#include "SlidingTilePuzzleIDA_Star.h"
#include "BTS_SlidingTilePuzzleSolver.h"

int main() {
    //SlidingTilePuzzleIDA_Star solver;

    BTS_SlidingTilePuzzleSolver solver;

    solver.fetchAllGames();
    solver.playAllGames();
    return 0;
}
