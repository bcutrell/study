# implement lempel-ziv-welch
# https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

encode_dict = {' ': 0, '.': 27}

for n in range(1, 27):
    letter = chr(ord('a') + n-1)
    encode_dict[letter] = n

# swap keys and values
decode_dict = dict((v,k) for k,v in encode_dict.items())

def encode_lzw(string):
    return [ encode_dict[char] for char in string ]

def decode_lzw(string):
    return ''.join([ decode_dict[char] for char in string ])

string1 = 'cat dog.'
assert(decode_lzw(encode_lzw(string1)) == string1)

string2 = 'the shovel was a ground breaking invention.'
assert(decode_lzw(encode_lzw(string2)) == string2)
