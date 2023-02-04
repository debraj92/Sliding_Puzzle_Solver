//
// Created by Debraj Ray on 2023-01-21.
//

#ifndef INC_658_A1_SLIDINGTILEBOARD_H
#define INC_658_A1_SLIDINGTILEBOARD_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;

using Long = long long;
using IntPair = pair<int, int>;
using MovePair = pair<IntPair, IntPair>;

class SlidingTileBoard {
    int board[4][4];
    IntPair zeroCoordinate;
    unordered_map<int, IntPair> actualXY;

public:

    int heuristic = 0;
    int heuristicTable[15][4][4];
    Long hashValue;

    void initialize(std::vector<string> &tileBoard);

    void printBoard();

    int calculateManhattanDistance(const IntPair &start, const IntPair &end);

    void move(const IntPair &from, const IntPair &to);

    bool isSolved();

    int getGCost();

    void generateValidMoves(vector<MovePair> &allMoves, const MovePair &parentMove);

    int getTile(IntPair &xy);

    IntPair getActualCoordinate(IntPair &xy);

    string serializeBoard();

    int getDeltaHeuristicFromMove(const MovePair &move);
};


#endif //INC_658_A1_SLIDINGTILEBOARD_H
