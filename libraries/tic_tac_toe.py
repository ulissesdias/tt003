## O nosso jogador fará uma jogada ao acaso, então usamos
## a biblioteca random para poder gerar números aleatórios
import random

## Bibliotecas que necessitamos
from PIL import Image, ImageDraw

from ipywidgets import interact


## Retorna o vencedor da partida
def winner(tab) :
  somas = [
     ## Linhas
     tab[0]+tab[1]+tab[2],
     tab[3]+tab[4]+tab[5],
     tab[6]+tab[7]+tab[8],

     ## Colunas
     tab[0]+tab[3]+tab[6],
     tab[1]+tab[4]+tab[7],
     tab[2]+tab[5]+tab[8],

     ## Diagonais
     tab[0]+tab[4]+tab[8],
     tab[6]+tab[4]+tab[2]
  ]
  if min(somas) == -3 :
    return -1
  elif max(somas) == 3 :
    return +1
  else :
    return 0

## Retorna os movimentos válidos
def get_valid_moves(tab) :
  valids = []
  for i in range(len(tab)) :
    if tab[i] == 0 :
      valids.append(i)
  return valids

## A função abaixo é um jogador. Ele receberá um tabuleiro
## como parâmetro pela variável "tab". Na variável "turn",
## o jogador saberá se deverá efetuar uma jogada como "x"
## ou "o". Em outras palavras, se turn = 1, então o jogador
## deverá efetuar uma jogada como "x". Caso contrário, se
## turn = -1, o jogador deverá efetuar uma jogada como "o".
def random_player(tab, turn) :
    valid_moves = get_valid_moves(tab)
    if valid_moves :
        return (turn, random.choice(valid_moves) )

## Abaixo uma função que gerencia um jogo.
def game(player1, player2, **argv) :
    ## Inicialização
    turn   = 1
    tab    = (0, 0, 0,  0, 0, 0,  0, 0, 0)
    result = 0

    ## Lista que guardará o histórico
    history = []

    ## Enquanto houverem jogadas, pedimos para o jogador vez prosseguir
    while get_valid_moves(tab) :

        ## Pedindo uma jogada ao jogador da vez.
        piece, pos = None, None
        if turn == 1 :
            piece, pos = player1(tab, turn, **argv)
        else :
            piece, pos = player2(tab, turn, **argv)

        ## Colocando a peça no tabuleiro
        ltab = list(tab)
        ltab[pos] = piece
        tab  = tuple(ltab)

        ## Adicionando tabuleiro no histórico
        history.append(tab)

        ## Verificando se alguém ganhou
        result = winner(tab)
        if result :
            break

        ## Trocando a vez de jogar
        turn = -turn

    return result, history

##################################################
## Interface Gráfica
##################################################

def draw_piece(draw, cell, piece) :
    ## Convertendo linear para matricial
    line   = cell // 3
    column = cell  % 3

    ## Gerando as coordenadas
    x0 = column * 50
    x1 = (column+1)*50
    y0 = line*50
    y1 = (line+1)*50

    if piece == 1 :
        draw.line([x0, y0, x1, y1], width=4, fill = "black")
        draw.line([x1, y0, x0, y1], width=4, fill = "black")
    elif piece == -1 :
        draw.ellipse([x0, y0, x1, y1], width=4, outline = "black")

def draw_board(tab) :
    board = Image.new('RGB', (150, 150),  "gray")
    draw  = ImageDraw.Draw(board)

    draw.line( (0, 50, 150,   50), fill = "black", width = 3 )
    draw.line( (0,100, 150, 100), fill = "black", width = 3 )

    draw.line( (50, 0, 50, 150), fill = "black", width = 3 )
    draw.line( (100, 0, 100, 150), fill = "black", width = 3 )

    for i in range(len(tab)) :
        if (tab[i]) :
            draw_piece(draw, i, tab[i])
    return board

def display_sequence(images) :
    def _show(frame=(0, len(images)-1)) :
        return images[frame]
    return interact(_show)

def generate_image_history(history) :
    image_history = []
    for i in range(len(history)) :
        image_history.append( draw_board( history[i] ) )
    return image_history
