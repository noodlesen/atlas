import pyglet

DEFAULT_W = 1400
DEFAULT_H = 800


def check_color(**kwargs):  # private
    c = kwargs.get('c', None)
    if c is not None:
        color = c
    else:
        color = [255, 255, 255]
    return color


class Mob():

    def __init__(self, name):
        self.name = name

class Vob():  # VISUAL OBJECT
    
    def __init__(self, vl, **kwargs):
        # self.name = name
        # self.gtype = gtype
        self.vl = vl
        self.mob = kwargs.get('mob', None)

    def shift(self, offset):  #REWRITE
        for n in range(0, len(self.vl.vertices)):
            self.vl.vertices[n] = self.vl.vertices[n] + offset[n % 2]


class C():

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def v2(self):
        return (
            (self.x, self.y,)
        ) 

    def v3(self):
            return (
                (self.x, self.y, self.z)
            )


class Pgl():

    def __init__(self, **kwargs):
        self.w = kwargs.get('w', DEFAULT_W)
        self.h = kwargs.get('h', DEFAULT_H)
        self.window = pyglet.window.Window(self.w, self.h)
        #self.window.set_mouse_visible(False)
        self.batch = pyglet.graphics.Batch()
        self.vobs = []
        self.mobs = []
        self.key = pyglet.window.key

    def set_auto_update(fn, rate):
        pyglet.clock.schedule_interval(fn, 1 / rate) 

    def draw_point2d(self, p, sz, **kwargs):
        color = check_color(**kwargs)
        pyglet.gl.glPointSize(sz)

        vl = self.batch.add(
            1, pyglet.gl.GL_POINTS, None,
            ('v2f', (p.x, p.y)),
            ('c3B', color)
        )
        self.vobs.append(
            Vob(vl, **kwargs)
        )


    def draw_line2d(self, p1, p2, **kwargs):
        w = kwargs.get('w', 0)
        if w > 0:
            pyglet.gl.glLineWidth(w)

        color = check_color(**kwargs)

        colors = tuple(color + color)

        vl = self.batch.add(
            2, pyglet.gl.GL_LINES, None,
            ('v2f', (p1.x, p1.y, p2.x, p2.y)),
            ('c3B', colors),
        )
        self.vobs.append(
            Vob(vl, **kwargs)
        )


    def draw_poly2d(self, ul, ur, lr, ll, **kwargs):

        color = check_color(**kwargs)

        colors = tuple(color*4)

        vl = self.batch.add(
            4, pyglet.gl.GL_POLYGON, None,
            ('v2f', (ul.x,ul.y,ur.x,ur.y,lr.x,lr.y,ll.x,ll.y)),
            ('c3B', colors),
        )
        self.vobs.append(
            Vob(vl, **kwargs)
        )

    def draw_rect2d(self, ul, pm1, pm2=None, **kwargs):
        if pm2 is None:  # 2 points method
            lr = pm1
        else:  # width & height method
            lr = C(
                ul.x + pm1,
                ul.y - pm2
            )

        ur = C(lr.x, ul.y)
        ll = C(ul.x, lr.y)
        self.draw_line2d(ul, ur, **kwargs)
        self.draw_line2d(ur, lr, **kwargs)
        self.draw_line2d(lr, ll, **kwargs)
        self.draw_line2d(ll, ul, **kwargs)

    def run(p):
        pyglet.app.run()


class Frame():
    """Frame UI element."""

    def __init__(self, name, **kwargs):
        """."""
        self.name = name

        if kwargs.get('main', False):
            self.ul = C(0, DEFAULT_H)
            self.lr = C(DEFAULT_W, 0)
        else:
            self.ul = C(kwargs.get('ulx', 0), kwargs.get('uly', DEFAULT_H))
            self.lr = C(kwargs.get('lrx', DEFAULT_W), kwargs.get('uly', 0))

        self.pd = 0  # pixels
        self.rebuild()

    def set_padding_percents(self, p):
        self.pd = self.w * p / 100
        self.rebuild()


    def rebuild(self):
        self.ur = C(self.lr.x, self.ul.y)
        self.ll = C(self.ul.x, self.lr.y)
        self.w = self.ur.x - self.ul.x
        self.h = self.ul.y - self.ll.y
        if self.pd > 0:
            self.iul = C(self.ul.x + self.pd, self.ul.y - self.pd)
            self.iur = C(self.ur.x - self.pd, self.ur.y - self.pd)
            self.ilr = C(self.lr.x - self.pd, self.lr.y + self.pd)
            self.ill = C(self.ll.x + self.pd, self.ll.y + self.pd)
        else:
            self.iul = self.ul
            self.iur = self.ur
            self.ilr = self.lr
            self.ill = self.ll

    def split(self, drc, prc):
        """Make two frames from this one."""
        f1 = Frame(self.name + '_s1')
        f2 = Frame(self.name + '_s2')

        if drc == 'v':
            xbreak = self.iul.x + (self.ilr.x - self.iul.x) * prc / 100
            f1.ul = self.iul
            f1.lr = C(xbreak, self.ilr.y)
            f2.ul = C(xbreak, self.iul.y)
            f2.lr = self.ilr
            f1.rebuild()
            f2.rebuild()
        elif drc == 'h':
            ybreak = self.ilr.y + (self.iul.y - self.ilr.y) * (100 - prc) / 100
            f1.ul = self.iul
            f1.lr = C(self.ilr.x, ybreak)
            f2.ul = C(self.iul.x, ybreak)
            f2.lr = self.ilr
            f1.rebuild()
            f2.rebuild()

        return (f1, f2)

    def draw_itself(self):
        if self.pd == 0:
            pgl.draw_rect2d(self.ul, self.lr, w=2, c=[20, 20, 20])
        else:
            pgl.draw_rect2d(self.iul, self.ilr, w=2, c=[20, 20, 20])




