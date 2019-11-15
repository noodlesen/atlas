
"""Run some command."""

import datetime
from django.core.management.base import BaseCommand
from aapp.models import Day, Bar, Stock
from aapp.pgllib import C, Mob, Pgl, DEFAULT_W, DEFAULT_H


class Chart(Mob):

    def __init__(self, pgl):
        self.points = []
        self.pfrom = 0
        self.pto = 0
        self.count = 0
        self.context = pgl

    def load_points(self, pp):
        self.points = pp
        self.pfrom = 0
        l = len(self.points)
        self.pto = l-1
        self.count = l


    def set_count(self, c):
        self.count = c
        self.pto = self.pfrom + c
        l = len(self.points)
        if self.pto >= l:
            self.pto = l-1
            self.pfrom = self.pto - c

    def set_from(self, f):
        self.pfrom = f
        self.count = self.pto - self.pfrom 

    def set_to(self, t):
        self.pto = t
        self.count = self.pto - self.pfrom

    def shift(self, offset):
        npf  = self.pfrom + offset
        if npf > 0:
            self.pfrom = npf
        else:
            self.pfrom = 0
        npt = self.pto+offset
        l = len(self.points)
        if npt < l-1:
            self.pto = npt
        else:
            self.pto = l-1
        self.count = self.pto - self.pfrom

    def grow(self, n=1):
        self.pfrom -= n
        self.pto += n
        if self.pfrom < 0:
            self.pfrom = 0
        l = len(self.points)
        if self.pto >= l:
            self.pto = l-1
        self.count = self.pto - self.pfrom

    def rebuild(self):
        for v in self.context.vobs:
            if v.mob == self:
                try:
                    v.vl.delete()
                    pass
                except AssertionError:
                    pass
                del v

        pts = self.points[self.pfrom:self.pto]
        pmax = max(pts)
        pmin = min(pts)
        sw = self.context.w/self.count  # slot width

        for i, p in enumerate(pts):
            dx = (i+0.5)*sw
            dy = (p-pmin)/(pmax-pmin) * self.context.h*0.9 + self.context.h*0.05
            self.context.draw_point2d(C(dx, dy), 5, mob=self)


        self.context.window.clear()
        self.context.batch.draw()






class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        """test drawing."""

        pgl = Pgl()

        chart = Chart(pgl)


        @pgl.window.event
        def on_draw():
            pass

        @pgl.window.event
        def on_mouse_motion(x, y, dx, dy):
            pass



        @pgl.window.event
        def on_key_press(symbol, modifiers):

            if symbol == pgl.key.LEFT:
                chart.shift(-1)
                chart.rebuild()

            if symbol == pgl.key.RIGHT:
                chart.shift(1)
                chart.rebuild()

            if symbol == pgl.key.UP:
                chart.grow(1)
                chart.rebuild()

            if symbol == pgl.key.DOWN:
                chart.grow(-1)
                chart.rebuild()



        #ADD POINTS

        bars = [b.c for b in Bar.objects.filter(stock=Stock.objects.get(symbol='AAPL')).order_by('d')]

        chart.load_points(bars)
        chart.set_from(50)
        chart.set_count(1000)
        chart.rebuild()

        pgl.run()
