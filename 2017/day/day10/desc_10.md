# --- Day 10: Knot Hash ---
You come across some programs that are trying to implement a software emulation of a hash based on knot-tying. The hash
these programs are implementing isn't very strong, but you decide to help them anyway. You make a mental note to remind
the Elves later not to invent their own cryptographic functions.

This hash function simulates tying a knot in a circle of string with 256 marks on it. Based on the input to be hashed,
the function repeatedly selects a span of string, brings the ends together, and gives the span a half-twist to reverse
the order of the marks within it. After doing this many times, the order of the marks is used to build the resulting
hash.

```
  4--5   pinch   4  5           4   1
 /    \  5,0,1  / \/ \  twist  / \ / \
3      0  -->  3      0  -->  3   X   0
 \    /         \ /\ /         \ / \ /
  2--1           2  1           2   5
```
To achieve this, begin with a __list__ of numbers from ```0``` to ```255```, a __current position__ which begins at
```0``` (the first element in the list), a __skip size__ (which starts at ```0```), and a sequence of __lengths__ (your
puzzle input).  Then, for each length:

- __Reverse__ the order of that __length__ of elements in the __list__, starting with the element at the __current
position__.
- __Move__ the __current position__ forward by that __length__ plus the __skip size__.
- __Increase__ the __skip size__ by one.

The __list__ is circular; if the __current position__ and the __length__ try to reverse elements beyond the end of the
list, the operation reverses using as many extra elements as it needs from the front of the list. If the __current
position__ moves past the end of the list, it wraps around to the front. __Lengths__ larger than the size of the
__list__ are invalid.

Here's an example using a smaller list:

Suppose we instead only had a circular list containing five elements, ```0, 1, 2, 3, 4```, and were given input lengths
of ```3, 4, 1, 5```.

- The list begins as ```[0] 1 2 3 4``` (where square brackets indicate the __current position__).
- The first length, ```3```, selects ```([0] 1 2) 3 4``` (where parentheses indicate the sublist to be reversed).
- After reversing that section (```0 1 2``` into ```2 1 0```), we get ```([2] 1 0) 3 4```.
- Then, the __current position__ moves forward by the __length__, ```3```, plus the __skip size__, 0: ```2 1 0 [3] 4```.
Finally, the __skip size__ increases to ```1```.

- The second length, ```4```, selects a section which wraps: ```2 1) 0 ([3] 4```.
- The sublist ```3 4 2 1``` is reversed to form ```1 2 4 3```: ```4 3) 0 ([1] 2```.
- The __current position__ moves forward by the __length__ plus the __skip size__, a total of ```5```, causing it not to
move because it wraps around: ```4 3 0 [1] 2```. The __skip size__ increases to ```2```.

- The third length, ```1```, selects a sublist of a single element, and so reversing it has no effect.
- The __current position__ moves forward by the __length__ (```1```) plus the __skip size__ (```2```): ```4 [3] 0 1
2```. The __skip size__ increases to ```3```.

- The fourth length, ```5```, selects every element starting with the second: ```4) ([3] 0 1 2```. Reversing this
sublist (```3 0 1 2 4``` into ```4 2 1 0 3```) produces: ```3) ([4] 2 1 0```.
- Finally, the __current position__ moves forward by ```8```: ```3 4 2 1 [0]```. The __skip size__ increases to ```4```.

In this example, the first two numbers in the list end up being ```3``` and ```4```; to check the process, you can
multiply them together to produce ```12```.

However, you should instead use the standard list size of ```256``` (with values ```0``` to ```255```) and the sequence
of __lengths__ in your puzzle input. Once this process is complete, __what is the result of multiplying the first two
numbers in the list__?
