# BeautyContest
Keynesian Beauty Contest Simulator \n
Assume there are x participants and y iterations in a guessing game. \n
The goal is to guess a number that will be (1/3) of the average guessed number. The number is between 0 and 1000 \n
This script simulates this game over many iteration, with the ability to employ 7 strategies: \n

# Random Strategy
  Random guess between 0 and 1000

# Low Strategy
  Random guess between 0 and 333

# High Strategy
  Random guess between 667 and 1000

# Mid Strategy
  Random guess between 34 and 66

# Random Walk Strategy
  Random guess between 0 and 100 upon first iteration
  Guess increases or decreases each iteration thereafter based on prev winner

# Learning Strategy
  Players adjust strategy based on stragies that have won the most
  in previous 10 rounds

# Copy Strategy
  Players copy a guess that was successful in previous rounds
