import json

escolha_menu = 0
escolha_config = 0

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
            print("Ainda não implementado.")
            escolha_menu = 0
        case 2:
            while escolha_config != 5:
                print("1. Criar nova questão")
                print("2. Visualizar questões")
                print("3. Atualizar uma questão")
                print("4. Excluir uma questão")
                print("5. Retornar ao menu inicial")

                while escolha_config not in range(1, 6):
                    try:
                        escolha_config = int(input("Escolha a opção desejada: "))
                        if escolha_config not in range(1, 6):
                            print("Digite um número de 1 a 5.")
                    except:
                        print("Digite um número de 1 a 5.")

                match escolha_config:
                    case 1:
                        questao = {}

                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)

                        questao["categoria"] = input("Categoria da questão: ")
                        questao["value"] = int(input("Valor númerico para o acerto da questão: "))
                        questao["questionPath"] = input("Caso queiram usar alguma informação multimídia para complementar a questão: ")
                        questao["questionText"] = input("Texto da questão: ")
                        questao["option1"] = input("Texto da opção 1: ")
                        questao["option2"] = input("Texto da opção 2: ")
                        questao["option3"] = input("Texto da opção 3: ")
                        questao["option4"] = input("Texto da opção 4: ")
                        questao["option5"] = input("Texto da opção 5: ")
                        questao["answer"] = int(input("Número da questão correta "))
                        questao["explanation"] = input("Explicação final da questão para o jogador")
                        questao["hint"] = input("Dica para o jogador: ")

                        lista_questoes.append(questao)

                        with open("questoes.json", 'w') as arquivo_q:
                            json.dump(lista_questoes, arquivo_q, indent=1)   

                        escolha_config = 0         
                    
                    case 2:
                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)
                        
                        print(f"Total de questões na lista: {len(lista_questoes)}")
                        escolha_ver = int(input("Deseja ver todas as questões (1) ou apenas uma específica? (2) "))
                        match escolha_ver:
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
                        
                        escolha_config = 0

                    case 3:
                        print("A implementar...")
                        escolha_config = 0
                    
                    case 4:
                        with open("questoes.json") as a:
                            lista_questoes = json.load(a)

                        q = int(input("ID da questão? "))
                        del lista_questoes[q]

                        with open("questoes.json", 'w') as arquivo_q:
                            json.dump(lista_questoes, arquivo_q, indent=1)   

                        escolha_config = 0

                    case 5:
                        escolha_menu = 0
        case 3:
            escolha_sair = input("Deseja realmente sair? (S/n)").upper()
            if escolha_sair == "N":
                escolha_menu = 0