//
// Created by Debraj Ray on 2023-02-04.
//

#ifndef INC_658_A1_BTS_SLIDINGTILEPUZZLESOLVER_H
#define INC_658_A1_BTS_SLIDINGTILEPUZZLESOLVER_H

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

#include "CostType.h"
#include "SlidingTileBoard.h"

using DoublePair = pair<double, double>;

class BTS_SlidingTilePuzzleSolver {

    const double INFINITY_DBL = (double) INT_MAX;
    const long long MAX_NODES = std::numeric_limits<long long>::max();

    vector<vector<string>> allGameBoards;

    SlidingTileBoard gameState;

    int pathLength = 0;
    int nodesExpanded = 0;
    u_long nodesGenerated = 0;

    double f_below = 0;
    double f_above = INFINITY_DBL;
    const long long c1 = 3;
    const long long c2 = 10;
    const double epsilon = 0.00001;
    long long nodes = 0;
    long long nodeBudget = 0;
    bool reportFinalState = false;
    double solutionCost = INFINITY_DBL;
    DoublePair fCostBound;
    double solutionLowerBound = INFINITY_DBL;

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

    bool limitedDFS(double pathCost, double costLimit, long long nodeLimit, const MovePair &parentMove);

    void search(double costLimit, long long nodeLimit, DoublePair &result);

    void solveWithBts();
};


#endif //INC_658_A1_BTS_SLIDINGTILEPUZZLESOLVER_H
