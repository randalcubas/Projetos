#***************************************************************#
#**                                                           **#
#**   Randal Cubas dos Reis             9350925               **#
#**   Exercício-Programa 03                                   **#
#**   Professor: Coelho                                       **#
#**   Turma: 01   (Engenharia Civil)                          **#
#**                                                           **#
#***************************************************************#
# EP3 -- Sokoban

#CONSTANTES!!!
PAREDE           = '#'
PISO_VAZIO       = ' '
MARCA_VAZIA      = '.'
CAIXA_NO_PISO    = '$'
CAIXA_NA_MARCA   = '*'
JOGADOR_NO_PISO  = '@'
JOGADOR_NA_MARCA = '+'

ESQUERDA = 'e'
DIREITA  = 'd'
CIMA     = 'c'
BAIXO    = 'b'
SAIR     = 's'
VOLTAR   = 'v'

ESQUERDA_CX = 'E'
DIREITA_CX  = 'D'
CIMA_CX     = 'C'
BAIXO_CX    = 'B'
def main():
    nome_sokoban = input("Digite o nome de um arquivo sokoban: ")
    mapa_matriz_provisorio = carregaMapa(nome_sokoban)
    mapa_matriz = ajusteMapa(mapa_matriz_provisorio)
    imprimeMapa(mapa_matriz)
    STOP = False
    jogo_concluido = False
    movimentos = ''
    mov_matriz = []
    mapa_valido = mapaValido(mapa_matriz)
    if not mapa_valido:
        print("Mapa inválido")
    while not jogo_concluido and not STOP and mapa_valido:
        print("\n--------------------------------------------------------------------\n")
        linha,coluna = posicaoJogador(mapa_matriz)
        print("Jogador indicado por %s está em (%d, %d)"%(mapa_matriz[linha][coluna],linha,coluna))
        mov = input("Digite d | e | c | b | v | s [dir, esq, cima, baixo, voltar, sair]: ")
        mov_list = []
        for ch in mov:
            mov_list.append(ch)
        i=0
        while not STOP and i <= (len(mov_list)-1):
            if mov_list[i] == SAIR:
                STOP = True
            elif mov_list[i] == VOLTAR:
                undo(mapa_matriz,mov_matriz[len(mov_matriz)-1])
                mov_matriz = mov_matriz[:len(mov_matriz)-1]
            else:
                validade, move_caixa = moveJogador(mapa_matriz, mov_list[i])
                if validade:
                    if move_caixa:
                        if mov_list[i] == ESQUERDA:
                            mov_list[i] = ESQUERDA_CX
                        elif mov_list[i] == DIREITA:
                            mov_list[i] = DIREITA_CX                            
                        elif mov_list[i] == CIMA:
                            mov_list[i] = CIMA_CX                            
                        else:
                            mov_list[i] = BAIXO_CX
                    mov_matriz.append(mov_list[i])
            i+=1
        jogo_concluido = nivelConcluido(mapa_matriz)
        print()
        if not STOP:
            imprimeMapa(mapa_matriz)
    for ch in mov_matriz:
        movimentos += ch
    if jogo_concluido:
        print("Parabéns")
        print("Seus movimentos foram:")
        print(movimentos)
    if STOP and not jogo_concluido:
        print(movimentos)
        print("Desistir é para os fracos, hahaha")
def  carregaMapa(nome):
    '''(string) -> list

    Função que carrega um mapa de um arquivo no formato TXT,
    e o retorna.

    Exemplo:
    Para o arquivo de entrada ".txt" com o mapa abaixo:
    #####
    #@$.#
    #####

    a seguinte lista de listas é retornada:
    [['#', '#', '#', '#', '#'], ['#', '@', '$', '.', '#'], ['#', '#', '#', '#', '#']]
    '''
    arq = open(nome, 'r')
    matriz = []
    for linha in arq:
        lista = []    
        for i in (linha):
            if i != "\n":
                lista.append(i)
        matriz.append(lista)
    return matriz
def ajusteMapa(mapa):
    ''' (list) -> list

    Função que recebe uma matriz e ajusta para uma matriz quadrada adicionando
    " " nas colunas que não têm elementos
    '''
    linha_maior = 0
    for i in range(len(mapa)):
        if len(mapa[i]) > linha_maior:
            linha_maior = len(mapa[i])
    for i in range(len(mapa)):
        while len(mapa[i]) < linha_maior:
            mapa[i].append(" ")
    return mapa
def imprimeMapa(mapa):
    '''(list) -> None

    Função que imprime um mapa com moldura
    '''
    moldura_num = "  "
    moldura_1 = "  "
    moldura_2 = ""
    linhas = len(mapa)
    colunas = len(mapa[0])
    for i in range(colunas):
        moldura_num += ("%3d "%i) 
        moldura_1 += "+---"
    moldura_1 += "+"
    print(moldura_num)
    for i in range(linhas):
        moldura_2 = ("%d "%i)
        for j in range(colunas):
            moldura_2 += ("|%2s "%(mapa[i][j]))
        moldura_2 += "|"
        print(moldura_1)
        print(moldura_2)
    print(moldura_1)
    
def posicaoJogador(mapa):
    '''(list) -> int, int

    Função que devolve as coordenadas (linha e coluna) do jogador na matriz mapa.
    Caso ele não seja encontrado, retorna None.

    Exemplo:
    Para o cenário abaixo:
    #######
    #     #
    # $+$ #
    #.*#*.#
    # $.$ #
    #     #
    #######

    Temos a posição (2, 3)
    '''
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == JOGADOR_NO_PISO or mapa[i][j] == JOGADOR_NA_MARCA:
                return i, j
# ---------------------------------------------------------------------------------
def moveJogador(mapa,mov):
    '''(list, string) -> bool, bool

    Função que realiza o movimento dado por mov atualizando a matriz de estado do jogo, 
    onde mov pode assumir um dentre os seguintes valores: CIMA, BAIXO, ESQUERDA, DIREITA.
    A função deve devolver dois valores booleanos: 
    - O primeiro indica se o movimento é válido (verdadeiro) ou inválido (falso), como por exemplo empurrar 
    duas ou mais caixas juntas de uma só vez.
    - O segundo indica se uma caixa foi empurrada pelo movimento.
    OBS: o segundo booleano deve ser sempre falso se o primeiro for falso.
    '''
    invalido_parede = False
    invalido_caixa_presa = False
    caixa_empurrada = False
    validade = False
    linha, coluna = posicaoJogador(mapa)
    if mov == CIMA or mov == ESQUERDA:
        p= -1
    if mov == BAIXO or mov == DIREITA:
        p = 1
    if mov == CIMA or mov == BAIXO:
        #trabalhar com mapa[linha+p][coluna]
        if mapa[linha+p][coluna]==PAREDE:
            invalido_parede=True
        elif mapa[linha+p][coluna]==CAIXA_NO_PISO or mapa[linha+p][coluna]==CAIXA_NA_MARCA:
            if mapa[linha+2*p][coluna]==PAREDE or mapa[linha+2*p][coluna]==CAIXA_NO_PISO or mapa[linha+2*p][coluna]==CAIXA_NA_MARCA:
                invalido_caixa_presa = True
            elif mapa[linha+2*p][coluna]==MARCA_VAZIA:
                caixa_empurrada = True
                mapa[linha+2*p][coluna]= CAIXA_NA_MARCA
                if mapa[linha+p][coluna]==CAIXA_NA_MARCA:
                    mapa[linha+p][coluna]= JOGADOR_NA_MARCA
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else: #mapa[linha][coluna]=="@"
                        mapa[linha][coluna]=PISO_VAZIO
                else: #if mapa[linha-1][coluna]="$"
                    mapa[linha+p][coluna]= JOGADOR_NO_PISO
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else:
                        mapa[linha][coluna]=PISO_VAZIO
            else: #if mapa[linha-2][coluna]==" ":
                caixa_empurrada = True
                mapa[linha+2*p][coluna]= CAIXA_NO_PISO
                if mapa[linha+p][coluna]==CAIXA_NA_MARCA:
                    mapa[linha+p][coluna]= JOGADOR_NA_MARCA
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else:
                        mapa[linha][coluna]= PISO_VAZIO
                else: #if mapa[linha-1][coluna]="$"
                    mapa[linha+p][coluna]= JOGADOR_NO_PISO
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else: #mapa[linha][coluna]=="@"
                        mapa[linha][coluna]=PISO_VAZIO
        elif mapa[linha+p][coluna] == MARCA_VAZIA:
            mapa[linha+p][coluna] = JOGADOR_NA_MARCA
            if mapa[linha][coluna] == JOGADOR_NO_PISO:
                mapa[linha][coluna] = PISO_VAZIO
            else:#mapa[linha][coluna] == JOGADOR_NA_MARCA
                mapa[linha][coluna] = MARCA_VAZIA
        else: #if mapa[linha-1][coluna]==" ":
            mapa[linha+p][coluna] = JOGADOR_NO_PISO
            if mapa[linha][coluna] == JOGADOR_NO_PISO:
                mapa[linha][coluna] = PISO_VAZIO
            else:
                mapa[linha][coluna] = MARCA_VAZIA
    if mov == ESQUERDA or mov == DIREITA:
        
        if mapa[linha][coluna+p]==PAREDE:
            invalido_parede=True
        elif mapa[linha][coluna+p]==CAIXA_NO_PISO or mapa[linha][coluna+p]==CAIXA_NA_MARCA:
            if mapa[linha][coluna+2*p]==PAREDE or mapa[linha][coluna+2*p]==CAIXA_NO_PISO or mapa[linha][coluna+2*p]==CAIXA_NA_MARCA:
                invalido_caixa_presa = True
            elif mapa[linha][coluna+2*p]==MARCA_VAZIA:
                caixa_empurrada = True
                mapa[linha][coluna+2*p]= CAIXA_NA_MARCA
                if mapa[linha][coluna+p]==CAIXA_NA_MARCA:
                    mapa[linha][coluna+p]= JOGADOR_NA_MARCA
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else: #mapa[linha][coluna]==" "
                        mapa[linha][coluna]=PISO_VAZIO
                else: #if mapa[linha][coluna+1]="$"
                    mapa[linha][coluna+p]= JOGADOR_NO_PISO
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else:
                        mapa[linha][coluna]=PISO_VAZIO
            else: #if mapa[linha][coluna+2]==" ":
                caixa_empurrada = True
                mapa[linha][coluna+2*p]= CAIXA_NO_PISO
                if mapa[linha][coluna+p]==CAIXA_NA_MARCA:
                    mapa[linha][coluna+p]= JOGADOR_NA_MARCA
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else:
                        mapa[linha][coluna]=PISO_VAZIO
                else: #if mapa[linha][coluna+1]="$"
                    mapa[linha][coluna+p]= JOGADOR_NO_PISO
                    if mapa[linha][coluna] == JOGADOR_NA_MARCA:
                        mapa[linha][coluna] = MARCA_VAZIA
                    else: #mapa[linha][coluna]=="@"
                        mapa[linha][coluna]=PISO_VAZIO
        elif mapa[linha][coluna+p] == MARCA_VAZIA:
            mapa[linha][coluna+p] = JOGADOR_NA_MARCA
            if mapa[linha][coluna] == JOGADOR_NO_PISO:
                mapa[linha][coluna] = PISO_VAZIO
            else:#mapa[linha][coluna] == JOGADOR_NA_MARCA
                mapa[linha][coluna] = MARCA_VAZIA
        else: #if mapa[linha][coluna+1]==" ":
            mapa[linha][coluna+p] = JOGADOR_NO_PISO
            if mapa[linha][coluna] == JOGADOR_NO_PISO:
                mapa[linha][coluna] = PISO_VAZIO
            else:
                mapa[linha][coluna] = MARCA_VAZIA
       #trabalhar com mapa[linha][coluna+p]
    if not invalido_parede and not invalido_caixa_presa:
        validade = True


    if invalido_parede:
        print("Movimento inválido: bati na parede!")
    if invalido_caixa_presa:
        print("Movimento inválido: a caixa está presa!")

    return validade, caixa_empurrada
def undo(mapa, mov):
    '''(list, string) -> None

    Função que desfaz o movimento mov, atualizando o mapa.

    OBS: mov pode assumir um dentre os seguintes valores: CIMA, BAIXO, ESQUERDA, DIREITA, 
         ESQUERDA_CX, DIREITA_CX, CIMA_CX, BAIXO_CX.
    '''
    linha,coluna = posicaoJogador(mapa)
    if mov == CIMA or mov == ESQUERDA or mov == ESQUERDA_CX or mov == CIMA_CX:
        p= 1
    if mov == BAIXO or mov == DIREITA or mov == BAIXO_CX or mov == DIREITA_CX:
        p = -1
    if mov == CIMA or mov == BAIXO:
        if mapa[linha][coluna] == JOGADOR_NA_MARCA:
            mapa[linha][coluna] = MARCA_VAZIA
        else:
            mapa[linha][coluna] = PISO_VAZIO
        if mapa[linha+p][coluna] == MARCA_VAZIA:
            mapa[linha+p][coluna] = JOGADOR_NA_MARCA
        else: #if mapa[linha+1][coluna] == ' '
            mapa[linha+p][coluna] = JOGADOR_NO_PISO
    if mov == ESQUERDA or mov == DIREITA:
        # ajustar a posição atual para a anterior
        if mapa[linha][coluna] == JOGADOR_NA_MARCA:
            mapa[linha][coluna] = MARCA_VAZIA
        else:
            mapa[linha][coluna] = PISO_VAZIO
        #------------------------
        #ajustar a nova posição do jogador
        if mapa[linha][coluna+p] == MARCA_VAZIA:
            mapa[linha][coluna+p] = JOGADOR_NA_MARCA
        else: #if mapa[linha][coluna+1] == ' '
            mapa[linha][coluna+p] = JOGADOR_NO_PISO
        #------------------------
    if mov == ESQUERDA_CX or mov == DIREITA_CX:
        #ajusta o piso do jogador
        if mapa[linha][coluna] == JOGADOR_NO_PISO:
            mapa[linha][coluna] = CAIXA_NO_PISO
        else:#mapa[linha][colna] == JOGADOR_NA_MARCA
            mapa[linha][coluna] = CAIXA_NA_MARCA
        #ajusta o piso da caixa
        if mapa[linha][coluna-p] == CAIXA_NA_MARCA:
            mapa[linha][coluna-p] = MARCA_VAZIA
        else: #mapa[linha][coluna+p] == CAIXA_NO_PISO
            mapa[linha][coluna-p] = PISO_VAZIO
        #ajusta para o piso anterior 
        if mapa[linha][coluna+p] == PISO_VAZIO:
            mapa[linha][coluna+p] = JOGADOR_NO_PISO
        else: #mapa[linha][coluna-p] == MARCA_VAZIA
            mapa[linha][coluna+p] = JOGADOR_NA_MARCA
    if mov == CIMA_CX or mov == BAIXO_CX:
        #ajusta o piso do jogador
        if mapa[linha][coluna] == JOGADOR_NO_PISO:
            mapa[linha][coluna] = CAIXA_NO_PISO
        else: #mapa[linha][colna] == JOGADOR_NA_MARCA
            mapa[linha][coluna] = CAIXA_NA_MARCA
        #ajusta o piso do jogador
        if mapa[linha-p][coluna] == CAIXA_NA_MARCA:
            mapa[linha-p][coluna] = MARCA_VAZIA
        else: #mapa[linha][coluna+p] == CAIXA_NO_PISO
            mapa[linha-p][coluna] = PISO_VAZIO
        #ajusta o piso da caixa 
        if mapa[linha+p][coluna] == PISO_VAZIO:
            mapa[linha+p][coluna] = JOGADOR_NO_PISO
        else: #mapa[linha-p][coluna] == MARCA_VAZIA
            mapa[linha+p][coluna] = JOGADOR_NA_MARCA

#-----------------------------------------------------------------------
    
def nivelConcluido(mapa):
    '''(list) -> bool

    Função que verifica se todas caixas estão colocadas nas marcas, indicando o fim do jogo. 
    A função deve devolver verdadeiro (vitória do jogador) ou falso (jogo não encerrado).
    '''
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == CAIXA_NO_PISO:
                return False
    return True

#-----------------------------------------------------------------------
def mapaValido(mapa):
    '''(list) -> bool

    Função que testa se um mapa é válido.
    Todo cenário deve ter:
    - um único jogador,
    - pelo menos uma marca vazia e
    - a quantidade de marcas deve ser a mesma que a de caixas.
    A função deve devolver verdadeiro (válido) ou falso (inválido).

    OBS: Por propósitos de simplicidade, a parte de verificar se o mapa
    está cercado por paredes é opcional.
    '''
    quant_jogador = 0
    marcas_vazias = 0
    quant_marcas = 0
    quant_caixas = 0
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == JOGADOR_NO_PISO:
                quant_jogador += 1
            elif mapa[i][j] == JOGADOR_NA_MARCA:
                quant_jogador += 1
                quant_marcas +=1
            elif mapa[i][j] == CAIXA_NO_PISO:
                quant_caixas += 1
            elif mapa[i][j] == CAIXA_NA_MARCA:
                quant_caixas += 1
                quant_marcas += 1
            elif mapa[i][j] == MARCA_VAZIA:
                quant_marcas += 1
                marcas_vazias +=1
    if quant_jogador == 1 and marcas_vazias != 0 and quant_marcas == quant_caixas:
        return True
    else:
        return False


main()
