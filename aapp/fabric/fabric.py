
"""Base classes for historical price data ops."""

from datetime import datetime

from aapp.fabric.candlesticks import Candle, Figure

from aapp.fabric.drawer import draw_chart

from aapp.models import Bar


class Asset():
    """Historical price data.

    Stores chart information for a single instrument
    """

    def __init__(self, **kwargs):
        """."""
        self.data = kwargs.get('data', [])
        self.symbol = kwargs.get('symbol', None)
        self.timeframe = kwargs.get('timeframe', None)
        self.itype = kwargs.get('itype', None)
        self.loaded = False
        self.count = 0
        self.filled = 0
        self.dt_from = None
        self.dt_to = None
        self.mapped = False
        self.data_from = None
        self.data_to = None

    def __str__(self):
        """."""
        f = datetime.strftime(self.dt_from, '%Y-%m-%d %H:%M:%S')
        t = datetime.strftime(self.dt_to, '%Y-%m-%d %H:%M:%S')
        return ('Asset: %s %s (%s) %s->%s'
                % (self.symbol, self.timeframe, self.itype, f, t)
                )

    def load_asset(self, symbol, itype, timeframe):
        """Load historical data from DB/server."""
        print('loading', symbol)

        self.data = [
            b.as_dict for b in Bar.objects.filter(symbol=symbol).order_by('d')
        ]

        if self.data is None:
            return False
        else:
            self.count = len(self.data)
            self.dt_from = self.data[0]['datetime']
            self.dt_to = self.data[self.count - 1]['datetime']
            self.data_from = self.dt_from
            self.data_to = self.dt_to
            self.symbol = symbol
            self.timeframe = timeframe
            self.itype = itype
            self.loaded = True
            return True

    def trim(self, from_dt, to_dt):
        """Trim all data sequences accordig to from/to."""
        self.data = [
            d for d in self.data
            if d["datetime"] >= from_dt and d["datetime"] <= to_dt
        ]
        self.count = len(self.data)
        self.dt_from = self.data[0]['datetime']
        self.dt_to = self.data[self.count - 1]['datetime']

    def cut_last(self, n):
        """Trim all data older than n-candles."""
        self.data = self.data[-1 * n:]
        self.count = len(self.data)

    def map_timecode(self, tc):
        """Synchronize the asset's data with external timecode."""
        success = False

        tcmap = [
            {
                "datetime": t,
                "open": None,
                "close": None,
                "high": None,
                "low": None
            } for t in tc
        ]
        print('tcmap length', len(tcmap))

        old_data_length = len(self.data)

        filled = 0
        data_from = None
        data_to = None
        p = 0
        for tc in tcmap:
            # print('P', p, self.count)
            if p < self.count:
                if tc['datetime'] == self.data[p]["datetime"]:
                    tc["open"] = self.data[p]["open"]
                    tc["close"] = self.data[p]["close"]
                    tc["high"] = self.data[p]["high"]
                    tc["low"] = self.data[p]["low"]
                    tc["volume"] = self.data[p]["volume"]
                    filled += 1

                    if data_from is None:
                        data_from = tc['datetime']

                    data_to = tc['datetime']

                    p += 1

                elif tc['datetime'] > self.data[p]["datetime"]:
                    p += 1

        print(self.symbol, old_data_length, filled)
        if old_data_length == filled:
            self.filled = filled
            self.count = len(tcmap)
            self.data = tcmap
            self.dt_from = tcmap[0]["datetime"]
            self.dt_to = tcmap[-1]["datetime"]
            self.data_from = data_from
            self.data_to = data_to
            self.mapped = True
            success = True

        return success


class Fabric():
    """Synchronized chart data from multiple instruments."""

    def __init__(self):
        """."""
        # self.data = []
        self.pointer = 0
        self.range_from = 0
        self.count = 0
        self.range_to = None  # self.count - 1
        self.canvas = {}
        self.helpers = []
        self.timeframe = None
        self.checked = False
        self.loaded = False
        self.range = 0  # self.range_to - self.range_from
        self.timecode = None

    def reset(self):
        """Set pointer to the start of the range."""
        self.pointer = self.range_from

    def set_to_last(self):
        """Set pointer to the end of the range."""
        self.pointer = self.range_to

    def reset_range(self):
        """Set range to all available data."""
        self.range_from = 0
        self.range_to = self.count - 1
        self.range = self.range_to - self.range_from + 1
        self.pointer = 0

    def set(self, n):
        """Set pointer to the specified position."""
        self.pointer = n

    def forth(self, n=1):
        """Shift the pointer forward by n positions."""
        self.pointer += n

    def back(self, n=1):
        """Shift the pointer back by n positions."""
        self.pointer -= n

    def next(self):
        """Shift the pointer forward by 1 position."""
        self.pointer += 1

    def prev(self):
        """Shift the pointer back by 1 position."""
        self.pointer -= 1

    def as_list(self):
        """Return Fabric as a list of assets."""
        return list(self.canvas.values())

    def tickers(self):
        """Return a list of tickers present in the Fabric."""
        return list(self.canvas.keys())

    def assets_number(self):
        """Return assets number."""
        return len(self.as_list())

    def load_data(self, symbols, itype, timeframe):
        """Load data specified by ticker and timeframe into assets."""
        assets = {}
        for s in symbols:
            a = Asset()
            load_success = a.load_asset(s, itype, timeframe)
            if not load_success:
                print('SOMETHING WENT WRONG')
            else:
                assets[s] = a

        self.timeframe = timeframe
        self.loaded = True
        self.canvas.update(assets)
        self.reset_range()

    def trim(self):
        """Trim all the data to the common time range for all assets."""
        # LEGACY???
        max_dt_from = max([a.dt_from for a in self.as_list()])
        min_dt_to = min([a.dt_to for a in self.as_list()])
        print(max_dt_from, min_dt_to)
        for a in self.as_list():
            a.trim(max_dt_from, min_dt_to)
        self.count = self.as_list()[0].count
        self.reset_range()

    def check(self):
        """Check canvas integrity."""
        # LEGACY???
        ok = True
        lengths = set([a.count for a in self.as_list()])
        various_lengths = len(lengths)
        if various_lengths != 1:
            # Different length of assets!
            print('Check-up failed! Different length of assets!')
            ok = False

            shorties = []
            max_length = max(lengths)
            for a in self.as_list():
                if a.count < max_length:
                    shorties.append((a.symbol, a.count))
            print('Normal length -', max_length)
            for s in shorties:
                print(s)

        else:
            # Check if bars with same index have same datetimes
            for i in range(
                max([len(a.data) for a in self.as_list()])
            ):
                if len(
                    set([a.data[i]["datetime"] for a in self.as_list()])
                ) != 1:
                    ok = False
                    print('Check-up failed! Async datetimes')
        return ok

    def cut_last(self, n):
        """
        Trim all the data older than n-candles for all assets.

        (this will lose all the trimmed data)
        """
        for k, v in self.canvas.items():
            v.cut_last(n)
        self.count = self.as_list()[0].count
        self.reset_range()

    def set_range_from_last(self, n):
        """
        Set range(by pointer) to the last n-candles.

        (this is data-safe trimming)
        """
        self.range_from = self.count - n
        self.range_to = self.count - 1
        self.pointer = self.range_from
        self.range = self.range_to - self.range_from

    def last(self, symbol, n, of=0, **kwargs):
        """
        Return raw data by ticker.

        n - number of candles
        of (default=0) - offset

        kwargs:
        figure - return as Figure object, else - raw
        """
        row = []

        fr = -1 * (n - 1) + of + self.pointer
        to = 1 + of + self.pointer
        row = self.canvas[symbol].data[fr:to]
        if kwargs.get('figure', False):
            return Figure(raw=row)
        else:
            return row

    def bar(self, symbol, n=-1):
        """Get bar by absoute index."""
        p = n if n >= 0 else self.pointer
        return Candle(bar=self.canvas[symbol].data[p])

    def get(self, symbol, n=0):
        """Get bar by pointer relative index."""
        return Candle(bar=self.canvas[symbol].data[self.pointer + n])

    def draw(self, symbol, dt_from, dt_to):
        """Draw a chart using drawer module."""
        data = [b for b in self.canvas[symbol].data
                if b['datetime'] >= dt_from and b['datetime'] <= dt_to]
        context = {
            'number': len(data),
            'width': 1400,
            'height': 800,
            'offset': 0
        }
        draw_chart(data, 'images/' + symbol + 'candles', context)

    def profile(self, ticker=None):
        """Making instrument's profile analyzing it's data."""
        # add pos%to high, to low, SPY outperform^
        # growth linearity - sum of differences from start-end line

        tickers = []

        res = {}

        if ticker is not None and ticker in self.tickers():
            tickers = [ticker]
        elif ticker is not None and ticker not in self.tickers():
            print('TICKER IS NOT LOADED')
            return None
        elif ticker is None:
            tickers = self.tickers()

        p = self.pointer

        for t in tickers:

            self.pointer = p

            gaps = 0
            body_prc = []
            body2hl_prc = []
            gap_prc = []
            c2c_prc = []
            bull = 0
            bear = 0
            doji = 0
            tf = 0
            bf = 0

            first = self.get(t, 0)
            last = self.get(t, self.range)
            fl_c2c_delta = last.close_price - first.close_price
            growth = fl_c2c_delta / first.close_price * 100

            for i in range(self.range - 1):
                this = self.get(t, i + 1)
                prev = self.get(t, i)
                if this.open_price != prev.close_price:
                    gaps += 1
                    c2o_delta = this.open_price - prev.close_price
                    gap_prc.append(c2o_delta / prev.close_price * 100)
                body_prc.append(this.body_size() / this.open_price * 100)
                cs = this.candle_size()
                if cs != 0:
                    body2hl_prc.append(this.body_size() / cs)
                else:
                    body2hl_prc.append(0)
                c2c_delta = this.close_price - prev.close_price
                c2c_prc.append(abs(c2c_delta / prev.close_price))

                if this.is_bullish():
                    bull += 1
                elif this.is_bearish():
                    bear += 1
                elif this.is_doji():
                    doji += 1

                if i > 5:
                    if self.last(t, 5, i, figure=True).is_top_fractal():
                        tf += 1
                    if self.last(t, 5, i, figure=True).is_bottom_fractal():
                        bf += 1

            res[t] = {
                'growth': growth,
                'bear': bear / self.range * 100,
                'bull': bull / self.range * 100,
                'doji': doji / self.range * 100,
                'top_fractals': tf / self.range * 100,
                'bottom_fractals': bf / self.range * 100,
                'gaps': gaps / self.range * 100,
                'avg_body_prc': sum(body_prc) / len(body_prc),
                'avg_gap_prc': sum(gap_prc) / len(gap_prc),
                'avg_c2c_prc': sum(c2c_prc) / len(c2c_prc),
                'avg_body2hl_prc': sum(body2hl_prc) / len(body2hl_prc)
            }

        return res

    def extract_timecode(self):
        """Extract timecode from loaded assets."""
        dts = []
        for a in self.as_list():
            for d in a.data:
                if not d['datetime'] in dts:
                    dts.append(d['datetime'])
        tc = sorted(dts)
        return(tc)

    def map_timecode(self):
        """Map common timecode to all assets."""
        success = True
        canvas_backup = self.canvas
        tc = self.extract_timecode()

        for a in self.as_list():
            res = a.map_timecode(tc)

            if not res:
                success = False
                print("Error mapping", a.symbol)

        if success:
            print('Mapping successful')
            self.timecode = tc
            self.count = len(tc)
            canvas_backup = None
        else:
            self.canvas = canvas_backup

        return success

    def compare(self, sym1, sym2, **kwargs):
        """WIP Compare correlation between two instruments."""
        ts = self.tickers()

        if sym1 in ts and sym2 in ts:

            res = {}

            srf = self.range_from
            srt = self.range_to
            sp = self.pointer

            sm = 0
            b2b = 0
            f1tops = []
            f2tops = []
            f1bots = []
            f2bots = []
            top_match = 0
            bot_match = 0

            for i in range(self.range):
                s1 = self.get(sym1)
                s2 = self.get(sym2)

                d = s1.growth() - s2.growth()
                sm += d
                if (
                    (s1.is_bullish() and s2.is_bullish()) or
                    (s1.is_bearish() and s2.is_bearish())
                ):
                    b2b += 1

                f1 = self.last(sym1, 5, figure=True)
                f2 = self.last(sym2, 5, figure=True)

                if f1.is_top_fractal():
                    f1tops.append(i)
                if f2.is_top_fractal():
                    f2tops.append(i)
                if f1.is_bottom_fractal():
                    f1bots.append(i)
                if f2.is_bottom_fractal():
                    f2bots.append(i)

                self.next()

            res['AVG'] = sm / self.range
            res['BODY'] = int(b2b / self.range * 100)

            for tr in f1tops:
                if tr in f2tops:
                    top_match += 1

            for tr in f1bots:
                if tr in f2bots:
                    bot_match += 1
            fsum = len(f1tops) + len(f2tops) + len(f1bots) + len(f2bots)
            diff = (fsum - top_match - bot_match)
            koef = (top_match + bot_match) / diff * 100
            res['FRAC'] = koef

            self.set_range_from_last(250)
            gres = []
            grid_min = 3
            grid_max = int(self.range / 3)
            for g in range(grid_min, grid_max):
                match = 0
                samples = int(self.range / g)
                for i in range(samples):
                    s1cp = self.get(sym1, g * i).close_price
                    s1ofcp = self.get(sym1, g * (i - 1)).close_price
                    s2cp = self.get(sym2, g * i).close_price
                    s2ofcp = self.get(sym2, g * (i - 1)).close_price

                    if (
                        (s1cp > s1ofcp and s2cp > s2ofcp) or
                        (s1cp < s1ofcp and s2cp < s2ofcp)
                    ):
                        match += 1

                cres = int(match / samples * 100)
                gres.append(cres)

            res['GRID'] = sum(gres) / len(gres)

            self.range_from = srf
            self.range_to = srt
            self.pointer = sp

            res['profiles'] = {}
            res['profiles'].update(self.profile(sym1))
            res['profiles'].update(self.profile(sym2))

            return res

        else:
            print('TICKERS ARE NOT LOADED')
            return None
