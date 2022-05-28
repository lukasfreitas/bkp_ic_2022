from os import path
import sys, mujoco_py, glfw

ROOT_PATH = f"{path.dirname(path.dirname(path.realpath(__file__)))}"

sys.path.append(path.dirname(ROOT_PATH + '/repository'))

from repository import simulation_class, model_class

try:
    simulation = simulation_class.simulation(ROOT_PATH + '/model/','furuta', xacro=True)

except FileNotFoundError:
    print("ERROR - MODELO NAO ENCONTRADO")

model  = simulation.generate_model()

print(model.infos())

motor_v  = model.actuator_dict['motor_vertical']
joint_v = model.joint_dict['motor_vertical']
haste_v = model.body_dict['haste_vertical']

joint_h = model.joint_dict['motor']
motor_h  = model.actuator_dict['motor']
haste_h = model.body_dict['haste_horizontal']

def check_haste_angle(sim_obj, haste_h, joint_v, joint_h, step, plotter_v, plotter_h, phase):

    if  phase == 0:
        if joint_v.angle() <= 359:
            plotter_v.input_value(step, joint_v.angle())
            joint_h.lock(sim_obj)
            joint_v.set_linear_vel(sim_obj, 1)
        else:
            phase = 1
    elif phase == 1:  
        if haste_h.angle() <= 359:
            plotter_h.input_value(step, haste_h.angle())
            joint_v.lock(sim_obj)
            joint_h.set_linear_vel(sim_obj, 1)
        else:
            joint_h.lock(sim_obj)
            phase==2
            return False, phase

    return True, phase

if __name__ == "__main__":

    plotter_h = model_class.Plotter()
    plotter_v = model_class.Plotter()

    step_counter = 0
    phase = 0
    simulation.view._paused = True
    while glfw.init():
        
        simulation.update(model)
        simulation.render_screen()

        simulation.add_to_screen('Torque', round(motor_h.torque[1], 2))
        simulation.add_to_screen('Haste_h angle', round(haste_h.angle(), 2))      
        simulation.add_to_screen('Joint_v angle', round(joint_v.angle(), 2))

        # motor_h.set_torque(-1000, simulation.sim)
        # motor_h.set_torque(1000, simulation.sim)
        # motor_v.set_torque(1, simulation.sim)
        
        # simulation.sim.reset()
        
        status, phase = check_haste_angle(simulation.sim, haste_h, joint_v, joint_h, step_counter, plotter_v, plotter_h, phase)
        if status:
            step_counter+=1
        else:
            break
        
    plotter_h.plot(title='Angulo motor',      x_label='Angulo haste_h', y_label='Passsos')
    plotter_v.plot(title='Angulo vertical',   x_label='Angulo haste_v', y_label='Passsos')






    


