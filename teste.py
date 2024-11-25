import threading
import time
import os

def timer():
    cont = 60
    while cont >= 0:
        print(cont)
        time.sleep(1)
        cont-=1
        os.system('cls' if os.name == 'nt' else 'clear')

def resposta():
    input("Insira sua resposta: ")

func = threading.Thread(target=timer)
func2 = threading.Thread(target=resposta)
func.start()
func2.start()
func.join()
func2.join()