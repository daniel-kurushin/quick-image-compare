# quick-image-compare

The idea of this tool is to demonstrate very simple image comparison method,
with rather good performance.

## compare.py

Image comparison and thumbnailin

## dedublicate.py

To find dublicates and move 'em to /tmp/ folder.
Tolerance is added to the file name to debug.

## Usage

$ dedublicate /path/

will search for dublicate images down the tree starting from /path/.
All images supposed to be dublicates of other are moved to /tmp.
Can be slow and memory unefficient on large datasets.
It's demo, not real tool.
