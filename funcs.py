import time, random

def print_questoes(x, category, op1, op2, op3, op4, op5, value, questionText, answer, hint, dicas_usadas, max_dicas, questoes_corretas):
    resposta_usuario = 0
    cont = 1
    opts = [op1, op2, op3, op4, op5]
    eliminados = []
    print(f"Questão {x} | Categoria: {category} | Valor: {value} pontos | Número de dicas restantes: {max_dicas - dicas_usadas}")
    print(f"{questionText}")
    for op in opts:
        print(f"{cont}. {op}")
        cont+=1
        
    resposta_certa = answer
    while resposta_usuario not in range(1,6):
        resposta_usuario = int(input("Insira sua resposta: "))
        if resposta_usuario == resposta_certa:
            questoes_corretas+=1
            if questoes_corretas % 3 == 0 and questoes_corretas > 0:
                dicas_usadas -= 1
            return True, dicas_usadas, questoes_corretas
        elif resposta_usuario == 0:
            if dicas_usadas < max_dicas:
                print("1. Dica textual")
                print("2. Eliminar 2 alternativas erradas")
                print("3. Pular questão")
                while True:
                    try:
                        dica = int(input("Qual dica quer usar? "))
                        if dica not in range(1, 4):
                            print("Digite um número de 1 a 3.")
                        else:
                            break
                    except ValueError:
                        print("Digite um número de 1 a 3.")

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
                        return "pular", dicas_usadas, questoes_corretas
                        
            else:
                print("Já usou todas as dicas.")
        else:
            return False, dicas_usadas, questoes_corretas
        
def timer(tempo_restante, parar_timer):
    while tempo_restante[0] > 0 and not parar_timer.is_set():
        print(f"Tempo restante: {tempo_restante[0]}")
        time.sleep(1)
        tempo_restante[0] -= 1

def ordena_ranking(lista):
    for i in range(len(lista)-1):
        menor = i
        for j in range(i+1, len(lista)):
            if lista[menor]["pontuacao"] < lista[j]["pontuacao"]:
                menor = j
        lista[menor]["pontuacao"], lista[i]["pontuacao"] = lista[i]["pontuacao"], lista[menor]["pontuacao"]
        lista[menor]["nome"], lista[i]["nome"] = lista[i]["nome"], lista[menor]["nome"]

def visualizar_ranking(ranking):
    cont = 0
    while cont <= 9 and cont < len(ranking):
        print(f"{cont+1}º lugar: {ranking[cont]["nome"]} | {ranking[cont]["pontuacao"]} pontos")
        cont+=1

def entrar_ranking(ranking, pont):
    try:
        if ranking[9]["pontuacao"] < pont:
            print("Sua pontuação foi o bastante para entrar no ranking!")
            nome = input(f"Pontuação {pont}. Digite seu nome para salvar sua pontuação: ")
            jogador = {"nome":nome, "pontuacao":pont}
            ranking[9] = jogador
        else:
            print("Sua pontuação não foi o bastante para entrar no ranking.")
    except IndexError:
        print("Sua pontuação foi o bastante para entrar no ranking!")
        nome = input(f"Pontuação {pont}. Digite seu nome para salvar sua pontuação: ")
        jogador = {"nome":nome, "pontuacao":pont}
        ranking.append(jogador)