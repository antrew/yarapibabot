#!/usr/bin/env python

import httplib
import json
import kivy
from kivy.app import App
from kivy.graphics.context import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Line
from kivy.uix.widget import Widget
from kivy.garden.graph import *


kivy.require('1.0.6')  # replace with your current kivy version !

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
        self.old_x = 0
        self.old_value = 0
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.5, 0.5, 0.5)
            Ellipse(pos=self.pos, size=self.size)
            
    def draw_something(self, *args):
        with self.canvas:
            Color(1, 0.5, 0.5)
            Ellipse(pos=self.pos, size=(10, 10))

    def line(self):
        with self.canvas:
            Color(0, 1, 0.5)
            Line(points=[100, 100, 200, 100, 100, 200], width=10)

    def plot_value(self, value):
        with self.canvas:
            Color(0, 0, 1)
#             Line(points=[100, 200, 200, 100, 300, 200], width=10)
            Line(points=[self.old_x, self.old_value, self.old_x + 1, value], width=1)
        self.old_x += 1
        self.old_value = value

class MyApp(App):
    def create_plots(self):
        self.plot_x = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot_y = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot_z = MeshLinePlot(color=[0, 0, 1, 1])
        self.graph.add_plot(self.plot_x)
        self.graph.add_plot(self.plot_y)
        self.graph.add_plot(self.plot_z)

    def roll_plots(self):
        self.plot_x_old = self.plot_x
        self.plot_y_old = self.plot_y
        self.plot_z_old = self.plot_z

        
    def build(self):
        self.widget = MyWidget()
        
        self.graph = Graph(
                           xlabel='t',
                           ylabel='g',
                           x_ticks_minor=5,
                           x_ticks_major=25,
                           y_ticks_major=1,
                           y_grid_label=True,
                           x_grid_label=True,
                           padding=5,
                           x_grid=True,
                           y_grid=True,
                           xmin=-0,
                           xmax=100,
                           ymin=-2,
                           ymax=2)

        self.create_plots()
        self.roll_plots()
        self.create_plots()
        
        self.my_t = 0

        return self.graph

    def get_accelerometer(self):
        connection = httplib.HTTPConnection('raspberrypi:8080')
        connection.request('GET', '/accel')
        response = connection.getresponse()
        axes = json.load(response)
        return axes
    
    def on_start(self):
        self.widget.draw_something()
        self.widget.line()
        for i in range(1, 1000):
            self.widget.plot_value(i % 100)

        self.widget.old_x = 0

        def my_callback(dt):
            # TODO request accelerometer values from the http://raspberrypi:8080/accel
            
            axes = self.get_accelerometer()
            self.plot_x.points.append([self.my_t, axes['x']])
            self.plot_y.points.append([self.my_t, axes['y']])
            self.plot_z.points.append([self.my_t, axes['z']])
            self.my_t += 1

            if self.my_t > self.graph.xmax:
                self.roll_plots()
                
                self.create_plots()
                self.my_t = 0

            if len(self.plot_x_old.points) > 0:
                del self.plot_x_old.points[0]
                del self.plot_y_old.points[0]
                del self.plot_z_old.points[0]
            else:
                self.graph.remove_plot(self.plot_x_old)
                self.graph.remove_plot(self.plot_y_old)
                self.graph.remove_plot(self.plot_z_old)
            
        # call my_callback every 0.5 seconds
        Clock.schedule_interval(my_callback, 0.1)

if __name__ == '__main__':
    MyApp().run()
