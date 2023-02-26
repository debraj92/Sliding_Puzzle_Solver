//
// Created by Debraj Ray on 2023-01-21.
//

#ifndef INC_658_A1_SLIDINGTILEPUZZLEIDA_STAR_H
#define INC_658_A1_SLIDINGTILEPUZZLEIDA_STAR_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include "SlidingTileBoard.h"

using namespace std;

class SlidingTilePuzzleIDA_Star {

    const double INFINITY_DBL = (double) INT_MAX;
    vector<vector<string>> allGameBoards;
    double nextBound = 0;
    SlidingTileBoard gameState;

    int pathLength = 0;
    long long nodesExpanded = 0;
    long long nodesGenerated = 0;

    const double epsilon = 0.0000001;
    bool showPath = false;

    double solutionCost;

    std::vector<std::string> split(const std::string& str, char delim) {
        std::vector<std::string> strings;
        size_t start;
        size_t end = 0;
        while ((start = str.find_first_not_of(delim, end)) != std::string::npos) {
            end = str.find(delim, start);
            strings.push_back(str.substr(start, end - start));
        }
        return strings;
    }

public:

    void fetchAllGames();
    void playAllGames();

    void playGame(string& board);

    bool solvePuzzle();

    bool search(double pathCost, double bound, const MovePair &parentMove);
};


#endif //INC_658_A1_SLIDINGTILEPUZZLEIDA_STAR_H
