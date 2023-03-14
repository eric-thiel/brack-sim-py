import pandas as pd
from tqdm import tqdm
from models import adjust_name
from scipy.stats import norm
import random

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



    
def get_game_picked(game_participants, pick_dict, round):
    if round == 1:
        one = pick_dict[game_participants[0].name][round]
        two = pick_dict[game_participants[1].name][round]
    else:
        one = pick_dict[game_participants[0].name][round] ** (1-round*0.09) # 0.07
        two = pick_dict[game_participants[1].name][round] ** (1-round*0.09) # 0.07
        if game_participants[0].name == 'Duke' or game_participants[0].name == 'Gonzaga':  # rabid fanbases
            one = pick_dict[game_participants[0].name][round] ** (1-round*0.09) + 0.02
            two = two = pick_dict[game_participants[1].name][round] ** (1-round*0.09) - 0.02
        if game_participants[1].name == 'Duke' or game_participants[1].name == 'Gonzaga':  # rabid fanbases
            one = pick_dict[game_participants[0].name][round] ** (1-round*0.09) -0.02
            two = two = pick_dict[game_participants[1].name][round] ** (1-round*0.09) + 0.02
    total = one + two
    one /= total
    two /= total
    if random.random() < one:
        return game_participants[0]
    else:
        return game_participants[1]



    # build_round(teams, first_four_winners)

def sim_choices(West, Midwest, East, South, n=100000):
    pick_dict = get_pick_percs()
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
    return choice_dict


def get_pick_percs():
    ok = pd.read_csv('/Users/ericthiel/Downloads/bracket_2023 - pick_perc_std.csv').to_dict('records')
    pick_dict = {}
    for i in ok:
        seed_list_adjusted_name = adjust_name(i['team'])
        pick_dict[seed_list_adjusted_name] = {1: i['prob_r1'], 2: i['prob_r2'], 3: i['prob_r3'], 4: i['prob_r4'], 5: i['prob_r5'], 6: i['prob_r6']}
    return pick_dict