'''
You're presented with a sequence of cards, some face up, some face down. 
You can remove any face up card, but you must then flip the adjacent cards (if any). 
The goal is to successfully remove every card. Making the wrong move can get you stuck.

In this challenge, a 1 signifies a face up card and a 0 signifies a face down card. 
We will also use zero-based indexing, starting from the left, to indicate specific cards. 
So, to illustrate a game, consider this starting card set.

Sample Inputs
0100110
01001100111
100001100101000

Sample Outputs
1 0 2 3 5 4 6
no solution
0 1 2 3 4 6 5 7 8 11 10 9 12 13 14
'''

# https://www.reddit.com/r/dailyprogrammer/comments/aq6gfy/20190213_challenge_375_intermediate_a_card/
# https://www.youtube.com/watch?v=CCxs-tu8tOU

import code

FACE_UP = '1'
FACE_DOWN = '0'

def flip_cards(seq):
    try_seq = list(seq) # convert string to list

    solution = []
    i = 0
    while i < len(try_seq):
        card = try_seq[i]

        if card == FACE_UP:
            solution.append(str(i))
            try_seq[i] = '.' # try flipping it

            # flip adjacent cards
            adjacents = []
            if i > 0:
                adjacents.append(i-1)
            if i < len(try_seq)-1:
                adjacents.append(i+1)

            for idx in adjacents:
                if try_seq[idx] == '0':
                    try_seq[idx] = '1'
                elif try_seq[idx] == '1':
                    try_seq[idx] = '0'

            if i != 0:
                i = 0
            else:
                i += 1

        else:
            i += 1

    if all([x == '.' for x in try_seq]):
        return solution
    else:
        return 'no solution'

cases = [
    ('0100110', '1023546'),
    ('1100', 'no solution'),
    ('01001100111','no solution'),
    ('100001100101000', '01234657811109121314')
]

for case, expected in cases:
    print("\n")
    print(case)

    result = flip_cards(case)
    print(''.join(result), expected)
    assert ''.join(result) == expected

