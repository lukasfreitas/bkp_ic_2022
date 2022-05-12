import config
import glfw
import mujoco_py as mj
from   os        import path

# -- Cor de cada eixo --
#   Vermelho  : eixo X
#   Verde     : eixo Y
#   Azul      : eixo Z

#  print("actuator_trntype", pendulum.actuator_trntype) // R: [0] no internal dynamics
#  print(pendulum.nu)  numero de atuadores presentes no modelo

project_path = f"{path.dirname(path.dirname(path.realpath(__file__)))}"

mode_type = [
    {'name':'sim','model_name':'furuta','motor_index':{'motor_h':0, 'motor_v':1}},
    {'name':'test_h','model_name':'test_axis/furuta_test_h','motor_index':0},
    {'name':'test_v','model_name':'test_axis/furuta_test_v','motor_index':0}
]

mode = mode_type[2]
motor_index = mode['motor_index']

config.xacro(project_path + '/model/', mode['model_name'] )
pendulum = mj.load_model_from_path(project_path + '/model/' + mode['model_name'] + '.xml')


if glfw.init():

    sim         = mj.MjSim(pendulum)
    view        = mj.MjViewer(sim)
    dinamica    = config.dinamica(sim, view, mode)

    if mode['name'] == 'sim':
        dinamica.control(motor_index['motor_v'])
    else:
        dinamica.control(motor_index)

    if mode['name'] == 'sim':
        for i in range(5000):# while True:
            sim.step()
            dinamica.screen()

    elif mode['name'] =='test_h':
        while dinamica.angulo()[0] <= 359:
            sim.step()
            dinamica.screen()

    else:
        for i in range(2000): #rever a haste V
            sim.step()
            dinamica.screen()

    dinamica.plotter.plot(title='Angulo das hastes', x_label='Haste Horizontal', y_label='Haste Vertical')
    dinamica.plotter.log_on_file(project_path + '/log/angulo_v' + f"_{mode['name']}.txt", dinamica.plotter.historic_serie_y)
else :
    print("Could not initialize OpenGL context")