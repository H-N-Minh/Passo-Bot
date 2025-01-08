#!/bin/bash

# Number of times to play the game
num_games=100
games_played=0
games_won=0

# Loop to play the game 50 times
for ((i=1; i<=num_games; i++))
do
    echo "Starting game $i"
    output=$(python3 main.py)
    echo "$output"
    echo "Finished game $i"
    echo "----------------------"

    ((games_played++))
    
    if [[ $output == *"MATCH_WON"* ]]; then
        ((games_won++))
    fi

done

echo "All games completed."
echo "Games played: $games_played"
echo "Games won: $games_won"
