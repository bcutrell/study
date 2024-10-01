import sys
sys.setrecursionlimit(2000)
from collections import Counter
from functools import reduce

def f(n):
    pass

if __name__ == "__main__":
    total_test_cases = int(sys.stdin.readline().rstrip())

    for _ in range(total_test_cases):
        test_case = [int(val) for val in sys.stdin.readline().split(' ')][0]

        result = f()
        print(result)
