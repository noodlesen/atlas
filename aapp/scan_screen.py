"""Load stock screener table data."""

# import requests
# from bs4 import BeautifulSoup
# from time import sleep
# from aapp.models import RawScan
# import json

# VENDOR = 'FV_CUSTOM'


# def scan():
#     """Load stock screener table data."""
#     url = (
#         "https://finviz.com/screener.ashx?v=152&f=cap_smallover,geo_usa,"
#         "ipodate_more5&o=-high52w&c=0,1,2,3,4,5,6,7,8,11,14,32,33,40,41,62,65"
#     )
#     headers = {
#         'User-Agent': (
#             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
#             'AppleWebKit/537.36 (KHTML, like Gecko)'
#             'Chrome/39.0.2171.95 Safari/537.36'
#         )
#     }
#     if VENDOR == 'FV_CUSTOM':
#         print("SCANNING SCREENER...")
#         print(headers)
#         print(url)
#         lines = []
#         url = url.strip()
#         pages = 2
#         for n in range(pages):

#             if n > 0:
#                 add = "&r=" + str(n * 20 + 1)
#                 url += add
#             try:
#                 soup = BeautifulSoup(
#                     requests.get(
#                         url.strip(), headers=headers
#                     ).text, 'html.parser'
#                 )
#             except:
#                 print('SOMETHING WENT WRONG')
#                 break

#             table = soup.find("div", id="screener-content")

#             if n == 0:
#                 cols = table.find_all("td", {'class': ["table-top"]})
#                 header_line = '\t'.join([c.text for c in cols])

#             rows = table.find_all(
#                 "tr", {'class': ["table-dark-row-cp", "table-light-row-cp"]}
#             )
#             for r in rows:
#                 line = '\t'.join([t.text for t in r.find_all('td')])
#                 lines.append(line)
#             if n < pages - 1:
#                 print('SLEEP')
#                 sleep(10)

#         hls = header_line.split('\t')

#         results = []
#         for l in lines:
#             if l != '':
#                 idict = {}
#                 ls = l.strip().split('\t')

#                 for i, c in enumerate(ls):
#                     idict[hls[i]] = ls[i]

#                 print(idict)

#                 results.append(idict)

#         s = RawScan()
#         s.query = url
#         s.data = json.dumps(results)
#         s.author = 'scan_test'
#         s.scan_type = 'SCREEN'
#         s.save()

#         return results
