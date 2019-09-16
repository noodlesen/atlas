
"""Draw candlesticks charts."""

from PIL import Image, ImageDraw

BLACK = (0, 0, 0, 0)
WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 0)
GREEN = (0, 255, 0, 0)

FILL_UP = WHITE
FILL_DOWN = BLACK
STROKE = BLACK


def get_coord(n, context):
    """Get picture Y-coordinate for the price."""
    cph = context['price_high']
    cpl = context['price_low']
    ch = context['height']
    return (cph - n) / (cph - cpl) * ch


def draw_candle(o, h, l, c, p, context, draw, **kwargs):
    """Draw a single candle."""
    w = context['width'] / context['number']
    left = w * p - w * 0.8
    right = w * p - w * 0.2
    mid = w * p - w * 0.5

    if o < c:
        draw.rectangle(
            [left, get_coord(o, context), right, get_coord(c, context)],
            FILL_UP, STROKE
        )
        draw.rectangle(
            [mid - 1, get_coord(h, context), mid, get_coord(c, context)],
            STROKE, STROKE
        )
        draw.rectangle(
            [mid - 1, get_coord(o, context), mid, get_coord(l, context)],
            STROKE, STROKE
        )
    else:
        draw.rectangle(
            [left, get_coord(c, context), right, get_coord(o, context)],
            FILL_DOWN, STROKE
        )
        draw.rectangle(
            [mid - 1, get_coord(h, context), mid, get_coord(o, context)],
            STROKE, STROKE
        )
        draw.rectangle(
            [mid - 1, get_coord(c, context), mid, get_coord(l, context)],
            STROKE, STROKE
        )

    sl = kwargs.get('sl', None)
    if sl:
        draw.rectangle(
            [
                mid - 2,
                get_coord(sl, context) - 2,
                mid + 2,
                get_coord(sl, context) + 2
            ],
            'red', 'red'
        )

    tp = kwargs.get('tp', None)
    if tp:
        draw.rectangle(
            [
                mid - 2,
                get_coord(tp, context) - 2,
                mid + 2,
                get_coord(tp, context) + 2
            ],
            'blue', 'blue'
        )

    if p in context['marked_positions']:
        for m in context['marks']:
            if m[0] == p:
                draw.ellipse(
                    [
                        mid - 5,
                        get_coord(m[1], context) - 5,
                        mid + 5,
                        get_coord(m[1], context) + 5
                    ],
                    'green', 'green'
                )


def draw_chart(data, name, context, **kwargs):
    """Draw candlesticks chart."""
    context['marked_positions'] = [m[0] for m in context.get('marks', [])]

    img = Image.new(
        'RGB',
        (context['width'], context['height'],),
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(img)

    cn = context['number']
    co = context['offset']
    if context['offset'] == 0:
        data_slice = data[-cn:]
    else:
        data_slice = data[-cn + co: co]

    highest = max([d['high'] for d in data_slice])
    lowest = min([d['low'] for d in data_slice])

    context['price_high'] = highest
    context['price_low'] = lowest

    for i, d in enumerate(data_slice):
        draw_candle(
            d['open'],
            d['high'],
            d['low'],
            d['close'],
            i + 1,
            context,
            draw,
            sl=d.get('stoploss', None),
            tp=d.get('takeprofit', None)
        )

    if context.get('levels', None):
        for level in context['levels']:
            ch = context['height']
            h = ch - ch * (level - lowest) / (highest - lowest)
            draw.line((0, h, context['width'], h), 'green')

    img.save(name + '.jpg', "JPEG")
