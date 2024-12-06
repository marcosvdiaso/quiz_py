import os
from funcs import *

escolha_menu = 0
infos_questoes = ["category", "value", "questionPath", "questionText", "option1", "option2", "option3", "option4", "option5", "answer", "hint"]

while escolha_menu != 4:
    escolha_config = 0
    escolha_modo = 0
    ranking = load_json("ranking.json") # Carrega o ranking.json para a variável de ranking
    
    print('''1. Jogar
2. Configurar
3. Ranking
4. Sair''')

    escolha_menu = validacao_menu(1, 5) # Menu inicial
    
    match escolha_menu:
        case 1: # Tela de jogo
            os.system('cls' if os.name == 'nt' else 'clear')
            lista_questoes = load_json("questoes.json") # Carrega a lista de questões para a variável
            config_modos = load_json("modos_de_jogo.json") # Carrega a configuração dos modos de jogo para a variável

            while escolha_modo != 4:
                print("1. Questões Fixas")
                print("2. Limite de Tempo")
                print("3. Tente não errar")
                print("4. Voltar")
                escolha_modo = validacao_menu(1, 5) # Menu de escolha de modo

                match escolha_modo:
                    case 1: # Questões fixas
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                        pont = modo_questoes_fixas(config_modos, lista_questoes) # Chama a função do modo de jogo, e retorna o valor final a variável pont

                        entrar_ranking(ranking[0], pont) # Verifica se a pontuação é o bastante para entrar no ranking
                        ordena_ranking(ranking[0]) # Organiza o ranking
                        dump_json("ranking.json", ranking) # Dump no novo ranking
                        os.system('cls' if os.name == 'nt' else 'clear')

                        escolha_modo = 0
                        escolha_menu = 0
                    case 2: # Limite de tempo
                        pont = modo_limite_de_tempo(config_modos, lista_questoes) # Chama a função do modo de jogo, e retorna o valor final a variável pont

                        entrar_ranking(ranking[1], pont) # Verifica se a pontuação é o bastante para entrar no ranking
                        ordena_ranking(ranking[1]) # Organiza o ranking
                        dump_json("ranking.json", ranking) # Dump no novo ranking
                        os.system('cls' if os.name == 'nt' else 'clear')

                        escolha_modo = 0
                        escolha_menu = 0
                    case 3: # Tente não errar
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                        pont = modo_tente_nao_errar(config_modos, lista_questoes) # Chama a função do modo de jogo, e retorna o valor final a variável pont
                        
                        entrar_ranking(ranking[2], pont) # Verifica se a pontuação é o bastante para entrar no ranking
                        ordena_ranking(ranking[2]) # Organiza o ranking
                        dump_json("ranking.json", ranking) # Dump no novo ranking
                        os.system('cls' if os.name == 'nt' else 'clear')

                        escolha_modo = 0 
                        escolha_menu = 0
                    case 4: # Voltar
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_menu = 0
        case 2: # Tela de configuração
            os.system('cls' if os.name == 'nt' else 'clear')
            while escolha_config != 6:
                print("1. Criar nova questão")
                print("2. Visualizar questões")
                print("3. Atualizar uma questão")
                print("4. Excluir uma questão")
                print("5. Configurar modos de jogo")
                print("6. Retornar ao menu inicial")

                escolha_config = validacao_menu(1, 7) # Menu de configuração

                match escolha_config:
                    case 1: # Criação de questões
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json") # Carrega o arquivo de questoes para a variavel

                        questao = criar_questao() # Chama a função criar questão e atribui o valor a variavel questao
                        if questao != 0:
                            lista_questoes.append(questao) # Adiciona a nova questao à variável

                            dump_json("questoes.json", lista_questoes) # Da dump na nova variável para o arquivo

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0         
                    
                    case 2: # Visualização de questões
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json") # Carrega o arquivo de questoes para a variavel
                        
                        visualizar_questao(lista_questoes) # Chama a função visualizar questao
                        
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 3: # Edição de questões
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json") # Carrega o arquivo de questoes para a variavel
                        
                        editar_questao(lista_questoes, infos_questoes) # Chama a função editar questao, as edições já alteram diretamente na lista_questoes
                            
                        dump_json("questoes.json", lista_questoes) # Da dump na nova lista_questoes para o arquivo
                            
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                    
                    case 4: # Deletar questões
                        os.system('cls' if os.name == 'nt' else 'clear')
                        lista_questoes = load_json("questoes.json") # Carrega o arquivo de questoes para a variavel

                        deletar_questao(lista_questoes) # Chama a função para deletar uma questão, já alterando a lista_questoes

                        dump_json("questoes.json", lista_questoes) # Da dump na nova lista_questoes para o arquivo

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0

                    case 5: # Configuração de modos de jogo
                        os.system('cls' if os.name == 'nt' else 'clear')
                        config_modos = load_json("modos_de_jogo.json") # Carrega o arquivo de configurações para a variavel
                        lista_questoes = load_json("questoes.json") # Carrega o arquivo de questoes para a variavel

                        print("Qual modo deseja configurar?")
                        print("1. Modo de questões fixas")
                        print("2. Modo de limite de tempo")
                        print("3. Modo tente não errar")
                        print("4. Voltar")
                        escolha_modo = validacao_menu(1, 5) # Menu de escolha

                        match escolha_modo:
                            # Em cada um dos cases chama as funções relacionadas aos fatores editáveis (dicas, e em alguns modos, questões)
                            # As funções já retornam os valores diretamente para as keys especificas dentro do dicionário
                            case 1: # Editar modo de questões fixas
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["questoes_fixas"]["questoes"] = config_modos_questoes(config_modos["questoes_fixas"]["questoes"], lista_questoes)
                                config_modos["questoes_fixas"]["dicas"] = config_modos_dicas(config_modos["questoes_fixas"]["dicas"])
                            case 2: # Editar modo limite de tempo
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["limite_de_tempo"]["questoes"] = config_modos_questoes(config_modos["limite_de_tempo"]["questoes"], lista_questoes)
                                config_modos["limite_de_tempo"]["dicas"] = config_modos_dicas(config_modos["limite_de_tempo"]["dicas"])
                            case 3: # Editar modo tente não errar
                                os.system('cls' if os.name == 'nt' else 'clear')
                                config_modos["tente_nao_errar"]["dicas"] = config_modos_dicas(config_modos["tente_nao_errar"]["dicas"])
                            case 4: # Voltar
                                os.system('cls' if os.name == 'nt' else 'clear')
                                escolha_config = 0
                                escolha_modo = 0

                        dump_json("modos_de_jogo.json", config_modos) # Dump no novo config_modos para o arquivo

                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_config = 0
                        escolha_modo = 0

                    case 6: # Voltar
                        os.system('cls' if os.name == 'nt' else 'clear')
                        escolha_menu = 0
        case 3: # Tela de exibição dos rankings
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Qual ranking deseja visualizar?")
            print("1. Questões Fixas")
            print("2. Limite de Tempo")
            print("3. Tente não Errar")
            print("4. Voltar")
            escolha_config = validacao_menu(1, 5) # Usuário decide qual ranking quer visualizar

            match escolha_config:
                case 1: # Ranking questões fixas
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING MODO DE QUESTÕES FIXAS")
                    visualizar_ranking(ranking[0]) # Chama a função visualizar_ranking no index 0 da matriz ranking, que a lista do modo de jogo questões fixas 
                    input()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 2: # Ranking limite de tempo
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING MODO LIMITE DE TEMPO")
                    visualizar_ranking(ranking[1]) # Chama a função visualizar_ranking no index 1 da matriz ranking, que a lista do modo de jogo limite de tempo 
                    input()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 3: # Ranking tente não errar
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("RANKING TENTE NÃO ERRAR")
                    visualizar_ranking(ranking[2]) # Chama a função visualizar_ranking no index 2 da matriz ranking, que a lista do modo de jogo tente não errar
                    input()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                case 4: # Voltar
                    os.system('cls' if os.name == 'nt' else 'clear')
                    escolha_config = 0
                    escolha_menu = 0
        case 4: # Encerrar o programa
            escolha_sair = input("Deseja realmente sair? (N para voltar) ").upper()
            if escolha_sair == "N":
                escolha_menu = 0
                os.system('cls' if os.name == 'nt' else 'clear')