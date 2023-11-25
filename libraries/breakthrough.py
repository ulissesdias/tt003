from IPython.display import display # para mostrar imagens
from PIL import Image, ImageDraw    # para ler imagens

    
## O nosso jogador fará uma jogada ao acaso, então usamos
## a biblioteca random para poder gerar números aleatórios
import random

def draw_board(lines, columns, white_positions, black_positions) :
    board = Image.new('RGB', (200, 200),  "gray")
    draw  = ImageDraw.Draw(board)

    ## Linhas e Colunas
    shift_lines = float(board.size[0])/lines
    for el in range(lines) :
        draw.line( (0, shift_lines *(el+1), board.size[0], shift_lines*(el+1)), fill = "black" )

    ## Linhas e Colunas
    shift_columns = float(board.size[1])/columns
    for el in range(columns) :
        draw.line( (shift_columns*(el+1), 0, shift_columns*(el+1), board.size[1]), fill = "black" )

    ## Peças
    for el in black_positions :
        x, y = lines-el[0]+1, el[1]
        draw.polygon([(shift_columns*(y-0.9),shift_lines*(x-0.9)),
                      (shift_columns*(y-0.5),shift_lines*(x-0.15)),
                      (shift_columns*(y-0.1),shift_lines*(x-0.9))],
                     fill = 'black')

    for el in white_positions :
        x, y = lines-el[0]+1, el[1]

        draw.polygon([(shift_columns*(y-0.9),shift_lines*(x-0.1)),
                      (shift_columns*(y-0.5),shift_lines*(x-0.85)),
                      (shift_columns*(y-0.1),shift_lines*(x-0.1))],
                     fill = 'white')
    return board


def display_sequence(images) :
    def _show(frame=(0, len(images)-1)) :
        return images[frame]
    return interact(_show)
    
    
def winner(lines, columns, white_positions, black_positions) :
    ## Se alguém ficou sem peças, encerrar a partida.
    if len(white_positions) == 0:
        return -1
    elif len(black_positions) == 0:
        return 1

    for peca in white_positions :
        ## Se a linha da peça for a última linha do tabuleiro
        if peca[0] == lines :
            return 1

    for peca in black_positions :
        ## Se a linha da peça for a primeira linha do tabuleiro
        if peca[0] == 1 :
            return -1

    ## Jogo ainda não acabou
    return 0

def valid_move(move, lines, columns, white_positions, black_positions) :
    ## Se não houver move, então já saia.
    if not move :
        return False

    origem, destino = move

    ## verificar limites do tabuleiro
    if not 0 < origem[0]  <= lines :
        return False
    if not 0 < destino[0] <= lines :
        return False
    if not 0 < origem[1]  <= columns :
        return False
    if not 0 < destino[1] <= columns :
        return False

    ## Verificar se origem é válida.
    if not origem in white_positions :
        return False

    ## Verificar se destino é livre de peças brancas
    if destino in white_positions :
        return False

    ## Verificar se a passagem origem --> destino é válida
    if not (destino[0] - origem[0] == 1 and
        abs(destino[1] - origem[1]) <= 1) :
        return False

    ## Em caso de ser uma jogada para frente, verificar se o destino não
    ## está bloqueada pelo oponente
    if (origem[1] == destino[1]) :
        if destino in black_positions :
            return False
    return True
    
def get_valid_moves(lines, columns, white_positions, black_positions) :
    valid_moves = []
    for origem in white_positions :
        destinos = (
            (origem[0]+1, origem[1]-1),
            (origem[0]+1, origem[1]),
            (origem[0]+1, origem[1]+1)
        )
        for destino in destinos :
            if valid_move( (origem, destino), lines, columns, white_positions, black_positions) :
               valid_moves.append(  (origem, destino)  )
    return tuple(valid_moves)


## A função abaixo é um jogador. Ele receberá um tabuleiro
## como parâmetro pelas variáveis  lines, columns, white_positions,
## black_positions.
def rnadom_player(lines, columns, white_positions, black_positions) :
    valid_moves = get_valid_moves(lines, columns, white_positions, black_positions)
    if valid_moves :
        return random.choice(valid_moves)


def human_player(lines, columns, white_positions, black_positions) :
    board = draw_board(lines, columns, white_positions, black_positions)
    display(board)
    print("Jogue no formato '(origemLine, origemColumn), (destinoLine, destinoColumn)' ")
    origem, destino = eval(input())
    return origem, destino
    
## Abaixo uma função que gerencia um jogo.
def game(player1, player2, lines = 5, columns = 5,
         white_positions = ( (1,1), (1,2), (1,3), (1,4), (1,5) ),
         black_positions = ( (5,1), (5,2), (5,3), (5,4), (5,5) ) ) :

    ## Inicialização
    turn   = 1
    result = 0

    ## Lista que guardará o histórico
    history = [ (lines, columns), (white_positions, black_positions)  ]

    ## Enquanto houverem jogadas, pedimos para o jogador vez prosseguir
    win = winner(lines, columns, white_positions, black_positions)
    while not win :

        ## Pedindo uma jogada ao jogador da vez.
        if turn == 1 :
            origem, destino = player1(lines, columns, white_positions, black_positions)

            lwhite_positions = list(white_positions)
            lwhite_positions.remove(origem)
            lwhite_positions.append(destino)
            white_positions = tuple(lwhite_positions)
            ## Se destino estiver na lista de pretas, então deve ser removido.
            if destino in black_positions :
                lblack_positions = list(black_positions)
                lblack_positions.remove(destino)
                black_positions = tuple(lblack_positions)

        else :
            origem, destino = player2(lines, columns, white_positions, black_positions)

            lblack_positions = list(black_positions)
            lblack_positions.remove(origem)
            lblack_positions.append(destino)
            black_positions = tuple(lblack_positions)

            ## Se destino estiver na lista de brancas, então deve ser removido.
            if destino in white_positions :
                lwhite_positions = list(white_positions)
                lwhite_positions.remove(destino)
                white_positions = tuple(lwhite_positions)

        ## Adicionando tabuleiro no histórico
        history.append( (white_positions, black_positions) )

        ## Atualizando a variável que verifica ganhador.
        win = winner(lines, columns, white_positions, black_positions)

        ## Trocando a vez de jogar
        turn = -turn

    return win, history
