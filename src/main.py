import os
import shutil

from helpers import *


def main():
    source = "static"
    target = "public"
    if os.path.exists(target):
        shutil.rmtree(target)
    copyStatic(source, target)

    generatePagesR('content', 'template.html', 'public/')

    return


main()
