# gui.py

import tkinter as tk
from tools.W2CTransform.cores import calculate
from tools.W2CTransform.cores import storge
from tools.W2CTransform.data.data import Data
from cores import JsonStorage as js
from assets.styles.tkinter_style import TkinterStyle

class W2CTransform(tk.Toplevel):
    data_filepath = Data.data_filepath
    
    entry_list = []
    
    label_format_dict = TkinterStyle.label_format_dict
    entry_format_dict = TkinterStyle.entry_format_dict
    button_format_dict = TkinterStyle.button_format_dict
        
    world_coordinates_widgets_postion_dict = {
        'label' : {'row' : 0, 'column' : 0}, 'x entry' : {'row' : 0, 'column' : 1}, 'y entry' : {'row' : 0, 'column' : 2}, 'z entry' : {'row' : 0, 'column' : 3}}
    camera_pose_widgets_position_dict = {
        'label' : {'row' : 1, 'column' : 0}, 'pitch entry' : {'row' : 1, 'column' : 1}, 'yaw entry' : {'row' : 1, 'column' : 2}, 'roll entry' : {'row' : 1, 'column' : 3}}
    fitting_func_coefs_widgets_position_dict = {
        'label' : {'row' : 2, 'column' : 0}, 'x5 entry' : {'row' : 2, 'column' : 1}, 'x4 entry' : {'row' : 2, 'column' : 2}, 
        'x3 entry' : {'row' : 2, 'column' : 3}, 'x2 entry' : {'row' : 2, 'column' : 4}, 'x1 entry' : {'row' : 2, 'column' : 5}, 'x0 entry' : {'row' : 2, 'column' : 6}}
    fitting_func_coefs_reverse_widgets_position_dict = {
        'label' : {'row' : 3, 'column' : 0}, 'x5 entry' : {'row' : 3, 'column' : 1}, 'x4 entry' : {'row' : 3, 'column' : 2}, 
        'x3 entry' : {'row' : 3, 'column' : 3}, 'x2 entry' : {'row' : 3, 'column' : 4}, 'x1 entry' : {'row' : 3, 'column' : 5}, 'x0 entry' : {'row' : 3, 'column' : 6}}
    sensor_params_widgets_position_dict = {
        'label' : {'row' : 4, 'column' : 0}, 'width entry' : {'row' : 4, 'column' : 1}, 'height entry' : {'row' : 4, 'column' : 2}, 'pixel size entry' : {'row' : 4, 'column' : 3}}
    camera_coordinates_widgets_position_dict = {
        'label' : {'row' : 5, 'column' : 0}, 'x entry' : {'row' : 5, 'column' : 1}, 'y entry' : {'row' : 5, 'column' : 2}, 'z entry' : {'row' : 5, 'column' : 3}}
    pixel_coordinates_widgets_position_dict = {
        'label' : {'row' : 6, 'column' : 0}, 'x entry' : {'row' : 6, 'column' : 1}, 'y entry' : {'row' : 6, 'column' : 2}}
    button_widgets_position_dict = {
        'calculate' : {'row' : 7, 'column' : 0}, 'save' : {'row' : 7, 'column' : 1}, 'positive' : {'row' : 7, 'column' : 2}, 
        'reverse' : {'row' : 7, 'column' : 3}, 'lock' : {'row' : 8, 'column' : 0}, 'unlock' : {'row' : 8, 'column' : 1}}
    label_widgets_position_dict = {
        'message' : {'row' : 8, 'column' : 2}}
    
    def __init__(self, root):
        self.root = root
        super().__init__(self.root)
        self.calculate_mode_positive = True
        self.lock_mode = True
        self._init_config_data()
        self._set_init_window()
        self.protocol('WM_DELETE_WINDOW', self._onclose)

    def _init_config_data(self):
        self.data = Data.data
        storage = js.JsonStorage(self.data_filepath)
        temp_data = storage.load()
        if temp_data != {}:
            self.data = temp_data
        else:
            storage.save(self.data)
            
        return

    def _set_init_window(self):
        # World Coordinates
        self.world_coordinate_label = tk.Label(self, text='P_w(XYZ): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.world_coordinate_label.grid(row=self.world_coordinates_widgets_postion_dict['label']['row'], column=self.world_coordinates_widgets_postion_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])

        self.world_coordinate_x_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.world_coordinate_x_entry.grid(row=self.world_coordinates_widgets_postion_dict['x entry']['row'], column=self.world_coordinates_widgets_postion_dict['x entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.world_coordinate_x_entry.insert(0, self.data['world coordinates']['x'])
        self.entry_list.append(self.world_coordinate_x_entry)
        
        self.world_coordinate_y_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.world_coordinate_y_entry.grid(row=self.world_coordinates_widgets_postion_dict['y entry']['row'], column=self.world_coordinates_widgets_postion_dict['y entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.world_coordinate_y_entry.insert(0, self.data['world coordinates']['y'])
        self.entry_list.append(self.world_coordinate_y_entry)
        
        self.world_coordinate_z_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.world_coordinate_z_entry.grid(row=self.world_coordinates_widgets_postion_dict['z entry']['row'], column=self.world_coordinates_widgets_postion_dict['z entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.world_coordinate_z_entry.insert(0, self.data['world coordinates']['z'])
        self.entry_list.append(self.world_coordinate_z_entry)
        
        background_color = 'lightblue'
        self.world_coordinate_x_entry.config(bg=background_color)
        self.world_coordinate_y_entry.config(bg=background_color)
        self.world_coordinate_z_entry.config(bg=background_color)
        
        # Camera Pose
        self.camera_pose_label = tk.Label(self, text='Pose(PYR): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.camera_pose_label.grid(row=self.camera_pose_widgets_position_dict['label']['row'], column=self.camera_pose_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.camera_pose_pitch_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_pose_pitch_entry.grid(row=self.camera_pose_widgets_position_dict['pitch entry']['row'], column=self.camera_pose_widgets_position_dict['pitch entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_pose_pitch_entry.insert(0, self.data['camera pose']['pitch'])
        self.entry_list.append(self.camera_pose_pitch_entry)
        
        self.camera_pose_yaw_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_pose_yaw_entry.grid(row=self.camera_pose_widgets_position_dict['yaw entry']['row'], column=self.camera_pose_widgets_position_dict['yaw entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_pose_yaw_entry.insert(0, self.data['camera pose']['yaw'])
        self.entry_list.append(self.camera_pose_yaw_entry)
        
        self.camera_pose_roll_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_pose_roll_entry.grid(row=self.camera_pose_widgets_position_dict['roll entry']['row'], column=self.camera_pose_widgets_position_dict['roll entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_pose_roll_entry.insert(0, self.data['camera pose']['roll'])
        self.entry_list.append(self.camera_pose_roll_entry)
        
        # Fitting Function Coefficients
        self.fitting_func_coefs_label = tk.Label(self, text='FitCoe(X5>0): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.fitting_func_coefs_label.grid(row=self.fitting_func_coefs_widgets_position_dict['label']['row'], column=self.fitting_func_coefs_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.fitting_func_coefs_x5_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x5_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x5 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x5 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x5_entry.insert(0, self.data['fitting func coefs']['x5'])
        self.entry_list.append(self.fitting_func_coefs_x5_entry)
        
        self.fitting_func_coefs_x4_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x4_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x4 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x4 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x4_entry.insert(0, self.data['fitting func coefs']['x4'])
        self.entry_list.append(self.fitting_func_coefs_x4_entry)
        
        self.fitting_func_coefs_x3_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x3_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x3 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x3 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x3_entry.insert(0, self.data['fitting func coefs']['x3'])
        self.entry_list.append(self.fitting_func_coefs_x3_entry)
        
        self.fitting_func_coefs_x2_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x2_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x2 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x2 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x2_entry.insert(0, self.data['fitting func coefs']['x2'])
        self.entry_list.append(self.fitting_func_coefs_x2_entry)
        
        self.fitting_func_coefs_x1_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x1_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x1 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x1 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x1_entry.insert(0, self.data['fitting func coefs']['x1'])
        self.entry_list.append(self.fitting_func_coefs_x1_entry)
        
        self.fitting_func_coefs_x0_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_x0_entry.grid(row=self.fitting_func_coefs_widgets_position_dict['x0 entry']['row'], column=self.fitting_func_coefs_widgets_position_dict['x0 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_x0_entry.insert(0, self.data['fitting func coefs']['x0'])
        self.entry_list.append(self.fitting_func_coefs_x0_entry)
        
        # Fitting Function Coefficients Reverse
        self.fitting_func_coefs_reverse_label = tk.Label(self, text='FitCoeR(X5>0): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.fitting_func_coefs_reverse_label.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['label']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.fitting_func_coefs_reverse_x5_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x5_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x5 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x5 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x5_entry.insert(0, self.data['fitting func coefs reverse']['x5'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x5_entry)
        
        self.fitting_func_coefs_reverse_x4_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x4_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x4 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x4 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x4_entry.insert(0, self.data['fitting func coefs reverse']['x4'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x4_entry)
        
        self.fitting_func_coefs_reverse_x3_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x3_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x3 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x3 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x3_entry.insert(0, self.data['fitting func coefs reverse']['x3'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x3_entry)
        
        self.fitting_func_coefs_reverse_x2_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x2_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x2 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x2 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x2_entry.insert(0, self.data['fitting func coefs reverse']['x2'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x2_entry)
        
        self.fitting_func_coefs_reverse_x1_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x1_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x1 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x1 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x1_entry.insert(0, self.data['fitting func coefs reverse']['x1'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x1_entry)
        
        self.fitting_func_coefs_reverse_x0_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.fitting_func_coefs_reverse_x0_entry.grid(row=self.fitting_func_coefs_reverse_widgets_position_dict['x0 entry']['row'], column=self.fitting_func_coefs_reverse_widgets_position_dict['x0 entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.fitting_func_coefs_reverse_x0_entry.insert(0, self.data['fitting func coefs reverse']['x0'])
        self.entry_list.append(self.fitting_func_coefs_reverse_x0_entry)
        
        # Sensor Params
        self.sensor_params_label = tk.Label(self, text='SenPrms(WHP): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.sensor_params_label.grid(row=self.sensor_params_widgets_position_dict['label']['row'], column=self.sensor_params_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.sensor_params_width_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.sensor_params_width_entry.grid(row=self.sensor_params_widgets_position_dict['width entry']['row'], column=self.sensor_params_widgets_position_dict['width entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.sensor_params_width_entry.insert(0, self.data['sensor params']['width'])
        self.entry_list.append(self.sensor_params_width_entry)
        
        self.sensor_params_height_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.sensor_params_height_entry.grid(row=self.sensor_params_widgets_position_dict['height entry']['row'], column=self.sensor_params_widgets_position_dict['height entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.sensor_params_height_entry.insert(0, self.data['sensor params']['height'])
        self.entry_list.append(self.sensor_params_height_entry)
        
        self.sensor_params_pixel_size_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.sensor_params_pixel_size_entry.grid(row=self.sensor_params_widgets_position_dict['pixel size entry']['row'], column=self.sensor_params_widgets_position_dict['pixel size entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.sensor_params_pixel_size_entry.insert(0, self.data['sensor params']['pixel size'])
        self.entry_list.append(self.sensor_params_pixel_size_entry)
        
        # camera Coordinates
        self.camera_corrdinates_label = tk.Label(self, text='P_c(XYZ): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.camera_corrdinates_label.grid(row=self.camera_coordinates_widgets_position_dict['label']['row'], column=self.camera_coordinates_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.camera_corrdinates_x_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_corrdinates_x_entry.grid(row=self.camera_coordinates_widgets_position_dict['x entry']['row'], column=self.camera_coordinates_widgets_position_dict['x entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_corrdinates_x_entry.insert(0, self.data['camera coordinates']['x'])
        self.camera_corrdinates_x_entry.config(state='readonly') # Set entry to read only
        self.entry_list.append(self.camera_corrdinates_x_entry)
        
        self.camera_corrdinates_y_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_corrdinates_y_entry.grid(row=self.camera_coordinates_widgets_position_dict['y entry']['row'], column=self.camera_coordinates_widgets_position_dict['y entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_corrdinates_y_entry.insert(0, self.data['camera coordinates']['y'])
        self.camera_corrdinates_y_entry.config(state='readonly') # Set entry to read only
        self.entry_list.append(self.camera_corrdinates_y_entry)
        
        self.camera_corrdinates_z_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.camera_corrdinates_z_entry.grid(row=self.camera_coordinates_widgets_position_dict['z entry']['row'], column=self.camera_coordinates_widgets_position_dict['z entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.camera_corrdinates_z_entry.insert(0, self.data['camera coordinates']['z'])
        self.camera_corrdinates_z_entry.config(state='readonly') # Set entry to read only
        self.entry_list.append(self.camera_corrdinates_z_entry)
        
        # Pixel Coordinates
        self.pixel_coordinates_label = tk.Label(self, text='P_p(XY): ', font=self.label_format_dict['font'], width=self.label_format_dict['width'])
        self.pixel_coordinates_label.grid(row=self.pixel_coordinates_widgets_position_dict['label']['row'], column=self.pixel_coordinates_widgets_position_dict['label']['column'], padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky=self.label_format_dict['sticky'])
        
        self.pixel_coordinate_x_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.pixel_coordinate_x_entry.grid(row=self.pixel_coordinates_widgets_position_dict['x entry']['row'], column=self.pixel_coordinates_widgets_position_dict['x entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.pixel_coordinate_x_entry.insert(0, self.data['pixel coordinates']['x'])
        self.pixel_coordinate_x_entry.config(state='readonly') # Set entry to read only
        self.entry_list.append(self.pixel_coordinate_x_entry)
        
        self.pixel_coordinate_y_entry = tk.Entry(self, font=self.entry_format_dict['font'], width=self.entry_format_dict['width'])
        self.pixel_coordinate_y_entry.grid(row=self.pixel_coordinates_widgets_position_dict['y entry']['row'], column=self.pixel_coordinates_widgets_position_dict['y entry']['column'], padx=self.entry_format_dict['padx'], pady=self.entry_format_dict['pady'], sticky=self.entry_format_dict['sticky'])
        self.pixel_coordinate_y_entry.insert(0, self.data['pixel coordinates']['y'])
        self.pixel_coordinate_y_entry.config(state='readonly') # Set entry to read only
        self.entry_list.append(self.pixel_coordinate_y_entry)
        
        # Calculate Button
        self.calculate_button = tk.Button(self, text='Calculate', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_calculate)
        self.calculate_button.grid(row=self.button_widgets_position_dict['calculate']['row'], column=self.button_widgets_position_dict['calculate']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])
                
        # Save Button
        self.save_button = tk.Button(self, text='Save', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_save)
        self.save_button.grid(row=self.button_widgets_position_dict['save']['row'], column=self.button_widgets_position_dict['save']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])        

        # Positive Button
        self.positive_button = tk.Button(self, text='Positive', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_positive)
        self.positive_button.grid(row=self.button_widgets_position_dict['positive']['row'], column=self.button_widgets_position_dict['positive']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])
        self.positive_button.config(state='disabled')
        
        # Reverse Button
        self.reverse_button = tk.Button(self, text='Reverse', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_reverse)
        self.reverse_button.grid(row=self.button_widgets_position_dict['reverse']['row'], column=self.button_widgets_position_dict['reverse']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])        
                
        # Lock Button
        self.lock_button = tk.Button(self, text='Lock', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_lock)
        self.lock_button.grid(row=self.button_widgets_position_dict['lock']['row'], column=self.button_widgets_position_dict['lock']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])
        self.lock_button.config(state='disabled')
        
        # Unlock Button
        self.unlock_button = tk.Button(self, text='Unlock', bg=self.button_format_dict['bg'], width=self.button_format_dict['width'], command=self.onclick_button_unlock)
        self.unlock_button.grid(row=self.button_widgets_position_dict['unlock']['row'], column=self.button_widgets_position_dict['unlock']['column'], padx=self.button_format_dict['padx'], pady=self.button_format_dict['pady'], sticky=self.button_format_dict['sticky'])
        
        # Message Label
        self.message_label = tk.Label(self, text='Welcome!', font=self.label_format_dict['font'], width=15, foreground='red', borderwidth=2, relief="solid")
        self.message_label.grid(row=self.label_widgets_position_dict['message']['row'], column=self.label_widgets_position_dict['message']['column'], columnspan=2, padx=self.label_format_dict['padx'], pady=self.label_format_dict['pady'], sticky='wesn')
                
    def onclick_button_positive(self):
        self.positive()
        self.message_label.config(text='Mode switched to Positive!')
    
    def positive(self):
        self.positive_button.config(state='disabled')
        self.reverse_button.config(state='active')
        
        background_color = 'lightblue'
        self.world_coordinate_x_entry.config(state='normal', bg=background_color)
        self.world_coordinate_y_entry.config(state='normal', bg=background_color)
        self.world_coordinate_z_entry.config(state='normal', bg=background_color)
        
        self.pixel_coordinate_x_entry.config(state='readonly')
        self.pixel_coordinate_y_entry.config(state='readonly')
        
        self.calculate_mode_positive = True
        return
              
    def onclick_button_reverse(self):
        self.reverse()
        self.message_label.config(text='Mode switched to Reverse!')
    
    def reverse(self):
        self.reverse_button.config(state='disabled')
        self.positive_button.config(state='active')
        
        self.world_coordinate_x_entry.config(state='readonly')
        self.world_coordinate_y_entry.config(state='readonly')
        self.world_coordinate_z_entry.config(state='readonly')
        
        background_color = 'lightblue'
        self.pixel_coordinate_x_entry.config(state='normal', bg=background_color)
        self.pixel_coordinate_y_entry.config(state='normal', bg=background_color)
    
        self.calculate_mode_positive = False
        return
                
    def onclick_button_save(self):
        if self.save_data_from_entry_to_memory() == -1:
            return
        
        if storge.save_data_to_json(self.data, self.data_filepath) == -1:
            return
  
        if self.refresh_data_in_gui() == -1:
            return
       
        self.message_label.config(text='Data saved!')
        return
                
    def onclick_button_calculate(self):
        self.save_data_from_entry_to_memory()
        
        if self.calculate_mode_positive:
            calculate.calculate_positive(self.data)
        else:
            calculate.calculate_reverse(self.data)
        
        self.refresh_data_in_gui()
        storge.save_data_to_json(self.data, self.data_filepath)
        
        self.message_label.config(text='Calculate finished!')
        
        return
        
    def save_data_from_entry_to_memory(self):      
        """
        Save data to memory. 
        """   
        # World Coordinates
        self.data['world coordinates'] = { 
            'x' : float(self.world_coordinate_x_entry.get().replace('E', 'e')), 
            'y' : float(self.world_coordinate_y_entry.get().replace('E', 'e')), 
            'z' : float(self.world_coordinate_z_entry.get().replace('E', 'e')) 
        }
        
        # Fitting Functiong Coefficients
        self.data['fitting func coefs'] = { 
            'x5' : float(self.fitting_func_coefs_x5_entry.get().replace('E', 'e')), 
            'x4' : float(self.fitting_func_coefs_x4_entry.get().replace('E', 'e')),
            'x3' : float(self.fitting_func_coefs_x3_entry.get().replace('E', 'e')), 
            'x2' : float(self.fitting_func_coefs_x2_entry.get().replace('E', 'e')),
            'x1' : float(self.fitting_func_coefs_x1_entry.get().replace('E', 'e')), 
            'x0' : float(self.fitting_func_coefs_x0_entry.get().replace('E', 'e')),
        }
        
        # Fitting Functiong Coefficients Reverse
        self.data['fitting func coefs reverse'] = { 
            'x5' : float(self.fitting_func_coefs_reverse_x5_entry.get().replace('E', 'e')), 
            'x4' : float(self.fitting_func_coefs_reverse_x4_entry.get().replace('E', 'e')),
            'x3' : float(self.fitting_func_coefs_reverse_x3_entry.get().replace('E', 'e')), 
            'x2' : float(self.fitting_func_coefs_reverse_x2_entry.get().replace('E', 'e')),
            'x1' : float(self.fitting_func_coefs_reverse_x1_entry.get().replace('E', 'e')), 
            'x0' : float(self.fitting_func_coefs_reverse_x0_entry.get().replace('E', 'e')),
        }
        
        # Camera Pose
        self.data['camera pose'] = { 
            'pitch' : float(self.camera_pose_pitch_entry.get().replace('E', 'e')), 
            'yaw' : float(self.camera_pose_yaw_entry.get().replace('E', 'e')), 
            'roll' : float(self.camera_pose_roll_entry.get().replace('E', 'e')) 
        }
        
        # Sensor Params
        self.data['sensor params'] = { 
            'width' : int(self.sensor_params_width_entry.get()), 
            'height' : int(self.sensor_params_height_entry.get()), 
            'pixel size' : float(self.sensor_params_pixel_size_entry.get().replace('E', 'e')) 
        }       
           
        # Camera Coordinates
        self.data['camera coordinates'] = {
            'x' : float(self.camera_corrdinates_x_entry.get().replace('E', 'e')), 
            'y' : float(self.camera_corrdinates_y_entry.get().replace('E', 'e')), 
            'z' : float(self.camera_corrdinates_z_entry.get().replace('E', 'e'))
        }
           
        # Pixel Coordinates
        self.data['pixel coordinates'] = {
            'x' : float(self.pixel_coordinate_x_entry.get().replace('E', 'e')), 
            'y' : float(self.pixel_coordinate_y_entry.get().replace('E', 'e'))
        }
           
        return
    
    def clear_data_in_gui(self):
        for entry in self.entry_list:
            entry.delete(0, tk.END)
    
    def refresh_data_in_gui(self):
        """ 
        Write data from memory to entry.
        """
        # Pose
        self.camera_pose_pitch_entry.delete(0, tk.END)
        self.camera_pose_yaw_entry.delete(0, tk.END)
        self.camera_pose_roll_entry.delete(0, tk.END)
        
        self.camera_pose_pitch_entry.insert(0, self.data['camera pose']['pitch'])
        self.camera_pose_yaw_entry.insert(0, self.data['camera pose']['yaw'])
        self.camera_pose_roll_entry.insert(0, self.data['camera pose']['roll'])

        # Fitting funcion coefficients
        self.fitting_func_coefs_x5_entry.delete(0, tk.END)
        self.fitting_func_coefs_x4_entry.delete(0, tk.END)
        self.fitting_func_coefs_x3_entry.delete(0, tk.END)
        self.fitting_func_coefs_x2_entry.delete(0, tk.END)
        self.fitting_func_coefs_x1_entry.delete(0, tk.END)
        self.fitting_func_coefs_x0_entry.delete(0, tk.END)
        
        self.fitting_func_coefs_x5_entry.insert(0, self.data['fitting func coefs']['x5'])
        self.fitting_func_coefs_x4_entry.insert(0, self.data['fitting func coefs']['x4'])
        self.fitting_func_coefs_x3_entry.insert(0, self.data['fitting func coefs']['x3'])
        self.fitting_func_coefs_x2_entry.insert(0, self.data['fitting func coefs']['x2'])
        self.fitting_func_coefs_x1_entry.insert(0, self.data['fitting func coefs']['x1'])
        self.fitting_func_coefs_x0_entry.insert(0, self.data['fitting func coefs']['x0'])
        
        # Fitting funcion coefficients reverse
        self.fitting_func_coefs_reverse_x5_entry.delete(0, tk.END)
        self.fitting_func_coefs_reverse_x4_entry.delete(0, tk.END)
        self.fitting_func_coefs_reverse_x3_entry.delete(0, tk.END)
        self.fitting_func_coefs_reverse_x2_entry.delete(0, tk.END)
        self.fitting_func_coefs_reverse_x1_entry.delete(0, tk.END)
        self.fitting_func_coefs_reverse_x0_entry.delete(0, tk.END)
        
        self.fitting_func_coefs_reverse_x5_entry.insert(0, self.data['fitting func coefs reverse']['x5'])
        self.fitting_func_coefs_reverse_x4_entry.insert(0, self.data['fitting func coefs reverse']['x4'])
        self.fitting_func_coefs_reverse_x3_entry.insert(0, self.data['fitting func coefs reverse']['x3'])
        self.fitting_func_coefs_reverse_x2_entry.insert(0, self.data['fitting func coefs reverse']['x2'])
        self.fitting_func_coefs_reverse_x1_entry.insert(0, self.data['fitting func coefs reverse']['x1'])
        self.fitting_func_coefs_reverse_x0_entry.insert(0, self.data['fitting func coefs reverse']['x0'])
        
        # Sensor params
        self.sensor_params_width_entry.delete(0, tk.END)
        self.sensor_params_height_entry.delete(0, tk.END)
        self.sensor_params_pixel_size_entry.delete(0, tk.END)
        
        self.sensor_params_width_entry.insert(0, self.data['sensor params']['width'])
        self.sensor_params_height_entry.insert(0, self.data['sensor params']['height'])
        self.sensor_params_pixel_size_entry.insert(0, self.data['sensor params']['pixel size'])
        
        # Positive mode
        if self.calculate_mode_positive:
            # World coordinates
            self.world_coordinate_x_entry.delete(0, tk.END)
            self.world_coordinate_y_entry.delete(0, tk.END)
            self.world_coordinate_z_entry.delete(0, tk.END)
            
            self.world_coordinate_x_entry.insert(0, self.data['world coordinates']['x'])
            self.world_coordinate_y_entry.insert(0, self.data['world coordinates']['y'])
            self.world_coordinate_z_entry.insert(0, self.data['world coordinates']['z'])
            
            # Camera coordinates
            self.camera_corrdinates_x_entry.config(state='normal')
            self.camera_corrdinates_y_entry.config(state='normal')
            self.camera_corrdinates_z_entry.config(state='normal')
            
            self.camera_corrdinates_x_entry.delete(0, tk.END)
            self.camera_corrdinates_y_entry.delete(0, tk.END)
            self.camera_corrdinates_z_entry.delete(0, tk.END)
            
            self.camera_corrdinates_x_entry.insert(0, self.data['camera coordinates']['x'])
            self.camera_corrdinates_y_entry.insert(0, self.data['camera coordinates']['y'])
            self.camera_corrdinates_z_entry.insert(0, self.data['camera coordinates']['z'])
            
            self.camera_corrdinates_x_entry.config(state='readonly')
            self.camera_corrdinates_y_entry.config(state='readonly')
            self.camera_corrdinates_z_entry.config(state='readonly')
            
            # Pixel coordinates
            self.pixel_coordinate_x_entry.config(state='normal')
            self.pixel_coordinate_y_entry.config(state='normal')
            
            self.pixel_coordinate_x_entry.delete(0, tk.END)
            self.pixel_coordinate_y_entry.delete(0, tk.END)
            
            self.pixel_coordinate_x_entry.insert(0, self.data['pixel coordinates']['x'])
            self.pixel_coordinate_y_entry.insert(0, self.data['pixel coordinates']['y'])
        
            self.pixel_coordinate_x_entry.config(state='readonly')
            self.pixel_coordinate_y_entry.config(state='readonly')
        
        # Reverse mode
        else:
            # World coordinates
            self.world_coordinate_x_entry.config(state='normal')
            self.world_coordinate_y_entry.config(state='normal')
            self.world_coordinate_z_entry.config(state='normal')
            
            self.world_coordinate_x_entry.delete(0, tk.END)
            self.world_coordinate_y_entry.delete(0, tk.END)
            self.world_coordinate_z_entry.delete(0, tk.END)
            
            self.world_coordinate_x_entry.insert(0, self.data['world coordinates']['x'])
            self.world_coordinate_y_entry.insert(0, self.data['world coordinates']['y'])
            self.world_coordinate_z_entry.insert(0, self.data['world coordinates']['z'])
            
            self.world_coordinate_x_entry.config(state='readonly')
            self.world_coordinate_y_entry.config(state='readonly')
            self.world_coordinate_z_entry.config(state='readonly')
            
            # Camera coordinates
            self.camera_corrdinates_x_entry.config(state='normal')
            self.camera_corrdinates_y_entry.config(state='normal')
            self.camera_corrdinates_z_entry.config(state='normal')
            
            self.camera_corrdinates_x_entry.delete(0, tk.END)
            self.camera_corrdinates_y_entry.delete(0, tk.END)
            self.camera_corrdinates_z_entry.delete(0, tk.END)
            
            self.camera_corrdinates_x_entry.insert(0, self.data['camera coordinates']['x'])
            self.camera_corrdinates_y_entry.insert(0, self.data['camera coordinates']['y'])
            self.camera_corrdinates_z_entry.insert(0, self.data['camera coordinates']['z'])
            
            self.camera_corrdinates_x_entry.config(state='readonly')
            self.camera_corrdinates_y_entry.config(state='readonly')
            self.camera_corrdinates_z_entry.config(state='readonly')
            
            # Pixel coordinates
            self.pixel_coordinate_x_entry.delete(0, tk.END)
            self.pixel_coordinate_y_entry.delete(0, tk.END)
            
            self.pixel_coordinate_x_entry.insert(0, self.data['pixel coordinates']['x'])
            self.pixel_coordinate_y_entry.insert(0, self.data['pixel coordinates']['y'])
            
        return
        
    def onclick_button_lock(self):
        self.lock()
        return
    
    def lock(self):
        # Lock camera pose
        self.camera_pose_pitch_entry.config(state='readonly')
        self.camera_pose_yaw_entry.config(state='readonly')
        self.camera_pose_roll_entry.config(state='readonly')
        
        # Lock Fit Coefs
        self.fitting_func_coefs_x5_entry.config(state='readonly')
        self.fitting_func_coefs_x4_entry.config(state='readonly')
        self.fitting_func_coefs_x3_entry.config(state='readonly')
        self.fitting_func_coefs_x2_entry.config(state='readonly')
        self.fitting_func_coefs_x1_entry.config(state='readonly')
        self.fitting_func_coefs_x0_entry.config(state='readonly')
        
        # Lock Fit Coefs Reverse
        self.fitting_func_coefs_reverse_x5_entry.config(state='readonly')
        self.fitting_func_coefs_reverse_x4_entry.config(state='readonly')
        self.fitting_func_coefs_reverse_x3_entry.config(state='readonly')
        self.fitting_func_coefs_reverse_x2_entry.config(state='readonly')
        self.fitting_func_coefs_reverse_x1_entry.config(state='readonly')
        self.fitting_func_coefs_reverse_x0_entry.config(state='readonly')
        
        # Lock Sensor Params
        self.sensor_params_width_entry.config(state='readonly')
        self.sensor_params_height_entry.config(state='readonly')
        self.sensor_params_pixel_size_entry.config(state='readonly')
        
        # Switch button state
        self.unlock_button.config(state='active')
        self.lock_button.config(state='disabled')
        
        return
    
    def onclick_button_unlock(self):
        self.unlock()
        return
        
    def unlock(self):
        # Unlock camera pose
        self.camera_pose_pitch_entry.config(state='normal')
        self.camera_pose_yaw_entry.config(state='normal')
        self.camera_pose_roll_entry.config(state='normal')
        
        # Unlock Fit Coefs
        self.fitting_func_coefs_x5_entry.config(state='normal')
        self.fitting_func_coefs_x4_entry.config(state='normal')
        self.fitting_func_coefs_x3_entry.config(state='normal')
        self.fitting_func_coefs_x2_entry.config(state='normal')
        self.fitting_func_coefs_x1_entry.config(state='normal')
        self.fitting_func_coefs_x0_entry.config(state='normal')
        
        # Unlock Fit Coefs Reverse
        self.fitting_func_coefs_reverse_x5_entry.config(state='normal')
        self.fitting_func_coefs_reverse_x4_entry.config(state='normal')
        self.fitting_func_coefs_reverse_x3_entry.config(state='normal')
        self.fitting_func_coefs_reverse_x2_entry.config(state='normal')
        self.fitting_func_coefs_reverse_x1_entry.config(state='normal')
        self.fitting_func_coefs_reverse_x0_entry.config(state='normal')
        
        # Unlock Sensor Params
        self.sensor_params_width_entry.config(state='normal')
        self.sensor_params_height_entry.config(state='normal')
        self.sensor_params_pixel_size_entry.config(state='normal')
        
        # Switch button state
        self.unlock_button.config(state='disabled')
        self.lock_button.config(state='active')
        
        return
    
    def onclick_menu_button_about(self):
        self.show_about()
    
    def show_about(self):
        self.about_window = tk.Toplevel(self)
        self.about_window.title('About')
        self.about_window.geometry('300x200')
        self.about_window_title_label = tk.Label(self.about_window, text='W2C Transform', font=('Arial', 20))
        self.about_window_title_label.pack()
        
    def _onclose(self):
        self.destroy()
        self.root.deiconify()