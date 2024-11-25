import time

def print_questoes(x, category, op1, op2, op3, op4, op5, value, questionText, answer, hint): #adicionar validação
    resposta_usuario = 0
    cont = 1
    opts = [op1, op2, op3, op4, op5]
    print(f"Questão {x} | Categoria: {category} | Valor: {value} pontos")
    print(f"{questionText}")
    for op in opts:
        print(f"{cont}. {op}")
        cont+=1

    resposta_certa = answer
    while resposta_usuario not in range(1,6):
        resposta_usuario = int(input("Insira sua resposta: "))
        if resposta_usuario == resposta_certa:
            return True
        elif resposta_usuario == 0: # configurar maximo de dicas, configurar pular questao, configurar remover 3 repostas erradas
            print(f"{hint}")
        else:
            return False
        
def timer(cont, parar_timer):
    while cont >= 0 and not parar_timer.is_set():
        print(f"Tempo restante: {cont}")
        time.sleep(1)
        cont-=1