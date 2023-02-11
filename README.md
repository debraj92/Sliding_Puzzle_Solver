# Sliding_Puzzle_Solver

![ezgif com-optimize](https://user-images.githubusercontent.com/10151782/218239443-e7b76494-bac6-4698-a9cb-e19b5bba20a3.gif)


Start State:
<img width="302" alt="Screen Shot 2023-02-10 at 9 08 46 PM" src="https://user-images.githubusercontent.com/10151782/218239637-8090e098-cbaf-4418-ba0d-687b203fd7a1.png">

Represented as: 1 5 2 3 0 6 10 7 4 8 9 11 12 13 14 15

Solved State:
<img width="301" alt="Screen Shot 2023-02-10 at 9 12 41 PM" src="https://user-images.githubusercontent.com/10151782/218239643-1e8c610e-80ec-4a3b-a161-5c5822f8a053.png">

Represented as: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15

This is obviously an easy example. We solve challenging board positions using IDA* and BTS.
IDA* or iterative deepening A* is good if the cost of moving a tile is uniform (say 1). It fails when the cost of moving a tile is non-uniform.
For example if cost of moving tile t is (t + 2) / (t + 1). In this case, tile 2 will cost 4/3 and tile 3 will cost 5/4.
BTS or budgeted tree search can solve the sliding tile puzzle for non-uniform costs.

https://webdocs.cs.ualberta.ca/~nathanst/papers/sturtevant2020btsguide.pdf

Commands to test using C++:

mkdir build;cd build
cmake ..
make
./658_A1 "1 5 2 3 0 6 10 7 4 8 9 11 12 13 14 15"


