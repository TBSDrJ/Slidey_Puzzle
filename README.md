# Slidey Puzzle Solution

So, we 3D printed this slidey puzzle and, a month or two later, no one had solved it.  So, we wanted to know if it was actually possible to solve it.  So, I wrote a computer program to decide.

This puzzle is equivalent to the [Klotski Puzzle](https://en.wikipedia.org/wiki/Klotski), which I didn't realize until after I had done all the programming.  So, probably someone has solved this before.

The engine is quite general for the most part.  If anyone wants to use this to find solutions to other similar puzzles with a different size or collection of pieces, you should be able to. I probably could have done a slightly better job of isolating the stuff that is specific to this puzzle, but it should be easy to tease out.  This is true in both the main code and the unit tests if you want to use the unit tests.  In the unit tests, I was pretty careful to comment the parts that assume the specifics of the setup, as far as I saw.  But I haven't tried with a different setup.

For this puzzle, there are 474 distinct solutions, the shortest of which involves 114 moves.  Here, "distinct" means that, in any solution, the puzzle is never in the same position as it is in any of the other solutions.  Here, "same" considers two positions the same if the only difference is that two (or more) pieces of the same size & orientation are swapped.

There 80,271 moves carried out in total, of which 55,484 moves ended in a position that was the same as one that had been seen before (including winning positions), and 24,787 moves ended in a new position that had not been seen before.

The file [wins.txt](wins.txt) includes all 474 different sequences of moves.  The file [first_win.txt](first_win.txt) shows the board after each of the 114 moves in the first solution found.