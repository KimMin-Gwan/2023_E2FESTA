#PATH 수정 필요

import ctypes

PATH='C:/Users/IT/Desktop/test/sort/x64/Debug/sort.dll'
c_module=ctypes.cdll.LoadLibrary(PATH)


print(c_module)

cal=c_module.calAccel

cal.argtypes=(ctypes.c_double, ctypes.c_double)
cal.restype= ctypes.c_double


answer=cal(4.0, 8.0)

print(answer)

