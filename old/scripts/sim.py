'''
1) Encontrar o angulo que a corda faz com o eixo vertical: [ok]

'''

import mujoco_py as mj
import glfw
import config
from os import path
from mujoco_py.generated import const
import numpy as np

model_folder_path   = f"{path.dirname(path.dirname(path.realpath(__file__)))}/model/"
model_name          = 'pendulum'

plane_pos = (0, 0, 0)
v_sphere        = []
v_eixoVertical  = []

config.xacro(model_folder_path, model_name)

pendulum = mj.load_model_from_path((model_folder_path + model_name + '.xml'))

pendulum.opt.viscosity  = 0.1
pendulum.opt.density    = 0.1

pendulum.opt.wind[0]    = 1000
pendulum.opt.wind[1]    = 1000
pendulum.opt.wind[2]    = 0

if glfw.init():

    sim     = mj.MjSim(pendulum)
    view    = mj.MjViewer(sim)
    
    suport_pos      = sim.data.body_xpos[1]
    v_eixoVertical  = np.array(suport_pos - plane_pos)

    while True:
        sim.step()
        view.render()
        
        esphere_pos = sim.data.body_xpos[2]
        v_sphere    = np.array(suport_pos - esphere_pos)

        alpha = np.cos(v_sphere.dot(v_eixoVertical)/(np.linalg.norm(v_eixoVertical)*np.linalg.norm(v_sphere)))

        view.add_overlay(const.GRID_TOPRIGHT,
                         "Posicao da esfera",f" X: {round(esphere_pos[0],2)} Y: {round(esphere_pos[1],2)} Z:{round(esphere_pos[2],2)}")
        view.add_overlay(const.GRID_TOPRIGHT,"Angulo: ",str(alpha))
        #Testar mj_applyFT  para aplicar força em pontos especificos, passando qfrc_applied como ultimo argumento.
        #Testar colocar mjModel.opt.viscosity e mjModel.opt.density para valores positivos
        #Testar colocar mjModel.opt.wind para valoes positivos 

        # sim.data.xfrc_applied[2] = (1000, 1000, 0, 100, 0, 0)
        # sim.data.xfrc_applied[2] = (np.random.randint(-1000,500), np.random.randint(-1000,500), 0, np.random.randint(-1000,500), 0, 0)
else :
    print("Could not initialize OpenGL context")