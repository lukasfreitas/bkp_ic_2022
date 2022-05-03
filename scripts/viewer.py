import config
import glfw
import mujoco_py as mj
from   os        import path,system

# -- Cor de cada eixo --
#   Vermelho  : eixo X
#   Verde     : eixo Y
#   Azul      : eixo Z

#  print("actuator_trntype", pendulum.actuator_trntype) // R: [0] no internal dynamics
#  print(pendulum.nu)  numero de atuadores presentes no modelo

model_folder_path   = f"{path.dirname(path.dirname(path.realpath(__file__)))}/model/"
model_name          = 'furuta'

config.xacro(model_folder_path, model_name)
# print(model_folder_path + model_name + '.xml')
pendulum = mj.load_model_from_path(model_folder_path + model_name + '.xml')

if glfw.init():

    sim         = mj.MjSim(pendulum)
    view        = mj.MjViewer(sim)
    dinamica    = config.dinamica(sim, view)
    dinamica.control()
    
    for i in range(10000):# while True:
        sim.step()
        dinamica.screen()

        

    dinamica.plotter.plot()

else :
    print("Could not initialize OpenGL context")