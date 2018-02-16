# Swiss Ranking

## Overview
This program is used to support any game tournaments that utilizes a Swiss system for pairing up players in each round: players are not eliminated, and each player is paired with another player with the same number of wins, or as close as possible. In case of a tie, the player who beat the toughest opponents will win.

## Installation
* Install Postgres on your machine as per instructions on [postgres site](https://www.postgresql.org/)
* Install Python 2.7.4 on your machine from the official [Python site](https://www.python.org/downloads/).
* Download the following code files from [github](https://github.com/udacity/fullstack-nanodegree-vm/tree/master/vagrant/tournament) 
      1. _tournament.sql_  - Setup database, tables and views
      2. _tournament.py_   - Python module containing DB api to register players and review standings and pairings
      3. _tournament_test.py_  - Tests to verify program is running as per specifications.
* Setup database by running the included sql file from postgres command line
  `psql> \i tournament.sql`
  
## Running program
* From python command line run the tournament_test.py program, or open the file from IDLE (python GUI), open this file, and run using F5. 
    `C:\  > tournament_test.py
    
* Verify that all the tests pass.
