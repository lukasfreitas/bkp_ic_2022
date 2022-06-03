import repository.elements_class as elem
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Plotter():

    historic_serie_x = []
    historic_serie_y = []

    def input_value(self, value_or_list_x=None, value_or_list_y=None) -> None:
        '''Add valores a serie historica para criacao o grafico'''

        dict_type = [np.float64, int, float]

        if value_or_list_x is not None:
            if type(value_or_list_x) in dict_type:
                self.historic_serie_x = np.append(arr=self.historic_serie_x, values=value_or_list_x)
				
        if value_or_list_y is not None:
            if type(value_or_list_y) in dict_type:
                self.historic_serie_y = np.append(self.historic_serie_y, value_or_list_y)
    
    def plot(self, c_map = 'viridis', title = 'title', x_label = 'x', y_label = 'y') -> None:
        '''Configurando e plotando o grafico'''

        cmap = mpl.colormaps[c_map] 
        plt.set_cmap(cmap)

        plt.plot(self.historic_serie_x, self.historic_serie_y)

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.show()


class model():

    body_dict       = {}
    actuator_dict   = {}
    joint_dict      = {}

    def generate_bodies(self, sim_obj, model_obj) -> None:

        for body_id in range(0, model_obj.nbody):

            new_body = elem.body(sim_obj, model_obj, body_id)
            self.body_dict.update({new_body.name : new_body})

    def generate_actuators(self, sim_obj, model_obj) -> None:

        for actuator_id in range(0, model_obj.nu):

            new_actuator = elem.actuator(model_obj, sim_obj, actuator_id)
            self.actuator_dict.update({new_actuator.name : new_actuator})

    def generate_joints(self, sim_obj, model_obj) -> None:

        for joint_id in range(0, model_obj.njnt):

            new_joint = elem.joint(sim_obj, model_obj, joint_id)
            self.joint_dict.update({new_joint.name : new_joint})

    def update(self, sim_obj):

        for item_name, item in self.body_dict.items():
            item.update(sim_obj)
        
        for item_name, item in self.actuator_dict.items():
            item.update(sim_obj)

        for item_name, item in self.joint_dict.items():
            item.update(sim_obj)

    def __init__(self, sim_obj, model_obj) -> None:

        self.generate_actuators(sim_obj, model_obj)
        self.generate_bodies(sim_obj, model_obj)
        self.generate_joints(sim_obj, model_obj)

    def infos(self)->None:
        bodies_names_list = []
        joints_names_list = []
        actuator_names_list = []
       
        for name in self.body_dict.keys():
            bodies_names_list.append(name)
        
        for name in self.joint_dict.keys():
            joints_names_list.append(name)
        
        for name in self.actuator_dict.keys():
            actuator_names_list.append(name)

        info = f'''
{50*'*'}INFO:
- Bodies = {bodies_names_list},\n
- Joints = {joints_names_list},\n
- Actuators = {actuator_names_list}
{50*'*'}
        '''

        return info



