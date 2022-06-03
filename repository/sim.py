from http.client import TOO_MANY_REQUESTS
from os import path
import sys, mujoco_py, glfw

from repository import simulation_class, model_class


class sim():
    sim_obj     = None
    model_obj   = None
    step        = 0
    torque      = 0

    historic_serie_x = None
    historic_serie_y = None

    historic_actuator = None

    _actuator_name  = None
    _joint_name     = None
    _haste_name     = None

    def __init__(self, path_to_model, model_name, actuator_name, joint_name, haste_name, xacro_mode=True) -> None:

        try:
            self.sim_obj = simulation_class.simulation(path_to_model, model_name, xacro=xacro_mode)

        except FileNotFoundError:
            print(f"ERROR - MODELO NAO ENCONTRADO EM -> {path_to_model}")

        self.model_obj = self.sim_obj.generate_model()
        self.historic_serie_x = []
        self.historic_serie_y = []
        self.historic_actuator = []

        self._actuator_name = actuator_name
        self._joint_name    = joint_name
        self._haste_name    = haste_name

    def input_series(self, value_y, torque) -> None:
        self.historic_serie_x.append(self.step)
        self.historic_actuator.append(torque)
        self.historic_serie_y.append(value_y)

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

    def run(self,  step_limit, constraint=None, render=False):

        motor = self.model_obj.actuator_dict[self._actuator_name]
        joint = self.model_obj.joint_dict[self._joint_name]
        base_haste = self.model_obj.body_dict[self._haste_name]

        while glfw.init():

            if constraint is None:
                motor.set_torque(0.5, self.sim_obj.sim)
                while self.step <= step_limit:
                    self.sim_obj.update(self.model_obj)
                    
                    if(render):
                        self.sim_obj.render_screen()
                        self.sim_obj.add_to_screen('Torque', round(motor.torque[1], 2))
                        self.sim_obj.add_to_screen('Angulo base', round(base_haste.angle(), 2))      
                        self.sim_obj.add_to_screen('Angulo vertical', round(joint.angle(), 2))
                    
                    self.input_series(joint.angle(), motor.torque[1])
                    self.step+=1

                    motor.set_torque(0, self.sim_obj.sim)
            
            return self.historic_serie_x, self.historic_serie_y, self.historic_actuator
            
