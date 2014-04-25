category_weight = \
{'109': 6356, '115': 46, '114': 308, '108': 5054, '116': 153, '110': 129, '113': 216, '112': 13, '102': 115, '103': 12092, '101': 9, '106': 13914, '107': 5644, '104': 3063}
hour_strategy = \
{'20': 7693, '21': 9483, '22': 8194, '23': 5756, '1': 5180, '0': 7681, '3': 4342, '2': 7273, '5': 9672, '4': 7456, '7': 12732, '6': 9289, '9': 21306, '8': 20990, '11': 23065, '10': 20942, '13': 11952, '12': 15607, '15': 19272, '14': 16650, '17': 14440, '16': 18838, '19': 11237, '18': 16105}

max_weight = max(category_weight.values()) + .0
for key in category_weight.keys():
    category_weight[key] = category_weight[key] / max_weight

max_weight = max(hour_strategy.values()) + .0
for key in hour_strategy.keys():
    hour_strategy[key] = (1 / (hour_strategy[key] / max_weight) - 1) / 3 + 1
# print category_weight
# print hour_strategy