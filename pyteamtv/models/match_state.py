class MatchState(object):
    def __init__(
        self,
        home_score: int,
        away_score: int,
        time: float,
        current_period: int,
        period_active: bool,
    ):
        self.home_score = home_score
        self.away_score = away_score
        self.time = time
        self.current_period = current_period
        self.period_active = period_active

    def __eq__(self, other: "MatchState"):
        return (
            self.home_score == other.home_score
            and self.away_score == other.away_score
            and self.time == other.time
            and self.current_period == other.current_period
            and self.period_active == other.period_active
        )

    @property
    def as_dict(self):
        return dict(
            home_score=self.home_score,
            away_score=self.away_score,
            time=self.time,
            current_period=self.current_period,
            period_active=self.period_active,
        )

    @property
    def time_str(self):
        if not self.period_active:
            if self.current_period == 0:
                return "START"
            elif self.current_period == 1:
                return "RUST"
            elif self.current_period == 2:
                return "EINDE"
        else:
            minutes, seconds = divmod(int(self.time), 60)
            return f"{minutes:02d}:{seconds:02d}"

    def __repr__(self):
        return f"<MatchState time={self.time} score={self.home_score}-{self.away_score} active={self.period_active}>"
