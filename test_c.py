from ctypes import CDLL

so_file = "/home/lucas/utfpr/ic/repo/bkp_ic_2022/c_functions/c_mujoco"

c_mujoco = CDLL(so_file)
c_mujoco.mj_local2Global(1,2,3,4,5)
print(dir(c_mujoco))