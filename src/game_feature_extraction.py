import os
import chess.pgn as pgn
import pandas as pd

from numpy import mean, median, var

from datetime import datetime
from datetime import timedelta

#GAMES_FILE = os.path.join('..', 'data', 'top200_sept2019', 'games0-199.pgn')
#TARGET_DATA_FILE = os.path.join('..', 'data', 'games_target_data.csv')

GAMES_FILE = os.path.join('..', 'data', 'test', 'games_october.pgn')
TARGET_DATA_FILE = os.path.join('..', 'data', 'test', 'games_target_data_test.csv')

COLUMNS = [
    'white_user_id',
    'white_elo',
    'white_aggressiveness',
    'white_total_time',
    'white_early_times_mean',
    'white_early_times_median',
    'white_early_times_variance',
    'white_early_times_max',
    'white_early_times_min',
    'white_mid_times_mean',
    'white_mid_times_median',
    'white_mid_times_variance',
    'white_mid_times_max',
    'white_mid_times_min',
    'white_end_times_mean',
    'white_end_times_median',
    'white_end_times_variance',
    'white_end_times_max',
    'white_end_times_min',

    'black_user_id',
    'black_elo',
    'black_aggressiveness',
    'black_total_time',
    'black_early_times_mean',
    'black_early_times_median',
    'black_early_times_variance',
    'black_early_times_max',
    'black_early_times_min',
    'black_mid_times_mean',
    'black_mid_times_median',
    'black_mid_times_variance',
    'black_mid_times_max',
    'black_mid_times_min',
    'black_end_times_mean',
    'black_end_times_median',
    'black_end_times_variance',
    'black_end_times_max',
    'black_end_times_min',

    'game_link',
    'opening',
    'result',
    'movements',
    'total_time',
    'points_balance',
    'taken_balance'
]

PIECE_WEIGHTS = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9
}

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

early_agressiveness = lambda early_taken_count: 0 if early_taken_count < 3 else (0.5 if early_taken_count < 6 else 1)

def time_metrics(times):
    '''
        Mean, median, variance, maximum, minimum
    '''
    return mean(times), median(times), var(times), max(times, default=None), min(times, default=None)

def partition_times(times, moves_count):
    '''
        Movement count / 2 => movements per player
        Movements per player / 3 => Movements per game stage
        
        Note: First movement time is omitted due to Lichess.org time format
    '''
    early_times = times[:int(moves_count/6)-1]
    mid_times = times[int(moves_count/6)-1:int(moves_count/3)]
    end_times = times[int(moves_count/3):]

    return early_times, mid_times, end_times

def process_game_movements(game):
    white = {'taken': [], 'times': [], '_last_time': None}
    black = {'taken': [], 'times': [], '_last_time': None}
    time_increase = int(game.headers['TimeControl'].split('+')[-1])

    board = game.board()

    for i, node in enumerate(game.mainline()):
        # Parse remaining time from GameMove
        try:
            t = datetime.strptime(node.comment[6:-1], "%H:%M:%S")
        except ValueError:
            t = datetime.strptime('0:0:0', "%H:%M:%S")
            
        remaining_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        # TIME_PER_MOVEMENT
        if i % 2 == 0:  # White player
            if white['_last_time'] is not None:
                white['times'].append(
                    (white['_last_time'] - remaining_time).total_seconds() + time_increase)
            white['_last_time'] = remaining_time
        else:  # Black player
            if black['_last_time'] is not None:
                black['times'].append(
                    (black['_last_time'] - remaining_time).total_seconds() + time_increase)
            black['_last_time'] = remaining_time

        ## TAKEN_BALANCE & POINTS_BALANCE
        if 'x' in node.san():
            taken_piece = board.piece_at(node.move.to_square)
            if taken_piece is None: # Take "on passant" (the Pawn is not in the dst square)
                piece_weight = PIECE_WEIGHTS['P']
            else:
                piece_weight = PIECE_WEIGHTS[taken_piece.symbol().upper()]
            
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

    return white, black

def calculate_aggressiveness(game, white, black, moves_count):
    white_aggressiveness = 0
    black_aggressiveness = 0

    # EARLY_TAKEN

    white_early_taken = sum([1 for white_taken in white['taken'][:int(moves_count/3)] if white_taken > 0])
    black_early_taken = sum([1 for black_taken in black['taken'][:int(moves_count/3)] if black_taken > 0])

    white_aggressiveness += early_agressiveness(white_early_taken)
    black_aggressiveness += early_agressiveness(black_early_taken)

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

    white_aggressive_opening = False
    black_aggressive_opening = False

    if game.headers['Opening'] in white_opening_aggressiveness:
        white_aggressive_opening = True
        white_aggressiveness += 2

    if game.headers['Opening'] in black_opening_aggressiveness:
        black_aggressive_opening = True
        black_aggressiveness += 2

    return white_aggressiveness, black_aggressiveness

def calculate_elo(game):
    try:
        white_elo = int(game.headers['WhiteElo'])
    except ValueError:
        white_elo = None

    try:
        black_elo = int(game.headers['BlackElo'])
    except ValueError:
        black_elo = None

    # Si el ELO es '?' (es la IA), rellenamos con el ELO del oponente (porque Lichess genera partidas de ELO similar)
    if white_elo is None:
        white_elo = black_elo
    if black_elo is None:
        black_elo = white_elo
    
    return white_elo, black_elo

def calculate_result(game):
    if "1/2" in game.headers['Result']: # Draw
        return 1
    elif game.headers['Result'][0] == "1":  # White wins
        return 0
    else:   # Black wins
        return 2


games_target_data = []

# Load games from PGN file
with open(GAMES_FILE, encoding="utf-8-sig") as f:
    game = pgn.read_game(f)
    
    game_index = 0
    while game:
        game_index += 1
        print(f"\r{game_index} {game.headers['Site']}", end='', flush=True)

        ## ELO
        white_elo, black_elo = calculate_elo(game)

        ## TIME_PER_MOVEMENT, POINTS_BALANCE, TAKEN_BALANCE
        white, black = process_game_movements(game)

        ## NUMBER_OF_MOVEMENTS
        assert len(white['taken']) == len(black['taken'])
        moves_count = len(white['taken'])
        
        ## AGGRESSIVENESS
        white_aggressiveness, black_aggressiveness = calculate_aggressiveness(game, white, black, moves_count)

        # Partition movement times in early/mid/end
        w_early, w_mid, w_end = partition_times(white['times'], moves_count)
        b_early, b_mid, b_end = partition_times(black['times'], moves_count)
        if(any(len(t) == 0 for t in [w_early, w_mid, w_end, b_early, b_mid, b_end])):
            print(" [ WARNING: Empty game slices ]")
            print(w_early, w_mid, w_end)
            print(b_early, b_mid, b_end)


        data_row = []

        # WHITE_USER_ID
        data_row.append(game.headers['White'])
        # WHITE_ELO
        data_row.append(white_elo)
        # WHITE_AGGRESSIVENESS
        data_row.append(white_aggressiveness)
        # WHITE_TOTAL_TIME
        data_row.append(sum(white['times']))
        # TIME_METRICS (mean, median, var, min, max)
        data_row.extend(time_metrics(w_early))
        data_row.extend(time_metrics(w_mid))
        data_row.extend(time_metrics(w_end))
        
        # BLACK_USER_ID
        data_row.append(game.headers['Black'])
        # BLACK_ELO
        data_row.append(black_elo)
        # BLACK_AGGRESSIVENESS
        data_row.append(black_aggressiveness)
        # BLACK_TOTAL_TIME
        data_row.append(sum(black['times']))
        # TIME_METRICS (mean, median, var, min, max)
        data_row.extend(time_metrics(b_early))
        data_row.extend(time_metrics(b_mid))
        data_row.extend(time_metrics(b_end))

        # GAME_LINK
        data_row.append(game.headers['Site'])
        # OPENING
        data_row.append(game.headers['Opening'])
        # RESULT
        data_row.append(calculate_result(game))
        # MOVEMENTS_COUNT
        data_row.append(moves_count)
        # TOTAL_TIME
        data_row.append(sum(white['times']) + sum(black['times']))
        # POINTS_BALANCE
        data_row.append(sum(white['taken']))
        # TAKEN_BALANCE
        data_row.append(sum([1 if t > 0 else 0 for t in white['taken']]) +
                        sum([-1 if t < 0 else 0 for t in white['taken']]))
        
        games_target_data.append(data_row)

        # Read next game. Iterate again
        game = pgn.read_game(f)

# Save target data into csv
df = pd.DataFrame(games_target_data, columns=COLUMNS)

# Borra nulls en las particiones de los tiempos (partidas muy cortas)
df = df.dropna()

NON_NEGATIVE_COLUMNS = [
    'white_total_time',
    'white_early_times_mean',
    'white_early_times_median',
    'white_early_times_variance',
    'white_early_times_max',
    'white_early_times_min',
    'white_mid_times_mean',
    'white_mid_times_median',
    'white_mid_times_variance',
    'white_mid_times_max',
    'white_mid_times_min',
    'white_end_times_mean',
    'white_end_times_median',
    'white_end_times_variance',
    'white_end_times_max',
    'white_end_times_min',

    'black_total_time',
    'black_early_times_mean',
    'black_early_times_median',
    'black_early_times_variance',
    'black_early_times_max',
    'black_early_times_min',
    'black_mid_times_mean',
    'black_mid_times_median',
    'black_mid_times_variance',
    'black_mid_times_max',
    'black_mid_times_min',
    'black_end_times_mean',
    'black_end_times_median',
    'black_end_times_variance',
    'black_end_times_max',
    'black_end_times_min',

    'total_time'
]

# Borra los tiempos negativos (un jugador le ha dado tiempo al otro)
df.drop(df[df[df[NON_NEGATIVE_COLUMNS] < 0].any(axis=1)].index, inplace=True)

# Encode categorical variables: colour and opening
df['opening'] = df['opening'].astype('category')
df['opening_enc'] = df['opening'].cat.codes

df.to_csv(path_or_buf=TARGET_DATA_FILE)
