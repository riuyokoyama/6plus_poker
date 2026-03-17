import qualify_fivecard
import itertools

six_plus_qualify_index = ['Hight card','OnePair','TwoPair','Tree of a kind','Straight','FullHouse','Flush','Four of a kind','StraightFlush']
stronger_five_index =[]
max_qualify=[]
max_qualify_num = []

def six_plus_qualify(hand,board):
  max_qualify=[]
  max_qualify_num=[]
  stronger_qualify = ' Hight card '
  qualify_index = hand + board
  max_num = 0
#5枚選ぶ
  for x in itertools.combinations(qualify_index, 5):
    
    qualify_alredy = qualify_fivecard.qualify(x)
#一番強い役の決定
    stronger_qualify = judge_stronger(stronger_qualify,qualify_alredy,max_num,list(x))
  label = str(stronger_qualify)
  for x in itertools.combinations(qualify_index, 5):
    qualify_alredy = qualify_fivecard.qualify(x)
    if label == qualify_alredy:
      max_qualify.append(list(x))
  for w in range(len(max_qualify)):
    for z in range(5):
      max_qualify[w][z] = (max_qualify[w][z])[1:]
  for list_f in range(len(max_qualify)):
    list_i=[]
    for list_s in range(5):
      list_i.append(int(max_qualify[list_f][list_s]))
    list_i.sort()
    max_qualify_num.append(list_i)    
  stronger_five = max_qualify_num[0]
  for f in range(len(max_qualify_num)-1):
    for f_s in range(5):
      if stronger_five[4 - f_s] < max_qualify_num[f+1][4 - f_s]:
        stronger_five = max_qualify_num[f+1]
        break
      elif stronger_five[4 - f_s] == max_qualify_num[f+1][4 - f_s]:
        if stronger_five[3 - f_s] < max_qualify_num[f+1][3 - f_s]:
          stronger_five = max_qualify_num[f+1]
          break
        elif stronger_five[3 - f_s] == max_qualify_num[f+1][3 - f_s]:
          if stronger_five[2 - f_s] < max_qualify_num[f+1][2 - f_s]:
            stronger_five = max_qualify_num[f+1]
            break
          elif stronger_five[2 - f_s] == max_qualify_num[f+1][2 - f_s]:
            if stronger_five[1 - f_s] < max_qualify_num[f+1][1 - f_s]:
              stronger_five = max_qualify_num[f+1]
              break
  return label,stronger_five



def judge_winner(list,ai_strong,player_strong):
  player_qualify_num = 0
  AI_qualify_num = 0
  for q in range(9):
    if list[0] == six_plus_qualify_index[q]:
      player_qualify_num = q
    if list[1] == six_plus_qualify_index[q]:
      AI_qualify_num = q
  if AI_qualify_num > player_qualify_num:
    return 'AI'
  elif player_qualify_num > AI_qualify_num:
    return 'player'
  else:
    if ai_strong == player_strong:
      return 'chop'
    for num in range(5):
      if ai_strong[4-num] > player_strong[4-num]:
        return 'AI'
      elif ai_strong[4-num] < player_strong[4-num]:
        return 'player'



def judge_stronger(max,judge,max_num,str_index):
  global stronger_five_index
  judge_num = 0
  for i in range(9):
    if judge == six_plus_qualify_index[i]:
      judge_num = i

    if max == six_plus_qualify_index[i]:
      max_num = i

  if max_num < judge_num:
    stronger_five_index = str_index
    return judge
  else:
    return max
