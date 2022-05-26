from os import path
import sys
ROOT_PATH = f"{path.dirname(path.dirname(path.realpath(__file__)))}"

sys.path.append(path.dirname(ROOT_PATH + '/repository'))

from repository import model_class, simulation_class


sim_elements = simulation_class.simulation(ROOT_PATH + '/model/furuta', xacro=True)

model_obj   = sim_elements.model
sim_obj     = sim_elements.sim
model_obj   = sim_elements.view

model = model_class(sim_obj, model_obj)

if __name__ == "__main__":
    print(type(model),dir(model), sep="\n")


