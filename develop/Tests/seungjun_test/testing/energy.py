#numba를 이용한 간단한 계산식 시간 측정

import time
from numba import jit 

m=4.0
v=8.0
count=0
result=0.0
@jit(nopython=True)
def calAccel(result,count):
    for i in range(500000):
        result = result + m * v * v
        count=count+1
    return result,count

begin=time.time()
answer=calAccel(result,count)
after=time.time()
elapsed = after- begin

print("걸린시간 : {:.5f}" .format(elapsed))
print("결과 : {:0}, {:1}".format(answer[0],answer[1]))

