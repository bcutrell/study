# implement lempel-ziv-welch
# https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

def encode_lzw(uncompressed):
    '''
    *     PSEUDOCODE
    Initialize table with single character strings
    P = first input character
    WHILE not end of input stream
    C = next input character
    IF P + C is in the string table
    P = P + C
    ELSE
    output the code for P
    add P + C to the string table
    P = C
    END WHILE
    output code for P
    '''
    dictionary = {chr(i+96): i for i in range(1, 27)}
    dictionary[chr(32)] = 0
    dictionary[chr(46)] = 27
    dict_size = len(dictionary)

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

def decode_lzw(compressed):
    '''
    *    PSEUDOCODE
    Initialize table with single character strings
    OLD = first input code
    output translation of OLD
    WHILE not end of input stream
    NEW = next input code
    IF NEW is not in the string table
    S = translation of OLD
    S = S + C
    ELSE
    S = translation of NEW
    output S
    C = first character of S
    OLD + C to the string table
    OLD = NEW
    END WHILE
    '''

    dictionary = {chr(i+96): i for i in range(1, 27)}
    dictionary[chr(32)] = 0
    dictionary[chr(46)] = 27
    dict_size = len(dictionary)
    dictionary = dict((v,k) for k,v in dictionary.items())

    w = result = dictionary[compressed.pop(0)]

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result += entry
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    return result

string1 = 'cat dog.'
assert(decode_lzw(encode_lzw(string1)) == string1)

string2 = 'the shovel was a ground breaking invention.'
assert(decode_lzw(encode_lzw(string2)) == string2)

