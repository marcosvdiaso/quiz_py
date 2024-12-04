import json, os, random, threading
from funcs import *

escolha_menu = 0
infos_questoes = ["category", "value", "questionPath", "questionText", "option1", "option2", "option3", "option4", "option5", "answer", "hint"]

while escolha_menu != 4:
    escolha_config = 0
    escolha_modo = 0
    ranking = load_json("ranking.json")
    
    print('''1. Jogar
2. Configurar
3. Ranking
4. Sair''')

    escolha_menu = validacao_menu(1, 5)
    
    match escolha_menu:
        case 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            lista_questoes = load_json("questoes.json")
            config_modos = load_json("modos_de_jogo.json")

            while escolha_modo != 4:
                questoes_feitas = []
                print("1. Questões Fixas")
                print("2. Limite de Tempo")
                print("3. Tente não errar")
                print("4. Voltar")
                escolha_modo = validacao_menu(1, 5)

                match escolha_modo:
                    case 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        cont_questao = 1
                        pont = 0
                        max_dicas = config_modos["questoes_fixas"]["dicas"]
                        dicas_usadas = 0
                        questoes_corretas = 0

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

                        entrar_ranking(ranking[0], pont)
                        ordena_ranking(ranking[0])
                        dump_json("ranking.json", ranking)

                        escolha_modo = 0
                        escolha_menu = 0
                    case 2:
                        parar_timer = threading.Event()
                        cont_questao = 1
                        pont = 0
                        max_dicas = config_modos["limite_de_tempo"]["dicas"]
                        dicas_usadas = 0
                        tempo = config_modos["limite_de_tempo"]["questoes"] * 10
                        tempo_restante = [tempo]
                        questoes_corretas = 0

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
                        pont = tempo_restante[0]
                        cont_tempo.join()

                        entrar_ranking(ranking[1], pont)
                        ordena_ranking(ranking[1])
                        dump_json("ranking.json", ranking)

                        escolha_modo = 0
                        escolha_menu = 0
                    case 3:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        cont_questao = 1
                        pont = 0
                        max_dicas = config_modos["tente_nao_errar"]["dicas"]
                        dicas_usadas = 0
                        questoes_corretas = 0
                        
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
                        
                        entrar_ranking(ranking[2], pont)
                        ordena_ranking(ranking[2])
                        dump_json("ranking.json", ranking)

                        escolha_modo = 0 
                        escolha_menu = 0
                    case 4:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_menu = 0
        case 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            while escolha_config != 6:
                print("1. Criar nova questão")
                print("2. Visualizar questões")
                print("3. Atualizar uma questão")
                print("4. Excluir uma questão")
                print("5. Configurar modos de jogo")
                print("6. Retornar ao menu inicial")

                escolha_config = validacao_menu(1, 7)

                match escolha_config:
                    case 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json")

                        questao = criar_questao()
                        lista_questoes.append(questao)

                        dump_json("questoes.json", lista_questoes)

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0         
                    
                    case 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json")
                        
                        visualizar_questao(lista_questoes)
                        
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 3:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json")
                        
                        editar_questao(lista_questoes, infos_questoes)
                            
                        dump_json("questoes.json", lista_questoes)
                            
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                    
                    case 4:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json")

                        deletar_questao(lista_questoes)

                        dump_json("questoes.json", lista_questoes)

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 5:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        config_modos = load_json("modos_de_jogo.json")
                        lista_questoes = load_json("questoes.json")

                        print("Qual modo deseja configurar?")
                        print("1. Modo de questões fixas")
                        print("2. Modo de limite de tempo")
                        print("3. Modo tente não errar")
                        print("4. Voltar")
                        escolha_modo = validacao_menu(1, 5)

                        match escolha_modo:
                            case 1:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["questoes_fixas"]["questoes"] = config_modos_questoes(config_modos["questoes_fixas"]["questoes"], lista_questoes)
                                config_modos["questoes_fixas"]["dicas"] = config_modos_dicas(config_modos["questoes_fixas"]["dicas"])
                            case 2:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["limite_de_tempo"]["questoes"] = config_modos_questoes(config_modos["limite_de_tempo"]["questoes"], lista_questoes)
                                config_modos["limite_de_tempo"]["dicas"] = config_modos_dicas(config_modos["limite_de_tempo"]["dicas"])
                            case 3:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["tente_nao_errar"]["dicas"] = config_modos_dicas(config_modos["tente_nao_errar"]["dicas"])
                            case 4:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                escolha_config = 0
                                escolha_modo = 0

                        dump_json("modos_de_jogo.json", config_modos)

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                        escolha_modo = 0

                    case 6:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_menu = 0
        case 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Qual ranking deseja visualizar?")
            print("1. Questões Fixas")
            print("2. Limite de Tempo")
            print("3. Tente não Errar")
            print("4. Voltar")
            escolha_config = validacao_menu(1, 5)

            match escolha_config:
                case 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING MODO DE QUESTÕES FIXAS")
                    visualizar_ranking(ranking[0])
                    input()
                    escolha_config = 0
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING MODO LIMITE DE TEMPO")
                    visualizar_ranking(ranking[1])
                    input()
                    escolha_config = 0
                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING TENTE NÃO ERRAR")
                    visualizar_ranking(ranking[2])
                    input()
                    escolha_config = 0
                case 4:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                    escolha_menu = 0

        case 4:
            escolha_sair = input("Deseja realmente sair? (S/n)").upper()
            if escolha_sair == "N":
                escolha_menu = 0