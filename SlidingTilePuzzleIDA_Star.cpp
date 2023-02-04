//
// Created by Debraj Ray on 2023-01-21.
//

#include "SlidingTilePuzzleIDA_Star.h"
#include <fstream>
#include <algorithm>

using namespace std;

void SlidingTilePuzzleIDA_Star::fetchAllGames() {
    std::ifstream file( "../korf100_run.txt" );
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            line = line.substr(5);
            allGameBoards.push_back(split(line, ' '));
        }
        file.close();
    } else {
        cout<<"Cant open file"<<endl;
    }
}

void SlidingTilePuzzleIDA_Star::playAllGames() {
    for(auto &board: allGameBoards) {
        pathLength = 0;
        nodesGenerated = 0;
        nodesExpanded = 0;
        nextBound = INT_MAX;
        gameState.initialize(board);
        auto start = chrono::steady_clock::now();
        auto pathFound = solvePuzzle();
        auto end = chrono::steady_clock::now();
        auto diff = end - start;
        auto sec = chrono::duration <double, milli> (diff).count() / 1000;
        if (pathFound) {
            cout << "IDA* "<< sec <<"s duration elapsed; "<< nodesExpanded << " expanded; "<< nodesGenerated << " generated; ";
            cout << "Solution Length " << pathLength <<endl<<endl;
        } else {
            cout<<" IDA* could not find a path "<<endl;
        }
    }

}

bool SlidingTilePuzzleIDA_Star::search(int pathCost, int bound, const MovePair &parentMove) {

    if (gameState.isSolved()) {
        cout<<"Final State "<<gameState.serializeBoard()<<endl;
        return true;
    }
    auto allMoves = gameState.getActions();
    nodesExpanded += 1;
    nodesGenerated += allMoves.size();
    bool found = false;
    for (auto const &move: allMoves) {
        if (parentMove.second.first == move.first.first && parentMove.second.second == move.first.second) {
            continue;
        }
        nodesGenerated += 1;
        gameState.move(move.first, move.second);
        auto gCost = pathCost + gameState.getGCost();
        auto f = gCost + gameState.heuristic;
        if (f > bound) {
            if (f < nextBound) {
                nextBound = f;
            }
        } else {
            found = search(gCost, bound, move);
        }
        //undo move
        gameState.move(move.second, move.first);
        if (found) {
            pathLength += 1;
            return true;
        }
    }
    return false;
}

bool SlidingTilePuzzleIDA_Star::solvePuzzle() {
    if (gameState.isSolved()) {
        cout<<"Final State "<<gameState.serializeBoard()<<endl;
        return true;
    }
    bool found = false;
    auto bound = gameState.heuristic;
    auto dummyStart = make_pair(make_pair(-1, -1), make_pair(-1, -1));
    cout<<"Starting from "<<gameState.serializeBoard()<<endl;
    while (!found and bound < INT_MAX) {
        nextBound = INT_MAX;
        cout<<"Starting iteration with bound "<< bound << "; " << nodesExpanded << " expanded; "<< nodesGenerated << " generated"<<endl;
        found = search(0, bound, dummyStart);
        bound = nextBound;
    }
    return found;
}
