//
// Created by Debraj Ray on 2023-02-04.
//

#include "BTS_SlidingTilePuzzleSolver.h"
#include <fstream>
#include <algorithm>

using namespace std;

void BTS_SlidingTilePuzzleSolver::fetchAllGames() {
    std::ifstream file( "../run.txt" );
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

void BTS_SlidingTilePuzzleSolver::playAllGames() {
    for(auto &board: allGameBoards) {
        pathLength = 0;
        nodesGenerated = 0;
        nodesExpanded = 0;
        gameState.initialize(board);
        auto start = chrono::steady_clock::now();
        solveWithBts();
        auto end = chrono::steady_clock::now();
        auto diff = end - start;
        auto sec = chrono::duration <double, milli> (diff).count() / 1000;
        cout << "BTS "<< sec <<"s duration elapsed; "<< nodesExpanded << " expanded; "<< nodesGenerated << " generated; ";
        cout << "Solution Length " << pathLength <<endl<<endl;
    }

}

void BTS_SlidingTilePuzzleSolver::search(const double costLimit, const unsigned long long nodeLimit, DoublePair &result) {

    f_below = 0;
    f_above = INFINITY_DBL;
    nodes = 0;
    auto dummyStart = make_pair(make_pair(-1, -1), make_pair(-1, -1));
    limitedDFS(0, costLimit, nodeLimit, dummyStart);
    if (nodes >= nodeLimit) {
        if (fCostBound.first <= f_below) {
            result = {fCostBound.first, f_below};
        } else {
            result = {0, f_below};
        }
    } else if (f_below >= solutionCost) {
        // solved
        result = {solutionCost, solutionCost};
    } else {
        if (fCostBound.second >= f_above) {
            result = {f_above, fCostBound.second};
        } else {
            result = {f_above, INFINITY_DBL};
        }
    }
}

bool BTS_SlidingTilePuzzleSolver::limitedDFS(double pathCost, const double costLimit, const unsigned long long nodeLimit, const MovePair &parentMove) {

    if (solutionCost == solutionLowerBound) {
        return false;
    }

    if (nodes >= nodeLimit) {
        return false;
    }
    nodes += 1;
    nodesExpanded += 1;
    bool found = false;
    auto allMoves = gameState.getActions();
    for (auto const &move: allMoves) {
        if (parentMove.second.first == move.first.first && parentMove.second.second == move.first.second) {
            continue;
        }
        nodesGenerated += 1;
        gameState.move(move.first, move.second);
#ifdef UNIFORM_COST
        auto gCost = pathCost + gameState.getGCost();
#else
        auto gCost = pathCost + gameState.getGCostWeighted(move.second);
#endif
        auto f = gCost + gameState.heuristic;

        if (gameState.isSolved()) {
            ++pathLength;
            solutionCost = f;
            if (reportFinalState) {
                cout<<"Final State "<<gameState.serializeBoard()<<endl;
                if (showPath) {
                    gameState.printBoard();
                }
            }
            //undo move
            gameState.move(move.second, move.first);
            return true;
        }

        if (f > costLimit) {
            f_above = f < f_above? f : f_above;
        } else if (f >= solutionCost) {
            f_below = solutionCost;
        } else {
            f_below = f > f_below ? f : f_below;
            found = limitedDFS(gCost, costLimit, nodeLimit, move);
        }

        //undo move
        gameState.move(move.second, move.first);

        if (found) {
            ++pathLength;
            if(reportFinalState && showPath) {
                gameState.printBoard();
            }
            return true;
        }
    }
    return false;
}

void BTS_SlidingTilePuzzleSolver::solveWithBts() {

    if (gameState.isSolved()) {
        cout<<"Final State "<<gameState.serializeBoard()<<endl;
        return;
    }

    fCostBound = {gameState.heuristic, INFINITY_DBL};
    solutionCost = INFINITY_DBL;
    nodeBudget = 0;
    solutionLowerBound = INFINITY_DBL;
    cout<<"Starting from "<<gameState.serializeBoard()<<endl;

    while (solutionCost > fCostBound.first) {
        solutionLowerBound = fCostBound.first;
        fCostBound.second = INFINITY_DBL;

        // Regular IDA*
        reportFinalState = true;
        cout<<"Starting iteration with bound "<< fCostBound.first << "; " << nodesExpanded << " expanded; "<< nodesGenerated << " generated"<<endl;
        search(fCostBound.first, MAX_NODES, fCostBound);
        if (nodes >= c1 * nodeBudget) {
            nodeBudget = nodes;
            continue;
        }
        reportFinalState = false;
        // Exponential Search
        double delta = 0;
        double nextCost;
        while (fabs(fCostBound.first - fCostBound.second) > epsilon && nodes < (c1 * nodeBudget)) {
            nextCost = fCostBound.first + pow(2, delta);
            ++delta;
            solutionLowerBound = fCostBound.first;
            search(nextCost, (c2 * nodeBudget), fCostBound);
        }

        // Binary Search
        while(fabs(fCostBound.first - fCostBound.second) > epsilon && (nodes < (c1 * nodeBudget) || nodes >= (c2 * nodeBudget))) {
            nextCost = (fCostBound.first + fCostBound.second) / 2;
            solutionLowerBound = fCostBound.first;
            search(nextCost, (c2 * nodeBudget), fCostBound);
            if (fCostBound.second == INFINITY_DBL) {
                break;
            }
        }

        nodeBudget = nodes > c1 * nodeBudget ? nodes : c1 * nodeBudget;

        if (solutionCost == fCostBound.first) {
            solutionCost = INFINITY_DBL;
            solutionLowerBound = fCostBound.first;
            fCostBound.second = INFINITY_DBL;
            pathLength = 0;
            reportFinalState = true;
            auto saveNodesExpanded = nodesExpanded;
            auto saveNodesGenerated = nodesGenerated;
            auto maxFCostBound = f_below;
            search(fCostBound.first, MAX_NODES, fCostBound);
            if (pathLength == 0) {
                nodesExpanded = saveNodesExpanded;
                nodesGenerated = saveNodesGenerated;
                search(maxFCostBound, MAX_NODES, fCostBound);
            }
            break;
        }
    }
}

void BTS_SlidingTilePuzzleSolver::playGame(string& board) {
    pathLength = 0;
    nodesGenerated = 0;
    nodesExpanded = 0;
    showPath = true;
    auto b = split(board, ' ');
    gameState.initialize(b);
    auto start = chrono::steady_clock::now();
    solveWithBts();
    auto end = chrono::steady_clock::now();
    auto diff = end - start;
    auto sec = chrono::duration <double, milli> (diff).count() / 1000;
    cout << "BTS "<< sec <<"s duration elapsed; "<< nodesExpanded << " expanded; "<< nodesGenerated << " generated; ";
    cout << "Solution Length " << pathLength <<endl<<endl;
}
