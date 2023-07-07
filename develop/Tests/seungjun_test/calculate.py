#numba를 이용한 선택정렬 시간 측정

import random as rand
import time
from numba import jit  
array = []

@jit(nopython = True)
def selectionSort(array):
    for i in range(len(array)):
        min_index=i
        for j in range(i+1, len(array)):
            if array[min_index]>array[j]:
                min_index=j
        if min_index!=i:        
            array[i],array[min_index]=array[min_index],array[i]
    return array    
array=rand.sample(range(100000),100000)

begin=time.time()
arr = selectionSort(array)
after=time.time()
elapsed_time=after-begin
    
print(arr)
print("elapsed_time = {:.5f}".format(elapsed_time))