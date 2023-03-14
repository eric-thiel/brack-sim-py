import pandas as pd
import numpy as np
from itertools import permutations
import random
from models import Team, adjust_name
from tqdm import tqdm
from generate_actuals import sim_actuals
from generate_choices import sim_choices
from collections import Counter
from scipy.stats import rankdata


def generate_bracket():
    seed_list = pd.read_csv('/Users/ericthiel/Downloads/bracket_2023 - seed_list.csv').to_dict('records')
    teams = {}
    for i in seed_list:
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

def score_brackets(player_brackets, sim_dict):
    score_dict = {1:1, 2:2, 3:4, 4:8, 5:16, 6:32}
    player_scores = {}
    for id, player_bracket in tqdm(player_brackets.items()):
        score = []
        for sim, picks in sim_dict.items():
            round_count = 1
            score_indiv = []
            for round, round_res in zip(player_bracket, picks):
                p = set(round)&set(round_res)
                score_indiv.append(len(p) * score_dict[round_count])
                round_count += 1
            score.append(sum(score_indiv) + random.uniform(-0.02, 0.02))  # nudge to avoid ties
        player_scores[id] = score
    

    return player_scores, player_brackets




def run_contest_sims(player_scores, player_brackets):
    player_placements = {}
    for player_id, obj in player_brackets.items():
        player_placements[player_id] = {'won': 0, 'top_10': 0, 'in': 0}
    for _ in tqdm(range(1000)):
        picked_brackets = {}
        shit = np.random.choice(list(player_brackets.keys()), 200)
        for i in shit:
            picked_brackets[i] = player_scores[i]
        contest = []
        for i in range(len(player_scores[0])):
            contest_scores = [item[i] for item in picked_brackets.values()]
            contest.append(contest_scores)
        ranks = len(contest[0]) - rankdata(contest, method="min", axis=1) + 1
        by_lineup = np.transpose(ranks)
        n_in_contest = len(by_lineup)
        g = 0
        hold = {}
        for id, obj in picked_brackets.items():
            hold[id] = by_lineup[g]
            g+=1
        for id, placements in hold.items():
            player_placements[id]['won'] += np.count_nonzero(placements == 1)
            player_placements[id]['top_10'] += np.count_nonzero(placements <= 10)
            player_placements[id]['in'] += len(player_scores[0])

    final = {}
    for id, obj in player_placements.items():
        try:
            final[id] = obj['top_10'] / obj['in']
        except:
            final[id] = 0
    # print(final)
    sorted_one = sorted(final.items(), key=lambda x:x[1], reverse=True)
    print("")
    print(sorted_one[0])
    print(player_placements[sorted_one[0][0]])
    print(sorted_one[1])
    print(player_placements[sorted_one[1][0]])
    print(sorted_one[2])
    print(player_placements[sorted_one[2][0]])
    print("")
    print("FIRST")
    print(player_brackets[sorted_one[0][0]])
    print("")
    print("SECOND")
    print(player_brackets[sorted_one[1][0]])
    print("")
    print("THIRD")
    print(player_brackets[sorted_one[2][0]])
    print("")




def run():
    West, Midwest, East, South = generate_bracket()
    sim_dict = sim_actuals(West, Midwest, East, South, n=5000)
    player_brackets = sim_choices(West, Midwest, East, South, n=1000)
    player_scores, player_brackets = score_brackets(player_brackets, sim_dict)
    run_contest_sims(player_scores, player_brackets)

    # winner = []
    # for sim_num, results in player_brackets.items():
    #     winner.append(results[5][0])
    # wins = Counter(winner)
    # df = pd.DataFrame.from_dict(wins, orient='index').reset_index()
    # df.to_csv('picks_attempt.csv')
    # print(df)


if __name__ == "__main__":
    run()


