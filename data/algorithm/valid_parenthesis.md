# Valid Parentheses

## Problem Summary

Given a string `s` containing just the characters:

    '(', ')', '{', '}', '[' and ']'

Determine if the input string is valid.

A string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every closing bracket has a corresponding opening bracket.

---

## Pattern

Stack (Last-In-First-Out)

---

## Key Idea

We use a stack to track opening brackets.

When we see:
- An opening bracket → push it onto the stack
- A closing bracket → check if it matches the top of the stack

If it does not match or the stack is empty, the string is invalid.

At the end, the stack must be empty for the string to be valid.

---

## Step-by-Step Approach

1. Initialize an empty stack.
2. Create a mapping of closing brackets to opening brackets:
   
       pairs = {')': '(', '}': '{', ']': '['}

3. Iterate through each character in the string:
   - If it's an opening bracket → push onto stack
   - If it's a closing bracket:
       - If stack is empty → return False
       - Pop from stack and check if it matches
4. After iteration, return True only if stack is empty.

---

## Python Template

```python
def is_valid(s):
    stack = []
    pairs = {
        ')': '(',
        '}': '{',
        ']': '['
    }

    for char in s:
        if char in pairs:
            # Closing bracket
            if not stack:
                return False

            top = stack.pop()
            if top != pairs[char]:
                return False
        else:
            # Opening bracket
            stack.append(char)

    return len(stack) == 0
```

---

## Complexity

Time Complexity: O(n)  
Space Complexity: O(n)

Reason:
- Each character is processed once.
- Stack may store up to n elements.

---

## Edge Cases

- Empty string → valid
- Single character → invalid
- Only opening brackets
- Only closing brackets
- Nested brackets
- Incorrect order (e.g., "(]")

---

## Common Mistakes

- Not checking if stack is empty before popping
- Forgetting to verify stack is empty at the end
- Treating all characters as valid brackets
- Using multiple if-else blocks instead of a mapping

---

## Self-Check Examples

Example 1:
s = "()"
Output: True

Example 2:
s = "()[]{}"
Output: True

Example 3:
s = "(]"
Output: False

Example 4:
s = "([)]"
Output: False

Example 5:
s = "{[]}"
Output: True

---

## Follow-Up

How would you modify this if the string contains other characters besides brackets?

Answer:
- Only process bracket characters
- Ignore all other characters

Another variation:
- What if we want to validate HTML/XML tags?
  → Use stack but match tag names instead of single characters.