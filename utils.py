from consts import Gender
from consts import last_names, male_names, female_names
from random import randint


def random_name_by_gender(gender: Gender):
    if gender is Gender.FEMALE:
        return last_names[randint(0, len(last_names) - 1)] + female_names[randint(0, len(female_names) - 1)]
    else:
        return last_names[randint(0, len(last_names) - 1)] + male_names[randint(0, len(male_names) - 1)]


if __name__ == '__main__':
    print(random_name_by_gender(Gender.random()))
