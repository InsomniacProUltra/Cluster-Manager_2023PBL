##  
import platform
import numpy as np

##  preparation
##  distribute the data
parallel_n=4
hostname=platform.node()
random_numbers=np.load('random_numbers.npy')
i=1
data = []
for number in random_numbers:
    if (i == int(hostname)):
        data.append(number)
    if(i == parallel_n):
        i = 1
    else:
        i = i + 1

##  process the data
array = np.array(data)
sum = np.sum(array)
average = np.mean(array)
max_value = np.max(array)
min_value = np.min(array)
standard_deviation = np.std(array)

##  print the result in terminal 
print(f'container:  container4parallelprocessing{hostname}')
print(f'sum:{sum}') 
print(f'average:{average}')
print(f'max_value:{max_value}')
print(f'min_value:{min_value}')
print(f'standard deviation:{standard_deviation}')
print('\n')

##  save the result as txt in volume
filepath=f'result{hostname}.txt'
try:
    file = open(filepath, "w")
    file.write(f'container:container4parallelprocessing{hostname}\n')
    file.write(f'sum:{sum}\n')
    file.write(f'average:{average}\n')
    file.write(f'max_value:{max_value}\n')
    file.write(f'min_value:{min_value}\n')
    file.write(f'standard deviation:{standard_deviation}\n')
    file.close()   
except FileNotFoundError:
    print("FileNotFound!")
except IOError:
    print("IOError relating file occured!")


    
