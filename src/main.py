import os
import shutil


def copyStatic(source, target):
    if not os.path.exists(target):
        os.mkdir(target)
    for item in os.listdir(source):
        sourceP = os.path.join(source, item)
        targetP = os.path.join(target, item)
        if not os.path.isfile(sourceP):
            copyStatic(sourceP, targetP)
        else:
            shutil.copy(sourceP, targetP)

    return


def main():
    source = "static"
    target = "public"
    if os.path.exists(target):
        shutil.rmtree(target)
    copyStatic(source, target)

    return


main()
