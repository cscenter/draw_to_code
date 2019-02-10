from random import randint, choice, sample, uniform
import numpy as np
import multiprocessing as mp


def try_random(chance):
    return uniform(0., 1.) < chance


"""
Find optimal (minimal) 'animal' for function goodness using genetic algorithm
ARGUMENTS:
    create_animal: function, that should take nothing and return random animal
    badness: function, that takes animal object and return it's characteristic (number)
    mutation: function, that takes one animal and return it's copy with some changes
    crossing: function, that takes two animals and return another animal - his 'mix'
        (warning - mutation and crossing shouldn't change they arguments)\
    
    population_count: it's clear
    best_survive: how many best animals survive in every generation
    random_survive: how many randomly selected animals survive in every generation
    random_appears: how many new random animals appears in every generation
    
    crossing_chance, mutation_chance: it's clear
    max_epochs: how many epochs should be completed to finish
    max_epochs_without_progress: how many epochs without increasing best result
        should be completed to finish
    
    
RETURN: three objects
    1) best animal
    2) his result
    3) list with all best results for every generation
"""
def genetic(create_animal, badness, mutation, crossing=None,
            population_count=25, best_survive=5, random_survive = 3, random_appears=2,
            crossing_chance = 0., mutation_chance=0.4,
            max_epochs = 1000, max_epochs_without_progress=25, max_cataclysm=3,
            use_multithread=False):

    assert population_count >= best_survive + random_survive + random_appears
    # First generation
    population = [[create_animal(), None] for _ in range(population_count)]

    history = []
    old_best_result = -np.inf
    epochs_without_progress = 0
    epoch_num = 0
    cataclysm_count = 0
    while epoch_num < max_epochs and cataclysm_count <= max_cataclysm:
        # Sorting by goodness
        if not use_multithread:
            for p in population:
                if p[1] is None:
                    p[1] = badness(p[0])
        else:
            mparr = mp.Array('d', population_count, lock=False)

            def calc(param, i, a):
                a[i] = badness(param)

            threads = []
            for i, p in enumerate(population):
                if p[1] is None:
                    thr = mp.Process(target=calc, args=(p[0], i, mparr))
                    threads.append(thr)
                    thr.start()

            for thr in threads:
                thr.join()

            for i, p in enumerate(population):
                if p[1] is None:
                    p[1] = mparr[i]

        population.sort(key=lambda p : p[1])

        #for p in population:
        #    print(p)

        # Select animals form last generation
        parents = population[0 : best_survive]
        parents += sample(population, random_survive)
        parents += [[create_animal(), None] for _ in range(random_appears)]

        # Creating new animals
        population = parents.copy()

        while len(population) < population_count:
            if try_random(crossing_chance):
                new_animal = crossing(choice(parents)[0], choice(parents)[0])
            else:
                new_animal = mutation(choice(parents)[0])

            while try_random(mutation_chance):
                new_animal = mutation(new_animal)

            population.append([new_animal, None])

        # Counting result
        best_result = population[0][1]
        if old_best_result == best_result:
            epochs_without_progress += 1
        else:
            epochs_without_progress = 0
        old_best_result = best_result
        epoch_num += 1

        # Cataclysm
        if epochs_without_progress >= max_epochs_without_progress:
            epochs_without_progress = 0
            cataclysm_count += 1
            print("Cataclysm!")
            population = [population[0]] + \
                         [[create_animal(), None] for _ in range(population_count - 1)]

        # Printing
        history.append(best_result)
        print("Generation {}, result: {}, animal: {}".format(epoch_num,
                                                             round(best_result),
                                                             population[0][0]))

    with open("genetic_log.txt", "w") as fout:
        fout.write("{}\n{}\n".format(population[0][0], population[0][1]))
    return population[0][0], population[0][1], history


"""
Find optimal params to maximize goodness, function
ARGUMENTS:
    param_variants: list of lists; params[i] contains all possible variants for i-th param
    all other arguments is same as for function 'genetic'
    you shouldn't write functions create_animal, mutation and crossing -
        they will be built automatically
RETURN: same objects as function 'genetic'
"""
def optimize_params(param_variants, badness, **kwargs):
    n = len(param_variants)

    def create_animal():
        return [choice(vars) for vars in param_variants]

    def mutation(parent):
        result = parent.copy()
        i = randint(0, n - 1)
        result[i] = choice(param_variants[i])
        return result

    def crossing(mother, father):
        return [choice([mother[i], father[i]]) for i in range(n)]

    return genetic(create_animal, badness, mutation, crossing, **kwargs)
