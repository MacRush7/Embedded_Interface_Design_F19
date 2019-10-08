# importing the multiprocessing module 
import multiprocessing
import time
import os
  
def print_cube(num): 
    """ 
    function to print cube of given num 
    """
    os.system("taskset -p 0x22 %d" % os.getpid())
    while True:
        print("Cube: {}".format(num * num * num))
        print("my id is: {}".format(os.getpid()))
        time.sleep(2)
  
def print_square(num): 
    """ 
    function to print square of given num 
    """
    os.system("taskset -p 0x44 %d" % os.getpid())
    while True:
        print("Square: {}".format(num * num))
        print("my id is: {}".format(os.getpid()))
        time.sleep(2)
  
if __name__ == "__main__": 
    # creating processes 
    p1 = multiprocessing.Process(target=print_square, args=(10, )) 
    p2 = multiprocessing.Process(target=print_cube, args=(10, )) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
    print("Done!") 