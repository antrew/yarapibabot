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


Builder.load_string('''
#:kivy 1.7.2
<SensorGraph@Graph>:
    xlabel: 'time'
    x_ticks_minor: 5
    x_ticks_major: 0.5
    x_grid_label: False
    y_grid_label: True
    xlog: False
    ylog: False
    x_grid: True
    y_grid: True
    xmin: 0
    xmax: 1
    label_options: {'bold': True}
    size_hint_y: 0.9  

<SensorsBoxLayout>:
    orientation: 'vertical'
    SensorGraph:
        id: accel_graph
        ylabel: 'accelerometer values'
        ymin: -2
        ymax: 2
        y_ticks_minor: 5
        y_ticks_major: 0.5
           
    SensorGraph:
        id: gyro_graph
        ylabel: 'gyroscope values'
        ymin: -90
        ymax: 90
        y_ticks_minor: 3
        y_ticks_major: 30

    SensorGraph:
        id: control_graph
        ylabel: 'control values'
        ymin: -0.5
        ymax: 0.5
        y_ticks_minor: 5
        y_ticks_major: 0.5
''')

class SensorsBoxLayout(BoxLayout):
    
    #list for storing t values
    pt = ListProperty([])
    #initialize t
    t = 0
    
    # ---------------- for ACCELEROMETER sensor --------------------
    #plot-line for the accelerometer's x values
    accel_line_x = ObjectProperty(None)
    #plot-line for the accelerometer's y values
    accel_line_y = ObjectProperty(None)
    #plot-line for the accelerometer's z values
    accel_line_z = ObjectProperty(None)
    
    #list for storing the accelerometer's x values
    accel_px = ListProperty([])
    #list for storing the accelerometer's y values
    accel_py = ListProperty([])
    #list for storing the accelerometer's z values
    accel_pz = ListProperty([])
    
    
    # ---------------- for GYROSCOPE sensor ----------------------
    #plot-line for the gyroscope's x values
    gyro_line_x = ObjectProperty(None)
    #plot-line for the gyroscope's y values
    gyro_line_y = ObjectProperty(None)
    #plot-line for the gyroscope's z values
    gyro_line_z = ObjectProperty(None)
    
    #list for storing the gyroscope's x values
    gyro_px = ListProperty([])
    #list for storing the gyroscope's y values
    gyro_py = ListProperty([])
    #list for storing the gyroscope's z values
    gyro_pz = ListProperty([])
    
    
    def __init__(self, sensor_data):
        super(BoxLayout, self).__init__()
        self.pt = [self.t]
        
        # ---------------- for ACCELEROMETER sensor --------------------
        self.accel_px = []
        self.accel_py = []
        self.accel_pz = []
        self.accel_line_x = MeshLinePlot(color=[1, 0, 0, 1]) # X values are RED
        self.accel_line_y = MeshLinePlot(color=[0, 1, 0, 1]) # Y values are GREEN
        self.accel_line_z = MeshLinePlot(color=[0, 0, 1, 1]) # Z values are BLUE
        self.accel_line_x.points = zip(self.pt, self.accel_px)
        self.accel_line_y.points = zip(self.pt, self.accel_py)
        self.accel_line_z.points = zip(self.pt, self.accel_pz)
        self.ids.accel_graph.add_plot(self.accel_line_x)
        self.ids.accel_graph.add_plot(self.accel_line_y)
        self.ids.accel_graph.add_plot(self.accel_line_z)
        
        # ---------------- for GYROSCOPE sensor ----------------------
        self.gyro_px = []
        self.gyro_py = []
        self.gyro_pz = []
        self.gyro_line_x = MeshLinePlot(color=[1, 0, 0, 1]) # X values are RED
        self.gyro_line_y = MeshLinePlot(color=[0, 1, 0, 1]) # Y values are GREEN
        self.gyro_line_z = MeshLinePlot(color=[0, 0, 1, 1]) # Z values are BLUE
        self.gyro_line_x.points = zip(self.pt, self.gyro_px)
        self.gyro_line_y.points = zip(self.pt, self.gyro_py)
        self.gyro_line_z.points = zip(self.pt, self.gyro_pz)
        self.ids.gyro_graph.add_plot(self.gyro_line_x)
        self.ids.gyro_graph.add_plot(self.gyro_line_y)
        self.ids.gyro_graph.add_plot(self.gyro_line_z)
    
        self.control_plot_error          = MeshLinePlot(color=[1, 0, 0, 1])
        self.control_plot_integral_error = MeshLinePlot(color=[0, 1, 0, 1])
        self.control_plot_u              = MeshLinePlot(color=[0, 0, 1, 1])
        self.ids.control_graph.add_plot(self.control_plot_error)
        self.ids.control_graph.add_plot(self.control_plot_integral_error)
        self.ids.control_graph.add_plot(self.control_plot_u)

    def refresh_plot(self, sensor_data):
        
        if self.t > self.ids.accel_graph.xmax:
            #reset t
            self.t = 0
            #clear the entire pt list 
            del self.pt[:]
            #clear the entire accel_px, accel_py and accel_pz lists
            del self.accel_px[:]
            del self.accel_py[:]
            del self.accel_pz[:]
            #clear the entire gyro_px, gyro_py and gyro_pz lists
            del self.gyro_px[:]
            del self.gyro_py[:]
            del self.gyro_pz[:]
            del self.control_plot_error.points[:]
            del self.control_plot_integral_error.points[:]
            del self.control_plot_u.points[:]
            
        #add new values to pt list
        self.pt.append(self.t)
        
        # ---------------- for ACCELEROMETER sensor --------------------
        #add new values
        self.accel_px.append(sensor_data['sensors']['x'])
        self.accel_py.append(sensor_data['sensors']['y'])
        self.accel_pz.append(sensor_data['sensors']['z'])
        #refresh the plot for the accelerometer's x values
        self.accel_line_x.points = zip(self.pt, self.accel_px)
        #refresh the plot for the accelerometer's y values
        self.accel_line_y.points = zip(self.pt, self.accel_py)
        #refresh the plot for the accelerometer's z values
        self.accel_line_z.points = zip(self.pt, self.accel_pz)
        
        # ---------------- for GYROSCOPE sensor ----------------------
        #add new values
        self.gyro_px.append(sensor_data['sensors']['gx'])
        self.gyro_py.append(sensor_data['sensors']['gy'])
        self.gyro_pz.append(sensor_data['sensors']['gz'])
        #refresh the plot for the gyroerometer's x values
        self.gyro_line_x.points = zip(self.pt, self.gyro_px)
        #refresh the plot for the gyroerometer's y values
        self.gyro_line_y.points = zip(self.pt, self.gyro_py)
        #refresh the plot for the gyroerometer's z values
        self.gyro_line_z.points = zip(self.pt, self.gyro_pz)
    
        self.control_plot_error.points.append          ([self.t, sensor_data['control']['error']])
        self.control_plot_integral_error.points.append ([self.t, sensor_data['control']['integral_error']])
        self.control_plot_u.points.append              ([self.t, sensor_data['control']['u']])

class PlotSensorsApp(App):
    k = 0 #used to generate dummy values for sensors.
    REFRESH_TIME = 0.1 #read and plot sensor data every REFRESH_TIME seconds
    TIME_AXIS_INCREMENT = 0.01
    
    def build(self):
        sensor_data = self.get_sensors_data()
        self.mySensorsBoxLayout = SensorsBoxLayout(sensor_data)
        return self.mySensorsBoxLayout
    
    def on_start(self):
        
        def plot_sensors_callback(dt):
            self.mySensorsBoxLayout.t += self.TIME_AXIS_INCREMENT
            self.k = self.mySensorsBoxLayout.t
            sensor_data = self.get_sensors_data()
            self.mySensorsBoxLayout.refresh_plot(sensor_data)
             
        # call my_plot_sensors_callback every 0.1 seconds
        Clock.schedule_interval(plot_sensors_callback, self.REFRESH_TIME)
    
    def get_sensors_data(self):
        connection = httplib.HTTPConnection('raspberrypi:8080')
        connection.request('GET', '/sensors')
        response = connection.getresponse()
        axes = json.load(response)
        return axes

#         #generate some dummy values for sensors' data
#         dummy_accel_x_values =  exp(-(self.k - 0.5)**2 / (2 * .25**2))
#         dummy_accel_y_values =  exp(-(self.k - 0.5)**4 / (2 * .25**2))
#         dummy_accel_z_values =  self.k;
#         
#         dummy_gyro_x_values =  dummy_accel_x_values / 2
#         dummy_gyro_y_values =  dummy_accel_y_values / 2
#         dummy_gyro_z_values =  dummy_accel_z_values / 2
        
        sensor_data = {
            'accelerometer':{'x': dummy_accel_x_values, 'y': dummy_accel_y_values, 'z': dummy_accel_z_values},
            'gyroscope': {'x': dummy_gyro_x_values, 'y': dummy_gyro_y_values, 'z': dummy_gyro_z_values},
            }
        return sensor_data

if __name__ == '__main__':
    PlotSensorsApp().run()