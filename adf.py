import random
import pandas as pd


class Person:
    def __init__(self, age, gender, name):
        self.age = age
        self.gender = gender
        self.fertile = True
        self.name = name

    def age_one_year(self):
        self.age += 1
        if self.age > 30:
            self.fertile = False


import math


def simulate_population(
    years, initial_population_size, growth_rate=0.02, growth_rate_increment=0.0001
):
    population = []
    g = growth_rate
    y = 0
    for _ in range(initial_population_size):
        age = random.randint(1, 30)
        gender = random.choice(["Male", "Female"])
        population.append(Person(age, gender, name=_))
    population_history = []
    while population:
        for year in range(1, years + 1):
            if year % 50 == 0:
                g += growth_rate_increment
            if year % 100 == 0:
                g -= growth_rate_increment * growth_rate_increment
            current_population = len(population)
            for person in population:
                person.age_one_year()
                if not person.fertile:
                    population.remove(person)
            possible_births = g * current_population
            if year % random.randint(3, 5) == 0:
                current_population -= 0.05 * current_population
            if year % random.randint(10, 25) == 0:
                current_population -= 0.3 * 0.34 * current_population
            if year % random.randint(15, 30) == 0:
                current_population -= 0.5 * 0.6 * current_population
            for _ in range(int(possible_births)):
                gender = random.choice(["Male", "Female"])
                population.append(Person(age=18, gender=gender, name=_))
            population_history.append(current_population)
            if len(population) >= 1500000:
                y = year
                print("Collapsed:", y)
                break
    print("Completed:", y)
    return population_history, y


from threading import Thread

t = [
    Thread(target=simulate_population, args=(1000, 1000, 0.02, 0.0001)),
    Thread(target=simulate_population, args=(1000, 10000, 0.02, 0.0001)),
    Thread(target=simulate_population, args=(100, 1000, 0.2, 0.0000001)),
    Thread(target=simulate_population, args=(1000, 10000, 0.02, 0.000003)),
]
print(*[i.start() for i in t])
