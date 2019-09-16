
"""
EVOLUTION ALGORITHM FOR TESTING.

Runs through management command run_evo
"""

from random import randint
from copy import deepcopy
import json
from aapp.fabric.multitester import multitest
from aapp.fabric.config import TS
from datetime import datetime, timedelta
from aapp.fabric.orm_reader import save_report


def mutate(p, nm):
    """Make a new variation of parameters."""
    new_params = TS.get_random_ts_params()
    numbers = []
    l = len(p.items())

    n = randint(1, round(nm / 100 * l))
    while len(numbers) < n:
        nn = randint(1, l)
        if nn not in numbers:
            numbers.append(nn)
    np = deepcopy(p)
    x = 1
    for k, v in new_params.items():
        if x in numbers:
            np[k] = new_params[k]
        x += 1
    return np


def generate(
    f,
    generations_count,
    mutations,
    outsiders,
    depth,
    strategy,
    **kwargs
):
    """Evo main function."""
    time_limit = kwargs.get('time_limit', None)

    now = datetime.now()
    stamp = TS.ts_name() + "-%d-%d-%d-%d" % (
        now.day, now.month, now.hour, now.minute
    )

    default_ir = {
        "DAYS_MAX": 0,
        "LOSES": 0,
        "MAX_LOSES_IN_A_ROW": 0,
        "MAX_LOSS_PER_TRADE": 0,
        "MAX_PROFIT_PER_TRADE": 0,
        "MAX_WINS_IN_A_ROW": 0,
        "PROFIT": 0,
        "ROI": 0,
        "TRADES": 1,
        "WINRATE": 0,
        "WINS": 0,
        "WINS_TO_LOSES": 0,
        "MAX_DRAWDOWN": 0
    }

    initial = kwargs.get('initial_params', None)

    initial_result = multitest(f, initial, **kwargs)

    if initial_result is None:
        initial_result = default_ir
    survivor = {'input': initial, 'output': initial_result}
    print(json.dumps(survivor['input'], sort_keys=True, indent=4))

    elapsed_times = []

    for n in range(1, generations_count + 1):
        print()
        print('GEN', n)
        st_time = datetime.now()
        offs = []
        for d in range(0, depth):
            m = mutate(survivor['input'], mutations)
            ta = multitest(f, m, **kwargs)
            if ta:
                offs.append({'input': m, 'output': ta})

        for x in range(0, outsiders):
            m = TS.get_random_ts_params()
            ta = multitest(f, m, **kwargs)
            if ta:
                offs.append({'input': m, 'output': ta})

        for off in offs:

            o_trades = off['output']['TRADES']
            o_wins = off['output']['WINS']
            o_maxdd = off['output']['MAX_DRAWDOWN']
            o_roi = off['output']['ROI']
            o_pr = off['output']['PROFIT']
            o_t_inv = off['output']['TOTAL_INV']

            s_trades = survivor['output']['TRADES']
            s_wins = survivor['output']['WINS']
            s_maxdd = survivor['output']['MAX_DRAWDOWN']
            s_roi = survivor['output']['ROI']
            s_pr = survivor['output']['PROFIT']

            if o_trades > 0:
                o_wr = o_wins / o_trades
                s_wr = s_wins / s_trades

                if strategy == 'ROI_AND_WINRATE_AND_MINDD':
                    cond = (
                        (
                            o_roi * o_wr / (o_maxdd + 0.0001) >
                            s_roi * s_wr / (s_maxdd + 0.0001)
                        ) and
                        off['output']['VERS'] > 0.4
                    )

                if strategy == 'ROI_AND_WINRATE':
                    cond = (
                        o_roi * o_wr > s_roi * s_wr and
                        off['output']['VERS'] > 0.4
                    )

                if strategy == 'PROFIT_INVEST_LIMIT':
                    cond = (
                        o_pr > survivor['output']['PROFIT'] and
                        o_t_inv <= 50000
                    )

                if strategy == 'FX':
                    off_dd = off['output']['MAX_DRAWDOWN']
                    sur_dd = survivor['output']['MAX_DRAWDOWN']
                    cond = (
                        o_roi * o_wr / (off_dd + 0.0001) >
                        s_roi * s_wr / (sur_dd + 0.0001) and
                        off['output']['VERS'] == 1
                    )

                if cond:
                    survivor = deepcopy(off)

        print(json.dumps(survivor['input'], sort_keys=True, indent=4))
        print(json.dumps(survivor['output'], sort_keys=True, indent=4))
        print('\n>>>>')
        print('\nWINRATE', '%.2f' % s_wr)
        print('PROFIT', '%.2f' % s_pr)
        print('ROI', '%.2f' % s_roi)

        now = datetime.now()
        elapsed = (now - st_time).total_seconds()
        elapsed_times.append(elapsed)
        average = sum(elapsed_times) / len(elapsed_times)
        print('elapsed:', int(elapsed), 'average:', int(average))
        gens_to_go = generations_count - n
        if time_limit:
            if (
                ((now - st_time) + timedelta(seconds=average)).seconds // 60 >
                time_limit
            ):
                print('STOP TIME ' + datetime.strftime(now, '%H:%M'))
                break
            else:
                togo = (st_time + timedelta(minutes=time_limit) - now)
                est_gens = togo.seconds // average
                est_gens = gens_to_go if est_gens > gens_to_go else est_gens
                print('est. gens: ', est_gens)
        else:
            est_time = now + timedelta(seconds=average * gens_to_go)
            print('est. finish: ', datetime.strftime(est_time, '%H:%M'))
        print()

    if kwargs.get('report', False):

        save_report(stamp)

        kwargs['draw'] = False
        kwargs['verbose'] = True
        multitest(f, survivor['input'], **kwargs)

        print(json.dumps(survivor['output'], sort_keys=True, indent=4))

    return(survivor)
