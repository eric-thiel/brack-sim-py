import pandas as pd
import numpy as np
from itertools import permutations
import random
from models import Team, adjust_name
from tqdm import tqdm
from generate_actuals import sim_actuals
from generate_choices import sim_choices


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

def run():
    West, Midwest, East, South = generate_bracket()
    sim_dict = sim_actuals(West, Midwest, East, South)
    player_brackets = sim_choices(West, Midwest, East, South)
    print(sim_dict[1])
    print(player_brackets[1])

if __name__ == "__main__":
    run()


