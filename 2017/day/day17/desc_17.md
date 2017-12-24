# --- Day 17: Spinlock ---
Suddenly, whirling in the distance, you notice what looks like a massive, pixelated hurricane: a deadly
[spinlock](https://en.wikipedia.org/wiki/Spinlock). This spinlock isn't just consuming computing power, but memory, too;
vast, digital mountains are being ripped from the ground and consumed by the vortex.

If you don't move quickly, fixing that printer will be the least of your problems.

This spinlock's algorithm is simple but efficient, quickly consuming everything in its path. It starts with a circular
buffer containing only the value ```0```, which it marks as the __current position__. It then steps forward through the
circular buffer some number of steps (your puzzle input) before inserting the first new value, ```1```, after the value
it stopped on.  The inserted value becomes the __current position__. Then, it steps forward from there the same number
of steps, and wherever it stops, inserts after it the second new value, ```2```, and uses that as the new __current
position__ again.

It repeats this process of __stepping forward__, __inserting a new value__, and __using the location of the inserted
value as the new current position__ a total of ```__2017__``` times, inserting ```2017``` as its final operation, and
ending with a total of ```2018``` values (including ```0```) in the circular buffer.

For example, if the spinlock were to step ```3``` times per insert, the circular buffer would begin to evolve like this
(using parentheses to mark the current position after each iteration of the algorithm):

- ```(0)```, the initial state before any insertions.
- ```0(1)```: the spinlock steps forward three times (```0```, ```0```, ```0```), and then inserts the first value,
```1```, after it. ```1``` becomes the current position.
- ```0(2)1```: the spinlock steps forward three times (```0```, ```1```, ```0```), and then inserts the second value,
```2```, after it. ```2``` becomes the current position.
- ```02(3)1```: the spinlock steps forward three times (```1```, ```0```, ```2```), and then inserts the third value,
```3```, after it. ```3``` becomes the current position.

And so on:

- ```02(4)31```
- ```0(5)2431```
- ```05243(6)1```
- ```05(7)24361```
- ```057243(8)61```
- ```0(9)57243861```

Eventually, after 2017 insertions, the section of the circular buffer near the last insertion looks like this:

```
1512  1134  151 (2017) 638  1513  851```
Perhaps, if you can identify the value that will ultimately be __after__ the last value written (```2017```), you can
short-circuit the spinlock.  In this example, that would be ```638```.

__What is the value after ```2017```__ in your completed circular buffer?
