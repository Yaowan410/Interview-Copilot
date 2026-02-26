# Merge Two Sorted Lists

## Problem Summary

You are given the heads of two sorted linked lists `l1` and `l2`.

Merge the two lists into one sorted linked list and return its head.

The merged list should be made by splicing together the nodes of the first two lists.

---

## Pattern

Two Pointers (Linked List Merge)

---

## Key Idea

Since both lists are already sorted, we can merge them similarly to the merge step in Merge Sort.

We maintain two pointers:
- One for each list
- At each step, choose the smaller node
- Move the pointer forward

Use a dummy node to simplify edge cases.

---

## Step-by-Step Approach

1. Create a dummy node to act as the start of the merged list.
2. Maintain a pointer `current` pointing to the dummy.
3. While both lists are not empty:
   - Compare `l1.val` and `l2.val`
   - Attach the smaller node to `current.next`
   - Move that list pointer forward
   - Move `current` forward
4. After the loop, attach the remaining part of the non-empty list.
5. Return `dummy.next`.

---

## Python Template

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(l1, l2):
    dummy = ListNode()
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next

        current = current.next

    # Attach remaining nodes
    current.next = l1 if l1 else l2

    return dummy.next
```

---

## Complexity

Time Complexity: O(n + m)  
Space Complexity: O(1)

Where:
- n = length of l1
- m = length of l2

Reason:
- Each node is visited exactly once.
- No extra data structures are used.

---

## Edge Cases

- One list is empty
- Both lists are empty
- Lists of unequal lengths
- All elements in one list are smaller than the other
- Duplicate values

---

## Common Mistakes

- Forgetting to use a dummy node
- Not attaching the remaining list
- Losing reference to head of merged list
- Incorrect pointer updates

---

## Self-Check Examples

Example 1:
l1 = 1 → 2 → 4  
l2 = 1 → 3 → 4  

Output:
1 → 1 → 2 → 3 → 4 → 4

Example 2:
l1 = []  
l2 = [0]  

Output:
0

Example 3:
l1 = []  
l2 = []  

Output:
[]

---

## Follow-Up

1. Can you solve this recursively?

Yes. Recursively compare heads and connect smaller node.

2. What if the lists are extremely large?

Iterative solution avoids recursion stack overflow.

3. How is this related to Merge Sort?

This is exactly the merge step of Merge Sort.