# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.


def player(prev_play, state={}):
    """Adaptive player for freeCodeCamp's Rock Paper Scissors challenge."""
    beat = {'R': 'P', 'P': 'S', 'S': 'R'}

    # An empty previous play marks the beginning of every new match.
    if prev_play == '' or not state:
        state.clear()
        state.update({
            'mine': [],
            'opp': [],
            'scores': {'quincy': 0, 'kris': 0, 'mrugesh': 0, 'abbey': 0},
            'last_predictions': {},
        })
    else:
        state['opp'].append(prev_play)
        # Score the predictions made for the move we have just observed.
        for name, prediction in state['last_predictions'].items():
            if prediction == prev_play:
                state['scores'][name] += 1

    mine = state['mine']
    round_no = len(mine)

    # Quincy: fixed five-move cycle. Its first returned move is P.
    quincy_cycle = ['R', 'P', 'P', 'S', 'R']
    pred_quincy = quincy_cycle[round_no % 5]

    # Kris: always counters our previous move (and treats the initial move as R).
    pred_kris = beat[mine[-1]] if mine else 'P'

    # Mrugesh: counters the most frequent move in our last ten inputs.
    # His history begins with an empty string, which he treats as S only when
    # choosing the first move.
    if not mine:
        pred_mrugesh = 'R'
    else:
        recent = mine[-10:]
        # max(set(...), key=count) has arbitrary tie behavior, so after enough
        # evidence the model-selection scores below decide whether to trust it.
        most = max(set(recent), key=recent.count)
        pred_mrugesh = beat[most]

    # Abbey: learns transitions in our plays, predicts what follows our latest
    # move, then counters that prediction. Rebuild her tiny transition table
    # from our history so the simulation stays exact and self-contained.
    abbey_inputs = ['R'] + mine
    order = {a + b: 0 for a in 'RPS' for b in 'RPS'}
    for a, b in zip(abbey_inputs, abbey_inputs[1:]):
        order[a + b] += 1
    current = abbey_inputs[-1]
    candidates = [current + x for x in 'RPS']
    predicted_us = max(candidates, key=lambda k: order[k])[-1]
    pred_abbey = beat[predicted_us]

    predictions = {
        'quincy': pred_quincy,
        'kris': pred_kris,
        'mrugesh': pred_mrugesh,
        'abbey': pred_abbey,
    }

    # Use the model that has explained the opponent best so far.  Early on,
    # Quincy is a safe default; within a handful of rounds the correct model
    # separates sharply from the others.
    if round_no < 4:
        chosen = 'quincy'
    else:
        chosen = max(state['scores'], key=state['scores'].get)

    guess = predictions[chosen]
    move = beat[guess]

    state['last_predictions'] = predictions
    mine.append(move)
    return move