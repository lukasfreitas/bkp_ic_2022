from xml.dom import ValidationErr
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
'''
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lucas/.mujoco/mujoco210/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so
'''
project_path = f"{path.dirname(path.dirname(path.realpath(__file__)))}"

mode_type = [
    {'name':'sim','model_name':'furuta','motor_index':{'motor_h':0, 'motor_v':1},'angulo':'angulo_h angulo_v'},
    {'name':'test_h','model_name':'test_axis/furuta_test_h','motor_index':0,'angulo':'angulo_h'},
    {'name':'test_v','model_name':'test_axis/furuta_test_v','motor_index':0,'angulo':'angulo_h'}
]

mode = mode_type[0]
motor_index = mode['motor_index']

config.xacro(project_path + '/model/', mode['model_name'] )
pendulum = mj.load_model_from_path(project_path + '/model/' + mode['model_name'] + '.xml')

# pendulum.opt.viscosity  = 0.1
# pendulum.opt.density    = 0.1

# pendulum.opt.wind[0]    = 1000
# pendulum.opt.wind[1]    = 1000
# pendulum.opt.wind[2]    = 0


print(pendulum.nu)


# print((pendulum.geom_size))
haste_v_radius = pendulum.geom_size[3][0]
haste_v_lenght = pendulum.geom_size[3][1]
if glfw.init():
# if False:

    sim         = mj.MjSim(pendulum,nsubsteps=1)

    # for method in dir(sim.data.qfrc_actuator[0]):
    #     print(method, end='\n')
    
    view        = mj.MjViewer(sim)
    dinamica    = config.dinamica(sim, view, mode)

    
    
    if mode['name'] == 'sim':
        dinamica.control(motor_index['motor_h'])
    else:
        dinamica.control(motor_index)

    if mode['name'] == 'sim':
        for i in range(3000):# while True:
            sim.step()

            print(pendulum.nbody)
            try:
                dinamica.screen()
            except ValidationErr:
                print("ERRO ANGULO")
                break

    elif mode['name'] =='test_h':
        while dinamica.angulo()[0] <= 359:
            sim.step()
            dinamica.screen()

    else:
        for i in range(2000): #rever a haste V
            sim.step()
            dinamica.screen()

    dinamica.plotter.plot(title='Angulo das hastes', x_label='Haste Horizontal', y_label='Haste Vertical')
    if mode['name'] == 'sim':
        dinamica.plotter.log_on_file(project_path + f"/log/angulo_h" + f"_{mode['name']}.txt", dinamica.plotter.historic_serie_x)
        dinamica.plotter.log_on_file(project_path + f"/log/angulo_v" + f"_{mode['name']}.txt", dinamica.plotter.historic_serie_y)
    else:
        dinamica.plotter.log_on_file(project_path + f"/log/{mode['angulo']}" + f"_{mode['name']}.txt", dinamica.plotter.historic_serie_y)
else :
    print("Could not initialize OpenGL context")