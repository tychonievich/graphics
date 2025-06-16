#!/bin/bash
here="$(dirname "$(readlink -f "$0")")/md/text"
updates=0

for f in "$here/"*md "$0"
do
    if [ "$f" != "$here/index.md" ] && [ "$f" != "$here/outline.md" ] && [ "$f" -nt "$here/index.md" ]
    then let updates+=1
    fi
done

if [ $updates -gt 0 ]
then
cat > "$here/index.md" <<EOF
---
title: Texts
...

A collection of references written by course instructors.

Luther Tychonievich began creating these in 2006 when a teaching assistant for a computer graphics course at BYU
based on observations of content that was missing or poorly explained in that course's textbook, and updated and added to that many times since then.
Because of that history, they vary widely in writing style and level of detail.

The pages are listed below in no particular order.
Those that are not listed from the [content page](../content.html) may be incomplete or out of date.

EOF

for f in "$here/"*md
do
    if [ "$f" != "$here/index.md" ] && [ "$f" != "$here/outline.md" ]
    then 
        echo "- ["$(grep 'title:' "$f" | head -1 | cut -d: -f2)" ]("$(basename "${f%md}html")"): "$(grep 'summary:' "$f" | head -1 | cut -d: -f2). >> "$here/index.md"
    fi
done

fi
