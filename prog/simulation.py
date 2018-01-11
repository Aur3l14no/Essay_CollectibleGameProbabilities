"""This is a simulation program
"""

import json
import random
import os
import time
import BitVector

os.chdir('prog')

G = BitVector.BitVector

item_total = 0
random_list = []

def load_items(file):
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


def check(collected: BitVector.BitVector, target):
    """ check whether the collected item set S contains G
    """
    result = ~collected & target
    return result.intValue() == 0

def flatten(list_):
    """ flatten a nested list
    """
    try:
        if len(list_) == 0:
            return []
        else:
            ret = []
            for nested_list in list_:
                ret += flatten(nested_list)
            return ret
    except TypeError:
        return [list_]

def generate_possibles(target):
    """ generate possible item collections [s]
    """
    def dfs(target, step):
        """ depth-first search
        """
        if step == len(target):
            return [G(size=item_total)]
        candidate = target[step]
        possibles = []
        for group in candidate:
            for possible in dfs(target, step + 1):
                possibles.append(possible ^ group)
        return possibles
    return dfs(target, 0)


def generate_random(item_json):
    random_list = []
    current = 0
    for item in item_json:
        current += item['probability']
        random_list.append(current)
    if current > 1:
        raise Exception('Probability > 1')
    return random_list

def random_item():
    try:
        rand = random.random()
        return next(i for i, x in enumerate(random_list) if x > rand)
    except StopIteration:
        return None

def trial(item_count, possibles):
    """ get $item_count items, see how it goes
    """
    collected = G(size=item_total)
    for everytime in range(item_count):
        item = random_item()
        if item is not None:
            collected[item] = 1
        # print(collected)
    # print(collected)
    return any([check(collected, possible) for possible in possibles])

def main():
    """ entry function
    """
    global item_total, random_list
    random.seed(time.time())
    item_json, groups = load_items('items.json')
    item_total = len(item_json)
    target1 = [
        [groups['皮甲']],
        [groups['太刀']],
        [groups['首饰']],
        [groups['辅助装备']],
        [groups['魔法石']],
        [groups['耳环']]
    ]
    target2 = [
        [groups['皮甲'], groups['轻甲']],
        [groups['太刀'], groups['巨剑']],
        [groups['首饰']],
        [groups['辅助装备']],
        [groups['魔法石']],
        [groups['耳环']]
    ]
    possibles = generate_possibles(target1)
    print(len(possibles))
    for possible in possibles:
        print(possible)
    trial_times = 10000
    success = 0

    try:
        random_list = generate_random(item_json)
        print(random_list)
    except Exception as e:
        print(e)

    for i in range(trial_times):
        if trial(item_count=491, possibles=possibles):
            success += 1
    print(success / trial_times)

if __name__ == "__main__":
    main()
