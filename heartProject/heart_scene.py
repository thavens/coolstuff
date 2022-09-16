from optparse import Values
import random
import numpy as np
import manim as mn
from tqdm import tqdm

class PointPath(mn.VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def generate_points(self):
        t = np.linspace(-2, 2, 256)

        ftop = np.sqrt(1 - (np.abs(t) - 1) ** 2)
        fbot = np.arccos(1 - np.abs(t)) - np.pi

        x = np.concatenate([t[::-1], t])
        y = np.concatenate([ftop, fbot])

        points = np.stack([x, y, np.zeros_like(y)], axis=-1)
        self.start_new_path(points[0])
        self.add_points_as_corners(points[1:])
        self.add_line_to(points[0])

        #self.center()

        return self

class Epicycle(mn.VMobject):
    def __init__(self, cycles=256, **kwargs):
        self.cycles = cycles
        super().__init__(**kwargs)
    
    def generate_points(self):
        x = np.linspace(-2, 2, 256)

        ftop = np.sqrt(1 - (np.abs(x) - 1) ** 2)
        fbot = np.arccos(1 - np.abs(x)) - np.pi

        newx = np.concatenate([x[::-1], x])
        newy = np.concatenate([ftop, fbot])

        coords = newx + 1j * newy

        Z = np.fft.fft(coords, coords.size) / coords.size
        k_sorted = np.argsort(-np.abs(Z)) # sort by descending amplitude
        Z = Z[k_sorted]
        Z = Z[:self.cycles]
        k_sorted = k_sorted[:self.cycles]

        t = np.linspace(0, 2*np.pi, coords.size+1)
        self.circle_centers = np.cumsum(Z.reshape(-1,1) * np.exp(1j * np.outer(k_sorted, t)), axis=0)
        values = self.circle_centers[-1]

        points = np.stack([values.real, values.imag, np.zeros_like(values.real)], axis=-1)
        self.start_new_path(points[0])
        self.add_points_as_corners(points[1:])
        self.add_line_to(points[0])

        return self
    
    def draw_circles(self, alpha, starting_submobject):
        if alpha < 1e-8:
            return self
        self.submobjects.clear()

        index = int(self.circle_centers.shape[1] * alpha)
        index = self.circle_centers.shape[1] - 1 if index >= self.circle_centers.shape[1] else index
        centers = self.circle_centers[:, index]

        center = 0 + 0j
        for i in centers:
            circ = mn.Circle(np.abs(i - center), mn.BLUE, stroke_width=2).move_to([center.real, center.imag, 0]).set_fill()
            line = mn.Line(np.array([center.real, center.imag, 0]), np.array([i.real, i.imag, 0]), color=mn.RED, stroke_width=3)
            self.add(circ)
            self.add(line)
            center = i
        
        return self
    
    def animate_circles(self, **kwargs):
        class Draw(mn.Animation):
            def interpolate_submobject(self, submobject, starting_submobject, alpha):
                submobject.draw_circles(alpha, starting_submobject, **kwargs)

        return Draw(self)

class HeartCycle(mn.Scene):
    def construct(self):
        #path = PointPath()
        #path.set_color(mn.RED).set_opacity(1)
        #self.add(path)

        for i in range(9):
            if i == 0:
                anno = mn.Text(f"1 cycle")
            else:
                anno = mn.Text(f"{int(2**i)} cycles")
            anno.shift(3*mn.UP)
            epicycle = Epicycle(2**i)
            epicycle.set_stroke(mn.WHITE)
            self.play(mn.FadeIn(anno))
            self.play(mn.Create(epicycle), epicycle.animate_circles(), run_time=10, name=f'cycle: {int(2**i)}', rate_func=mn.linear)
            self.wait(1)
            self.play(mn.FadeOut(mn.VGroup(epicycle, anno)))
