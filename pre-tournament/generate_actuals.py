import pandas as pd
from tqdm import tqdm
from models import adjust_name
from scipy.stats import norm
import random

game_probs = {}

def sim_actuals(West, Midwest, East, South, n=10000):
    kenpom = pd.read_csv('/Users/ericthiel/Downloads/testing_brackets - KP.csv').to_dict('records')
    kp_dict = {}
    for team in kenpom:
        seed_list_adjusted_name = adjust_name(team['TeamName'])
        kp_dict[seed_list_adjusted_name] = team
    sim_dict = {}
    for i in tqdm(range(n)):
        sim_winners = []
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West, Midwest, East, South, kp_dict, 1)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West_winners, Midwest_winners, East_winners, South_winners, kp_dict, 2)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West_winners, Midwest_winners, East_winners, South_winners, kp_dict, 3)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West_winners, Midwest_winners, East_winners, South_winners, kp_dict, 4)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West_winners, Midwest_winners, East_winners, South_winners, kp_dict, 5)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_round(West_winners, Midwest_winners, East_winners, South_winners, kp_dict, 6)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        sim_dict[i] = sim_winners
    return sim_dict

def get_game_winner(game_participants, kp_dict):
    game_name = f"{game_participants[0].name} vs {game_participants[0].name}"
    if game_name not in game_probs:
        one = kp_dict[game_participants[0].name]['AdjEM']
        two = kp_dict[game_participants[1].name]['AdjEM']
        prob = norm.cdf(one - two, 0, 9)
        game_probs[game_name] = prob
    else:
        prob = game_probs[game_name]
    # print(prob, game_participants[0], game_participants[1])
    if random.random() < prob:
        return game_participants[0]
    else:
        return game_participants[1]
    
def sim_round(West, Midwest, East, South, kp_dict, round):
    West_winners = []
    Midwest_winners = []
    East_winners = []
    South_winners = []
    # print("")
    # print(West)
    # print(East)
    if round <= 4:
        for i in range(0, len(West), 2):
            # print(West[i], West[i+1])
            West_winners.append(get_game_winner([West[i], West[i+1]], kp_dict))
        # print(West_winners)
        for i in range(0, len(Midwest), 2):
            # print(West[i], West[i+1])
            Midwest_winners.append(get_game_winner([Midwest[i], Midwest[i+1]], kp_dict))
        # print(Midwest_winners)
        for i in range(0, len(East), 2):
            # print(West[i], West[i+1])
            East_winners.append(get_game_winner([East[i], East[i+1]], kp_dict))
        # print(East_winners)
        for i in range(0, len(South), 2):
            # print(West[i], West[i+1])
            South_winners.append(get_game_winner([South[i], South[i+1]], kp_dict))
        # print("")
    if round == 5:
        West_winners.append(get_game_winner([West[0], Midwest[0]], kp_dict))
        East_winners.append(get_game_winner([East[0], South[0]], kp_dict))
    if round == 6:
        West_winners.append(get_game_winner([West[0], East[0]], kp_dict))
    
    return West_winners, Midwest_winners, East_winners, South_winners