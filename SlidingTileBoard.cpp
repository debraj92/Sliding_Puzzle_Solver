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
    board[to.first][to.second] = board[from.first][from.second];
    board[from.first][from.second] = 0;
    zeroCoordinate = from;
}

bool SlidingTileBoard::isSolved() {
#ifdef UNIFORM_COST
    return heuristic == 0;
#else
    return heuristic < 0.005;
#endif
}

int SlidingTileBoard::getGCost() {
    return 1;
}

double SlidingTileBoard::getGCostWeighted(const IntPair& tileCoordinate) {
    auto t = (double) board[tileCoordinate.first][tileCoordinate.second];
    return (t + 2) / (t + 1);
}

// Never Used
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

    actualXY.clear();
    heuristic = 0;

    int k = 0;
    for(int r=0; r<4; ++r) {
        for(int c=0; c<4; ++c) {
            board[r][c] = std::stoi(tileBoard[k]);
            if (!board[r][c]) {
                zeroCoordinate = make_pair(r, c);
            }
            actualXY.insert({k, make_pair(r, c)});
            ++k;
        }
    }

#ifdef UNIFORM_COST
    initializeUniformHeuristic();
#else
    initializeNonUniformHeuristic();
#endif

}

int SlidingTileBoard::getTile(IntPair &xy) {
    return board[xy.first][xy.second];
}

IntPair SlidingTileBoard::getActualCoordinate(IntPair &xy) {
    return actualXY.at(getTile(xy));
}

string SlidingTileBoard::serializeBoard() {
    string output;
    for(auto & r : board) {
        for (int c : r) {
            output += " " + to_string(c);
        }
    }
    return output;
}

void SlidingTileBoard::initActionCache() {
    for(int x=0; x < 4; ++x) {
        for (int y=0; y < 4; ++y) {
            pair<int, int> targetCoordinate = {x, y};
            vector<MovePair> allMoves;
            if (x > y) {
                if (x > 0) {
                    allMoves.emplace_back(make_pair(make_pair(x - 1, y), targetCoordinate));
                }
                if (x < 3) {
                    allMoves.emplace_back(make_pair(make_pair(x + 1, y), targetCoordinate));
                }
                if (y > 0) {
                    allMoves.emplace_back(make_pair(make_pair(x, y - 1), targetCoordinate));
                }
                if (y < 3) {
                    allMoves.emplace_back(make_pair(make_pair(x, y + 1), targetCoordinate));
                }
            } else {
                if (y > 0) {
                    allMoves.emplace_back(make_pair(make_pair(x, y - 1), targetCoordinate));
                }
                if (y < 3) {
                    allMoves.emplace_back(make_pair(make_pair(x, y + 1), targetCoordinate));
                }
                if (x > 0) {
                    allMoves.emplace_back(make_pair(make_pair(x - 1, y), targetCoordinate));
                }
                if (x < 3) {
                    allMoves.emplace_back(make_pair(make_pair(x + 1, y), targetCoordinate));
                }
            }
            actionCache[x][y] = allMoves;
        }
    }

}

vector<MovePair>& SlidingTileBoard::getActions() {
    return actionCache[zeroCoordinate.first][zeroCoordinate.second];
}

void SlidingTileBoard::initializeUniformHeuristic() {
#ifdef UNIFORM_COST
    for(int r=0; r < 4; ++r) {
        for (int c = 0; c < 4; ++c) {
            if (board[r][c]) {
                heuristic += calculateManhattanDistance(make_pair(r, c), actualXY.at(board[r][c]));
            }
        }
    }

    for(int k=1; k <= 15; ++k) {
        for(int r=0; r < 4; ++r) {
            for (int c = 0; c < 4; ++c) {
                heuristicTable[k-1][r][c] = calculateManhattanDistance(make_pair(r, c), actualXY.at(k));
            }
        }
    }
#endif
}

void SlidingTileBoard::initializeNonUniformHeuristic() {
#ifndef UNIFORM_COST
    for(int r=0; r < 4; ++r) {
        for (int c = 0; c < 4; ++c) {
            if (board[r][c]) {
                heuristic += ((double) calculateManhattanDistance(make_pair(r, c), actualXY.at(board[r][c]))) * getGCostWeighted({r, c});
            }
        }
    }

    for(int k=1; k <= 15; ++k) {
        auto t = (double) k;
        auto tileWeight = (t + 2) / (t + 1);
        for(int r=0; r < 4; ++r) {
            for (int c = 0; c < 4; ++c) {
                heuristicTable[k-1][r][c] = ((double) calculateManhattanDistance(make_pair(r, c), actualXY.at(k))) * tileWeight;
            }
        }
    }
#endif
}

