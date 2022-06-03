from os import path
from xml.dom import NOT_FOUND_ERR
from repository import sim
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np      

'''
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lucas/.mujoco/mujoco210/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so
'''

ROOT_PATH   = f"{path.dirname(path.realpath(__file__))}"
sys.path.append(path.dirname(ROOT_PATH + '/repository'))

MODEL_PATH  =  f"{ROOT_PATH}/model/"

def plot(x_serie, y_serie, c_map = 'viridis', title = 'title', x_label = 'x', y_label = 'y') -> None:
        '''Configurando e plotando o grafico'''

        cmap = mpl.colormaps[c_map] 
        plt.set_cmap(cmap)

        plt.plot(x_serie, y_serie)

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.show()


class controller():
        B = None
        A = None


        def __init__(self, output,input, nbd=1, nad=2) -> None:
                self.output = output
                self.input  = input

                self.npts = len(self.output)
                self.nbd = nbd
                self.nad = nad

        def ols(self):
                Y = []
                phi = []

                for j in range(max(self.nad,self.nbd)+1, self.npts-1):
                    phirow = []

                    for i in range(self.nad):
                        phirow.append(-self.output[j-i-1])

                    for i in range(self.nbd+1):
                        phirow.append(self.input[j-i-1])

                    Y.append([self.output[j]])
                    phi.append(phirow)

                Y = np.array(Y)
                phi = np.array(phi)
                theta, _, _, _ = np.linalg.lstsq(phi, Y, rcond=None)

                theta = theta.flatten()

                self.B = theta[self.nad:]
                self.A = np.concatenate(([1], theta[:self.nad]))

                # return self.B, self.A
if __name__ == '__main__':

        simulation = sim.sim(MODEL_PATH,'furuta','motor_vertical','motor_vertical','haste_horizontal')

        steps, outputs, inputs = simulation.run(step_limit=20000, render=False) 

        ctrl = controller(outputs, inputs)

        ctrl.ols()
        print('B/A model')
        print(f'B: {ctrl.B}', f'A: {ctrl.A}')

        plot(steps,outputs, x_label='Passos', y_label='Angulo vertical')
        plot(steps,inputs, x_label='Passos', y_label='Torque')




