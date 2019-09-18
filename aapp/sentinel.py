
"""
Checks if all the data is up to date.

And if not - downloads it from online sources.
"""

import json

from datetime import datetime

from time import sleep

from aapp.models import Inst

from aapp.webfront import wf_get_history, wf_get_details

REGULAR = ['SPY']

HIST_REFRESH_TIME = 3600 * 24 * 30  # seconds
DTLS_REFRESH_TIME = 3600 * 24 * 30  # seconds


def check(symbols):
    """Check if instrument's data exists in the system."""
    sleep_time = 10
    success = True
    symbols.extend(REGULAR)
    for s in symbols:
        exists = False
        print('checking', s)
        try:
            inst = Inst.objects.get(ticker=s)
        except Inst.DoesNotExist:
            inst = Inst(ticker=s)
        else:
            exists = True

        now = datetime.now()
        if exists:
            hu = inst.hist_last_update
            du = inst.details_last_update
        elif not exists:
            hu = datetime(1979, 6, 3, 0, 0, 0)
            du = datetime(1979, 6, 3, 0, 0, 0)

        if (
            not hu or
            (now - hu).seconds > HIST_REFRESH_TIME or
            not exists
        ):
            print(s, 'updating history')
            history = wf_get_history(s, 'ASTOCKS', 'DAILY')
            if history is not None:
                inst.history = history
                inst.hist_last_update = now
                inst.save()
            else:
                print('SOMETHING WENT WRONG')
                success = False
                return None

            # REWRITE VVV
            for n in range(sleep_time):
                sleep(1)
                print('.')

        if (
            not du or
            (now - du).seconds > DTLS_REFRESH_TIME or
            not exists
        ):
            print(s, 'updating details')
            details = wf_get_details(s)

            if details is not None:
                inst.details = json.dumps(details)
                inst.details_last_update = now
                inst.parse()
                inst.save()
            else:
                print('SOMETHING WENT WRONG')
                success = False
                return None

        inst.save()

    return success
