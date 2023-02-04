//
// Created by Debraj Ray on 2023-01-21.
//

#include "SlidingTilePuzzleIDA_Star.h"
#include <fstream>

using namespace std;

void SlidingTilePuzzleIDA_Star::fetchAllGames() {
    std::ifstream file( "/Users/debrajray/CLionProjects/658_A1/korf100.txt" );
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
    gameState.initialize(allGameBoards[0]);
    auto start = chrono::steady_clock::now();
    solvePuzzle();
    auto end = chrono::steady_clock::now();
    auto diff = end - start;
    auto sec = chrono::duration <double, milli> (diff).count() / 1000;
    cout << sec << " s" << endl;
}

bool SlidingTilePuzzleIDA_Star::search(int pathCost, int bound, const MovePair &parentMove) {

    if (gameState.isSolved()) {
        cout<<"Solved"<<endl;
        gameState.printBoard();
        return true;
    }

    vector<MovePair> allMoves;
    gameState.generateValidMoves(allMoves, parentMove);
    bool found = false;
    for (auto const &move: allMoves) {
        gameState.move(move.first, move.second);
        auto gCost = pathCost + gameState.getGCost();
        auto f = gCost + gameState.heuristic;

        if (f > bound) {
            if (f < nextBound) {
                nextBound = f;
            }
        } else {
            bool isCurrentNodeBetterThanCached;
            if (auto cachedData = visited.find(gameState.hashValue); cachedData != visited.end()) {
                isCurrentNodeBetterThanCached = (gCost < cachedData->second.first) || (gCost == cachedData->second.first && cachedData->second.second < bound);
                if (isCurrentNodeBetterThanCached) {
                    visited[gameState.hashValue] = {gCost, bound};
                }
            } else {
                isCurrentNodeBetterThanCached = true;
                visited[gameState.hashValue] = {gCost, bound};
            }
            if (isCurrentNodeBetterThanCached) {
                found = search(gCost, bound, move);
            }
        }
        //undo move
        gameState.move(move.second, move.first);
        if (found) {
            return true;
        }
    }
    return false;
}

bool SlidingTilePuzzleIDA_Star::solvePuzzle() {
    if (gameState.isSolved()) {
        cout<<"Solved"<<endl;
        gameState.printBoard();
        return true;
    }
    bool found = false;
    auto bound = gameState.heuristic;
    auto dummyStart = make_pair(make_pair(-1, -1), make_pair(-1, -1));
    while (!found) {
        nextBound = INT_MAX;
        cout <<"Bound "<< bound << endl;
        visited.insert({gameState.hashValue, {0, bound}});
        found = search(0, bound, dummyStart);
        bound = nextBound;
    }
    cout<<endl;
    gameState.printBoard();
    return found;
}
