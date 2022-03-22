from cmath import sqrt
from   os        import path,system
import numpy as np
import mujoco_py as mj

from os import path
from mujoco_py.generated import const



def exportLib():
	system("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lucas/.mujoco/mujoco210/bin")
	system("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia")

def xacro(model_path, model_name):

	if path.exists(model_path): 
		system(f"xacro  {model_path}{model_name}.xacro > {model_path}{model_name}.xml")
		# print(f"xacro  {model_path}{model_name}.xacro > {model_path}{model_name}.xml")
	else:
		print('Não encontrei o arquivo')


def rot(vector, angle=90, axe=(0,1,0)):

	vector_np = np.array(vector)
	angleR    = np.radians(angle)

	if   axe == (1,0,0):
		rot_matrix = np.matrix([[1,              0,                 0],
								[0, np.cos(angleR), -(np.sin(angleR))],
								[0, np.sin(angleR),  (np.cos(angleR))]])
		
	elif axe == (0,1,0):
		rot_matrix = np.matrix([[np.cos(angleR) , 0, np.sin(angleR)],
								[0		        , 1, 			 0 ],
								[-np.sin(angleR), 0, np.cos(angleR)]])
		print(rot_matrix)
	elif axe == (0,0,1):
		rot_matrix = np.matrix([[np.cos(angleR) , -np.sin(angleR),0 ],
								[np.sin(angleR) ,  np.cos(angleR),0 ],
								[0              , 		        0,1 ]])
		
	else :
		print("Eixo invalido")

	rot_vector = rot_matrix.dot(vector_np)

	return rot_vector.A1

def angle_bw2_vectors (v1, v2, result="radians"):

	inner_product = v1.dot(v2)
	modules_dot   = np.linalg.norm(v1) * np.linalg.norm(v2)
	

	if result == "radians":
		return np.arccos(inner_product/modules_dot)

	elif result == "degrees":
		
		return np.degrees(np.arccos(round(float(inner_product/modules_dot),3)))

	else:
		print("Erro on [result karg]")


class dinamica:
	sim  	= ''
	view 	= ''
	phase 	= ''
	angle_h = 0
	angle_v = 0
	torque  = 0

	def __init__(self, sim, view) -> None:
		self.sim 	= sim
		self.view 	= view
		self.phase 	= "inicial"

	def control(self, init_torque=0.5):
		self.torque = init_torque
		self.sim.data.ctrl[0] = self.torque

	def angulo(self):
		haste_h_rot_matrix = self.sim.data.get_geom_xmat("haste_horizontal_geom")
		self.angle_h = np.degrees(np.arccos(haste_h_rot_matrix[0][2]))

		haste_v_rot_matrix = self.sim.data.get_geom_xmat("haste_vertical_geom")
		self.angle_v = np.degrees(np.arccos(haste_v_rot_matrix[0][2]))

		
		
		print(self.sim.data.geom_xmat.shape)
	
	

		return (self.angle_h, self.angle_v)
	
	def screen(self):
		self.angulo()

		self.view.add_overlay(const.GRID_TOPRIGHT,"Fase",f"{self.phase}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Haste_H Angulo",f"{round(self.angle_h,1):0^5}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Haste_V Angulo",f"{round(self.angle_v,1):0^5}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Torque",f"{round(self.torque,1):0^4}")

		return self.view.render()



if __name__ == '__main__' :
	...
	# print(rot())
	# print(angle_2_vectors((3,2,1),(1,2,3),result="degrees"))
