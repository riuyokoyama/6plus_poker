import itertools
import qualify_fivecard
import qualify_holdem

def AI_prefrop(AI_hand,bet_count):
  print('bet_count: '+str(bet_count))
  #premium
  if (int((AI_hand[0])[1:]) > 9 or int((AI_hand[0])[1:]) == 1) and (int((AI_hand[1])[1:]) >9 or int((AI_hand[1])[1:]) == 1):
    if bet_count < 3 :
      return 'bet to '
    else:
      return 'call'
  #suit(30%)
  elif int((AI_hand[0])[0]) == int((AI_hand[1])[0]):
    return 'bet to '
  #conecter(40%)
  elif  abs(int((AI_hand[0])[1:]) - int((AI_hand[1])[1:])) == 1:
    if bet_count == 0:
      return 'bet to '
    else:
      return 'call'
  #pocket(jj under 30%)
  elif int((AI_hand[0])[1:]) == int((AI_hand[1])[1:]):
    if bet_count == 0:
      return 'bet to '
    else:
      return 'call'
  elif bet_count > 0:
    return 'fold'
  elif bet_count < 1:
    return 'check'

def judge_flush_draw(index):
  suit_index=[]
  for x in index:
    suit_index.append(x[1])
  if suit_index[0]==suit_index[1] and suit_index[1]==suit_index[2] and suit_index[2]==suit_index[3]:
    return True
  return False
def judge_stright_draw(index):
  stright_index = []
  qualify = ''
  for x in index:
    stright_index.append(int(x[1:]))
  sorted(stright_index)
  if stright_index[3] - stright_index[2] == 1 and stright_index[2] - stright_index[1] == 1 and stright_index[1] - stright_index[0] == 1:
    return True
  return False
  
def AI_action(AI_hand,bord,action_count,bet_count):
  index = AI_hand + bord
  qualify_alredy = ''
  stronger_qualify=' Hight card '
  max_num = 0
  for y in itertools.combinations(index, 5):
    qualify_alredy = qualify_fivecard.qualify(y)
    stronger_qualify = qualify_holdem.judge_stronger(stronger_qualify,qualify_alredy,max_num,list(y))

  if stronger_qualify == 'StraightFlush':
    if bet_count < 5:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'Four of a kind':
    if bet_count < 5:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'FullHouse':
    if bet_count < 5:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'Flush':
    if bet_count < 5:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'Straight':
    if bet_count < 5:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'Tree of a kind':
    if bet_count < 2:
      return 'bet to '
    else:
      return 'call'
  elif stronger_qualify == 'TwoPair':
    if bet_count < 2:
      return 'bet to '
    else:
      return 'call'
  elif  stronger_qualify == 'OnePair':
    if bet_count > 0:
      return 'call'
    elif bet_count > 2:
      return 'fold'
    else:
      return 'bet to '
  elif bet_count == 0:
    return 'check'
  else:
    for x in itertools.combinations(y, 4):
      if judge_flush_draw(x) and action_count < 3 :
        if bet_count > 0:
          return 'call'
        else:
          return 'check'
      elif judge_stright_draw(x) and action_count < 3:
        if bet_count > 0:
          return 'call'
        else:
          return 'check'
    return 'fold'


  #bet to call,if not river qualify flush draw or straight draw and any onepair
  #check to bet, qualify one pair
  #bet to bet, qualify two pair over
  #bet to fold check to check,qualify highCard
  return 'error'


  