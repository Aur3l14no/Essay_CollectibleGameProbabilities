"""This is a simulation program
"""

import json
import random
import os
import time
import pickle
import BitVector
import numpy as np
import matplotlib.pyplot as plt

os.chdir('prog')

G = BitVector.BitVector


class Simulation:
    def __init__(self):
        self.item_json = []
        self.groups = []
        self.possibles = []
        self.random_item = None
    
    def preproess(self, item_file):
        """ initialize seed, load file, initialize generator
        """
        random.seed(time.time())
        self.item_json, self.groups = self.load_items(item_file)
        self.random_item = self.item_generator()
        return self.groups

    def load_target(self, target):
        """ load target, generate possible item collections [s]
        """
        def dfs(target, step):
            """ depth-first search
            """
            if step == len(target):
                return [G(size=len(self.item_json))]
            candidate = target[step]
            possibles = []
            for group in candidate:
                for possible in dfs(target, step + 1):
                    possibles.append(possible ^ group)
            return possibles
        self.possibles = dfs(target, 0)
        print(len(self.possibles))
        for possible in self.possibles:
            print(possible)

    def load_items(self, file):
        """ returns items json and groups
        """
        with open(file, encoding='utf8') as f:
            j = json.load(f)
        total = len(j)
        groups = {}
        for index, item in enumerate(j):
            if item['group'] not in groups:
                groups[item['group']] = G(size=total)
            groups[item['group']][index] = 1
        return j, groups

    def item_generator(self):
        """ generate random item
        """
        random_list = []
        current = 0
        for item in self.item_json:
            current += item['probability']
            random_list.append(current)
        if current > 1:
            raise Exception('Probability > 1')
        while True:
            try:
                rand = random.random()
                yield next(i for i, x in enumerate(random_list) if x > rand)
            except StopIteration:
                yield None
        

    def trials(self, max_item_retrieved, trial_total):
        """ make $trial_total players, let them get items, returns how the percentage of finishing players grows by item count
        """
        def check(collection):
            """ check whether the collected item set S contains G
            """
            def include(collected: BitVector.BitVector, target):    
                result = ~collected & target
                return result.intValue() == 0
            return any([include(collection, possible) for possible in self.possibles])
        result = [0]
        collections = [G(size=len(self.item_json)) for i in range(trial_total)]
        count = 0
        for every_item in range(max_item_retrieved):  # give out an item to every player
            for collection in collections:
                item = next(self.random_item)  # player check what the item is
                if item is not None:
                    collection[item] = 1  # put it in his pack
                # print(collection)
                if check(collection):
                    collections.remove(collection)  # if he's happy, get out of here
                    count += 1
            result.append(count / trial_total)
        return result


def myplot(result):
    plt.plot(range(501), result)
    current_milestone = 0.5
    milestone = []
    for i, v in enumerate(result):
        if result[i] > current_milestone:
            milestone.append((i, result[i]))
            current_milestone += 0.1
    for stone in milestone:
        plt.annotate('({0}, {1:.1})'.format(round(stone[0]), stone[1]), xy=stone, xycoords='data',
            xytext=(-80, +10), textcoords='offset points', fontsize=16)
        plt.scatter([stone[0],],[stone[1],], 50, color ='r')
    plt.yticks(np.arange(0.0, 1.1, 0.1))
    plt.show()

def main():
    """ entry function
    """
    MAX_ITEMS = 500
    TRIALS = 10000
    TARGET = 1
    try:
        with open('result-target%d-%d-%d' % (TARGET, MAX_ITEMS, TRIALS), 'rb') as f:
            result = pickle.load(f)
    except FileNotFoundError:
        simulation = Simulation()
        groups = simulation.preproess('items.json')
        targets = [[
            [groups['皮甲']],
            [groups['太刀']],
            [groups['首饰']],
            [groups['辅助装备']],
            [groups['魔法石']],
            [groups['耳环']]
        ],[
            [groups['皮甲'], groups['轻甲']],
            [groups['太刀'], groups['巨剑']],
            [groups['首饰']],
            [groups['辅助装备']],
            [groups['魔法石']],
            [groups['耳环']]
        ]]
        simulation.load_target(targets[TARGET])
        result = simulation.trials(max_item_retrieved=MAX_ITEMS, trial_total=TRIALS)
        with open('result-target%d-%d-%d' % (TARGET, MAX_ITEMS, TRIALS), 'wb') as f:
            pickle.dump(result, f)
    # print(result)
    myplot(result)

if __name__ == "__main__":
    main()
