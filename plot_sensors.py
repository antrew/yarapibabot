import httplib
import json
import kivy
from kivy.app import App
from kivy.graphics.context import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from math import exp

from kivy.garden.graph import Graph, MeshLinePlot


kivy.require('1.7.2')


Builder.load_file('plotter.kv')

class SensorsBoxLayout(BoxLayout):
    
    def __init__(self):
        super(BoxLayout, self).__init__()
        self.t = 0
        self.create_plots()
        self.roll_plots()
        self.create_plots()

    def create_plots(self):
        # ---------------- for ACCELEROMETER sensor --------------------
        self.accel_line_x = MeshLinePlot(color=[1, 0, 0, 1]) # X values are RED
        self.accel_line_y = MeshLinePlot(color=[0, 1, 0, 1]) # Y values are GREEN
        self.accel_line_z = MeshLinePlot(color=[0, 0, 1, 1]) # Z values are BLUE
        self.ids.accel_graph.add_plot(self.accel_line_x)
        self.ids.accel_graph.add_plot(self.accel_line_y)
        self.ids.accel_graph.add_plot(self.accel_line_z)
        
        # ---------------- for GYROSCOPE sensor ----------------------
        self.gyro_line_x = MeshLinePlot(color=[1, 0, 0, 1]) # X values are RED
        self.gyro_line_y = MeshLinePlot(color=[0, 1, 0, 1]) # Y values are GREEN
        self.gyro_line_z = MeshLinePlot(color=[0, 0, 1, 1]) # Z values are BLUE
        self.ids.gyro_graph.add_plot(self.gyro_line_x)
        self.ids.gyro_graph.add_plot(self.gyro_line_y)
        self.ids.gyro_graph.add_plot(self.gyro_line_z)
    
        self.control_plot_error          = MeshLinePlot(color=[1, 0, 0, 1])
        self.control_plot_integral_error = MeshLinePlot(color=[0, 1, 0, 1])
        self.control_plot_u              = MeshLinePlot(color=[0, 0, 1, 1])
        self.ids.control_graph.add_plot(self.control_plot_error)
        self.ids.control_graph.add_plot(self.control_plot_integral_error)
        self.ids.control_graph.add_plot(self.control_plot_u)

    def roll_plots(self):
        self.old_accel_line_x = self.accel_line_x
        self.old_accel_line_y = self.accel_line_y
        self.old_accel_line_z = self.accel_line_z
        self.old_gyro_line_x  = self.gyro_line_x
        self.old_gyro_line_y  = self.gyro_line_y
        self.old_gyro_line_z  = self.gyro_line_z
        self.old_control_plot_error          = self.control_plot_error         
        self.old_control_plot_integral_error = self.control_plot_integral_error
        self.old_control_plot_u              = self.control_plot_u             


    def refresh_plot(self, sensor_data):
        
        # ---------------- for ACCELEROMETER sensor --------------------
        self.accel_line_x.points.append([self.t, sensor_data['sensors']['x']])
        self.accel_line_y.points.append([self.t, sensor_data['sensors']['y']])
        self.accel_line_z.points.append([self.t, sensor_data['sensors']['z']])
        # ---------------- for GYROSCOPE sensor ----------------------
        self.gyro_line_x.points.append ([self.t, sensor_data['sensors']['gx']])
        self.gyro_line_y.points.append ([self.t, sensor_data['sensors']['gy']])
        self.gyro_line_z.points.append ([self.t, sensor_data['sensors']['gz']])
    
        self.control_plot_error.points.append          ([self.t, sensor_data['control']['error']])
        self.control_plot_integral_error.points.append ([self.t, sensor_data['control']['integral_error']])
        self.control_plot_u.points.append              ([self.t, sensor_data['control']['u']])

        self.t += 1

        if self.t > self.ids.accel_graph.xmax:
            self.roll_plots()
            self.create_plots()
            #reset t
            self.t = 0

        if len(self.old_accel_line_x.points) > 0:
            del self.old_accel_line_x.points[0]
            del self.old_accel_line_y.points[0]
            del self.old_accel_line_z.points[0]
            del self.old_gyro_line_x.points[0]
            del self.old_gyro_line_y.points[0]
            del self.old_gyro_line_z.points[0]
            del self.old_control_plot_error.points[0]
            del self.old_control_plot_integral_error.points[0]
            del self.old_control_plot_u.points[0]
        else:
            self.ids.accel_graph.add_plot(self.old_accel_line_x)
            self.ids.accel_graph.add_plot(self.old_accel_line_y)
            self.ids.accel_graph.add_plot(self.old_accel_line_z)
            self.ids.gyro_graph.add_plot(self.old_gyro_line_x)
            self.ids.gyro_graph.add_plot(self.old_gyro_line_y)
            self.ids.gyro_graph.add_plot(self.old_gyro_line_z)
            self.ids.control_graph.add_plot(self.old_control_plot_error)
            self.ids.control_graph.add_plot(self.old_control_plot_integral_error)
            self.ids.control_graph.add_plot(self.old_control_plot_u)

class PlotSensorsApp(App):
    k = 0 #used to generate dummy values for sensors.
    REFRESH_TIME = 0.1 #read and plot sensor data every REFRESH_TIME seconds
    TIME_AXIS_INCREMENT = 0.01
    
    def build(self):
        self.mySensorsBoxLayout = SensorsBoxLayout()
        return self.mySensorsBoxLayout
    
    def on_start(self):
        
        def plot_sensors_callback(dt):
            # True - use real HTTP server
            # False - use fake values
            if False:
                sensor_data = self.get_sensors_data()
            else:
                sensor_data = self.get_fake_sensor_data()
            for single_data_set in sensor_data:
                self.mySensorsBoxLayout.refresh_plot(single_data_set)
             
        # call my_plot_sensors_callback every 0.1 seconds
        Clock.schedule_interval(plot_sensors_callback, self.REFRESH_TIME)
    
    def get_sensors_data(self):
        connection = httplib.HTTPConnection('raspberrypi:8080')
        connection.request('GET', '/sensors')
        response = connection.getresponse()
        axes = json.load(response)
        return axes

    def get_fake_sensor_data(self):
        # simulate that we get an array of log points from the server
        log_values = []
        for i in range(1, 10):
            log_values.append(self.get_fake_sensor_data_single_point())
        return log_values

    def get_fake_sensor_data_single_point(self):
        self.k += 0.02

        # generate some dummy values for sensors' data
        dummy_accel_x_values = exp(-(self.k - 0.5) ** 2 / (2 * .25 ** 2))
        dummy_accel_y_values = exp(-(self.k - 0.5) ** 4 / (2 * .25 ** 2))
        dummy_accel_z_values = self.k;
         
        dummy_gyro_x_values = dummy_accel_x_values / 2
        dummy_gyro_y_values = dummy_accel_y_values / 2
        dummy_gyro_z_values = dummy_accel_z_values / 2
    
        sensor_data = {
            'sensors':{'x': dummy_accel_x_values, 'y': dummy_accel_y_values, 'z': dummy_accel_z_values,
                       'gx': dummy_gyro_x_values, 'gy': dummy_gyro_y_values, 'gz': dummy_gyro_z_values},
            'control': {'error': 0.1, 'integral_error': 0.2, 'u':-0.2},
            }
        return sensor_data

if __name__ == '__main__':
    PlotSensorsApp().run()
