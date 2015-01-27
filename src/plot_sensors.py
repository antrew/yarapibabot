import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.context import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from math import exp

Builder.load_string('''
#:kivy 1.7.2
<SensorGraph@Graph>:
    xlabel: 'time'
    x_ticks_minor: 5
    x_ticks_major: 0.1
    y_ticks_minor: 5
    y_ticks_major: 0.1
    x_grid_label: False
    y_grid_label: True
    xlog: False
    ylog: False
    x_grid: False
    y_grid: False
    xmin: 0
    xmax: 1
    ymin: 0
    ymax: 1
    label_options: {'bold': True}
    size_hint_y: 0.9  

<SensorsBoxLayout>:
    orientation: 'vertical'
    SensorGraph:
        id: accel_graph
        ylabel: 'accelerometer values'
           
    SensorGraph:
        id: gyro_graph
        ylabel: 'gyroscope values'
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
        self.accel_px = [sensor_data['accelerometer']['x']]
        self.accel_py = [sensor_data['accelerometer']['y']]
        self.accel_pz = [sensor_data['accelerometer']['z']]
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
        self.gyro_px = [sensor_data['gyroscope']['x']]
        self.gyro_py = [sensor_data['gyroscope']['y']]
        self.gyro_pz = [sensor_data['gyroscope']['z']]
        self.gyro_line_x = MeshLinePlot(color=[1, 0, 0, 1]) # X values are RED
        self.gyro_line_y = MeshLinePlot(color=[0, 1, 0, 1]) # Y values are GREEN
        self.gyro_line_z = MeshLinePlot(color=[0, 0, 1, 1]) # Z values are BLUE
        self.gyro_line_x.points = zip(self.pt, self.gyro_px)
        self.gyro_line_y.points = zip(self.pt, self.gyro_py)
        self.gyro_line_z.points = zip(self.pt, self.gyro_pz)
        self.ids.gyro_graph.add_plot(self.gyro_line_x)
        self.ids.gyro_graph.add_plot(self.gyro_line_y)
        self.ids.gyro_graph.add_plot(self.gyro_line_z)
    
    def refresh_plot(self, sensor_data):
        # TODO request accelerometer values from the http://raspberrypi:8080/accel   
        
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
            
        #add new values to pt list
        self.pt.append(self.t)
        
        # ---------------- for ACCELEROMETER sensor --------------------
        #add new values to accel_px list
        self.accel_px.append(sensor_data['accelerometer']['x'])
        #add new values to accel_py list
        self.accel_py.append(sensor_data['accelerometer']['y'])
        #add new values to accel_pz list
        self.accel_pz.append(sensor_data['accelerometer']['z'])
        #refresh the plot for the accelerometer's x values
        self.accel_line_x.points = zip(self.pt, self.accel_px)
        #refresh the plot for the accelerometer's y values
        self.accel_line_y.points = zip(self.pt, self.accel_py)
        #refresh the plot for the accelerometer's z values
        self.accel_line_z.points = zip(self.pt, self.accel_pz)
        
        # ---------------- for GYROSCOPE sensor ----------------------
        #add new values to gyro_px list
        self.gyro_px.append(sensor_data['gyroscope']['x'])
        #add new values to gyro_py list
        self.gyro_py.append(sensor_data['gyroscope']['y'])
        #add new values to gyro_pz list
        self.gyro_pz.append(sensor_data['gyroscope']['z'])
        #refresh the plot for the gyroerometer's x values
        self.gyro_line_x.points = zip(self.pt, self.gyro_px)
        #refresh the plot for the gyroerometer's y values
        self.gyro_line_y.points = zip(self.pt, self.gyro_py)
        #refresh the plot for the gyroerometer's z values
        self.gyro_line_z.points = zip(self.pt, self.gyro_pz)
    

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
#         connection = httplib.HTTPConnection('raspberrypi:8080')
#         connection.request('GET', '/accel')
#         response = connection.getresponse()
#         axes = json.load(response)

        #generate some dummy values for sensors' data
        dummy_accel_x_values =  exp(-(self.k - 0.5)**2 / (2 * .25**2))
        dummy_accel_y_values =  exp(-(self.k - 0.5)**4 / (2 * .25**2))
        dummy_accel_z_values =  self.k;
        
        dummy_gyro_x_values =  dummy_accel_x_values / 2
        dummy_gyro_y_values =  dummy_accel_y_values / 2
        dummy_gyro_z_values =  dummy_accel_z_values / 2
        
        sensor_data = {
            'accelerometer':{'x': dummy_accel_x_values, 'y': dummy_accel_y_values, 'z': dummy_accel_z_values},
            'gyroscope': {'x': dummy_gyro_x_values, 'y': dummy_gyro_y_values, 'z': dummy_gyro_z_values},
            }
        return sensor_data

if __name__ == '__main__':
    PlotSensorsApp().run()