import time
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "1000"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("Você não tem valor suficiente para saldo, tente novamente!")
        elif valor > 0:
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor))
            print(f"Saque no valor de R${valor} efetuado com sucesso!\n")
            return True
        else:
            print("A sua transação foi cancelada, tente novamente.")
        return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print(f"Depósito no valor de R${valor} efetuado com sucesso!\n")
            return True
        else:
            print("A sua transação foi cancelada, tente novamente.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=5):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == "Saque"])

        if valor > self.limite:
            print("O seu saldo é insuficiente para essa operação.")
        elif numero_saques >= self.limite_saques:
            print("O seu limite de saques diários acabou.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
            Agência: {self.agencia}
            Conta Corrente: {self._numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def validar_escolha(valor_minimo, valor_maximo):
    while True:
        try:
            escolha_usuario = int(input("Escolha uma opção: "))
            if valor_minimo <= escolha_usuario <= valor_maximo:
                return escolha_usuario
            else:
                print("\nOpção inválida, por favor verifique as informações e tente novamente.\n")
        except ValueError:
            print("Entrada inválida, por favor digite um número.")

def buscar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Você não possui conta em nosso Banco, ficaremos felizes se quiser se cadastrar!")
        return
    return cliente.contas[0]

def depositar(usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("Cliente não encontrado, faça um cadastro!\n")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta(usuario)
    if not conta:
        return
    
    usuario.realizar_transacao(conta, transacao)

def sacar(usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("Cliente não encontrado, faça um cadastro!\n")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta(usuario)
    if not conta:
        return
    
    usuario.realizar_transacao(conta, transacao)

def exibir_extrato(usuarios):
    print("\n==============Extrato==============\n")

    cpf = input("Informe seu CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if not usuario:
        print("Cliente não encontrado, faça um cadastro!\n")
        return

    conta = recuperar_conta(usuario)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes

    if not transacoes:
        extrato = "Não foi realizada nenhuma movimentação."
    else:
        extrato = ""
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo atual: R${conta.saldo:.2f}\n")

def criar_nova_conta(numero_conta, usuarios, contas):
    print("\n===========Cadastro de Contas===========\n")

    cpf = input("Informe seu CPF: ")
    cliente = buscar_usuario(cpf, usuarios)

    if not cliente:
        print("Cliente não encontrado, faça um cadastro!\n")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\nNova conta adicionada com sucesso, você pode verificar as contas vinculadas ao seu CPF em (Exibir Contas Cadastradas)\n")

def listar_contas(usuarios):
    print("\n==============Suas Contas==============\n")
    for usuario in usuarios:
        for conta in usuario.contas:
            print(f"CPF: {usuario.cpf}, Agência: {conta.agencia}, Conta: {conta.numero}\n")

def criar_usuario(usuarios):
    print("\n===========Cadastro de Usuário===========\n")

    cpf = input("Informe seu CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe um usuário com este CPF!\n")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento conforme o modelo -> (DD/MM/AAAA): ")
    endereco = input("Informe seu endereço conforme o exemplo -> (Logradouro, Cidade - Sigla do Estado): ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco) 
    
    usuarios.append(cliente)

    print(f"\nSeja bem-vindo {nome}, sua conta foi criada com sucesso. Você já pode utilizar os benefícios.\n")

def menu_pagina_inicial():
    print('''==============Seja bem-vindo ao banco DIO!==============\n
    Menu:
        1 - Cadastrar
        2 - Solicitar Nova Conta
        3 - Exibir Contas Cadastradas
        4 - Depositar
        5 - Sacar
        6 - Exibir Extrato
        7 - Sair
    ''')

def main():
    usuarios = []
    contas = []

    while True:
        menu_pagina_inicial()
        numero_da_operacao = validar_escolha(1, 7)

        if numero_da_operacao == 1:
            criar_usuario(usuarios)
        elif numero_da_operacao == 2:
            numero_da_conta = len(contas) + 1
            criar_nova_conta(numero_da_conta, usuarios, contas)
        elif numero_da_operacao == 3:
            listar_contas(usuarios)
        elif numero_da_operacao == 4:
            depositar(usuarios)
        elif numero_da_operacao == 5:
            sacar(usuarios)
        elif numero_da_operacao == 6:
            exibir_extrato(usuarios)
        elif numero_da_operacao == 7:
            print("Programa finalizado com sucesso!")
            break

main()
