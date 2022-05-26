import repository.elements_class as elem

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

            new_actuator = elem.actuator(sim_obj, model_obj, actuator_id)
            self.actuator_dict.update({new_actuator.name : new_actuator})

    def generate_joints(self, sim_obj, model_obj) -> None:

        for joint_id in range(0, model_obj.njnt):

            new_joint = elem.joint(sim_obj, joint_id)
            self.joint_dict.update({new_joint.name : new_joint})

    def update(self):

        for item_name, item in self.body_dict.items():
            item.update()
        
        for item_name, item in self.actuator_dict.items():
            item.update()

        for item_name, item in self.joint_dict.items():
            item.update()

    def __init__(self, sim_obj, model_obj) -> None:

        self.generate_actuators(sim_obj, model_obj)
        self.generate_bodies(sim_obj, model_obj)
        self.generate_joints(sim_obj, model_obj)



