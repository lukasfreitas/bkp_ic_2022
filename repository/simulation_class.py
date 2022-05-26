import mujoco_py
from os import system, path

class simulation():
    '''Returns a basic simulation obj'''

    model = None
    sim   = None
    view  = None

    def set_model(self, modelPath, xacro=False):
        '''Returns mj_model instance'''
        print(modelPath)

        if xacro:
            if path.exists(modelPath):
                system(f"xacro  {modelPath}.xacro > {modelPath}.xml")
                return mujoco_py.load_model_from_path(f'{modelPath}.xml')
            else:
                print('Não encontrei o arquivo')
                raise FileNotFoundError
		
        return mujoco_py.load_model_from_path(f'{path}.xml')

    def set_sim(self,model_obj,substeps=1):
        '''Returns mj_sim instance'''

        if isinstance(model_obj, mujoco_py.PyMjModel):
            return mujoco_py.MjSim(model_obj,substeps)
        
        raise TypeError

    def set_view(self, sim_obj):

        if isinstance(sim_obj, mujoco_py.MjSim):
            return mujoco_py.MjViewer(sim_obj)
		
        raise TypeError

    def __init__(self, modelPath, xacro=False) -> None:
        self.model 	= self.set_model(modelPath, xacro=xacro)
        self.sim	= self.set_sim(self.model)
        self.view	= self.set_view(self.sim)

