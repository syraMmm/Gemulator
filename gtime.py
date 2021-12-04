from consts import *


class GTime:
    year: int   # 年
    month: Month  # 月
    period: Period     # 旬

    def __init__(self, year, month: Month, period: Period):
        self.year = year
        self.month = month
        self.period = period

    def next(self):
        self._next_period()
        if self.period == Period.FIRST:
            self.month = Month((self.month.value + 1) % 12)
            if self.month == Month.JAN:
                self.year += 1

    def _next_period(self):
        if self.period == Period.FIRST:
            self.period = Period.SECOND
        elif self.period == Period.SECOND:
            self.period = Period.THIRD
        else:
            self.period = Period.FIRST

