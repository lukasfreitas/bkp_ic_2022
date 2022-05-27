import numpy as np

class body():   
    name = ''
    id          = None
    parent_id   = None
    xpos 	    = None  # Cartesian position of body frame
    xmat 	    = None 	# Cartesian orientation of body frame 
    ximat 	    = None 	# Cartesian orientation of body inertia 
    xvelp  	    = None  # Positional velocity in world frame 
    xvelr  	    = None  # Potational velocity in world frame    

    def __init__(self, sim_obj, model_obj, obj_id) -> None:  

        self.name  =  model_obj.body_id2name(obj_id)   

        if isinstance(self.name, str):  

            self.id         = obj_id
            self.parent_id  = model_obj.body_parentid[self.id]

            self.ximat 	    = [sim_obj.data.get_body_ximat(self.name)]
            self.xmat	    = [sim_obj.data.get_body_xmat(self.name)]
            self.xpos	    = [sim_obj.data.get_body_xpos(self.name)]
            self.xvelp	    = [sim_obj.data.get_body_xvelp(self.name)]
            self.xvelr	    = [sim_obj.data.get_body_xvelr(self.name)] 

            self.ximat.append(self.ximat)
            self.xmat.append(self.xmat)
            self.xpos.append(self.xpos)
            self.xvelp.append(self.xvelp)
            self.xvelr.append(self.xvelr)
        else:   
            raise TypeError

    def angle(self):

        rot_matrix = self.xmat[1][0]

        arccos_0_2 = np.degrees(np.arccos(rot_matrix[0][2]))
        arcsin_0_1 = np.degrees(np.arcsin(rot_matrix[0][1]))
        
        if arcsin_0_1 >= 0:
            # if self.test.set_dinamica(arccos_0_2, constraint='range:5'):
            return arccos_0_2
        else :
			# if self.test.set_dinamica(( 180 - (arccos_0_2)) + 180, constraint='range:5'):
            return ( 180 - (arccos_0_2)) + 180

    def update(self, sim_obj) -> None:
        self.xpos[1]    = [sim_obj.data.get_body_xpos(self.name)]
        self.xmat[1]    = [sim_obj.data.get_body_xmat(self.name)]
        self.ximat[1]   = [sim_obj.data.get_body_ximat(self.name)]
        self.xvelp[1]   = [sim_obj.data.get_body_xvelp(self.name)]
        self.xvelr[1]   = [sim_obj.data.get_body_xvelr(self.name)]

class actuator():
    id		= None
    name 	= None
    torque 	= None

    def __init__(self, model_obj, sim_obj, actuator_id) -> None:
        self.id 	= actuator_id

        if isinstance(self.id, int): 

            self.name	= model_obj.actuator_id2name(self.id)
            self.torque	= [sim_obj.data.qfrc_actuator[self.id]]

            self.torque.append(self.torque)
            
    def set_torque(self, torque, sim_obj) -> None:
        self.torque[1] = torque
        sim_obj.data.ctrl[self.id] = self.torque[1]
    
    def update(self, sim_obj)->None:
        self.torque[1] = sim_obj.data.qfrc_actuator[self.id]

class joint():

    name    = ''
    id      = None
    qpos    = None
    qvel    = None
    xaxis   = None

    def __init__(self, sim_obj, model_obj, joint_id) -> None:

        self.id = joint_id
        self.name  =  model_obj.joint_id2name(self.id) 

        self.qpos   = [sim_obj.data.get_joint_qpos(self.name)]
        self.qvel   = [sim_obj.data.get_joint_qvel(self.name)]
        self.xaxis  = [sim_obj.data.get_joint_xaxis(self.name)]

        self.qpos.append(self.qpos)
        self.qvel.append(self.qvel)
        self.xaxis.append(self.xaxis)

    def update(self, sim_obj) -> None:
    
        self.qpos[1]   = [sim_obj.data.get_joint_qpos(self.name)]
        self.qvel[1]   = [sim_obj.data.get_joint_qvel(self.name)]
        self.xaxis[1]  = [sim_obj.data.get_joint_xaxis(self.name)]
        
		
            