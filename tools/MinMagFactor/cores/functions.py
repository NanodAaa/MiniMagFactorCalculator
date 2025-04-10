import numpy as np
import matplotlib.pyplot as plt
from cores import functions as func

def calculate_hor_min_mag_factor(data):
    data = _monitor_sensor_transform(data)
    data = _sensor_origin_point_convert(data)
    data = _sensor_world_transform(data)
    data = _insert_points_into_range(data)
    data = _points_world_sensor_transform(data)
    data = _change_points_sensor_into_pixel(data)
    data = _deconvert_points_sensor(data)
    data = _points_sensor_monitor_transform(data)
    
    return data

def _deconvert_points_sensor(data):
    """ 
    Deconverting points within ef sensor.
    """
    points_converted_pixel = data['points within ef sensor converted pixel']
    
    points_pixel = []
    for point_pixel_converted in points_converted_pixel:
        point_pixel = { 
            'x' : int(point_pixel_converted['x'] + data['sensor params']['width'] / 2), 
            'y' : int(point_pixel_converted['y'] + data['sensor params']['height'] / 2),
        }
        points_pixel.append(point_pixel)
        
    points_mm = []
    for point_pixel in points_pixel:
        point_mm = { 
            'x' : round(point_pixel['x'] * data['sensor params']['pixel size'], 3),
            'y' : round(point_pixel['y'] * data['sensor params']['pixel size'], 3),
        }
        points_mm.append(point_mm)
        
    data['points within ef sensor mm'] = points_mm
    data['points within ef sensor pixel'] = points_pixel
    
    return data
        

def _change_points_sensor_into_pixel(data):
    """ 
    Change coordinates of points within ef from mm into pixel.
    """
    points = data['points within ef sensor converted mm']
    points_pixel = []
    for point in points:
        point_pixel = func.coordinates_mm_to_pixel(point, data['sensor params']['pixel size'])
        points_pixel.append(point_pixel)
    
    data['points within ef sensor converted pixel'] = points_pixel
    
    return data

def _monitor_sensor_transform(data):
    """ 
    Transform monitor coordinates to sensor coordinates (Pixel format).
    """
    x_a = data['monitor point a']['x']
    y_a = data['monitor point a']['y']
    x_b = data['monitor point b']['x']
    y_b = data['monitor point b']['y']
    
    sensor_param_width = data['sensor params']['width']
    sensor_param_height = data['sensor params']['height']
    sensor_param_pixel_size = data['sensor params']['pixel size']
    
    monitor_param_width = data['monitor params']['width']
    monitor_param_height = data['monitor params']['height']
    
    x_c = int(x_a * ( (sensor_param_width - 0) / (monitor_param_width - 0) ) + 0)
    x_c_mm = round(x_c * sensor_param_pixel_size, 3)
    y_c = int(y_a * ( (sensor_param_height - 0) / (monitor_param_height - 0) ) + 0)
    y_c_mm = round(y_c * sensor_param_pixel_size, 3)
    
    x_d = int(x_b * ( (sensor_param_width - 0) / (monitor_param_width - 0) ) + 0)
    x_d_mm = round(x_d * sensor_param_pixel_size, 3)
    y_d = int(y_b * ( (sensor_param_height - 0) / (monitor_param_height - 0) ) + 0)
    y_d_mm = round(y_d * sensor_param_pixel_size, 3)
    
    data['sensor point c'] = { 'x' : x_c, 'y' : y_c }
    data['sensor point c mm'] = { 'x' : x_c_mm, 'y' : y_c_mm }
    data['sensor point d'] = { 'x' : x_d, 'y' : y_d }
    data['sensor point d mm'] = { 'x' : x_d_mm, 'y' : y_d_mm }
    
    return data

def _points_sensor_monitor_transform(data):
    """ 
    Transforming points withing ef from sensor to monitor coordinates.
    """
    points_sensor_pixel = data['points within ef sensor pixel']
    points_monitor_pixel = []
    for point_sensor_pixel in points_sensor_pixel:
        point_monitor_pixel = func.sensor_monitor_transform(point_sensor_pixel, data['sensor params'], data['monitor params'])
        points_monitor_pixel.append(point_monitor_pixel)
    
    points_monitor_mm = []
    for point_monitor_pixel in points_monitor_pixel:
        point_monitor_mm = func.coordinates_pixel_to_mm(point_monitor_pixel, data['monitor params']['pixel size'])
        points_monitor_mm.append(point_monitor_mm)
    
    data['points within ef monitor mm'] = points_monitor_mm
    data['points within ef monitor pixel'] = points_monitor_pixel
    
    return data

def _sensor_origin_point_convert(data):
    """ 
    Convert sensor coordinates' origin point to center.
    """
    x_c = data['sensor point c']['x']
    y_c = data['sensor point c']['y']
    x_d = data['sensor point d']['x']
    y_d = data['sensor point d']['y']
    
    sensor_param_width = data['sensor params']['width']
    sensor_param_height = data['sensor params']['height']
    sensor_param_pixel_size = data['sensor params']['pixel size']
    
    x_c_converted = int(x_c - sensor_param_width / 2)
    y_c_converted = int(y_c - sensor_param_height / 2)
    x_d_converted = int(x_d - sensor_param_width / 2)
    y_d_converted = int(y_d - sensor_param_height / 2)
    
    x_c_mm_converted = round(x_c_converted * sensor_param_pixel_size, 3)
    y_c_mm_converted = round(y_c_converted * sensor_param_pixel_size, 3)
    x_d_mm_converted = round(x_d_converted * sensor_param_pixel_size, 3)
    y_d_mm_converted = round(y_d_converted * sensor_param_pixel_size, 3)
    
    data['sensor point c converted'] = { 'x' : x_c_converted, 'y' : y_c_converted }
    data['sensor point c mm converted'] = { 'x' : x_c_mm_converted, 'y' : y_c_mm_converted }
    data['sensor point d converted'] = { 'x' : x_d_converted, 'y' : y_d_converted }
    data['sensor point d mm converted'] = { 'x' : x_d_mm_converted, 'y' : y_d_mm_converted }
    
    return data

def _sensor_world_transform(data):
    """ 
    Transform e & f from sensor coordinates to world coordinates.
    """
    # Sensor coordinates to Camera coordinatess
    data['world point e'] = func.sensor_world_transform(data['sensor point d mm converted'], data['fitting func coefs reverse'])['world coordinates']
    data['world point f'] = func.sensor_world_transform(data['sensor point c mm converted'], data['fitting func coefs reverse'])['world coordinates']

    return data

def _insert_points_into_range(data):
    """ 
    Insert 20 points into range e ~ f.
    """
    points = func.insert_point_into_range((data['world point e']['y'], data['world point f']['y']), 20)
    points_within_ef = []
    for point in points:
        points_within_ef.append({ 'x' : data['world point e']['x'], 'y' : point, 'z' : data['world point e']['z'], })
    
    data['points within ef'] = tuple(points_within_ef)
    return data

def _points_world_sensor_transform(data):
    """ 
    Transform points from world to sensor coordinates.
    """
    points = data['points within ef']
    points_sensor = []
    for point in points:
        point_sensor = func.world_sensor_transform(point, data['camera pose'], data['sensor params'], data['fitting func coefs'])['sensor coordinates']
        points_sensor.append(point_sensor)
    
    data['points within ef sensor converted mm'] = points_sensor
    
    return data

""" 
Show plots
"""

def show_plot(data):
    """ 
    """
    points_x = []
    points_y = []
    for point in data['points within ef monitor pixel']:
        points_x.append(point['x'])
        points_y.append(point['y'])
        
    points_monitor_pixel = data['points within ef monitor pixel']
    points_monitor_pixel_x = []
    for point in points_monitor_pixel:
        points_monitor_pixel_x.append(point['x'])
        
    points_monitor_pixel_x_dist = [abs(round(x - points_monitor_pixel_x[0], 3)) for x in points_monitor_pixel_x]
    
    points_world = data['points within ef']
    points_world_y = []
    for point in points_world:
        points_world_y.append(point['y'])
        
    points_world_y_dist = [abs(round(y - points_world_y[0], 3)) for y in points_world_y]
    
    # 5 Degrees Ploynomial fitting
    degree = 5
    poly_coeffs = np.polyfit(points_world_y_dist, points_monitor_pixel_x_dist, degree)
    poly_func = np.poly1d(poly_coeffs)
    deriv_poly = np.polyder(poly_func)  # 1th Step Dervivated Func
    x_fit = points_world_y_dist
    y_fit = poly_func(x_fit)
    y_fit_deriv = deriv_poly(x_fit)
    y_fit_deriv_ = y_fit_deriv * 0.887058824
    
    
    plt.figure(figsize=(12, 12))
    
    # Points distance from MP_A
    plt.subplot(2, 2, 1)
    plt.title(label='Points distance from MP_A', fontweight="bold")
    plt.xlabel(xlabel='Point distance from WP_F (mm)')
    plt.ylabel(ylabel='Point distance from MP_A')
    plt.scatter(points_world_y_dist, points_monitor_pixel_x_dist, color='red')
    plt.plot(x_fit, y_fit, color='blue', linestyle='-.')

    # Magnification Factors
    plt.subplot(2, 2, 2)
    plt.title(label='Magnification Factors of points', fontweight="bold")
    plt.xlabel(xlabel='Point distance from WP_F (mm)')
    plt.ylabel(ylabel='Maginification Factor')
    plt.scatter(x_fit, y_fit_deriv_)

    # Points position on monitor
    plt.subplot(2, 2, 3)
    plt.title(label='Points position on monitor', fontweight="bold")
    plt.xlabel(xlabel='Width')
    plt.ylabel(ylabel='Height')
    plt.scatter(points_x, points_y)

    plt.show()    
    
    return