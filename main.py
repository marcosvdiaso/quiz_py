#comentariosfuncoes

import json, os, random, threading
from funcs import *

escolha_menu = 0
escolha_config = 0
escolha_modo = 0
infos_questoes = ["category", "value", "questionPath", "questionText", "option1", "option2", "option3", "option4", "option5", "answer", "hint"]

while escolha_menu != 3:
    print('''1. Jogar
2. Configurar
3. Sair''')

    while escolha_menu not in range(1, 4):
        try:
            escolha_menu = int(input("Escolha a opção desejada: "))
            if escolha_menu not in range(1, 4):
                print("Digite um número de 1 a 3.")
        except:
            print("Digite um número de 1 a 3.")
    
    match escolha_menu:
        case 1:
            with open("questoes.json") as a:
                lista_questoes = json.load(a)

            with open("modos_de_jogo.json") as b:
                config_modos = json.load(b)

            print("1. Questões Fixas")
            print("2. Limite de Tempo")
            print("3. Tente não errar")
            while escolha_modo not in range(1, 4):
                try:
                    escolha_modo = int(input("Escolha a opção desejada: "))
                    if escolha_modo not in range(1, 4):
                        print("Digite um número de 1 a 3.")
                except:
                    print("Digite um número de 1 a 3.")

            match escolha_modo:
                case 1:
                    cont_questao = 1
                    pont = 0
                    max_dicas = config_modos["questoes_fixas"]["dicas"] # configurar maximo de dicas, configurar pular questao, configurar remover 3 repostas erradas
                    while cont_questao <= config_modos["questoes_fixas"]["questoes"]: # impedir repetição de questões
                        questao_escolhida = random.choice(lista_questoes)
                        resposta = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"])
                        if resposta == True:
                            print("Resposta Correta!")
                            pont += questao_escolhida["value"]
                        else:
                            print("Resposta errada...")
                        cont_questao+=1

                    input(f"Pontuação {pont}. Sua pontuação é o bastante para entrar no Hall da Fama, para prosseguir insira seu nome: ")
                    escolha_modo = 0 # adicionar jogar novamente
                    escolha_menu = 0
                case 2: # A finalizar
                    parar_timer = threading.Event()
                    cont_questao = 1
                    pont = 0
                    max_dicas = config_modos["limite_de_tempo"]["dicas"]
                    tempo = config_modos["limite_de_tempo"]["questoes"] * 10

                    questao_escolhida = random.choice(lista_questoes)
                    cont_tempo = threading.Thread(target=timer, args=(tempo,parar_timer,))
                    cont_tempo.start()

                    while tempo >= 0 and cont_questao <= config_modos["limite_de_tempo"]["questoes"]:
                        resp = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"])
                        if resp == True:
                            print("Resposta Correta!")
                            questao_escolhida = random.choice(lista_questoes)
                            cont_questao+=1
                        else:
                            print("Resposta errada, tente novamente.")

                    parar_timer.set()
                    cont_tempo.join()

                    if tempo > 0:
                        pont = tempo

                    input(f"Pontuação {pont}. Sua pontuação é o bastante para entrar no Hall da Fama, para prosseguir insira seu nome: ")
                    escolha_modo = 0 # adicionar jogar novamente
                    escolha_menu = 0
                case 3:
                    cont_questao = 1
                    pont = 0
                    max_dicas = config_modos["tente_não_errar"]["dicas"] # configurar maximo de dicas, configurar pular questao, configurar remover 3 repostas erradas
                    while cont_questao <= len(lista_questoes): # impedir repetição de questões
                        questao_escolhida = random.choice(lista_questoes)
                        resposta = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], questao_escolhida["value"], questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"])
                        if resposta == True:
                            print("Resposta Correta!")
                            pont += questao_escolhida["value"]
                        else:
                            print("Você errou.")
                            break
                        cont_questao+=1

                    if cont_questao >= len(lista_questoes):
                        print("As questões acabaram. Você venceu o modo Tente não errar.")
                    input(f"Pontuação {pont}. Sua pontuação é o bastante para entrar no Hall da Fama, para prosseguir insira seu nome: ")
                    escolha_modo = 0 # adicionar jogar novamente
                    escolha_menu = 0
                case 4:
                    escolha_modo = 0 # adicionar jogar novamente
                    escolha_menu = 0
        case 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            while escolha_config != 5:
                print("1. Criar nova questão")
                print("2. Visualizar questões")
                print("3. Atualizar uma questão")
                print("4. Excluir uma questão")
                print("5. Configurar modos de jogo")
                print("6. Retornar ao menu inicial")

                while escolha_config not in range(1, 7):
                    try:
                        escolha_config = int(input("Escolha a opção desejada: "))
                        if escolha_config not in range(1, 7):
                            print("Digite um número de 1 a 6.")
                    except:
                        print("Digite um número de 1 a 5.")

                match escolha_config:
                    case 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        questao = {}

                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)

                        questao["category"] = input("Categoria da questão: ")
                        questao["value"] = int(input("Valor númerico para o acerto da questão: "))
                        questao["questionPath"] = input("Caso queiram usar alguma informação multimídia para complementar a questão: ")
                        questao["questionText"] = input("Texto da questão: ")
                        questao["option1"] = input("Texto da opção 1: ")
                        questao["option2"] = input("Texto da opção 2: ")
                        questao["option3"] = input("Texto da opção 3: ")
                        questao["option4"] = input("Texto da opção 4: ")
                        questao["option5"] = input("Texto da opção 5: ")
                        questao["answer"] = int(input("Número da questão correta: "))
                        questao["hint"] = input("Dica para o jogador: ")

                        lista_questoes.append(questao)

                        with open("questoes.json", 'w') as arquivo_q:
                            json.dump(lista_questoes, arquivo_q, indent=1)   

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0         
                    
                    case 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)
                        
                        print(f"Total de questões na lista: {len(lista_questoes)}")
                        escolhas = int(input("Deseja ver todas as questões (1) ou apenas uma específica? (2) "))
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
                                q = int(input("ID da questão? "))
                                for keys in lista_questoes[q]:
                                    print(keys, end =': ')
                                    print(lista_questoes[q][keys])

                        input()
                        
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 3:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)
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
                                            lista_questoes[q][infos_questoes[escolhas-1]] = input(f"Digite o novo {infos_questoes[escolhas-1]}: ")
                                            while escolhas not in ["S", "N"]:
                                                escolhas = input("Deseja editar mais algo? (S/n)").upper()
                                            if escolhas == "N":
                                                break
                                        except:
                                            print("Digite um número inteiro válido.")    
                            except:
                                print("Digite um número inteiro referente ao ID de uma questão.")
                                
                            if escolhas == "N":
                                    break
                            
                        with open("questoes.json", 'w') as arquivo_q:
                                json.dump(lista_questoes, arquivo_q, indent=1) 
                            
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                    
                    case 4:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)

                        q = int(input("ID da questão? "))
                        del lista_questoes[q]

                        with open("questoes.json", 'w') as arquivo_q:
                            json.dump(lista_questoes, arquivo_q, indent=1)   

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 5:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        with open("modos_de_jogo.json") as a:
                            config_modos = json.load(a)
                        with open("questoes.json") as b:
                            lista_questoes = json.load(b)

                        print("Qual modo deseja configurar?")
                        print("1. Modo de questões fixas")
                        print("2. Modo de limite de tempo")
                        print("3. Modo tente não errar")
                        print("4. Voltar")
                        while escolha_modo not in range(1, 5):
                            try:
                                escolha_modo = int(input("Escolha a opção desejada: "))
                                if escolha_modo not in range(1, 5):
                                    print("Digite um número de 1 a 4.")
                            except:
                                print("Digite um número de 1 a 3.")

                        # validações
                        match escolha_modo:
                            case 1:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["questoes_fixas"]["questoes"] = int(input("Insira o número de questões: "))
                                config_modos["questoes_fixas"]["dicas"] = int(input("Insira o número de dicas: "))
                            case 2:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["limite_de_tempo"]["questoes"] = int(input("Insira o número de questões: "))
                                config_modos["limite_de_tempo"]["dicas"] = int(input("Insira o número de dicas: "))
                            case 3:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["tente_nao_errar"]["dicas"] = int(input("Insira o número de dicas: "))
                            case 4:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                escolha_config = 0
                                escolha_modo = 0

                        with open("modos_de_jogo.json", 'w') as arquivo_m:
                            json.dump(config_modos, arquivo_m, indent=1)  

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                        escolha_modo = 0

                    case 6:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_menu = 0
        case 3:
            escolha_sair = input("Deseja realmente sair? (S/n)").upper()
            if escolha_sair == "N":
                escolha_menu = 0