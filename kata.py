def longest_consecutive(nums):
    """
    Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
    You must write an algorithm that runs in O(n) time.

    Example 1:
        Input: nums = [100,4,200,1,3,2]
        Output: 4
        Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

    Example 2:
        Input: nums = [0,3,7,2,5,8,4,6,0,1]
        Output: 9
    """
    max_consecutive = 0
    num_set = set(nums)

    for num in num_set:
        if num - 1 not in num_set:
            curr_num = num
            curr_streak = 1

            while curr_num + 1 in num_set:
                curr_num += 1
                curr_streak += 1

            max_consecutive = max(max_consecutive, curr_streak)

    return max_consecutive

def main():
    # test longest_consecutive
    test_cases = [
        ([100,4,200,1,3,2], 4),
        ([0,3,7,2,5,8,4,6,0,1], 9),
    ]
    for nums, expected in test_cases:
        print(f"Testing with nums={nums}, expected={expected}")
        print(f"longest_consecutive({nums}) = {longest_consecutive(nums)}")
        assert longest_consecutive(nums) == expected

if __name__ == "__main__":
    main()
