import time, random, json, threading, os

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNÇÕES RELACIONADAS AO JOGO

'''
FUNÇÃO DO MODO DE JOGO QUESTÕES FIXAS
O loop roda até que o número total de questões configurado seja exibido
Soma pontuação sempre que a função "print_questoes" retorna True, soma pontuação pela metade se usar a dica de pular questão e não soma pontuação se errar
No fim do loop, retorna a pontuação
'''
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


'''
FUNÇÃO DO MODO DE JOGO LIMITE DE TEMPO
O loop roda até que o tempo restante seja maior que 0 ou até que o número total de questões configurado tenha sido antigido
Utiliza da biblioteca threading para que o timer e o input do usuário rodem ao mesmo tempo
A variável "tempo restante" é uma variável compartilhada entre essa função e a função timer, onde essa variável determina a pontuação final,
essa variável é uma lista pois, sendo a lista um tipo mutável, as alterações feitas nela durante a execução da função timer, refletem também na função do modo de jogo
A variável "parar_timer" funciona como um interruptor para a função timer, quando ela é definida como "set()" após o fim do loop, o timer finaliza
Sempre que uma questão é errada, o jogador perde 3 segundos do seu tempo
Retorna o tempo restante
'''
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
    cont_tempo.start() # Inicia o timer
    os.system('cls' if os.name == 'nt' else 'clear')                    

    while tempo_restante[0] > 0 and cont_questao <= config_modos["limite_de_tempo"]["questoes"]:
        resposta, dicas_usadas, questoes_corretas = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], "Tempo", questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"], dicas_usadas, max_dicas, questoes_corretas)
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

    parar_timer.set() # Seta o parar_timer, encerrando o timer
    cont_tempo.join() # Encerra o timer
    return tempo_restante[0]

'''
FUNÇÃO DO MODO TENTE NÃO ERRAR
O loop roda até que não tenha passado por todas as questões da lista
Soma pontuação sempre que a função "print_questoes" retorna True
Caso o usuário erre uma questão, o loop se encerra precocemente
Após o fim ou quebra do loop, retorna a pontuação
'''
def modo_tente_nao_errar(config_modos, lista_questoes):
    cont_questao = 1
    pont = 0
    max_dicas = config_modos["tente_nao_errar"]["dicas"]
    dicas_usadas = 0
    questoes_corretas = 0
    questoes_feitas = []
    
    while cont_questao <= len(lista_questoes):
        questao_escolhida = selecionar_questao(lista_questoes, questoes_feitas)
        resposta, dicas_usadas, questoes_corretas = print_questoes(cont_questao, questao_escolhida["category"], questao_escolhida["option1"], questao_escolhida["option2"], questao_escolhida["option3"], questao_escolhida["option4"], questao_escolhida["option5"], 1, questao_escolhida["questionText"], questao_escolhida["answer"], questao_escolhida["hint"], dicas_usadas, max_dicas, questoes_corretas)
        if resposta == True:
            print("Resposta Correta!\n")
            pont += 1
        elif resposta == "pular":
            print("Questão pulada. Sem pontuação.\n")
        else:
            print("Você errou.\n")
            break
        cont_questao+=1

    if cont_questao >= len(lista_questoes):
        print("As questões acabaram. Você venceu o modo Tente não errar.")

    return pont

'''
FUNÇÃO PARA EXIBIÇÃO DAS QUESTÕES + DICAS + VERIFICAÇÃO DA RESPOSTA DO USUÁRIO
Essa função vai sempre retornar 3 valores: a relação da resposta do usuário com a resposta da questão (Certo, errado ou pulou), número atual de dicas usadas
e número de questões acertadas
'''
def print_questoes(x, category, op1, op2, op3, op4, op5, value, questionText, answer, hint, dicas_usadas, max_dicas, questoes_corretas):
    resposta_usuario = 0
    cont = 1
    opts = [op1, op2, op3, op4, op5]
    eliminados = []
    print(f"Questão {x} | Categoria: {category} | Valor: {value} | Número de dicas restantes: {max_dicas - dicas_usadas}")
    print(f"{questionText}")
    for op in opts:
        print(f"{cont}. {op}")
        cont+=1
        
    resposta_certa = answer # Define a resposta certa como o "answer" do arquivo
    while resposta_usuario not in range(1,6):
        while True:
            try:
                resposta_usuario = int(input("Insira sua resposta (1 a 5, ou 0 para dicas): "))
                if resposta_usuario not in range(0, 6):
                    print("Digite 0 (para dicas) ou um número entre 1 e 5 para respostas.")
                else:
                    break
            except ValueError:
                print("Digite 0 (para dicas) ou um número entre 1 e 5 para respostas.")
        if resposta_usuario == resposta_certa: # Se a resposta do usuário estiver correta, retorna True e soma +1 nas questões corretas
            questoes_corretas+=1
            if questoes_corretas % 3 == 0 and questoes_corretas > 0: # A cada 3 questões que o jogador acerta, ele ganha 1 dica nova para usar
                dicas_usadas -= 1
            return True, dicas_usadas, questoes_corretas
        elif resposta_usuario == 0: # Se o usuário digita 0 ele abre o painel de dicas
            if dicas_usadas < max_dicas: # Se tiver dicas sobrando
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
                    case 1: # Printa o "hint" do arquivo e consome uma dica
                        dicas_usadas+=1
                        print(f"{hint}")
                    case 2:
                        cont = 1
                        dicas_usadas+=1 # Consome uma dica
                        for i in range(2): # Sorteia duas opções para serem eliminadas
                            eliminado = random.choice(opts)
                            while eliminado == opts[answer-1] or eliminado in eliminados: # Verifica se a questão sorteada é a correta ou se já foi eliminada, se sim sorteia de novo até ser uma válida
                                eliminado = random.choice(opts)
                            eliminados.append(eliminado) # Adiciona a questão eliminada a lista de eliminados, para que não "elimine" as mesmas que já eliminou

                        for op in opts: # Printa as novas opções
                            if op not in eliminados:
                                print(f"{cont}. {op}")
                            cont+=1
                    case 3: # Consome uma dica e retorna "pular", que dependendo do modo de jogo tem efeitos diferentes
                        dicas_usadas+=1
                        return "pular", dicas_usadas, questoes_corretas
                        
            else: # Se não tiver dicas sobrando
                print("Já usou todas as dicas.")
        else: # Se errou, retorna False
            return False, dicas_usadas, questoes_corretas
        
'''
Função do timer do modo de jogo "limite de tempo"
Enquanto a variável compartilhada "tempo_restante" for maior que 0 e enquanto a variável "interruptor" parar_timer não estiver setada, roda o timer
A cada 1 segundo printa o tempo restante atual e diminui 1 da variável tempo restante
'''
def timer(tempo_restante, parar_timer):
    while tempo_restante[0] > 0 and not parar_timer.is_set():
        # Utiliza \r para printar sempre na mesma linha. Da um espaço após o print, para que dê para o usuário digitar a resposta correta, sem bagunçar muito a visualização
        print(f"\rTempo restante: {tempo_restante[0]}{' ' * 30}", end='') 
        time.sleep(1)
        tempo_restante[0] -= 1
    if tempo_restante[0] == 0:
        print("Seu tempo acabou.")

'''
Função para selecionar questão aleatória
Seleciona uma questão da lista de questões, e verifica se ela está na lista "questoes_feitas", se estiver, sorteia até selecionar uma que não esteja
Após isso adiciona a questão sorteada a lista de questões feitas, para que ela não se repita depois
Retorna a questão sorteada
'''
def selecionar_questao(lista_questoes, questoes_feitas):
    questao = random.choice(lista_questoes)
    while questao in questoes_feitas:
        questao = random.choice(lista_questoes)
    questoes_feitas.append(questao)
    return questao

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNÇÕES CRUD QUESTÕES

'''
Função para criar novas questões
Cria um dicionário vazio, e passa cada uma das chaves como um input para o usuário inserir
Após isso retorna o dicionário "questao"
'''
def criar_questao():
    questao = {}
    print("Digite 0 em \"Categoria\" para retornar.")
    questao["category"] = input("Categoria da questão: ")
    if questao["category"] == "0":
        return 0
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

'''
Função para visualizar todas ou uma questão específica
'''
def visualizar_questao(lista_questoes):
    print(f"Total de questões na lista: {len(lista_questoes)}")
    while True:
        try:
            escolhas = int(input("1. Ver todas as questões.\n2. Ver uma questão específica\n3. Voltar\n"))
            if escolhas not in range(1, 4):
                print("Digite um número entre 1 e 3.")
            else:
                break
        except ValueError:
            print("Digite um número entre 1 e 3.")
    match escolhas:
        case 1: # Caso o usuário tenha escolhido ver todas as questões
            cont = 1
            for questoes in lista_questoes:
                print(f"Questão {cont}:")
                for keys in questoes: 
                    print(keys, end =': ') # Printa chave
                    print(questoes[keys]) # Printa valor da chave
                cont+= 1
                print("---------------------------------------------")
        case 2: # Caso o usuário tenha escolhido ver uma questão específica
            while True:
                try:
                    q = int(input("ID da questão? "))
                    if q < 0:
                        print(f"Digite um número entre 0 e {len(lista_questoes)-1}")
                    else:
                        for keys in lista_questoes[q]:
                            print(keys, end =': ') # Printa a chave
                            print(lista_questoes[q][keys]) # Printa valor da chave
                        break
                except ValueError:
                    print("Digite um número inteiro.")
                except IndexError:
                    print(f"Digite um número entre 0 e {len(lista_questoes)-1}")
        case 3:
            return

    input()

'''
Função para editar questão
Solicita o ID da questão
Então printa uma lista com todas as "keys" do dicionário e um representante númerico
O usuário então digita o número correspondente a chave que quer editar e insere o novo valor
Após isso o usuário tem a opção de editar mais algo da questão ou não
'''
def editar_questao(lista_questoes, infos_questoes):
    cont = 1
    escolhas = 0

    while True:
        try:
            q = int(input("Qual o ID da questão que deseja editar? (Digite -1 para voltar) "))
            if q == -1:
                break
            elif q >= len(lista_questoes) or q < 0:
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
        
'''
Função para deletar questão
Solicita o ID da questão, se for um ID válido, deleta a questão
'''
def deletar_questao(lista_questoes):
    while True:
        try:
            q = int(input("ID da questão? (Digite -1 para voltar)"))
            if q == -1:
                break
            elif q < 0:
                print(f"Os IDs das questões estão entre 0 e {len(lista_questoes)-1}")
            else:
                del lista_questoes[q]
                input("Questão deletada com sucesso.")
                break
        except ValueError:
            print("Digite um número inteiro.")
        except IndexError:
            print(f"Digite um número entre 0 e {len(lista_questoes)-1}")

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNÇÕES CONFIGURAÇÃO DE MODOS DE JOGO
'''
Ambas as funções funcionam da mesma forma, solicitam um valor inteiro ao usuário e atribuem esse valor a chave relacionada ou ao número de questões
ou ao número de dicas.
'''

def config_modos_questoes(questoes, lista_questoes):
    while True:
        try:
            questoes = int(input("Insira o número de questões: "))
            if questoes > len(lista_questoes) or questoes < 1:
                print(f"Digite um valor entre 1 e {len(lista_questoes)}.")
            else:
                input("Número de questões alterado com sucesso.")
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
                input("Número de dicas alterado com sucesso.")
                return dicas
        except ValueError:
            print("Digite um número inteiro válido.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNÇÕES RANKING

'''
Ordena a lista de forma decrescente com base na pontuação
Utiliza do método "Selection Sort"
Itera por toda a lista, selecionando o maior valor, após selecionar o maior, ele troca de posição com o i
E então o loop reinicia, porém a partir de i+1, isso se repete até que todo o ranking esteja organizado
'''
def ordena_ranking(lista):
    for i in range(len(lista)-1):
        maior = i
        for j in range(i+1, len(lista)):
            if lista[maior]["pontuacao"] < lista[j]["pontuacao"]:
                maior = j
        lista[maior]["pontuacao"], lista[i]["pontuacao"] = lista[i]["pontuacao"], lista[maior]["pontuacao"]
        lista[maior]["nome"], lista[i]["nome"] = lista[i]["nome"], lista[maior]["nome"]

'''
Printa até que cont atinja 9 (as 10 primeiras posições), ou caso o ranking tenha menos que 10 nomes, printa até o len(ranking)
'''
def visualizar_ranking(ranking):
    cont = 0
    while cont <= 9 and cont < len(ranking):
        print(f"{cont+1}º lugar: {ranking[cont]["nome"]} | {ranking[cont]["pontuacao"]} pontos")
        cont+=1

'''
Verifica se o usuário pode entrar no ranking
Se a pontuação do usuário for maior que a do 10º colocado, solicita o nome do usuário e ele entra no ranking
Se for menor que a do 10º colocado, ele não entra no ranking
Se der IndexError, então o ranking tem menos que 10 pessoas, logo o usuário entra no ranking
'''
def entrar_ranking(ranking, pont):
    try:
        if ranking[9]["pontuacao"] < pont:
            print("Sua pontuação foi o bastante para entrar no ranking!")
            nome = input(f"Pontuação {pont}. Digite seu nome para salvar sua pontuação: ")
            jogador = {"nome":nome, "pontuacao":pont}
            ranking[9] = jogador
        else:
            print("Sua pontuação não foi o bastante para entrar no ranking.")
            input()
    except IndexError:
        print("Sua pontuação foi o bastante para entrar no ranking!")
        nome = input(f"Pontuação {pont}. Digite seu nome para salvar sua pontuação: ")
        jogador = {"nome":nome, "pontuacao":pont}
        ranking.append(jogador)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
# OUTRAS FUNÇÕES

'''
Função de validação de inteiros
'''
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

'''
Função para carregar arquivos json
'''
def load_json(arquivo):
    with open(arquivo) as x:
        return json.load(x)

'''
Função para sobrescrever arquivos json
''' 
def dump_json(arquivo, variavel):
    with open(arquivo, "w") as x:
        json.dump(variavel, x, indent=1)