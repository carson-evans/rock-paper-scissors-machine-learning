import itertools
import random

def create_matrix(order):
    def create_keys(order):
        keys = ['R', 'P', 'S']

        for i in range((order * 2 - 1)):
            key_len = len(keys)
            for i in itertools.product(keys, ''.join(keys)):
                keys.append(''.join(i))
            keys = keys[key_len:]
        return keys
    
    keys = create_keys(order)

    matrix = {}
    for key in keys:
        matrix[key] = {
            'R': {
                'prob': 1/3,
                'n_obs': 0
            },
            'P': {
                'prob': 1/3,
                'n_obs': 0
            },
            'S': {
                'prob': 1/3,
                'n_obs': 0
            }
        }
    return matrix

def update_matrix(matrix, pair, input, decay):
    for i in matrix[pair]:
        matrix[pair][i]['n_obs'] = decay * matrix[pair][i]['n_obs']
    
    matrix[pair][input]['n_obs'] = matrix[pair][input]['n_obs'] + 1

    n_total = 0
    for i in matrix[pair]:
        n_total += matrix[pair][i]['n_obs']
    
    for i in matrix[pair]:
        matrix[pair][i]['prob'] = matrix[pair][i]['n_obs'] / n_total

def predict(matrix, pair):
    probs = matrix[pair]

    y = []
    x = []
    for k in probs:
        for v in probs[k]:
            if v == 'prob':
                y.append(probs[k][v])
                x.append(k)

    if max(y) == min(y):
        return random.choice(['R', 'P', 'S'])
    else:
        max_index = y.index(max(y))
        return x[max_index]


beat = {'R': 'P', 'P': 'S', 'S': 'R'}

m = create_matrix(1)
output = ""
pair_diff1 = ""
pair_diff2 = ""

def player(prev_play):
    global pair_diff1, pair_diff2, output, m
    if not prev_play:
        reset()

    input = prev_play

    pair_diff2 = pair_diff1
    pair_diff1 = output + input

    if pair_diff2 != '':
        update_matrix(m, pair_diff2, input, 0.9)
        output = beat[predict(m, pair_diff1)]
    else:
        output = random.choice(['R', 'P', 'S'])
    
    return output

def reset():
    global m, output, pair_diff1, pair_diff2
    m = create_matrix(1)
    pair_diff1 = ""
    pair_diff2 = ""
    output = ""
