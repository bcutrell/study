# visualizing sorting algorithms
# www.sorting-algorithms.com
# visualgo.net

# bubble
# multiple passes to compare adjacent items and exchanges those that are out of order
# each "bubbles" up to the location it belongs

def bubble_sort(alist):
    print(alist)
    # count in reverse
    for n in range(len(alist)-1, 0, -1):

        for k in range(n):
            if alist[k] > alist[k+1]:
                print('indicies', n, k)
                print('swap', alist[k], alist[k+1])
                temp = alist[k]
                alist[k] = alist[k+1]
                alist[k+1] = temp
                
    return alist

# test = [5,3,1,2,4]
# print(bubble_sort(test))

# selection sort
# looks for largest value as it makes a pass and, after completing the pass, 
# place it in the proper location

def selection_srt(alist):
    for n in range(len(alist)-1, 0, -1):
        max_idx = 0
        for k in range(1,n+1):
            
            if alist[k] > alist[max_idx]:
                max_idx = k
                maxn = alist[k]
                max_idx = k
        temp = alist[k]
        alist[n] = alist[max_idx]
        alist[max_idx] = temp

    return alist
    
# test = [5,3,1,2,4]
# print(selection_srt(test))

# insertion sort
# always maintains a sorted sublist in the lower positions of the list
# each new item is then "inserted" back into the previous sublist 
# such that the sorted sublist is one item larger

def insertion_sort(arr):
    # n - 1 passes

    # For every index in array
    for i in range(1,len(arr)):
        
        # Set current values and position
        currentvalue = arr[i]
        position = i
        
        print(currentvalue, position)
        # Sorted Sublist
        while position>0 and arr[position-1]>currentvalue:
            print(arr)
            arr[position]=arr[position-1]
            position = position-1

        arr[position]=currentvalue
    return arr

# test = [5,3,1,2,4, 9, 0, 50]
# print(insertion_sort(test))

# shell sort
# similar to insertion but it creates a series of sublists
# each sublist is using insertion_sort
# the key is breaking up the sublists

def shell_sort(arr):
    sublistcount = len(arr)//2
    while sublistcount > 0:
        for start in range(sublistcount):

            gap_insertion_sort(arr, start, sublistcount)
        
        print('After increments of size', sublistcount)
        print('List', arr)
        sublistcount = sublistcount//2
    return arr

def gap_insertion_sort(arr, start, gap):
    for i in range(start+gap, len(arr), gap):
        currentvalue = arr[i]
        position = i
        while position >= gap and arr[position-gap] > currentvalue:
            arr[position] = arr[position-gap]
            position = position-gap
        
        arr[position] = currentvalue

test = [5,3,1,2,4, 9, 0, 50]
print(shell_sort(test))

# 