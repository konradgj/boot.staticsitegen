import os
import shutil
import sys
from helpers import *


def main():
    basepath = '/'
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    source = "static"
    target = "docs"
    if os.path.exists(target):
        shutil.rmtree(target)
    copyStatic(source, target)

    generatePagesR('content', 'template.html', 'docs/', basepath)

    return


main()
