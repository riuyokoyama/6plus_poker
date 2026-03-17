def GetCardSuits(card):
  get_suits = card[0]
  return int(get_suits)

def GetCardNum(card):
  get_num = card[1:]
  return int(get_num)

def high_card(index):
  #ハイカード判定
  high_num = 0  
  hight_index=[]
  for i in range(5):
    hight_index.append(GetCardNum(index[i]))
  index.sort()
  if IsStraight(index) and (index[4])[1:] == 9:
    return 9
  else:
    high_num = hight_index[4]

  if high_num == 1:
    return 'A'
  elif high_num == 11:
    return 'J'
  elif high_num == 12:
    return 'Q'
  elif high_num == 13:
    return 'K'
  else:
    return str(high_num)
  
def low_card(hight_num):
  int(hight_num)
  low_num = 0
  if hight_num == 9:
    return 'A'
  else:
    return str(low_num)
  
def IsStraightFlush(index):
  if IsFlush(index) and IsStraight(index):
    return True
  return False

def IsFlush(index):
  #フラッシュの判定
  for i in range(4):
    if GetCardSuits(index[i]) != GetCardSuits(index[i+1]):
      return False
  return True

def IsStraight(index):
  straight_index=[]
  for i in range(len(index)):
    straight_index.append(int((index[i])[1:]))
  straight_index.sort()
  if straight_index == [1,6,7,8,9]:
    return True
  for i in range(len(straight_index)-1):
    if straight_index[i+1] - straight_index[i] != 1:
      return False
  return True

def CountSameRankLine(index):
  #ペア系の判定
  count = 0
  j = 0
  for i in range(5):
    for j in range(i+1,5):
      if GetCardNum(index[i]) == GetCardNum(index[j]):
        count += 1
  return count

def IsQuads(index):
  count = CountSameRankLine(index)
  return count == 6

def IsFullHouse(index):
  count = CountSameRankLine(index)
  return count == 4

def IsTrips(index):
  count = CountSameRankLine(index)
  return count == 3

def IsTwoPair(index):
  count = CountSameRankLine(index)
  return count == 2

def IsOnePair(index):
  count = CountSameRankLine(index)
  return count == 1

def qualify(index):
  if IsStraightFlush(index):
     return 'StraightFlush'
  elif IsQuads(index):
    return 'Four of a kind'
  elif IsFullHouse(index):
    return 'FullHouse'
  elif IsFlush(index):
    return 'Flush'
  elif IsStraight(index):
    return 'Straight'
  elif IsTrips(index):
    return 'Tree of a kind'
  elif IsTwoPair(index):
    return 'TwoPair'
  elif IsOnePair(index):
    return 'OnePair'
  else:
    return 'High card'


