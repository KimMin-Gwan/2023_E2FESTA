#간단한 계산식 시간 측정

import time
from numba import jit 

m=4.0
v=8.0
	
count=0
result=0.0
begin=time.time()
for i in range(500000):
	result = result + m * v * v
	count=count+1
after=time.time()

elapsed = after- begin

print("걸린시간 : {:.5f}" .format(elapsed))
print("횟수 : {:d}".format( count))
print("결과값 : {:f}".format(result))