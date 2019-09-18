
"""Data requests from finviz.com."""

import json

import requests

from time import sleep

from aapp.models import RawData

from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/39.0.2171.95 Safari/537.36'
    )
}

SCREEN_URL = (
    "https://finviz.com/screener.ashx?v=152&f=cap_smallover,geo_usa,"
    "ipodate_more5&o=-high52w&c=0,1,2,3,4,5,6,7,8,11,14,32,33,40,41,62,65"
)

DETAILS_URL = "https://finviz.com/quote.ashx?t="


def fv_scan_screen():
    """Load stock screener table data."""
    print("SCANNING SCREENER...")
    print(HEADERS)
    print(SCREEN_URL)
    lines = []
    url = SCREEN_URL.strip()
    pages = 2
    for n in range(pages):

        if n > 0:
            add = "&r=" + str(n * 20 + 1)
            url += add
        try:
            soup = BeautifulSoup(
                requests.get(
                    url.strip(), headers=HEADERS
                ).text, 'html.parser'
            )
        except:
            print('SOMETHING WENT WRONG')
            break

        table = soup.find("div", id="screener-content")

        if n == 0:
            cols = table.find_all("td", {'class': ["table-top"]})
            header_line = '\t'.join([c.text for c in cols])

        rows = table.find_all(
            "tr", {'class': ["table-dark-row-cp", "table-light-row-cp"]}
        )
        for r in rows:
            line = '\t'.join([t.text for t in r.find_all('td')])
            lines.append(line)
        if n < pages - 1:
            print('SLEEP')
            sleep(10)

    hls = header_line.split('\t')

    results = []
    for l in lines:
        if l != '':
            idict = {}
            ls = l.strip().split('\t')

            for i, c in enumerate(ls):
                idict[hls[i]] = ls[i]

            print(idict)

            results.append(idict)

    s = RawData()
    s.query = url
    s.data = json.dumps(results)
    s.author = 'fv_scan_screen'
    s.data_type = 'SCREEN'
    s.save()

    return results


def fv_scan_details(ticker):
    """Load an exact's stock details from web."""
    url = DETAILS_URL + ticker
    try:
        soup = BeautifulSoup(
            requests.get(
                url.strip(),
                headers=HEADERS
            ).text,
            'html.parser'
        )

        table = soup.find("table", class_="snapshot-table2")

        header = soup.find("table", class_="fullview-title")

        header_title = header.find_all("b")[0].text

        full_view_links = header.find("td", class_="fullview-links")
        links = [
            l.text for l in full_view_links.find_all("a")
        ]

        cells = table.find_all("td")

    except:
        print('SOMETHING WENT WRONG')
        return None

    res = {}

    for i, n in enumerate(cells):

        if i % 2 == 0:
            name = n.text
            if n.text == 'EPS next Y':
                if '%' in cells[i + 1].text:
                    name = 'EPS next Y growth'

            res[name] = cells[i + 1].text

    res['Company'] = header_title

    if len(links) == 3:
        res['Sector'] = links[0]
        res['Industry'] = links[1]
        res['Country'] = links[2]
    else:
        print("WRONG NUMBER OF LINKS", len(links))
        print(links)
        input()

    print(res)

    s = RawData()
    s.data = json.dumps(res)
    s.query = ticker
    s.data_type = 'DETAILS'
    s.author = 'fv_scan_details'
    s.save()

    return res
