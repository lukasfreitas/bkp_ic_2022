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
test_h_model_name     = 'test_axis/furuta_test_h'
test_v_model_name     = 'test_axis/furuta_test_v'

mode_type = ['sim','test_h','test_v']
mode = mode_type[0]

if mode == mode_type[0]:

    config.xacro(model_folder_path, model_name)
    pendulum = mj.load_model_from_path(model_folder_path + model_name + '.xml')

elif mode == mode_type[1]:

    config.xacro(model_folder_path, test_h_model_name)
    pendulum = mj.load_model_from_path(model_folder_path + test_h_model_name + '.xml')

else:

    config.xacro(model_folder_path, test_v_model_name)
    pendulum = mj.load_model_from_path(model_folder_path + test_v_model_name + '.xml')

if glfw.init():

    sim         = mj.MjSim(pendulum)
    view        = mj.MjViewer(sim)
    dinamica    = config.dinamica(sim, view, mode)
    dinamica.control()

    if mode == 'sim':
        for i in range(10000):# while True:
            sim.step()
            dinamica.screen()

    elif mode =='test_h':
        while dinamica.angulo()[0] <= 359:
            sim.step()
            dinamica.screen()

    else:
        while dinamica.angulo()[1] >= 89: #rever a haste V
            sim.step()
            dinamica.screen()

    dinamica.plotter.plot(title='Angulo das hastes', x_label='Haste Horizontal', y_label='Haste Vertical')

else :
    print("Could not initialize OpenGL context")