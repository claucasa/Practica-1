# -*- coding: utf-8 -*-
"""
Alumno:Claudia Casado Poyatos, Práctica 1
En este fichero he implepentado el caso más basico donde tenemos un numero de productores que procucen un número
ilimitado de números de uno en uno y el consumidor consume cuando todos los productores han producido
uno y avisa al productor del que ha consumido el producto para que genere más""


"""
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
import random
from time import sleep

import numpy as np

NPROD = 4 #Num de productores
NCONS = 1 #Num de consumidores


def productor(pid, storage, empty, non_empty): #Esta función hace que cada productor me genere numeros de forma creciente
    data = random.randint(0,5)
    while True:
        empty[pid].acquire()
        data += random.randint(0,5)
        print (f"productor {current_process().name} produciendo")
        storage[pid] = data
        print (f"productor {current_process().name} almacenado {data}")
        non_empty[pid].release()
        
def consumidor(storage, empty, non_empty): #Esta función hace que el consumidor seleccione el número mínimo y los va almacenando de forma creciente
    for s in non_empty:
      s.acquire()
      print (f"consumidor {current_process().name} desalmacenando")
      sleep(2)
    crecientes = []
    while True:
        data = np.amin(storage)
        crecientes.append(data)
        pid = storage[:].index(data)
        empty[pid].release()
        print (f"consumidor {current_process().name} consumiendo {data}")
        non_empty[pid].acquire()
    print(crecientes)
  
def main():
    empty = [BoundedSemaphore(1) for _ in range (NPROD)] 
    non_empty = [Semaphore(0) for _ in range (NPROD)]
    storage = Array('i', NPROD) 
    print("almacen inicial", storage[:])
    prodlst = [Process(target = productor,
                        name = f'prod_{i}',
                        args = (i, storage, empty, non_empty))
                for i in range(NPROD)]
    cons = [Process(target = consumidor,
                     name = f"cons_",
                     args = (storage, empty, non_empty))]
    for p in prodlst + cons:
        p.start()
    for p in prodlst + cons:
        p.join()
           
if __name__ == '__main__':
    main()