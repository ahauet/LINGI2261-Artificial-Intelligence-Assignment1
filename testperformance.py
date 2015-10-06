import copy
import time

number_of_copy = 1000000


start_time = time.time()

dico = {'A' : [[0,0],[0,1]], 'B' : [[1,1], [2,2]], 'C' : [[1,1], [2,2]], 'D' : [[1,1], [2,2]], 'E' : [[1,1], [2,2]]}
for i in range(0, number_of_copy):
    dico2 = copy.copy(dico)

print("---dico took %s seconds ---" % (time.time() - start_time))






start_time = time.time()

list = ['A', 'B', 'C', 'D', 'E']
for i in range(0, number_of_copy):
    list2 = copy.copy(list)

print("---list took %s seconds ---" % (time.time() - start_time))