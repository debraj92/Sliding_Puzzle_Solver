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

    vector<vector<string>> allGameBoards;
    int nextBound = 0;
    SlidingTileBoard gameState;

    int pathLength = 0;
    int nodesExpanded = 0;
    u_long nodesGenerated = 0;

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

    bool solvePuzzle();

    bool search(int pathCost, int bound, const MovePair &parentMove);
};


#endif //INC_658_A1_SLIDINGTILEPUZZLEIDA_STAR_H
