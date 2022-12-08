# --- Day 6: Tuning Trouble ---
The preparations are finally complete; you and the Elves leave camp on foot and begin to make your way toward the
__star__ fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a handheld __device__. He says that it has many
fancy features, but the most important one to set up right now is the __communication system__.

However, because he's heard you have [significant](/2016/day/6) [experience](/2016/day/25) [dealing](/2019/day/7)
[with](/2019/day/9) [signal-based](/2019/day/16) [systems](/2021/day/25), he convinced the other Elves that it would be
okay to give you their one malfunctioning device - surely you'll have no problem fixing it.

As if inspired by comedic timing, the device emits a few colorful sparks.

To be able to communicate with the Elves, the device needs to __lock on to their signal__. The signal is a series of
seemingly-random characters that the device receives one at a time.

To fix the communication system, you need to add a subroutine to the device that detects a __start-of-packet marker__ in
the datastream. In the protocol being used by the Elves, the start of a packet is indicated by a sequence of __four
characters that are all different__.

The device will send your subroutine a datastream buffer (your puzzle input); your subroutine needs to identify the
first position where the four most recently received characters were all different. Specifically, it needs to report the
number of characters from the beginning of the buffer to the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

<pre>
mjqjpqmgbljsphdztnvjfqwrcgsmlb</pre>

After the first three characters (<code>mjq</code>) have been received, there haven't been enough characters received
yet to find the marker. The first time a marker could occur is after the fourth character is received, making the most
recent four characters <code>mjqj</code>. Because <code>j</code> is repeated, this isn't a marker.

The first time a marker appears is after the __seventh__ character arrives. Once it does, the last four characters
received are <code>jpqm</code>, which are all different. In this case, your subroutine should report the value
<code><b>7</b></code>, because the first start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

- <code>bvwbjplbgvbhsrlpgdmjqwftvncz</code>: first marker after character <code><b>5</b></code>
- <code>nppdvjthqldpwncqszvftbrmjlhg</code>: first marker after character <code><b>6</b></code>
- <code>nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg</code>: first marker after character <code><b>10</b></code>
- <code>zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw</code>: first marker after character <code><b>11</b></code>

__How many characters need to be processed before the first start-of-packet marker is detected?__
