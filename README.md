# MTGS Post Wordcloud generator

Tool to parse posts in MTGSalvation threads and generate a word cloud for an arbitrary number of posters. 

## Usage
`python MTGSWordCloud.py [thread link] -p [player1 player2 player3 ...]` will generated a word cloud (default 200 words) of posts made by the listed players from the linked thread.

- Thread link is the full URL to the start of the game
- Player list is just names separated by spaces
- Player names with spaces in them must be enclosed "in quotes"
- Player names must exactly match MTGS user name (no nicknames)
- If no players are given, a word cloud will be generated for everyone that posted in the thread

`python MTGSWordCloud.py -h` will print a  help message.

## Requirements
This project requires the pip packages beautiful soup, wordcloud, and argparse. See requirements.txt for full details.
Use `pip install -r requirements.txt` to install them before use.
