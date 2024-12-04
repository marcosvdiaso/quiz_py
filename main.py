import os
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
                print("1. Questões Fixas")
                print("2. Limite de Tempo")
                print("3. Tente não errar")
                print("4. Voltar")
                escolha_modo = validacao_menu(1, 5)

                match escolha_modo:
                    case 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                        pont = modo_questoes_fixas(config_modos, lista_questoes)

                        entrar_ranking(ranking[0], pont)
                        ordena_ranking(ranking[0])
                        dump_json("ranking.json", ranking)
                        os.system('cls' if os.name == 'nt' else 'clear')

                        escolha_modo = 0
                        escolha_menu = 0
                    case 2:
                        pont = modo_limite_de_tempo(config_modos, lista_questoes)

                        entrar_ranking(ranking[1], pont)
                        ordena_ranking(ranking[1])
                        dump_json("ranking.json", ranking)
                        os.system('cls' if os.name == 'nt' else 'clear')

                        escolha_modo = 0
                        escolha_menu = 0
                    case 3:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                        pont = modo_tente_nao_errar(config_modos, lista_questoes)
                        
                        entrar_ranking(ranking[2], pont)
                        ordena_ranking(ranking[2])
                        dump_json("ranking.json", ranking)
                        os.system('cls' if os.name == 'nt' else 'clear')

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
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING MODO LIMITE DE TEMPO")
                    visualizar_ranking(ranking[1])
                    input()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING TENTE NÃO ERRAR")
                    visualizar_ranking(ranking[2])
                    input()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 4:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                    escolha_menu = 0

        case 4:
            escolha_sair = input("Deseja realmente sair? (S/n)").upper()
            if escolha_sair == "N":
                escolha_menu = 0