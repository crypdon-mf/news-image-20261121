"""News-image entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file. The program copies it
to /output/entry.png. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Why a copy and not a draw: the grader runs the program with no network and
only the standard library, so no image library is available at run time.
The image is drawn beforehand by generate_image.py (Pillow, run on the
build machine) and shipped in the repository; this program just places
those exact bytes at the output path, so both of the grader's runs write
the same bytes.
"""

import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
