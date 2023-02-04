//
// Created by Debraj Ray on 2023-01-21.
//

#include "SlidingTileBoard.h"
#include <iostream>

using namespace std;

void SlidingTileBoard::printBoard() {
    for(int r=0; r<4; ++r) {
        for (int c = 0; c < 4; ++c) {
            if (board[r][c] >= 10) {
                cout << "  " << board[r][c];
            } else {
                cout << "   " << board[r][c];
            }
        }
        cout<<endl;
    }
}

int SlidingTileBoard::calculateManhattanDistance(const IntPair &start, const IntPair &end) {
    return abs(start.first - end.first) + abs(start.second - end.second);
}

void SlidingTileBoard::move(const IntPair &from, const IntPair &to) {
    heuristic += heuristicTable[board[from.first][from.second] - 1][to.first][to.second] - heuristicTable[board[from.first][from.second]  - 1][from.first][from.second];
    hashValue ^= ((Long)(from.first * 4 + from.second)) << (board[from.first][from.second] * 4);
    board[to.first][to.second] = board[from.first][from.second];
    board[from.first][from.second] = 0;
    hashValue ^= ((Long)(to.first * 4 + to.second)) << (board[to.first][to.second] * 4);
    zeroCoordinate = from;
}

bool SlidingTileBoard::isSolved() {
    return heuristic == 0;
}

int SlidingTileBoard::getGCost() {
    return 1;
}

void SlidingTileBoard::generateValidMoves(vector<MovePair> &allMoves, const MovePair &parentMove) {
    int x = zeroCoordinate.first;
    int y = zeroCoordinate.second;
    if (x > 0 && (parentMove.second.first != x - 1 || parentMove.second.second != y)) {
        allMoves.emplace_back(make_pair(make_pair(x - 1, y), zeroCoordinate));
    }
    if (x < 3 && (parentMove.second.first != x + 1 || parentMove.second.second != y)) {
        allMoves.emplace_back(make_pair(make_pair(x + 1, y), zeroCoordinate));
    }
    if (y > 0 && (parentMove.second.first != x || parentMove.second.second != y - 1)) {
        allMoves.emplace_back(make_pair(make_pair(x, y - 1), zeroCoordinate));
    }
    if (y < 3 && (parentMove.second.first != x || parentMove.second.second != y + 1)) {
        allMoves.emplace_back(make_pair(make_pair(x, y + 1), zeroCoordinate));
    }
}

void SlidingTileBoard::initialize(vector<string> &tileBoard) {
    int k = 0;
    for(int r=0; r<4; ++r) {
        for(int c=0; c<4; ++c) {
            board[r][c] = std::stoi(tileBoard[k]);
            if (!board[r][c]) {
                zeroCoordinate = make_pair(r, c);
            } else {
                hashValue ^= ((Long) (r * 4 + c)) << (board[r][c] * 4);
            }
            actualXY.insert({k, make_pair(r, c)});
            ++k;
        }
    }
    for(int r=0; r < 4; ++r) {
        for (int c = 0; c < 4; ++c) {
            if (board[r][c]) {
                heuristic += calculateManhattanDistance(make_pair(r, c), actualXY.at(board[r][c]));
            }
        }
    }

    for(k=1; k <= 15; ++k) {
        for(int r=0; r < 4; ++r) {
            for (int c = 0; c < 4; ++c) {
                heuristicTable[k-1][r][c] = calculateManhattanDistance(make_pair(r, c), actualXY.at(k));
            }
        }
    }
}

int SlidingTileBoard::getTile(IntPair xy) {
    return board[xy.first][xy.second];
}

IntPair SlidingTileBoard::getActualCoordinate(IntPair xy) {
    return actualXY.at(getTile(xy));
}

