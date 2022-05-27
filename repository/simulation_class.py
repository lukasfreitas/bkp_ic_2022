from re import sub
import mujoco_py
from mujoco_py.generated import const

from os import system, path

from repository.model_class import model

class simulation():
    '''Returns a basic simulation obj'''

    model = None
    sim   = None
    view  = None
    screen_info = {}

    def set_model(self, modelPath, model_name, xacro=False):
        '''Returns mj_model instance'''

        if xacro:
            if path.exists(modelPath):
                system(f"xacro  {modelPath}{model_name}.xacro > {modelPath}{model_name}.xml")
                return mujoco_py.load_model_from_path(f'{modelPath}{model_name}.xml')
            else:
                print('Não encontrei o arquivo')
                raise FileNotFoundError
		
        return mujoco_py.load_model_from_path(f'{path}.xml')

    def set_sim(self, model_obj, substeps=1):
        '''Returns mj_sim instance'''

        if isinstance(model_obj, mujoco_py.cymj.PyMjModel):
            return mujoco_py.MjSim(model_obj, nsubsteps=substeps)
        
        raise TypeError

    def set_view(self, sim_obj):

        if isinstance(sim_obj, mujoco_py.MjSim):
            return mujoco_py.MjViewer(sim_obj)
		
        raise TypeError

    def __init__(self, modelPath, model_name,  xacro=False) -> None:
        self.model 	= self.set_model(modelPath, model_name, xacro=xacro)
        self.sim	= self.set_sim(self.model)
        self.view	= self.set_view(self.sim)

    def generate_model(self) -> None:
        return model(self.sim, self.model)

    def add_to_screen(self, text, value):
        self.screen_info[text] = value
    
    def render_screen(self) -> None:
        for txt, value in self.screen_info.items():
            self.view.add_overlay(const.GRID_TOPRIGHT,f"{txt}",f"{value}")
        self.view.render()

    def update(self, model) -> None:
        self.sim.step()
        
        model.update(self.sim)


