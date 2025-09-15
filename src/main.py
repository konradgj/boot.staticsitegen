import os
import shutil

from helpers import *


def main():
    source = "static"
    target = "public"
    if os.path.exists(target):
        shutil.rmtree(target)
    copyStatic(source, target)

    generatePage('content/index.md', 'template.html', 'public/index.html')

    return


main()
