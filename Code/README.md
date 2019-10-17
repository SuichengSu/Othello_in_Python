# AI Design
## Summary
Separate procedures are implemented to enhance computer player's strategy. For each step, computer player analyzes the entire current game state and find the best next move. 

## How does computer player think?
The computer player(program) stimulates every possible valid move on the board and calculate the number of opponent tiles will be flipped if each valid move is made. Then the program returns the valid move that can flip the most opponent tiles. Then computer player will pick this move as the next move. 

## Outcome
The outcome of this program has improved the win rate of computer player. My computer beats me along with other testers at a win rate of around 60-70%.

## Potential/Future Improments
Potentially, computer player can be even smarter if certain rules or conditions are applied to the program such as placing a tile at a location that the opponent can't flip in the next move; or avoid placing a tile at second to the last row/column since a place on the last tile of a column/row can usually dominate that column/row later on in the game, etc. 
