from typing import List

def longest_positive_streak(nums: List[int]) -> int:
    """
    Calculates the length of the longest consecutive run of strictly positive integers.

    Args:
        nums: A list of integers.

    Returns:
        The length of the longest streak of positive numbers.
        Returns 0 if the list is empty or contains no positive numbers.
    """
    max_streak = 0
    current_streak = 0
    for num in nums:
        if num > 0:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 0
    max_streak = max(max_streak, current_streak)
    return max_streak