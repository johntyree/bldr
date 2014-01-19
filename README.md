bldr
====

A very simple builder for sharing examples.

bldr searches your file for lines containing the magic string
"`bldr: <command> [# comment]`".
It then runs the commands in order from top to bottom. Everything between
`bldr:` and `#` is the command. Everything else on the line is ignored.

It supports a few magical Vim variables to smartly find and manipulate the file
path and name. Currently this is just `%` with the modifiers `:p` and `:r`.

From Vim's help (`:help expand`):

```
%		current file name
Modifiers:
        :p		expand to full path
        :h		head (last path component removed)
        :t		tail (last path component only)
        :r		root (one extension removed)
        :e		extension only
```

You may think to yourself, "Hey. This is just shell scripting, minus all the
features." You're right. That's it.

```
// bldr: gcc -lm -o %:r %  # compile and link with math lib
// bldr: ./%:r  # run
// bldr: rm %:r  # cleanup

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>

int main() {
    printf("%f\n", sin(M_PI_4));
    return 0;
}
```
