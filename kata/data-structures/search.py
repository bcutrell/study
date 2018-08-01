
def seq_search(arr, ele):
    pos = 0
    found = False

    while pos < len(arr) and not found:
        if arr[pos] == ele:
            found = True
        else:
            pos += 1

def ordered_seq_search(arr, ele):
    """
    Input array must be sorted
    """
    pos = 0
    found = False
    stopped = False

    while pos < len(arr) and not found and not stopped:
        if arr[pos] == ele:
            found = True
        else:
            if arr[pos] > ele:
                stopped = True
            else:
                pos += 1

def binary_search():
    first = 0
    last = len(arr) - 1
    found = False
    while first <= last and not found:
        mid = ( first + last )/2

        if arr[mid] == ele:
            found = True
        else:
            if ele < arr[mid]:
                last = mid-1
            else:
                first = mid+1
    
    return found

def rec_bin_search(arr, ele):
    if len(arr) == 0:
        return False
    else:
        mid = len(arr) / 2
        if arr[mid] == ele:
            return True
        else:
            if ele < arr[mid]:
                return rec_bin_search(arr[:mid])
            else:
                return rec_bin_search(arr[mid+1:])


# Hash table
# A collection of items which are stored in asuch a way as to make it easy to find them letter
# Hash function
# mapping between an item and the slot where that item belongs in the hash
# Collision
# having two items in the same slot

# collison resolution 
# open addressing -> linear probing
# looking for the next open slot
# chaining
# allow mulitple items to be in a single slot
