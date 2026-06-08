import sys
import random
SUITS =[' Clubs',' Diemonds',' Hearts',' Spades',]
RANKS =[' 2',' 3',' 4',' 5','6',' 7',' 8',' 9',' 10',' Jack',' Queen',' King',' ACE',]
m = int(sys.argv[1])
n = int(sys.argv[2])
perm = [i for i in range(n)]
for i in range(m):
    r= random.randrange(i, n)
    perm[r] , perm[i] = perm[i] , perm[r]
for i in range(m):
    rank_index =perm[i] % 13
    suit_index =perm[i] // 13
print(RANKS[rank_index] + "of" + SUITS[suit_index])
print()
