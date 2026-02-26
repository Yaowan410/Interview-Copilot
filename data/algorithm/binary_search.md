# Binary Search

## Problem Summary

Given a sorted array `nums` and a target value `target`, return the index of the target if it exists.

If the target does not exist, return -1.

Assumptions:
- The array is sorted in ascending order.
- No duplicate elements (basic version).

---

## Pattern

Binary Search (Divide and Conquer)

---

## Key Idea

Since the array is sorted, we can repeatedly divide the search space in half.

At each step:
- Compare the middle element with the target.
- If equal → return index.
- If target is smaller → search left half.
- If target is larger → search right half.

This reduces time complexity from O(n) to O(log n).

---

## Step-by-Step Approach

1. Initialize two pointers:
   - left = 0
   - right = len(nums) - 1

2. While left <= right:
   - Compute mid = left + (right - left) // 2
   - If nums[mid] == target → return mid
   - If nums[mid] < target → search right half
       left = mid + 1
   - Else → search left half
       right = mid - 1

3. If loop ends, target does not exist → return -1

---

## Python Template

```python
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

---

## Complexity

Time Complexity: O(log n)  
Space Complexity: O(1)

Reason:
- Each iteration halves the search space.
- No additional data structures used.

---

## Edge Cases

- Empty array → return -1
- Single element array
- Target smaller than smallest element
- Target larger than largest element
- Off-by-one errors in loop condition

---

## Common Mistakes

- Using (left + right) // 2 without considering overflow (in some languages)
- Incorrect loop condition (left < right vs left <= right)
- Infinite loop due to wrong pointer updates
- Forgetting to return -1 when not found

---

## Self-Check Examples

Example 1:
nums = [-1, 0, 3, 5, 9, 12]
target = 9
Output: 4

Example 2:
nums = [-1, 0, 3, 5, 9, 12]
target = 2
Output: -1

Example 3:
nums = [1]
target = 1
Output: 0

Example 4:
nums = []
target = 5
Output: -1

---

## Follow-Up

1. What if duplicates exist?
   → Modify binary search to find leftmost or rightmost occurrence.

2. What if array is rotated?
   → Use modified binary search for rotated sorted array.

3. What if the search space is very large?
   → Use binary search on answer space (e.g., search for minimal feasible value).