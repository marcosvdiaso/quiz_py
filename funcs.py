import time, random

def print_questoes(x, category, op1, op2, op3, op4, op5, value, questionText, answer, hint, dicas_usadas, max_dicas): #adicionar validação
    resposta_usuario = 0
    cont = 1
    opts = [op1, op2, op3, op4, op5]
    eliminados = []
    print(f"Questão {x} | Categoria: {category} | Valor: {value} pontos")
    print(f"{questionText}")
    for op in opts:
        print(f"{cont}. {op}")
        cont+=1

    resposta_certa = answer
    while resposta_usuario not in range(1,6):
        resposta_usuario = int(input("Insira sua resposta: "))
        if resposta_usuario == resposta_certa:
            return True, dicas_usadas
        elif resposta_usuario == 0: # configurar maximo de dicas, configurar pular questao, configurar remover 3 repostas erradas
            if dicas_usadas < max_dicas: # variavel dicas_usadas so esta funcionando por questao, configurar por modo de jogo todo
                print("1. Dica textual")
                print("2. Eliminar 2 alternativas erradas")
                print("3. Pular questão")
                dica = int(input("Qual dica quer usar? ")) # add validacao

                match dica:
                    case 1:
                        dicas_usadas+=1
                        print(f"{hint}")
                    case 2:
                        cont = 1
                        dicas_usadas+=1
                        for i in range(2):
                            eliminado = random.choice(opts)
                            while eliminado == opts[answer-1] or eliminado in eliminados:
                                eliminado = random.choice(opts)
                            eliminados.append(eliminado)

                        for op in opts:
                            if op not in eliminados:
                                print(f"{cont}. {op}")
                            cont+=1
                    case 3:
                        dicas_usadas+=1
                        return "pular", dicas_usadas
                        
            else:
                print("Já usou todas as dicas.")
        else:
            return False, dicas_usadas
        
def timer(tempo_restante, parar_timer):
    while tempo_restante[0] > 0 and not parar_timer.is_set():
        print(f"Tempo restante: {tempo_restante[0]}")
        time.sleep(1)
        tempo_restante[0] -= 1