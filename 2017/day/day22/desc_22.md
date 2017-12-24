# --- Day 22: Sporifica Virus ---
Diagnostics indicate that the local __grid computing cluster__ has been contaminated with the __Sporifica Virus__. The
grid computing cluster is a seemingly-infinite two-dimensional grid of compute nodes.  Each node is either __clean__ or
__infected__ by the virus.
To [prevent overloading](https://en.wikipedia.org/wiki/Morris_worm#The_mistake) the nodes (which would render them
useless to the virus) or detection by system administrators, exactly one __virus carrier__ moves through the network,
infecting or cleaning nodes as it moves. The virus carrier is always located on a single node in the network (the
__current node__) and keeps track of the __direction__ it is facing.

To avoid detection, the virus carrier works in bursts; in each burst, it __wakes up__, does some __work__, and goes back
to __sleep__. The following steps are all executed __in order__ one time each burst:

- If the __current node__ is __infected__, it turns to its __right__.  Otherwise, it turns to its __left__. (Turning is
done in-place; the __current node__ does not change.)
- If the __current node__ is __clean__, it becomes __infected__.  Otherwise, it becomes __cleaned__. (This is done
__after__ the node is considered for the purposes of changing direction.)
- The virus carrier [moves](https://www.youtube.com/watch?v=2vj37yeQQHg) __forward__ one node in the direction it is
facing.

Diagnostics have also provided a __map of the node infection status__ (your puzzle input).  __Clean__ nodes are shown as
```.```; __infected__ nodes are shown as ```#```.  This map only shows the center of the grid; there are many more nodes
beyond those shown, but none of them are currently infected.

The virus carrier begins in the middle of the map facing __up__.

For example, suppose you are given a map like this:

```
..#
#..
...
```
Then, the middle of the infinite grid looks like this, with the virus carrier's position marked with ```[ ]```:

```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
The virus carrier is on a __clean__ node, so it turns __left__, __infects__ the node, and moves left:

```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]# . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
The virus carrier is on an __infected__ node, so it turns __right__, __cleans__ the node, and moves up:

```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . . # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
Four times in a row, the virus carrier finds a __clean__, __infects__ it, turns __left__, and moves forward, ending in
the same place and still facing up:

```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . #[#]. # . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
Now on the same node as before, it sees an infection, which causes it to turn __right__, __clean__ the node, and move
forward:

```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . # .[.]# . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
After the above actions, a total of ```7``` bursts of activity had taken place. Of them, ```5``` bursts of activity
caused an infection.

After a total of ```70```, the grid looks like this, with the virus carrier facing up:

```
. . . . . # # . .
. . . . # . . # .
. . . # . . . . #
. . # . #[.]. . #
. . # . # . . # .
. . . . . # # . .
. . . . . . . . .
. . . . . . . . .
```
By this time, ```41``` bursts of activity caused an infection (though most of those nodes have since been cleaned).

After a total of ```10000``` bursts of activity, ```5587``` bursts will have caused an infection.

Given your actual map, after ```10000``` bursts of activity, __how many bursts cause a node to become infected__? (Do
not count nodes that begin infected.)
