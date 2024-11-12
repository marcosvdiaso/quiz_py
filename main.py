import json

escolha_menu = 0
escolha_config = 0
infos_questoes = ["category", "value", "questionPath", "questionText", "option1", "option2", "option3", "option4", "option5", "answer", "explanation", "hint"]

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
                        questao["explanation"] = input("Explicação final da questão para o jogador: ")
                        questao["hint"] = input("Dica para o jogador: ")

                        lista_questoes.append(questao)

                        with open("questoes.json", 'w') as arquivo_q:
                            json.dump(lista_questoes, arquivo_q, indent=1)   

                        escolha_config = 0         
                    
                    case 2:
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
                        
                        escolha_config = 0

                    case 3:
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
                                    while escolhas not in range(1, 13):
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