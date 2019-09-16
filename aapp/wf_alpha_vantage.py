
"""Data requests from Alpha Vantage API."""

import json

import requests

from aapp.fabric.keys import AV_API_KEY

from aapp.models import RawData


def av_get_history(symbol, itype, timeframe, **kwargs):
    """Request historical price data from web."""
    if itype == 'ASTOCKS':
        if timeframe == 'DAILY':
            adj = kwargs.get('adjusted', False)
            if adj:
                url_temp = (
                    'https://www.alphavantage.co/query'
                    '?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s'
                    '&outputsize=full&apikey='
                )
            else:
                url_temp = (
                    'https://www.alphavantage.co/query?'
                    'function=TIME_SERIES_DAILY&symbol=%s'
                    '&outputsize=full&apikey='
                )
    elif itype == 'FX':
        if timeframe == 'DAILY':
            url_temp = (
                'https://www.alphavantage.co/query'
                '?function=FX_DAILY&from_symbol=%s'
                '&to_symbol=%s&outputsize=full&apikey='
            )
        if timeframe == '60MIN':
            url_temp = (
                'https://www.alphavantage.co/query?function=FX_INTRADAY'
                '&from_symbol=%s&to_symbol=%s'
                '&interval=60min&outputsize=full&apikey='
            )

    print('requesting ' + symbol)
    if itype == 'ASTOCKS':
        url = url_temp % symbol
    elif itype == 'FX':
        url = url_temp % (symbol[:3], symbol[-3:])

    response = requests.request('GET', url + AV_API_KEY)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        print('OK')
        res = response.text

        s = RawData()
        s.data = json.dumps(res)
        s.query = symbol
        s.data_type = 'HISTORY'
        s.author = 'av_get_history'
        s.save()

        return (res)
    else:
        return None
