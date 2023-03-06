

def adjust_name(KP_name):
    kp_seedlist = {'Connecticut': 'UConn', "Saint Mary's": "Saint Mary's (CA)",
                   'Texas A&M Corpus Chris':'A&M-Corpus Christi',
                   'USC': 'Southern California',
                   'Miami FL': "Miami (FL)"}
    if KP_name in kp_seedlist:
        return kp_seedlist[KP_name]
    else:
        return KP_name


class Team:
    def __init__(
        self,
        name=None,
        region=None,
        seed=None,
        first_four=None,
        elim_round=None
    ):
        self.name = name
        self.region = region
        self.seed = seed
        self.first_four = first_four
        self.elim_round = elim_round
    def __repr__(self):
            return f"{self.name}"