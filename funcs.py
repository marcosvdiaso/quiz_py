import time, random, json, threading, os

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
        while True:
            try:
                resposta_usuario = int(input("Insira sua resposta: "))
                break
            except ValueError:
                print("Digite 0 (para dicas) ou um número entre 1 e 5 para respostas.")
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
        print(f"\rTempo restante: {tempo_restante[0]}{' ' * 10}", end='')
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

def validacao_menu(x, y):
    while True:
        try:
            escolha = int(input("Escolha a opção desejada: "))
            if escolha not in range(x, y):
                print(f"Digite um número de {x} a {y-1}.")
            else:
                return escolha
        except ValueError:
            print(f"Digite um número de {x} a {y-1}.")

def selecionar_questao(lista_questoes, questoes_feitas):
    questao = random.choice(lista_questoes)
    while questao in questoes_feitas:
        questao = random.choice(lista_questoes)
    questoes_feitas.append(questao)
    return questao

def load_json(arquivo):
    with open(arquivo) as x:
        return json.load(x)
    
def dump_json(arquivo, variavel):
    with open(arquivo, "w") as x:
        json.dump(variavel, x, indent=1)

def config_modos_questoes(questoes, lista_questoes):
    while True:
        try:
            questoes = int(input("Insira o número de questões: "))
            if questoes > len(lista_questoes) or questoes < 1:
                print(f"Digite um valor entre 1 e {len(lista_questoes)}.")
            else:
                return questoes
        except ValueError:
            print("Digite um número inteiro válido.")

def config_modos_dicas(dicas):
    while True:
        try:
            dicas = int(input("Insira o número de dicas: "))
            if dicas < 0:
                print("Digite um número inteiro válido.")
            else:
                return dicas
        except ValueError:
            print("Digite um número inteiro válido.")

def criar_questao():
    questao = {}
    questao["category"] = input("Categoria da questão: ")
    while True:
        try:
            questao["value"] = int(input("Valor númerico para o acerto da questão: "))
            if questao["value"] < 0:
                print("Digite um número inteiro.")
            else:
                break
        except:
            print("Digite um número inteiro.")
    questao["questionPath"] = input("Caso queiram usar alguma informação multimídia para complementar a questão: ")
    questao["questionText"] = input("Texto da questão: ")
    questao["option1"] = input("Texto da opção 1: ")
    questao["option2"] = input("Texto da opção 2: ")
    questao["option3"] = input("Texto da opção 3: ")
    questao["option4"] = input("Texto da opção 4: ")
    questao["option5"] = input("Texto da opção 5: ")
    while True:
        try:
            questao["answer"] = int(input("Número da questão correta: "))
            if questao["answer"] not in range(1, 6):
                print("Digite um número entre 1 e 5")
            else:
                break
        except:
            print("Digite um número entre 1 e 5")
    questao["hint"] = input("Dica para o jogador: ")
    return questao

def visualizar_questao(lista_questoes):
    print(f"Total de questões na lista: {len(lista_questoes)}")
    while True:
        try:
            escolhas = int(input("Deseja ver todas as questões (1) ou apenas uma específica? (2) "))
            if escolhas not in range(1, 3):
                print("Digite 1 ou 2.")
            else:
                break
        except ValueError:
            print("Digite 1 ou 2.")
    match escolhas:
        case 1:
            cont = 1
            for questoes in lista_questoes:
                print(f"Questão {cont}:")
                for keys in questoes:
                    print(keys, end =': ')
                    print(questoes[keys])
                cont+= 1
                print("---------------------------------------------")
        case 2:
            while True:
                try:
                    q = int(input("ID da questão? "))
                    if q < 0:
                        print(f"Digite um número entre 0 e {len(lista_questoes)-1}")
                    else:
                        for keys in lista_questoes[q]:
                            print(keys, end =': ')
                            print(lista_questoes[q][keys])
                        break
                except ValueError:
                    print("Digite um número inteiro.")
                except IndexError:
                    print(f"Digite um número entre 0 e {len(lista_questoes)-1}")

    input()

def editar_questao(lista_questoes, infos_questoes):
    cont = 1
    escolhas = 0

    while True:
        try:
            q = int(input("Qual o ID da questão que deseja editar? "))
            if q >= len(lista_questoes) or q < 0:
                print("Não existe questão com esse ID.")
            else:
                for item in infos_questoes:
                    print(f"{cont}. {item}")
                    cont+=1
                while escolhas not in range(1, 12):
                    try:
                        escolhas = int(input("Digite o número correspondente a informação que deseja editar: "))
                        if infos_questoes[escolhas-1] == "value":
                            while True:
                                try:
                                    lista_questoes[q][infos_questoes[escolhas-1]] = int(input(f"Digite o novo {infos_questoes[escolhas-1]}: "))
                                    if lista_questoes[q][infos_questoes[escolhas-1]] < 0:
                                        print("Digite um número inteiro.")  
                                    else:
                                        break
                                except:
                                    print("Digite um número inteiro.")
                        elif infos_questoes[escolhas-1] == "answer":
                            while True:
                                try:
                                    lista_questoes[q][infos_questoes[escolhas-1]] = int(input(f"Digite o novo {infos_questoes[escolhas-1]}: "))
                                    if lista_questoes[q][infos_questoes[escolhas-1]] not in range(1, 6):
                                        print("Digite um número entre 1 e 5")
                                    else:
                                        break
                                except:
                                    print("Digite um número entre 1 e 5")
                        else:
                            lista_questoes[q][infos_questoes[escolhas-1]] = input(f"Digite o novo {infos_questoes[escolhas-1]}: ")
                        while escolhas not in ["S", "N"]:
                            escolhas = input("Deseja editar mais algo? (S/n)").upper()
                        if escolhas == "N":
                            break
                    except ValueError:
                        print("Digite um número inteiro válido.")    
        except ValueError:
            print("Digite um número inteiro referente ao ID de uma questão.")
            
        if escolhas == "N":
                break
        
def deletar_questao(lista_questoes):
    while True:
        try:
            q = int(input("ID da questão? "))
            if q < 0:
                print(f"Digite um número entre 0 e {len(lista_questoes)-1}")
            else:
                del lista_questoes[q]
                break
        except ValueError:
            print("Digite um número inteiro.")
        except IndexError:
            print(f"Digite um número entre 0 e {len(lista_questoes)-1}")

def modo_questoes_fixas(config_modos, lista_questoes):
    cont_questao = 1
    pont = 0
    max_dicas = config_modos["questoes_fixas"]["dicas"]
    dicas_usadas = 0
    questoes_corretas = 0
    questoes_feitas = []

    while cont_questao <= config_modos["questoes_fixas"]["questoes"]:
        questao_escolhida = selecionar_questao(lista_questoes, questoes_feitas)
        resposta, dicas_usadas, questoes_corretas = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"], dicas_usadas, max_dicas, questoes_corretas)
        if resposta == True:
            print("Resposta Correta!\n")
            pont += questao_escolhida["value"]
        elif resposta == "pular":
            print("Questão pulada. Pontuação recebida reduzida.\n")
            pont += (questao_escolhida["value"]//2)
        else:
            print("Resposta errada. Sem pontuação.\n")
        cont_questao+=1

    return pont

def modo_limite_de_tempo(config_modos, lista_questoes):
    parar_timer = threading.Event()
    cont_questao = 1
    max_dicas = config_modos["limite_de_tempo"]["dicas"]
    dicas_usadas = 0
    tempo = config_modos["limite_de_tempo"]["questoes"] * 10
    tempo_restante = [tempo]
    questoes_corretas = 0
    questoes_feitas = []

    questao_escolhida = random.choice(lista_questoes)
    questoes_feitas.append(questao_escolhida)

    cont_tempo = threading.Thread(target=timer, args=(tempo_restante,parar_timer,))
    cont_tempo.start()    
    os.system('cls' if os.name == 'nt' else 'clear')                    

    while tempo_restante[0] > 0 and cont_questao <= config_modos["limite_de_tempo"]["questoes"]:
        resposta, dicas_usadas, questoes_corretas = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"], dicas_usadas, max_dicas, questoes_corretas)
        if resposta == True:
            print("Resposta Correta!\n")
            questao_escolhida = selecionar_questao(lista_questoes, questoes_feitas)
            cont_questao+=1
        elif resposta == "pular":
            print("Questão pulada. Sem pontuação.\n")
            cont_questao+=1
        else:
            print("Resposta errada, perdeu 3 segundos.\n")
            tempo_restante[0] -= 3

    parar_timer.set()
    cont_tempo.join()
    return tempo_restante[0]

def modo_tente_nao_errar(config_modos, lista_questoes):
    cont_questao = 1
    pont = 0
    max_dicas = config_modos["tente_nao_errar"]["dicas"]
    dicas_usadas = 0
    questoes_corretas = 0
    questoes_feitas = []
    
    while cont_questao <= len(lista_questoes):
        questao_escolhida = selecionar_questao(lista_questoes, questoes_feitas)
        resposta, dicas_usadas, questoes_corretas = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"], dicas_usadas, max_dicas, questoes_corretas)
        if resposta == True:
            print("Resposta Correta!\n")
            pont += questao_escolhida["value"]
        elif resposta == "pular":
            print("Questão pulada. Sem pontuação.\n")
        else:
            print("Você errou.\n")
            break
        cont_questao+=1

    if cont_questao >= len(lista_questoes):
        print("As questões acabaram. Você venceu o modo Tente não errar.")

    return pont