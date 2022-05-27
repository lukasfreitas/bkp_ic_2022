from os import path
import sys, mujoco_py, glfw

ROOT_PATH = f"{path.dirname(path.dirname(path.realpath(__file__)))}"

sys.path.append(path.dirname(ROOT_PATH + '/repository'))

from repository import simulation_class

try:
    simulation = simulation_class.simulation(ROOT_PATH + '/model/','furuta', xacro=True)
except FileNotFoundError:
    print("ERROR - MODELO NAO ENCONTRADO")

model  = simulation.generate_model()
motor  = model.actuator_dict['motor']

haste_v = model.body_dict['haste_vertical']
haste_h = model.body_dict['haste_horizontal']

joit_v = model.joint_dict['motor_vertical']

print(model.infos())

if __name__ == "__main__":

    while glfw.init():
        print(joit_v.xaxis[1][0])
        simulation.update(model)
        simulation.add_to_screen('Torque', round(motor.torque[1], 2))
        simulation.add_to_screen('Haste_v angle', round(haste_h.angle(), 2))
        # simulation.add_to_screen('Junta_v angle', joit_v.qvel[1])
        simulation.render_screen()



        motor.set_torque(0.5, simulation.sim)






    


