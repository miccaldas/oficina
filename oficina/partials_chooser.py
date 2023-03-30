"""
Module shows all files in partials, user chooses one,
and the choice is available via mouse's middle finger.
"""
import os
import subprocess

import dmenu
import snoop
from dotenv import load_dotenv
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


@snoop
def partials_chooser():
    """
    Create a list with the full path for the files
    in the 'partials' folder. We open the list in
    Dmenu, choose one content using Xclip, and the
    content is available through mouse middle finger.
    """
    pth = "/home/mic/python/reusable_files/reusable_files/partials"
    filepaths = []
    for f in os.listdir(pth):
        filepath = os.path.join(pth, f)
        filepaths.append(filepath)

    choice = dmenu.show(filepaths, lines=5)

    cmd = f"xclip -i {choice}"
    # cmd1 = "xclip -o"

    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    partials_chooser()
