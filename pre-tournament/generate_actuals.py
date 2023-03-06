import pandas as pd


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