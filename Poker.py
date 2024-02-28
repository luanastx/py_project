
import random

class Carta:
    def __init__(self, numero, naipe):
        self.numero = numero
        self.naipe = naipe

    def __repr__(self):
        return f'"{self.numero}" de "{self.naipe}"'

naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']
valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Dama', 'Rei', 'As']

def criar_baralho():
    baralho = [Carta(valor, naipe) for naipe in naipes for valor in valores]
    return baralho

def embaralhar_baralho(baralho):
    random.shuffle(baralho)

def distribuir_cartas(baralho, num_jogadores, num_cartas_por_jogador):
    maos = []
    for _ in range(num_jogadores):
        mao = [baralho.pop() for _ in range(num_cartas_por_jogador)]
        maos.append(mao)
    return maos

def trocar_cartas(mao, baralho):
    print("Sua mão atual é:", mao)

    while True:
        cartas_para_trocar = input("Digite os valores das cartas que deseja trocar (separados por vírgula): ").split(",")
        try:
            nova_mao = []
            for carta in mao:
                if carta.numero in cartas_para_trocar:
                    nova_mao.append(baralho.pop())
                else:
                    nova_mao.append(carta)
            break
        except ValueError:
            print("Por favor, digite apenas valores válidos correspondentes aos ranks das cartas!")

    return nova_mao

def determinar_tipo_de_mao(mao):
    valores_cartas = [carta.numero for carta in mao]
    naipes_cartas = [carta.naipe for carta in mao]

    if all(valor in valores_cartas for valor in ['10', 'Valete', 'Dama', 'Rei', 'As']) and len(set(naipes_cartas)) == 1:
        return "Royal Flush"

    for i in range(len(valores) - 4):
        if all(valor in valores_cartas for valor in valores[i:i+5]) and len(set(naipes_cartas)) == 1:
            return "Straight Flush"

    for valor in valores_cartas:
        if valores_cartas.count(valor) == 4:
            return "Quadra"

    tem_trio = False
    tem_par = False
    for valor in valores_cartas:
        if valores_cartas.count(valor) == 3:
            tem_trio = True
        elif valores_cartas.count(valor) == 2:
            tem_par = True
    if tem_trio and tem_par:
        return "Full House"

    if len(set(naipes_cartas)) == 1:
        return "Flush"

    for i in range(len(valores) - 4):
        if all(valor in valores_cartas for valor in valores[i:i+5]):
            return "Straight"

    for valor in valores_cartas:
        if valores_cartas.count(valor) == 3:
            return "Trinca"

    pares = [valor for valor in set(valores_cartas) if valores_cartas.count(valor) == 2]
    if len(pares) == 2:
        return "Dois Pares"

    for valor in valores_cartas:
        if valores_cartas.count(valor) == 2:
            return "Par"

    return "Carta Alta"

def determinar_vencedor(maos):
    valores_cartas_maos = []

    for mao in maos:
        valores_cartas = [valores.index(carta.numero) for carta in mao]
        maior_valor = max(valores_cartas)
        valores_cartas_maos.append(maior_valor)

    if len(set(valores_cartas_maos)) == 1:
        tipo_mao = determinar_tipo_de_mao(maos[0])
        return [i + 1 for i in range(len(maos))], tipo_mao
    else:
        maior_valor_carta = max(valores_cartas_maos)
        vencedores = [i + 1 for i, valor in enumerate(valores_cartas_maos) if valor == maior_valor_carta]
        tipo_mao = determinar_tipo_de_mao(maos[vencedores[0] - 1])
        return vencedores, tipo_mao

def jogar_poker():
    while True:
        num_jogadores = 2
        num_cartas_por_jogador = 5

        baralho = criar_baralho()
        embaralhar_baralho(baralho)

        maos = distribuir_cartas(baralho, num_jogadores, num_cartas_por_jogador)

        for i, mao in enumerate(maos):
            print(f"Jogador {i+1}:")
            maos[i] = trocar_cartas(mao, baralho)
            print(f"Nova mão do Jogador {i+1}: {maos[i]}")

        vencedores, tipo_mao = determinar_vencedor(maos)
        if len(vencedores) == 1:
            print(f"O Jogador {vencedores[0]} venceu com um(a) {tipo_mao}!")
        elif len(vencedores) > 1:
            print(f"Houve um empate entre os jogadores {', '.join(map(str, vencedores))}!")
            maiores_cartas = [max([valores.index(carta.numero) for carta in mao]) for mao in maos]
            maior_carta = max(maiores_cartas)
            vencedor_empate = vencedores[maiores_cartas.index(maior_carta)]
            print(f"O Jogador {vencedor_empate} ganhou com a maior carta!")
        else:
            print("Nenhum vencedor determinado.")

        jogar_novamente = input("Deseja jogar novamente? (s/n): ")
        if jogar_novamente.lower() != 's':
            break

jogar_poker()
