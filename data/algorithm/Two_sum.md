# Two Sum

## Problem Summary

Given an integer array `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

Assume:
- Exactly one solution exists.
- You may not use the same element twice.
- The order of indices does not matter.

---

## Pattern

Hash Map (Dictionary lookup)

---

## Key Idea

Instead of checking all pairs in O(n²) time, we use a dictionary to store previously seen numbers.

For each number `num`, we compute:

    complement = target - num

If the complement already exists in the dictionary, we have found the solution.

This reduces time complexity to O(n).

---

## Step-by-Step Approach

1. Initialize an empty dictionary `seen = {}`.
2. Iterate through the array using `enumerate`.
3. For each element:
   - Compute `complement = target - num`
   - If complement exists in `seen`, return the pair of indices
4. Otherwise store `seen[num] = i`
5. Continue until the solution is found

---

## Python Template

```python
def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return None
```

---

## Complexity

Time Complexity: O(n)  
Space Complexity: O(n)

Reason:
- Each element is processed once.
- Dictionary lookup is O(1) average case.

---

## Edge Cases

- Duplicate values (e.g., [3, 3])
- Negative numbers
- Large input size
- Target equals twice a number
- No solution case (if problem variant allows it)

---

## Common Mistakes

- Inserting into dictionary before checking complement
- Overwriting duplicate keys incorrectly
- Forgetting that dictionary keys must be unique
- Returning values instead of indices

---

## Self-Check Examples

Example 1:
nums = [2, 7, 11, 15]
target = 9
Output: [0, 1]

Example 2:
nums = [3, 3]
target = 6
Output: [0, 1]

Example 3:
nums = [-1, -2, -3, -4, -5]
target = -8
Output: [2, 4]

---

## Follow-Up

If the array is sorted, we can use the Two Pointers technique:

- Left pointer at start
- Right pointer at end
- Move pointers inward based on comparison

This reduces space complexity to O(1).