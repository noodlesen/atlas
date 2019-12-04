
"""Candles and figures identifying."""


class Candle():
    """A single candle data and methods."""

    def __init__(self, **kwargs):
        """."""
        bar = kwargs.get('bar', None)
        if bar:
            self.high_price = bar['high']
            self.low_price = bar['low']
            self.open_price = bar['open']
            self.close_price = bar['close']
            self.volume = bar.get('volume', 0)
            self.datetime = bar.get('datetime', None)
        else:
            self.high_price = kwargs['high']
            self.low_price = kwargs['low']
            self.open_price = kwargs['open']
            self.close_price = kwargs['close']
            self.volume = kwargs.get('volume', 0)
            self.datetime = kwargs.get('datetime', None)
            self.stock = kwargs.get('stock', None)

    def __str__(self):
        """."""
        return (
            '%s O:%r H:%r L: %r C: %r V: %d' % (
                self.datetime, self.open_price, self.high_price,
                self.low_price, self.close_price, self.volume
            )
        )

    def get_dict(self):
        """Return the candle's price data as a dict."""
        return {
            'open': self.open_price,
            'high': self.high_price,
            'low': self.low_price,
            'close': self.close_price,
            'volume': self.volume,
        }

    def body_size(self):
        """Return the candle's absolute body size."""
        return abs(self.close_price - self.open_price)

    def body(self):
        """Return the candle's body size with a sign."""
        return self.close_price - self.open_price

    def candle_size(self):
        """Return size of the candle from high to low."""
        return self.high_price - self.low_price

    def body_to_candle(self):
        """Return body size to candle size relation in decimals."""
        try:
            return self.body_size() / self.candle_size()
        except:
            return 0

    def growth(self):
        """Return candle's growth from it's own open price (in %)."""
        return (self.close_price - self.open_price) / self.open_price * 100

    def close_at_percent(self):
        """
        Return at which percent of candle the close price is.

        (in prc from low)
        """
        try:
            return (
                (self.close_price - self.low_price) / self.candle_size() * 100
            )
        except:
            return 0

    def open_at_percent(self):
        """
        Return at which percent of candle the open price is.

        (in prc from low)
        """
        try:
            return(
                (self.open_price - self.low_price) / self.candle_size() * 100
            )
        except:
            return 0

    def body_high(self):
        """Return the highest price of the candle's body."""
        return self.open_price if self.is_bearish() else self.close_price

    def body_low(self):
        """Return the lowest price of the candle's body."""
        return self.open_price if self.is_bullish() else self.close_price

    def high_tail(self):
        """Return size of the candle's high tail."""
        return self.high_price - self.body_high()

    def low_tail(self):
        """Return size of the candle's low tail."""
        return self.body_low() - self.low_price

    def high_tail_to_candle(self):
        """Return size of the high tail in percents from the candle's size."""
        try:
            return self.high_tail() / self.candle_size()
        except:
            return 0

    def low_tail_to_candle(self):
        """Return size of the low tail in percents from the candle's size."""
        try:
            return self.low_tail() / self.candle_size()
        except:
            return 0

    def is_bullish(self):
        """Check if the candle is is bullish."""
        return self.close_price > self.open_price

    def is_bearish(self):
        """Check if the candle is is bearish."""
        return self.close_price < self.open_price

    def is_doji(self):
        """Check if the candle is is a doji."""
        return self.close_price == self.open_price

    def is_hammer(self):
        """Check if the candle is is a hammer."""
        return (
            self.low_tail() > self.body_size() * 2 and
            self.high_tail() < self.low_tail() / 4
        )

    def is_shooting_star(self):
        """Check if the candle is is a shooting star."""
        return(
            self.high_tail() > self.body_size() * 2 and
            self.low_tail() < self.high_tail() / 4
        )


class Figure():
    """A group of candles."""

    def __init__(self, **kwargs):
        """."""
        candles = kwargs.get('candles', None)
        raw = kwargs.get('raw', None)

        self.candles = []

        if candles:
            self.candles = candles
        elif raw:
            for r in raw:
                self.candles.append(Candle(bar=r))

    def summary(self, **kwargs):
        """Return the figure as one resulting candle."""
        last = kwargs.get('last', None)
        candles = self.candles[-last:] if last else self.candles
        o = candles[0].open_price
        c = candles[-1].close_price
        h = max([cn.high_price for cn in candles])
        l = min([cn.low_price for cn in candles])
        return Candle(open=o, high=h, low=l, close=c)

    def is_harami(self):
        """Check if the figure is a harami."""
        if (
            self.candles[-1].body_high() < self.candles[-2].body_high() and
            self.candles[-1].body_low() > self.candles[-2].body_low()
        ):
            return True
        else:
            return False

    def is_harami_breakup(self):
        """Check if the figure is harami followed by price break up."""
        f = Figure(candles=self.candles[:-1])
        if (
            f.is_harami() and
            self.candles[-1].close_price > self.candles[-3].body_high()
        ):
            return True
        else:
            return False

    def is_breakup(self, **kwargs):
        """
        Check if the last candle breaks the maximum of the prev candles.

        Number of candles is defined by 'last' parameter
        If it's absent - it uses all the figure's candles
        """
        last = kwargs.get('last', None)
        candles = self.candles[-last:] if last else self.candles
        return(
            candles[-1].close_price > max(
                [cn.high_price for cn in candles[:-1]]
            )
        )

    def is_breakdown(self, **kwargs):
        """
        Check if the last candle breaks the lowest price of the prev candles.

        Number of candles is defined by 'last' parameter
        If it's absent - it uses all the figure's candles
        """
        last = kwargs.get('last', None)
        candles = self.candles[-last:] if last else self.candles
        return(
            candles[-1].close_price < min(
                [cn.low_price for cn in candles[:-1]]
            )
        )

    def is_top_fractal(self):
        """Check if the figure is a top fractal."""
        candles = self.candles[-5:]
        return candles[-3].high_price == max([c.high_price for c in candles])

    def is_bottom_fractal(self):
        """Check if the figure is a bottom fractal."""
        candles = self.candles[-5:]
        return candles[-3].low_price == min([c.low_price for c in candles])

    def is_power_growth(self):
        """Check if the figure has a power growth."""
        # candles = self.candles[-10:]
        # c1 = candles[-1].is_bullish() and candles[-1].body_to_candle() > 0.9
        # return c1
        return(
            self.candles[-1].is_bullish() and
            self.candles[-1].body_to_candle() > 0.9
        )
