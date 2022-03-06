"""
Alumno: Claudia Casado Poyatos. Práctica 1


En este fichero hago el caso definitivo que es cuando los productores pueden producir más de un número en su turno
(como mucho K numeros), producen un número finito de veces N, y cuando no pueden producir más producen un -1
y el consumidor consume una vez que hayan producido todos los productores

"""





from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Manager
from time import sleep
import random

N = 4 # Cantidad de productos que puede fabricar cada productor 
K = 2 # Cantidad de procuctos que puede tener generados el productor a la vez
NPROD = 3 

def add_data(storage, pid, data, mutex): #He creado una función auxiliar para generar los datos de forma creciente
    mutex.acquire()
    try:
        storage.append(pid*1000 + data) #Hago esa multiplicación para poder saber que productor lo produce
        sleep(1)
    finally:
        mutex.release()

def productor(storage, pid, empty, non_empty, mutex): #mi función productor que llama a add_data para producir
    data = random.randint(0,5)
    for n in range(N):
        empty[pid].acquire()
        data += random.randint(0,5)
        print (f"productor {current_process().name} produciendo")
        add_data(storage, pid, data, mutex)
        print (f"productor {current_process().name} almacenado {data}")
        non_empty[pid].release()   #Avisamos a los non_empty de que añadimos un numero
    print(f"producer {current_process().name} Ha terminado de producir") 
    empty[pid].acquire()
    sleep(1)
    storage.append(-1)      #Añade el -1 una vez no puede producir más
    non_empty[pid].release()
    
def consumidor(storage, empty, non_empty, mutex): #Me consume el mínimo de los elementos del almacen
    for s in non_empty:
        s.acquire()
    print (f"consumidor {current_process().name} desalmacenando")
    sleep(1)
    crecientes = []
    while len(crecientes) < NPROD * N: #Es mi límite para saber que ha consumido todos
        posibles_minimos = []
        lista_pid = []
        for i in range(len(storage)):
            if storage[i] >= 0:       #Para que me coja solo los positivos
                posibles_minimos.append(storage[i] % 1000)
                lista_pid.append(storage[i]//1000)
        if posibles_minimos == []:
            break
        data = min(posibles_minimos)
        pid = lista_pid[posibles_minimos.index(data)]
        data_remove= data + pid*1000
        storage.remove(data_remove) #Borro el dato consumido del almacen
        crecientes.append(data)
        empty[pid].release()
        sleep(1)
        print (f"consumidor {current_process().name} consumiendo {data}")
        non_empty[pid].acquire() 
    print(crecientes)

def main():
    manager = Manager()
    storage = manager.list()
    non_empty = [Semaphore(0) for _ in range (NPROD)]
    empty = [BoundedSemaphore(K) for _ in range (NPROD)]
    mutex = Lock()
    prodlst = [Process(target=productor,
                        name=f'prod_{i}',
                        args=(storage, i, empty, non_empty, mutex))
                for i in range(NPROD)]
    cons = [ Process(target=consumidor,
                      name=f"cons_",
                      args=(storage, empty, non_empty, mutex))]
    for p in prodlst + cons:
        p.start()
    for p in prodlst + cons:
        p.join()

if __name__ == '__main__':
    main()