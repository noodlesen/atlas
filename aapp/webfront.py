
"""All external data requests."""

from aapp.wf_finviz import fv_scan_screen, fv_scan_details

from aapp.wf_alpha_vantage import av_get_history

HISTORY_SOURCE = 'ALPHA VANTAGE'
SCREEN_SOURCE = 'FINVIZ'
DETAILS_SOURCE = 'FINVIZ'


def wf_get_history(symbol, itype, timeframe, **kwargs):
    """Get history from the prefered source."""
    if HISTORY_SOURCE == 'ALPHA VANTAGE':
        return av_get_history(symbol, itype, timeframe, **kwargs)
    else:
        print('NO HISTORY SOURCE')
        return(None)


def wf_get_screen():
    """Get screener data from the prefered source."""
    if SCREEN_SOURCE == 'FINVIZ':
        return fv_scan_screen()
    else:
        print('NO SCREEN SOURCE')
        return(None)


def wf_get_details(symbol):
    """Get the inst's details from the prefered source."""
    if DETAILS_SOURCE == 'FINVIZ':
        return fv_scan_details(symbol)
    else:
        print('NO DETAILS SOURCE')
        return(None)
