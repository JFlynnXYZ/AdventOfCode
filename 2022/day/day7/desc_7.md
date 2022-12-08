# --- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear
much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

<pre>
$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
</pre>

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For
example:

<pre>
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
</pre>

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called <code>/</code>. You can navigate around the filesystem, moving into or out of
directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with <code>$</code> are __commands you executed__, very much like some
modern computers:

- <code>cd</code> means __change directory__. This changes which directory is the current directory, but the specific
result depends on the argument:
    - <code>cd x</code> moves __in__ one level: it looks in the current directory for the directory named <code>x</code>
and makes it the current directory.
  - <code>cd ..</code> moves __out__ one level: it finds the directory that contains the current directory, then makes
that directory the current directory.
  - <code>cd /</code> switches the current directory to the outermost directory, <code>/</code>.



<code>ls</code> means __list__. It prints out all of the files and directories immediately contained by the current
directory:
    - <code>123 abc</code> means that the current directory contains a file named <code>abc</code> with size
<code>123</code>.
  - <code>dir xyz</code> means that the current directory contains a directory named <code>xyz</code>.




Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

<pre>
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
</pre>

Here, there are four directories: <code>/</code> (the outermost directory), <code>a</code> and <code>d</code> (which are
in <code>/</code>), and <code>e</code> (which is in <code>a</code>). These directories also contain files of various
sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To
do this, you need to determine the __total size__ of each directory. The total size of a directory is the sum of the
sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic
size.)

The total sizes of the directories above can be found as follows:

- The total size of directory <code>e</code> is __584__ because it contains a single file <code>i</code> of size 584 and
no other directories.
- The directory <code>a</code> has total size __94853__ because it contains files <code>f</code> (size 29116),
<code>g</code> (size 2557), and <code>h.lst</code> (size 62596), plus file <code>i</code> indirectly (<code>a</code>
contains <code>e</code> which contains <code>i</code>).
- Directory <code>d</code> has total size __24933642__.
- As the outermost directory, <code>/</code> contains every file. Its total size is __48381165__, the sum of the size of
every file.

To begin, find all of the directories with a total size of __at most 100000__, then calculate the sum of their total
sizes. In the example above, these directories are <code>a</code> and <code>e</code>; the sum of their total sizes is
<code><b>95437</b></code> (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. __What is the sum of the total sizes of those
directories?__
