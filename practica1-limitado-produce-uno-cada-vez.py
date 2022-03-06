"""
Alumno: Claudia Casado Poyatos. Práctica 1

En este fichero he implementado otro caso que es cuando los consumidores paran de consumir, es decir, producen 
un número limitado de números N y cuando eso pasa añaden un -1, siguen produciendo de uno en uno y el consumidor 
consume el mínimo de ellos y lo almacena.

"""
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
import random


N = 7     #Cantidad de numeros que se pueden producir
NPROD = 4 #Num de productores
NCONS = 1 #Num de consumidores


def productor(pid, storage, empty, non_empty): #Cada productor genera N números de forma creciente y al terminar genera un -1
    data = random.randint(1,5)
    for n in range(N):
        empty[pid].acquire()
        data += random.randint(1,5)
        print (f"productor {current_process().name} produciendo")
        storage[pid] = data
        print (f"productor {current_process().name} almacenado {data}")
        non_empty[pid].release()   #Avisamos a los non_empty de que añadimos un numero
    print(f"producer {current_process().name} Ha terminado de producir") 
    empty[pid].acquire()
    sleep(2)
    storage[pid] = -1
    non_empty[pid].release()

def consumidor(storage, empty, non_empty):
    for s in non_empty:
        s.acquire()
        sleep(2)
        print (f"consumidor {current_process().name} desalmacenando")
    running = [True for _ in range (NPROD)]
    crecientes = []
    while True in running:
        posibles_minimos = [] #Esto lo hago para que en el mínimo no me coja los -1
        for i in range(NPROD):
            running[i] = storage[i]>=0
            if running[i]:
                posibles_minimos.append(storage[i])
        if posibles_minimos == []:
            break
        data = min(posibles_minimos)
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
    prodlst = [ Process(target = productor,
                        name = f'prod_{i}',
                        args = (i, storage, empty, non_empty))
                for i in range(NPROD) ]

    cons = [ Process(target = consumidor,
                     name = f"cons_",
                     args = (storage, empty, non_empty))]
    
    for p in prodlst + cons:
        p.start()

    for p in prodlst + cons:
        p.join()   
    
if __name__ == '__main__':
    main()