"""News-image entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file. The program copies it
to /output/entry.png. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
