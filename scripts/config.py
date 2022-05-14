
__doc__ = 'suporte'

from os import path, system
from xml.dom import ValidationErr
import numpy as np
from mujoco_py.generated import const
import matplotlib.pyplot as plt
import matplotlib as mpl


def xacro(model_path, model_name):
	'''Converter o arquivo .xacro para .xml'''
	if path.exists(model_path):
		system(
		    f"xacro  {model_path}{model_name}.xacro > {model_path}{model_name}.xml")
	else:
		print('Não encontrei o arquivo')


class Plotter():
	historic_serie_x = []
	historic_serie_y = []

	def __init__(self) -> None:
		self.historic_serie_x = np.array(self.historic_serie_x, copy=False)
		self.historic_serie_y = np.array(self.historic_serie_y, copy=False)
	
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

		if (len(self.historic_serie_x) > 0) and (len(self.historic_serie_y) > 0):
			plt.plot(self.historic_serie_x, self.historic_serie_y)

		elif (len(self.historic_serie_x) > 0) and (len(self.historic_serie_y) == 0):
			plt.plot(np.arange(0, len(self.historic_serie_x)), self.historic_serie_x)

		elif (len(self.historic_serie_x) == 0) and (len(self.historic_serie_y) > 0):
			plt.plot(np.arange(0, len(self.historic_serie_y)),self.historic_serie_y)

		else:
			return 'series vazias'

		plt.title(title)
		plt.xlabel(x_label)
		plt.ylabel(y_label)

		plt.show()

	def log_on_file(self, file_name, list_or_value) -> None:
		file = open(file_name, "w")

		for value in list_or_value:
			file.write(f'{value}\n')

		file.close() 

class tets_dinamica():
	count = 0
	series_index = {}
	serie = []
	atual = 0
	passada = 0
	erro_serie = []

	def erro_range(self, accuracy, value, interval = 1, delay=1):
		self.count+=1
		
		if (self.count <= delay):
			return True
		else:
			self.erro_serie.append(abs(value -  self.passada))
			mean_erro = sum(self.erro_serie) / float(len(self.erro_serie))

			if (len(self.erro_serie) >= interval):
				print(
				'value',round(value,2),
				'count',self.count,
				'passada', round(self.passada, 2),
				"total",round(sum(self.erro_serie),2),
				'media',round(mean_erro,2),
				'tamanho vetor', len(self.erro_serie),
				sep=' | ')
				if (mean_erro > accuracy):
					return False
				self.erro_serie = []

			return True

	def set_dinamica(self, value, constraint='', index=None):

		resolve = constraint.split(':')
		resolve[1] = float(resolve[1])
		if index is None and resolve[0] == 'range' and self.erro_range(resolve[1], value) :
			
			self.atual = value
			self.passada = self.atual
			self.serie.append(self.atual)

			return value
		else:
			raise ValueError('SET_DINAMICA ERROR')



	

	
class dinamica:
	sim  	= ''
	view 	= ''
	mode    = ''
	phase 	= ''
	angle_h = 0
	angle_v = 0
	torque  = 0
	
	plotter = Plotter()
	test 	= tets_dinamica()

	def __init__(self, sim, view, mode) -> None:
		self.sim 	= sim
		self.view 	= view
		self.phase 	= "inicial"
		self.mode	= mode

	def control(self, motor_index, init_torque=0.5):

		self.torque 					= init_torque
		self.sim.data.ctrl[motor_index]	= self.torque
		

	def angulo(self):
		if self.mode['name'] == 'sim' or self.mode['name'] == 'test_h':
			haste_h_rot_matrix = self.sim.data.get_geom_xmat("haste_horizontal_geom")

			arccos_h_0_2 = np.degrees(np.arccos(haste_h_rot_matrix[0][2]))
			arcsin_h_0_1 = np.degrees(np.arcsin(haste_h_rot_matrix[0][1]))


			if arcsin_h_0_1 >= 0:
				# if self.test.set_dinamica(arccos_h_0_2, constraint='range:5'):
				self.angle_h = arccos_h_0_2
			else :
				# if self.test.set_dinamica(( 180 - (arccos_h_0_2)) + 180, constraint='range:5'):
				self.angle_h = ( 180 - (arccos_h_0_2)) + 180

		if self.mode['name'] == 'sim' or self.mode['name'] == 'test_v':
			haste_v_rot_matrix = self.sim.data.get_geom_xmat("haste_vertical_geom")

			arccos_v_1_2 = np.degrees(np.arccos(haste_v_rot_matrix[1][2]))
			arcsin_v_2_2 = np.degrees(np.arcsin(haste_v_rot_matrix[2][2]))

			if arcsin_v_2_2 >= 0:
				try:
					self.angle_v = self.test.set_dinamica(arccos_v_1_2 + 180, constraint='range:0.5')
				except ValueError:
					return -1
			else :
				try:
					self.angle_v = self.test.set_dinamica( 180 - (arccos_v_1_2), constraint='range:0.5')
				except ValueError:
					return -1
			

		if self.mode['name'] == 'sim':

			self.plotter.input_value(value_or_list_x=self.angle_h, value_or_list_y=self.angle_v)

		elif self.mode['name'] == 'test_h':

			self.plotter.input_value(value_or_list_y=self.angle_h)

		else:

			self.plotter.input_value(value_or_list_y=self.angle_v)

		return (self.angle_h, self.angle_v)
	
	def screen(self):
		
		if self.angulo() == -1:
			raise ValidationErr


		self.view.add_overlay(const.GRID_TOPRIGHT,"Fase",f"{self.phase}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Haste_H Angulo",f"{round(self.angle_h,1):0^5}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Haste_V Angulo",f"{round(self.angle_v,1):0^5}")
		self.view.add_overlay(const.GRID_TOPRIGHT,"Torque",f"{round(self.torque,1):0^4}")

		return self.view.render()

def rot(vector, angle=90, axe=(0,1,0)):
	'''calculo rotacional de um eixo'''
	vector_np = np.array(vector)
	angle_r   = np.radians(angle)

	if   axe == (1,0,0):
		rot_matrix = np.matrix([[1,              0,                 0],
								[0, np.cos(angle_r), -(np.sin(angle_r))],
								[0, np.sin(angle_r),  (np.cos(angle_r))]])
		
	elif axe == (0,1,0):
		rot_matrix = np.matrix([[np.cos(angle_r) , 0, np.sin(angle_r)],
								[0		        , 1, 			 0 ],
								[-np.sin(angle_r), 0, np.cos(angle_r)]])
		print(rot_matrix)
	elif axe == (0,0,1):
		rot_matrix = np.matrix([[np.cos(angle_r) , -np.sin(angle_r),0 ],
								[np.sin(angle_r) ,  np.cos(angle_r),0 ],
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

	
if __name__ == '__main__' :
	...
	# print(rot())
	# print(angle_2_vectors((3,2,1),(1,2,3),result="degrees"))
