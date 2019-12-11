
import os
import chess.pgn as pgn

from datetime import datetime
from datetime import timedelta

GAMES_FILE = os.path.join('..', 'data', 'games.pgn')
PIECE_WEIGHTS = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9
}

# Load games from PGN file
with open(GAMES_FILE) as f:
    game = pgn.read_game(f)

row_white = []
row_black = []

# USER_ID
row_white.append(game.headers['White'])
row_black.append(game.headers['Black'])

# GAME_LINK
row_white.append(game.headers['Site'])
row_black.append(game.headers['Site'])

# ELO
row_white.append(game.headers['WhiteElo'])
row_black.append(game.headers['BlackElo'])

# COLOUR
row_white.append('White')
row_black.append('Black')

# OPENING
row_white.append(game.headers['Opening'])
row_black.append(game.headers['Opening'])

# RESULT

if "1/2" in game.headers['Result']:
    result_white = 2
    result_black = 2
elif game.headers['Result'][0] == "1":
    result_white = 1
    result_black = 0
else:
    result_white = 0
    result_black = 1

row_white.append(result_white)
row_black.append(result_black)

## TIME_PER_MOVEMENT, POINTS_BALANCE, TAKEN_BALANCE

white = {'taken': [], 'times': [], '_last_time': None}
black = {'taken': [], 'times': [], '_last_time': None}

board = game.board()

for i, node in enumerate(game.mainline()):
    # Parse remaining time from GameMove
    t = datetime.strptime(node.comment[6:-1], "%H:%M:%S")
    remaining_time = timedelta(
        hours=t.hour, minutes=t.minute, seconds=t.second)

    # TIME_PER_MOVEMENT
    if i % 2 == 0:  # White player
        if white['_last_time'] is not None:
            white['times'].append(
                (white['_last_time'] - remaining_time).total_seconds())
        white['_last_time'] = remaining_time
    else:  # Black player
        if black['_last_time'] is not None:
            black['times'].append(
                (black['_last_time'] - remaining_time).total_seconds())
        black['_last_time'] = remaining_time

    ## TAKEN_BALANCE & POINTS_BALANCE
    if 'x' in node.san():
        piece_weight = PIECE_WEIGHTS[board.piece_at(
            node.move.to_square).symbol().upper()]
        if i % 2 == 0:  # White player takes the piece
            white['taken'].append(1 * piece_weight)
            black['taken'].append(-1 * piece_weight)
        else:  # Black player takes the piece
            black['taken'].append(1 * piece_weight)
            white['taken'].append(-1 * piece_weight)
    else:  # No takes in this movement
        white['taken'].append(0)
        black['taken'].append(0)

    board.push(node.move)

del white['_last_time']
del black['_last_time']

# MOVEMENTS

moves_white = len(white['taken'])
moves_black = len(black['taken'])

row_white.append(moves_white)
row_black.append(moves_black)

# TOTAL_TIME_PER_PLAYER

row_white.append(sum(white['times']))
row_black.append(sum(black['times']))

# TOTAL_TIME

total_time = sum(white['times']) + sum(black['times'])

row_white.append(total_time)
row_black.append(total_time)

## POINTS_BALANCE & TAKEN_BALANCE

row_white.append(sum(white['taken']))
row_white.append(sum([1 if t > 0 else 0 for t in white['taken']]) +
                 sum([-1 if t < 0 else 0 for t in white['taken']]))

row_black.append(sum(black['taken']))
row_black.append(sum([1 if t > 0 else 0 for t in black['taken']]) +
                 sum([-1 if t < 0 else 0 for t in black['taken']]))

# AGGRESSIVENESS

white_aggressiveness = 0
black_aggressiveness = 0

# EARLY_TAKEN

moves = max(moves_white, moves_black)

white_early_game = white['taken'][:int(moves*1/3)]
black_early_game = black['taken'][:int(moves*1/3)]

# CASTLING

white_castling = False
black_castling = False

for i, move in enumerate(game.mainline()):
    if move.san() == 'O-O':
        if i % 2 == 0:  # White player
            white_castling = True
        else:  # Black player
            black_castling = True

if not white_castling:
    white_aggressiveness += 2

if not black_castling:
    black_aggressiveness += 2

# AGGRESSIVE_OPENING

white_opening_aggressiveness = ['Sicilian Defense: Grand Prix Attack', 'Sicilian Defense: Smith-Morra Gambit', 'Trompowsky Attack', 'Trompowsky Attack: Classical Defense',
                                'Trompowsky Attack: Borg Variation', 'Trompowsky Attack: Raptor Variation', 'Trompowsky Attack: Edge Variation', 'Danish Gambit',
                                'Sicilian Defense: Alapin Variation', 'Sicilian Defense: Alapin Variation, Smith-Morra Declined', 'King\'s Gambit', 'Petrov\'s Defense',
                                'Four Knights Game: Italian Variation', 'Four Knights Game: Italian Variation, Noa Gambit', 'Four Knights Game: Scotch Variation Accepted',
                                'Four Knights Game: Scotch Variation, Belgrade Gambit', 'Four Knights Game: Spanish Variation', 'Four Knights Game: Spanish Variation, Classical Variation',
                                'Four Knights Game: Spanish Variation, Rubinstein Variation']
black_opening_aggressiveness = ['Queen\'s Gambit Refused: Albin Countergambit', 'Queen\'s Gambit Refused: Albin Countergambit, Modern Line', 'Queen\'s Gambit Refused: Albin Countergambit, Normal Line',
                                'Scandinavian Defense: Portuguese Variation', 'Alekhine Defense', 'Alekhine Defense: Balogh Variation', 'Alekhine Defense: Brooklyn Variation', 'Alekhine Defense: Exchange Variation',
                                'Alekhine Defense: Four Pawns Attack', 'Alekhine Defense: Four Pawns Attack, Main Line', 'Alekhine Defense: Four Pawns Attack, Trifunovic Variation', 'Alekhine Defense: Hunt Variation',
                                'Alekhine Defense: Hunt Variation, Lasker Simul Gambit', 'Alekhine Defense: Maróczy Variation', 'Alekhine Defense: Modern Variation, Alekhine Gambit', 'Alekhine Defense: Modern Variation, Alekhine Variation',
                                'Alekhine Defense: Modern Variation, Larsen Variation', 'Alekhine Defense: Modern Variation, Larsen-Haakert Variation', 'Alekhine Defense: Modern Variation, Main Line',
                                'Alekhine Defense: Modern Variation, Panov Variation', 'Alekhine Defense: Normal Variation', 'Alekhine Defense: Scandinavian Variation', 'Alekhine Defense: Sämisch Attack', 'Alekhine Defense: Two Pawn Attack',
                                'Alekhine Defense: Two Pawn Attack, Lasker Variation', 'Budapest Defense', 'Budapest Defense: Adler Variation', 'Budapest Defense: Rubinstein Variation', 'Sicilian Defense', 'Sicilian Defense: Accelerated Dragon',
                                'Sicilian Defense: Accelerated Dragon, Maróczy Bind', 'Sicilian Defense: Accelerated Dragon, Modern Bc4 Variation', 'Sicilian Defense: Alapin Variation', 'Sicilian Defense: Alapin Variation, Smith-Morra Declined',
                                'Sicilian Defense: Bowdler Attack', 'Sicilian Defense: Canal Attack, Haag Gambit', 'Sicilian Defense: Canal-Sokolsky Attack', 'Sicilian Defense: Classical Variation', 'Sicilian Defense: Closed', 'Sicilian Defense: Closed Variation',
                                'Sicilian Defense: Closed Variation, Chameleon Variation', 'Sicilian Defense: Closed Variation, Traditional', 'Sicilian Defense: Delayed Alapin', 'Sicilian Defense: Delayed Alapin Variation', 'Sicilian Defense: Dragon Variation',
                                'Sicilian Defense: Dragon Variation, Classical Variation', 'Sicilian Defense: Dragon Variation, Levenfish Variation', 'Sicilian Defense: Dragon Variation, Yugoslav Attack', 'Sicilian Defense: Dragon Variation, Yugoslav Attack, Belezky Line',
                                'Sicilian Defense: Dragon Variation, Yugoslav Attack, Modern Line', 'Sicilian Defense: Dragon, 6. Be3', 'Sicilian Defense: Four Knights Variation', 'Sicilian Defense: Franco-Sicilian Variation', 'Sicilian Defense: French Variation',
                                'Sicilian Defense: Grand Prix Attack', 'Sicilian Defense: Hyperaccelerated Dragon', 'Sicilian Defense: Kalashnikov Variation', 'Sicilian Defense: Kan Variation, Modern Variation', 'Sicilian Defense: Kramnik Variation',
                                'Sicilian Defense: Lasker-Dunne Attack', 'Sicilian Defense: Lasker-Pelikan Variation, Exchange Variation', 'Sicilian Defense: Lasker-Pelikan Variation, Schlechter Variation', 'Sicilian Defense: Lasker-Pelikan Variation, Sveshnikov Variation',
                                'Sicilian Defense: Lasker-Pelikan Variation, Sveshnikov Variation, Chelyabinsk Variation', 'Sicilian Defense: McDonnell Attack', 'Sicilian Defense: McDonnell Attack, Tal Gambit', 'Sicilian Defense: Modern Variations, Anti-Qxd4 Move Order',
                                'Sicilian Defense: Modern Variations, Tartakower', 'Sicilian Defense: Morphy Gambit', 'Sicilian Defense: Najdorf Variation', 'Sicilian Defense: Najdorf Variation, Adams Attack', 'Sicilian Defense: Najdorf Variation, Amsterdam Variation',
                                'Sicilian Defense: Najdorf Variation, English Attack', 'Sicilian Defense: Najdorf Variation, Main Line', 'Sicilian Defense: Najdorf Variation, Opocensky Variation', 'Sicilian Defense: Najdorf, Lipnitsky Attack', 'Sicilian Defense: Nyezhmetdinov-Rossolimo Attack',
                                'Sicilian Defense: O\'Kelly Variation, Maróczy Bind, Robatsch Line', 'Sicilian Defense: Old Sicilian', 'Sicilian Defense: Open', 'Sicilian Defense: Paulsen Variation', 'Sicilian Defense: Paulsen Variation, Bastrikov Variation', 'Sicilian Defense: Paulsen Variation, Normal Variation',
                                'Sicilian Defense: Paulsen Variation, Szén Variation', 'Sicilian Defense: Scheveningen Variation, Classical Variation', 'Sicilian Defense: Scheveningen Variation, Delayed Keres Attack', 'Sicilian Defense: Scheveningen Variation, English Attack', 'Sicilian Defense: Smith-Morra Gambit',
                                'Sicilian Defense: Smith-Morra Gambit Accepted, Classical Formation', 'Sicilian Defense: Smith-Morra Gambit Accepted, Fianchetto Defense', 'Sicilian Defense: Smith-Morra Gambit Accepted, Kan Formation', 'Sicilian Defense: Smith-Morra Gambit Accepted, Paulsen Formation',
                                'Sicilian Defense: Smith-Morra Gambit Accepted, Pin Defense', 'Sicilian Defense: Smith-Morra Gambit Accepted, Scheveningen Formation', 'Sicilian Defense: Smith-Morra Gambit Declined, Dubois Variation', 'Sicilian Defense: Smith-Morra Gambit Declined, Push Variation',
                                'Sicilian Defense: Smith-Morra Gambit Declined, Scandinavian Formation', 'Sicilian Defense: Smith-Morra Gambit Deferred', 'Sicilian Defense: Staunton-Cochrane Variation', 'Sicilian Defense: Wing Gambit', 'Sicilian Defense: Wing Gambit, Carlsbad Variation',
                                'Sicilian Defense: Wing Gambit, Marshall Variation']

white_aggressive_opening = False
black_aggressive_opening = False

if game.headers['Opening'] in white_opening_aggressiveness:
    white_aggressive_opening = True
    white_aggressiveness += 2

if game.headers['Opening'] in black_opening_aggressiveness:
    black_aggressive_opening = True
    black_aggressiveness += 2

row_white.append(white_aggressiveness)
row_black.append(black_aggressiveness)
