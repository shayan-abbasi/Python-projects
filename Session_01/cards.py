SUITS = ['Clubs','Diamonds','Hearts','Spades']
RANKS = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','ACE']
deck = []
for rank in RANKS :
    for suit in SUITS :
        card = rank + 'of' + suit 
        deck .append (card)
for c in deck:
 print (c)
