import tkinter
import random
import qualify_holdem
import poker_AI
from pathlib import Path

##ターミナルから起動
deck_list =[
        ['card_img/spade1.png','card_img/spade2.png','card_img/spade3.png','card_img/spade4.png','card_img/spade5.png','card_img/spade6.png','card_img/spade7.png','card_img/spade8.png','card_img/spade9.png','card_img/spade10.png','card_img/spade11.png','card_img/spade12.png','card_img/spade13.png',],
        ['card_img/heart1.png','card_img/heart2.png','card_img/heart3.png','card_img/heart4.png','card_img/heart5.png','card_img/heart6.png','card_img/heart7.png','card_img/heart8.png','card_img/heart9.png','card_img/heart10.png','card_img/heart11.png','card_img/heart12.png','card_img/heart13.png',],
        ['card_img/diamond1.png','card_img/diamond2.png','card_img/diamond3.png','card_img/diamond4.png','card_img/diamond5.png','card_img/diamond6.png','card_img/diamond7.png','card_img/diamond8.png','card_img/diamond9.png','card_img/diamond10.png','card_img/diamond11.png','card_img/diamond12.png','card_img/diamond13.png',],
        ['card_img/clab1.png','card_img/clab2.png','card_img/clab3.png','card_img/clab4.png','card_img/clab5.png','card_img/clab6.png','card_img/clab7.png','card_img/clab8.png','card_img/clab9.png','card_img/clab10.png','card_img/clab11.png','card_img/clab12.png','card_img/clab13.png']
    ] 

def centering_main_window(event):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = screen_width / 2 - window_width /2
    y = screen_height / 2 - window_height / 2
    window.geometry("+%d+%d" % (x, y))

# 画面作成
window = tkinter.Tk()
window.geometry("350x500")
window.title("ポーカー")
window.bind("<Map>", centering_main_window)  

ai_hands_index = []
board_index = []
player_hands_index = []
use_list = []
game_count = 1
count=0
bet_action_count=0
pot = 0
bet_count = 0
AI_action = ''
player_action = ''
player_chip = 100
ai_chip = 100
ai_bet = 0
player_bet = 0
winner = ''
img_card_board1 = None
img_card_board2 = None
img_card_board3 = None
img_card_board4 = None
img_card_board5 = None
img_card_ai1 = None
img_card_ai2 = None


def call_action():
    global ai_bet,player_chip,player_chip_label,pot,bet_count,game_pot,bet_action_count,ai_chip,ai_label,player_bet,bet_count
    bet_action_count += 1
    player_bet = (bet_count*5)
    player_chip = player_chip - ai_bet
    player_chip_label.set('playerの残りチップ：'+str(player_chip))
    ai_chip = ai_chip - ai_bet
    ai_chip_label.set('AIの残りチップ：'+str(ai_chip))
    #make pot
    pot = pot + ai_bet + ai_bet
    game_pot.set('pot :'+str(pot))
    player_bet = 0
    ai_bet = 0

    AI_action = ''
    game_messeage.set(AI_action)
    button_state()
    if bet_action_count == 1:
        board_1.create_image(0, 0, image= img_card_board1, anchor=tkinter.NW, tag ='board_1')
        board_2.create_image(0, 0, image= img_card_board2, anchor=tkinter.NW, tag ='board_2')
        board_3.create_image(0, 0, image= img_card_board3, anchor=tkinter.NW, tag ='board_3')
        bet_count = 0
    elif bet_action_count == 2:
        board_4.create_image(0, 0, image= img_card_board4, anchor=tkinter.NW, tag ='board_4')
        bet_count = 0
    elif bet_action_count == 3:
        board_5.create_image(0, 0, image= img_card_board5, anchor=tkinter.NW, tag ='board_5')
        bet_count = 0
    elif bet_action_count == 4:
        bet_count = 0
        end_game('None')
        bet_action_count = 0

    print_test()


def check_action():
    global check_button,bet_action_count,bet_count,ai_bet,player_bet,pot,ai_chip,player_chip,pot
    print('1st bet_count: '+str(bet_count))
    bet_action_count += 1
    if bet_action_count == 1:
        AI_action = poker_AI.AI_prefrop(ai_hands_index,0)
        if AI_action == 'bet to ':
            bet_action_count -= 1
            bet_count += 1
            ai_bet = (5*bet_count)
            AI_action += str(ai_bet)
        elif AI_action == 'fold':
            end_game('None')
    elif bet_action_count > 1:
        AI_action = poker_AI.AI_action(ai_hands_index,board_index[:(bet_action_count+2)],bet_action_count,bet_count)
        if AI_action == 'bet to ':
            bet_action_count -= 1
            bet_count += 1
            ai_bet = (5*bet_count)
            AI_action += str(ai_bet)
        elif AI_action == 'fold':
            end_game('None')

    #make pot
    if AI_action != 'fold' and player_bet == ai_bet:
        pot = pot + player_bet + ai_bet
        game_pot.set('pot :'+str(pot))

        ai_chip = ai_chip - ai_bet
        ai_chip_label.set('aiの残りチップ：'+str(ai_chip))

        player_chip = player_chip - player_bet
        player_chip_label.set('playerの残りチップ：'+str(player_chip))
        bet_count = 0
        player_bet = 0
        ai_bet = 0

    game_messeage.set(AI_action)
    button_state()
    if bet_action_count == 1:
        board_1.create_image(0, 0, image= img_card_board1, anchor=tkinter.NW, tag ='board_1')
        board_2.create_image(0, 0, image= img_card_board2, anchor=tkinter.NW, tag ='board_2')
        board_3.create_image(0, 0, image= img_card_board3, anchor=tkinter.NW, tag ='board_3')
        bet_count = 0
    elif bet_action_count == 2:
        board_4.create_image(0, 0, image= img_card_board4, anchor=tkinter.NW, tag ='board_4')
        bet_count = 0
    elif bet_action_count == 3:
        board_5.create_image(0, 0, image= img_card_board5, anchor=tkinter.NW, tag ='board_5')
        bet_count = 0
    elif bet_action_count == 4:
        bet_count = 0
        end_game('None')
        bet_action_count = 0
    
    print_test()

def bet_action():
    global game_pot,pot,player_chip,ai_chip,bet_value,bet_button,fold_button,bet_action_count,bet_count,AI_action,ai_bet,player_bet
    bet_action_count += 1
    bet_count += 1
    player_bet = (bet_count*5)
    if bet_action_count == 1:
        AI_action = poker_AI.AI_prefrop(ai_hands_index,bet_count)
        if AI_action == 'bet to ':
            bet_action_count -= 1
            bet_count += 1
            ai_bet = (5*bet_count)
            AI_action += str(ai_bet)
        elif AI_action == 'fold':
            end_game('None')
        elif AI_action == 'call':
           ai_bet = (5*bet_count)

    elif bet_action_count > 1:
        AI_action = poker_AI.AI_action(ai_hands_index,board_index[:(bet_action_count+2)],bet_action_count,bet_count)
        if AI_action == 'bet to ':
            bet_action_count -= 1
            bet_count += 1
            ai_bet = (5*bet_count)
            AI_action += str(ai_bet)
        elif AI_action == 'fold':
            end_game('None')
    

    #make pot
    if AI_action != 'fold' and player_bet == ai_bet:
        pot = pot + player_bet + ai_bet
        game_pot.set('pot :'+str(pot))

        ai_chip = ai_chip - ai_bet
        ai_chip_label.set('aiの残りチップ：'+str(ai_chip))

        player_chip = player_chip - player_bet
        player_chip_label.set('playerの残りチップ：'+str(player_chip))
        bet_count = 0
        player_bet = 0
        ai_bet = 0
    game_messeage.set(AI_action)
    button_state()
    if bet_action_count == 1:
        board_1.create_image(0, 0, image= img_card_board1, anchor=tkinter.NW, tag ='board_1')
        board_2.create_image(0, 0, image= img_card_board2, anchor=tkinter.NW, tag ='board_2')
        board_3.create_image(0, 0, image= img_card_board3, anchor=tkinter.NW, tag ='board_3')
        
    elif bet_action_count == 2:
        board_4.create_image(0, 0, image= img_card_board4, anchor=tkinter.NW, tag ='board_4')
        
    elif bet_action_count == 3:
        board_5.create_image(0, 0, image= img_card_board5, anchor=tkinter.NW, tag ='board_5')
        
    elif bet_action_count == 4:
        end_game('None')
        bet_action_count = 0
    print_test()

    
def end_game(player_act):
    global player_chip_label,player_chip,ai_chip,pot,game_count,ai_qualify_label,player_qualify_label,winner_label,next_game_button,winner,bet_action_count,AI_action
    ai_1.delete('ai_1')
    ai_2.delete('ai_2')
    ai_1.create_image(0, 0, image=img_card_ai1, anchor=tkinter.NW,tag='ai_1')
    ai_2.create_image(0, 0, image=img_card_ai2, anchor=tkinter.NW,tag='ai_2')
    winner_label = tkinter.StringVar()

    if bet_action_count == 4:
    #役判定label
        ai_qualify,ai_stronger_five = qualify_holdem.six_plus_qualify(ai_hands_index,board_index)
        ai_qualify_label = tkinter.StringVar()
        ai_qualify_label.set('AI qualify: '+ str(ai_qualify))
        ai_qualify_label = tkinter.Label(window,textvariable = ai_qualify_label)
        player_qualify,player_stronger_five = qualify_holdem.six_plus_qualify(player_hands_index,board_index)
        player_qualify_label = tkinter.StringVar()
        player_qualify_label.set('Player qualify: '+ str(player_qualify))
        player_qualify_label = tkinter.Label(window,textvariable = player_qualify_label)
        player_qualify_label.pack() 
        ai_qualify_label.pack()
        judge_list = [str(player_qualify),str(ai_qualify)]
        winner = judge_win(judge_list,ai_stronger_five,player_stronger_five)   
    else:
        if AI_action == 'fold':
            winner = 'player'
        elif player_act == 'fold':
            winner = 'AI'
    
    winner_label.set('Winner: '+ winner)
    winner_label = tkinter.Label(window,textvariable = winner_label)
    winner_label.pack()
    #chipの受け渡し
    if winner == 'player':
        player_chip += pot
    elif winner == 'AI':
        ai_chip += pot
    elif winner == 'chop':
        player_chip += int(pot/2)
        ai_chip += int(pot/2)
    player_chip_label.set('playerの残りチップ：'+str(player_chip))
    ai_chip_label.set('AIの残りチップ：'+str(ai_chip))
    
    pot = 0
    game_pot.set('pot :'+str(pot))

    #ゲームの継続判定
    if game_count < 3:
        next_game_button = tkinter.Button(next_game_frame, text="next Game",command=next_game)
        next_game_button.pack(side=tkinter.BOTTOM)
        next_game_frame.pack()
        game_count += 1
        bet_action_count = 0
    else:
        total_player_chip = str(player_chip - 100)
        total_AI_chip = str(ai_chip - 100)
        if player_chip - 100 > 0:
            total_player_chip  = '+' + total_player_chip 
        
        if ai_chip - 100 > 0:
            total_AI_chip  = '+' + total_AI_chip 

        print('total Player chips: '+str(player_chip)+'('+(total_player_chip)+')')
        print('total AI chips: '+str(ai_chip)+'('+(total_AI_chip)+')')
    
    return

def button_state():
    print('AI bet:'+str(ai_bet))
    print('Player bet:'+str(player_bet))
    if  bet_count == 5:
        call_button['state'] = 'active'
        fold_button['state'] = 'active'
        check_button['state'] = 'disable'
        bet_button['state'] = 'disable' 
    elif  ai_bet > player_bet and player_bet != 0:
        call_button['state'] = 'active'
        fold_button['state'] = 'active'
        check_button['state'] = 'disable'
        bet_button['state'] = 'active' 
    elif ai_bet < player_bet and ai_bet != 0:
        call_button['state'] = 'active'
        fold_button['state'] = 'active'
        check_button['state'] = 'disable'
        bet_button['state'] = 'active' 
    elif ai_bet > player_bet and player_bet == 0:
        check_button['state'] = 'disable'
        call_button['state'] = 'active'
        fold_button['state'] = 'active'
        bet_button['state'] = 'active'
    elif ai_bet < player_bet and ai_bet == 0:
        check_button['state'] = 'active'
        call_button['state'] = 'active'
        fold_button['state'] = 'disable'
        bet_button['state'] = 'active'
    elif player_bet == 0 and ai_bet == 0:
        check_button['state'] = 'active'
        call_button['state'] = 'disable'
        fold_button['state'] = 'disable'
        bet_button['state'] = 'active'

    

def print_test():
    if game_count == 3:
        return

    trun = ''
    if bet_action_count == 0:
        trun = 'prefrop'
    elif bet_action_count == 1:
        trun = 'frop'
    elif bet_action_count == 2:
        trun = 'trun'
    elif bet_action_count == 3:
        trun = 'river'
    print('action_count: '+ trun + ' : '+ str(bet_action_count))
    print('bet_count: '+ str(bet_count))
    print('pot size: ' + str(pot))
    print('AI chip :'+str(ai_chip))
    print('player chip :'+str(player_chip))

    return

#UI of AI
img_card_ai = tkinter.PhotoImage(file="card_img/card_back.png")

 #label of AI chip
ai_chip_label = tkinter.StringVar()
ai_chip_label.set('AIの残りチップ：'+str(ai_chip))
ai_label = tkinter.Label(window,textvariable = ai_chip_label)

ai_label.pack()
#make AI frame
ai_card_frame = tkinter.Frame(window, width=350, height=70, background='blue')
# make canvas
ai_1 = tkinter.Canvas(ai_card_frame, bg="#deb887", height=70, width=70)
ai_2 = tkinter.Canvas(ai_card_frame, bg="#deb887", height=70, width=70)

# display canvas
ai_1.place(x=80, y=0)
ai_2.place(x=160, y=0)


ai_qualify_label = tkinter.Label(window,textvariable = '')
player_qualify_label = tkinter.Label(window,textvariable = '')


action_frame = tkinter.Frame(window, width=350, height=40,)

next_game_frame = tkinter.Frame(window, width=350, height=40,)
next_game_button = tkinter.Button(next_game_frame, text="next Game")

board_card_frame = tkinter.Frame(window, width=350, height=70, background='red')
board_label = tkinter.Label(window,text = 'board')

# make canvas
board_1 = tkinter.Canvas(board_card_frame, bg="#deb887", height=70, width=70)
board_2 = tkinter.Canvas(board_card_frame, bg="#deb887", height=70, width=70)
board_3 = tkinter.Canvas(board_card_frame, bg="#deb887", height=70, width=70)
board_4 = tkinter.Canvas(board_card_frame, bg="#deb887", height=70, width=70)
board_5 = tkinter.Canvas(board_card_frame, bg="#deb887", height=70, width=70)

# display canvas
board_1.place(x=0, y=0)
board_2.place(x=70, y=0)
board_3.place(x=140, y=0)
board_4.place(x=210, y=0)
board_5.place(x=280, y=0)

label = tkinter.Label(window,text ='first bet する額を入力(5以上)')
#make player frame
player_card_frame = tkinter.Frame(window, width=350, height=70, background='blue')
player_1 = tkinter.Canvas(player_card_frame, bg="#deb887", height=70, width=70,)
player_2 = tkinter.Canvas(player_card_frame, bg="#deb887", height=70, width=70,)

# display canvas
player_1.place(x=80, y=0)
player_2.place(x=160, y=0)

bet_button = tkinter.Button(action_frame, text="bet",command= bet_action,state='active')
bet_button.pack(side=tkinter.LEFT)
call_button = tkinter.Button(action_frame, text="call",command=call_action,state='active')
call_button.pack(side=tkinter.LEFT)
check_button  = tkinter.Button(action_frame, text="check",command=check_action,state='active')
check_button.pack(side=tkinter.LEFT)
fold_button = tkinter.Button(action_frame, text="fold",command = lambda x = 'fold':end_game(x),state='disable')
fold_button.pack(side=tkinter.LEFT)

#game message setting
game_messeage = tkinter.StringVar()
game_pot = tkinter.StringVar()
game_pot.set('pot :'+str(pot))
game_messeage_label = tkinter.Label(window,textvariable = game_messeage)
game_pot_label = tkinter.Label(window,textvariable = game_pot)
game_messeage_label.pack()


#label of player chip
player_chip_label = tkinter.StringVar()
player_chip_label.set('playerの残りチップ：'+str(player_chip))
player_label = tkinter.Label(window,textvariable = player_chip_label)

ai_card_frame.pack()
#make board frame
board_label.pack()
board_card_frame.pack()
label.pack()
player_card_frame.pack()
action_frame.pack()
player_label.pack()
game_pot_label.pack()
game_messeage_label.pack()


def check_used(card_num):
    for i in use_list:
        if i == card_num:
            return True
    use_list.append(card_num)
    return False

def random_card():
    global deck_list,use_list,count
    suits = random.randrange(1,5)
    number = random.randrange(6,14)
    while check_used(str(suits)+str(number)):
        suits = random.randrange(1,5)
        number = random.randrange(6,14)
    card_image=tkinter.PhotoImage(file=Path(deck_list[suits-1][number-1]))
    card = str(suits)+str(number)
    count += 1
    return card_image,card

def bet_action_frame():
    #actionframe setting
    global bet_value,bet_button,fold_button
    bet_button = tkinter.Button(action_frame, text="bet",command=bet_action)
    bet_button.pack(side=tkinter.LEFT)
    call_button = tkinter.Button(action_frame, text="call",command=call_action)
    call_button.pack(side=tkinter.LEFT)
    check_button  = tkinter.Button(action_frame, text="check",command=check_action)
    check_button.pack(side=tkinter.LEFT)
    fold_button = tkinter.Button(action_frame, text="fold",command = end_game)
    fold_button.pack(side=tkinter.LEFT) 
    

    
def judge_win(qualify_list,ai_stronger,player_stronger_five):
    return qualify_holdem.judge_winner(qualify_list,ai_stronger,player_stronger_five)


def next_game():
    global player_qualify_label,ai_qualify_label,next_game_button,winner_label,game_count
    player_qualify_label.destroy()
    ai_qualify_label.destroy()
    next_game_button.destroy()

    ai_1.delete('ai_1')
    ai_2.delete('ai_2')
    board_1.delete('board_1')
    board_2.delete('board_2')
    board_3.delete('board_3')
    board_4.delete('board_4')
    board_5.delete('board_5')
    player_1.delete('player_1')
    player_2.delete('player_2')
    player_qualify_label.destroy()
    ai_qualify_label.destroy()
    winner_label.destroy()
    next_game_button.destroy()

    player_hands_index.clear()
    board_index.clear()
    ai_hands_index.clear()


    
    start()
    return

def start():
    global img_card_ai1,img_card_ai2,img_card_board1,img_card_board2,img_card_board3,img_card_board4,img_card_board5,img_card_player1,img_card_player2,game_count,bet_count
    print('game_count: '+ str(game_count))

    bet_count = 0
    AI_action = ''

    game_messeage.set(AI_action)

    call_button['state'] = 'disable'
    fold_button['state'] = 'active'
    check_button['state'] = 'active'
    bet_button['state'] = 'active' 

    # make image
    img_card_ai1,aicard1 = random_card()
    img_card_ai2,aicard2 = random_card()


    # display image on canvas
    ai_1.create_image(0, 0, image=img_card_ai, anchor=tkinter.NW,tag='ai_1')
    ai_2.create_image(0, 0, image=img_card_ai, anchor=tkinter.NW,tag='ai_2')

    #ai hands add index 
    ai_hands_index.append(aicard1)
    ai_hands_index.append(aicard2)

    

    img_card_board1,board_card_1=random_card()
    img_card_board2,board_card_2=random_card()
    img_card_board3,board_card_3=random_card()
    img_card_board4,board_card_4=random_card()
    img_card_board5,board_card_5=random_card()

   

    #board add index 
    board_index.append(board_card_1)
    board_index.append(board_card_2)
    board_index.append(board_card_3)
    board_index.append(board_card_4)
    board_index.append(board_card_5)

    # display image on canvas
    img_card_player1,player_hand1 = random_card()
    player_1.create_image(0, 0, image= img_card_player1, anchor=tkinter.NW, tag ='player_1')
    img_card_player2,player_hand2 = random_card()
    player_2.create_image(0, 0, image=img_card_player2, anchor=tkinter.NW, tag ='player_2')
    #player hands add index
    player_hands_index.append(player_hand1)
    player_hands_index.append(player_hand2)
    
    player_card_frame.pack()

    #test to collect hands and board(1=♠︎,2=❤︎,3=♦︎,4=♣︎)
    print('AI:'+ str(ai_hands_index))
    print('Board:'+ str(board_index))
    print('Player:'+ str(player_hands_index))
    return

start()

window.mainloop()