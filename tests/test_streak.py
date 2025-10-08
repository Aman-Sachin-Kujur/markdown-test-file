import pytest
from streak import longest_positive_streak

def test_empty_list():
    """Test that an empty list returns a streak of 0."""
    assert longest_positive_streak([]) == 0

def test_longest_streak_in_the_middle():
    """Test finding the longest streak when it's surrounded by non-positives."""
    assert longest_positive_streak([2, 3, -1, 5, 6, 7, 0, 4]) == 3

def test_all_positive_numbers():
    """Test a list containing only positive numbers."""
    assert longest_positive_streak([1, 2, 3, 4, 5]) == 5

def test_all_non_positive_numbers():
    """Test a list with no positive numbers."""
    assert longest_positive_streak([-1, -5, 0, -10]) == 0

def test_streak_at_the_beginning():
    """Test when the longest streak is at the start of the list."""
    assert longest_positive_streak([4, 5, 6, 0, 1, 2]) == 3

def test_streak_at_the_end():
    """Test when the longest streak is at the end of the list."""
    assert longest_positive_streak([1, 2, 0, 4, 5, 6, 7]) == 4

def test_single_element_list():
    """Test lists with a single element."""
    assert longest_positive_streak([10]) == 1
    assert longest_positive_streak([-5]) == 0
    assert longest_positive_streak([0]) == 0

def test_with_zeros_and_negatives():
    """Test a mix of positive, zero, and negative numbers."""
    assert longest_positive_streak([1, 0, 2, 3, -4, 5, 6, 7, 8, 0, 9]) == 4