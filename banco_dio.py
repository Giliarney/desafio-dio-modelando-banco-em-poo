import time

class Cliente:
    def __init__(self, nome, sobrenome, idade, cpf, email, senha):
        self.nome = nome
        self.sobrenome = sobrenome 
        self.idade = idade
        self.cpf = cpf
        self.email = email
        self.senha = senha

class BancoDIO:
    def __init__(self):
        self._saldo = 0.0
        self.AGENCIA = "067-8"
        self.numero_conta = 1000
        self.lista_usuarios = []
        self.extrato = []

    def cadastrar(self):
        nome = input("Insira seu nome: ")
        sobrenome = input("Insira seu sobrenome: ")
        idade = int(input("Insira sua idade: "))
        cpf = input("Insira seu CPF: ")
        email = input("Insira seu e-mail: ")
        senha = input("Insira sua senha: ")
        
        novo_usuario = Cliente(nome, sobrenome, idade, cpf, email, senha)
        nome_usuario = f"{nome} {sobrenome}"
        agencia_usuario = self.AGENCIA
        conta_usuario = self.numero_conta

        usuario_cadastrado = {
            "nome_usuario": nome_usuario,
            "idade": idade,
            "cpf": cpf,
            "email": email,
            "senha": senha,
            "agencia": agencia_usuario,
            "conta": conta_usuario
        }

        self.lista_usuarios.append(usuario_cadastrado)
        self.numero_conta += 1

        print("Cadastro realizado com sucesso!\n")

    def logar(self): 
        if self.lista_usuarios == []:
            print("Realize um cadastro para realizar o login.")
        else:
            numero_agencia = input("Informe sua agência: ")
            numero_conta = int(input("Informe sua conta: "))
            senha_usuario = input("Informe sua senha: ")
        
        for usuario in self.lista_usuarios:
            if usuario["agencia"] == numero_agencia and usuario["conta"] == numero_conta and usuario["senha"] == senha_usuario:
                print(f"Login efetuado com sucesso!")
                time.sleep(2)
                self.pagina_inicial_banco(usuario)
            else:
                print("Verifique as informações fornecidas e tente novamente.")
                return
            
    
    @staticmethod
    def pagina_inicial_login():
        print("""
        ================== Seja bem-vindo ao Banco DIO! ==================
            
                                Menu de Opções:
                                --------------
                                1 - Login
                                2 - Cadastrar
                                --------------
        """)

    def pagina_inicial_banco(self, usuario):
        print(f"""
        ================== Seja bem-vindo {usuario["nome_usuario"]} ao Banco DIO! ==================
            
                                Menu de Opções:
                                --------------
                                1 - Depositar
                                2 - Sacar
                                3 - Exibir Extrato
                                4 - Exibir Informações da Conta
                                5 - Sair
                                --------------
        """)
        self.menu_banco(usuario)

    def menu_banco(self, usuario):
        while True:
            escolha = int(input("Selecione uma opção: "))
            if escolha == 1:
                self.depositar()
            elif escolha == 2:
                self.sacar()
            elif escolha == 3:
                self.exibir_extrato()
            elif escolha == 4:
                self.exibir_informacoes_conta(usuario)
            elif escolha == 5:
                print("Obrigado por usar o Banco DIO!")
                break
            else:
                print("Escolha uma opção válida.")
                
    def depositar(self):
        valor_deposito = float(input("Por favor informe o valor do depósito: "))
        self._saldo += valor_deposito
        self.extrato.append(f"Depósito no valor de R${valor_deposito:.2f}")
        print(f"Depósito no valor de R${valor_deposito:.2f} realizado com sucesso!")

    def sacar(self):
        valor_saque = float(input("Por favor informe o valor do saque: "))
        if valor_saque <= self._saldo:
            self._saldo -= valor_saque
            self.extrato.append(f"Saque no valor de R${valor_saque:.2f}")
            print(f"Saque no valor de R${valor_saque:.2f} realizado com sucesso!")
        else:
            print("Operação cancelada! Saldo insuficiente.")

    def exibir_extrato(self):
        if self.extrato:
            for transacao in self.extrato:
                print(transacao)
        else:
            print("Nenhuma transação realizada.")
        print(f"Seu saldo atual é de: R${self._saldo:.2f}")

    def exibir_informacoes_conta(self, usuario):
        for chave, valor in usuario.items():
            print(f"{chave}: {valor}")

def validar_escolha():
    banco = BancoDIO()
    while True:
        BancoDIO.pagina_inicial_login()
        escolha_pagina_login = int(input("Selecione uma opção: "))
        if escolha_pagina_login == 1:
            banco.logar()
            break
        elif escolha_pagina_login == 2:
            banco.cadastrar()
            break
        else:
            print("Escolha uma opção válida.")

validar_escolha()
