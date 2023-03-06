


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