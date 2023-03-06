import pandas as pd
import numpy as np
from itertools import permutations
from scipy.stats import norm
import random
from models import Team
from tqdm import tqdm


game_probs = {}

def generate_bracket():
    seed_list = pd.read_csv('/Users/ericthiel/Downloads/testing_brackets - seed_list.csv').to_dict('records')
    teams = {}
    for i in seed_list:
        if i['team'] not in ['Texas Southern', 'Indiana', 'Bryant', 'Notre Dame']:
            teams[i['team']] = Team(name=i['team'], region=i['region'], seed=i['seed'], first_four=i['first_four'], elim_round=i['elim_round'])
    position_map = {1:1, 16:2, 8:3, 9:4, 5:5, 12:6, 4:7, 13:8, 6:9, 11:10, 3:11, 14:12, 7:13, 10:14, 2:15, 15:16}
    West = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    Midwest = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    East = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    South = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
    for team, team_model in teams.items():
        if team_model.region == 'West':
            West[position_map[team_model.seed]-1] = team_model
        if team_model.region == 'Midwest':
            Midwest[position_map[team_model.seed]-1] = team_model
        if team_model.region == 'East':
            East[position_map[team_model.seed]-1] = team_model
        if team_model.region == 'South':
            South[position_map[team_model.seed]-1] = team_model
    return West, Midwest, East, South


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
        

def sim_choice_round(West, Midwest, East, South, pick_dict, round):
    West_winners = []
    Midwest_winners = []
    East_winners = []
    South_winners = []
    if round <= 4:
        for i in range(0, len(West), 2):
            # print(West[i], West[i+1])
            West_winners.append(get_game_picked([West[i], West[i+1]], pick_dict, round))
        # print(West_winners)
        for i in range(0, len(Midwest), 2):
            # print(West[i], West[i+1])
            Midwest_winners.append(get_game_picked([Midwest[i], Midwest[i+1]], pick_dict, round))
        # print(Midwest_winners)
        for i in range(0, len(East), 2):
            # print(West[i], West[i+1])
            East_winners.append(get_game_picked([East[i], East[i+1]], pick_dict, round))
        # print(East_winners)
        for i in range(0, len(South), 2):
            # print(West[i], West[i+1])
            South_winners.append(get_game_picked([South[i], South[i+1]], pick_dict, round))
        # print("")
    if round == 5:
        West_winners.append(get_game_picked([West[0], Midwest[0]], pick_dict, round))
        East_winners.append(get_game_picked([East[0], South[0]], pick_dict, round))
    if round == 6:
        West_winners.append(get_game_picked([West[0], East[0]], pick_dict, round))
    
    return West_winners, Midwest_winners, East_winners, South_winners


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
    
def get_game_picked(game_participants, pick_dict, round):
    one = pick_dict[game_participants[0].name][round]
    two = pick_dict[game_participants[1].name][round]
    total = one + two
    one /= total
    two /= total
    if random.random() < one:
        return game_participants[0]
    else:
        return game_participants[1]


def adjust_name(KP_name):
    kp_seedlist = {'Connecticut': 'UConn', "Saint Mary's": "Saint Mary's (CA)",
                   'Texas A&M Corpus Chris':'A&M-Corpus Christi',
                   'USC': 'Southern California',
                   'Miami FL': "Miami (FL)"}
    if KP_name in kp_seedlist:
        return kp_seedlist[KP_name]
    else:
        return KP_name


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

    # build_round(teams, first_four_winners)

def sim_choices(West, Midwest, East, South, pick_dict, n=10000):
    choice_dict = {}
    for i in tqdm(range(n)):
        sim_winners = []
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West, Midwest, East, South, pick_dict, 1)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West_winners, Midwest_winners, East_winners, South_winners, pick_dict, 2)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West_winners, Midwest_winners, East_winners, South_winners, pick_dict, 3)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West_winners, Midwest_winners, East_winners, South_winners, pick_dict, 4)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West_winners, Midwest_winners, East_winners, South_winners, pick_dict, 5)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        West_winners, Midwest_winners, East_winners, South_winners = sim_choice_round(West_winners, Midwest_winners, East_winners, South_winners, pick_dict, 6)
        sim_winners.append(West_winners + Midwest_winners + East_winners + South_winners)
        choice_dict[i] = sim_winners
    print(len(choice_dict))
    return choice_dict


def get_pick_percs():
    ok = pd.read_csv('/Users/ericthiel/Downloads/testing_brackets - pick_perc_std.csv').to_dict('records')
    pick_dict = {}
    for i in ok:
        seed_list_adjusted_name = adjust_name(i['team'])
        pick_dict[seed_list_adjusted_name] = {1: i['prob_r1'], 2: i['prob_r2'], 3: i['prob_r3'], 4: i['prob_r4'], 5: i['prob_r5'], 6: i['prob_r6']}
    return pick_dict

if __name__ == "__main__":

    pick_dict = get_pick_percs()
    West, Midwest, East, South = generate_bracket()
    sim_dict = sim_actuals(West, Midwest, East, South)
    # player_brackets = sim_choices(West, Midwest, East, South, pick_dict)

