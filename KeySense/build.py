# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause


import os
import shutil


def main():

    if keysense_built():
        remove_built()

    build_keysense()


def build_keysense():
    print("-------------------- BUILDING NEW APP --------------------")

    keysenseico = "../img/keysense_ico.ico"

    keysenseexe = "KeySense.py"

    os.system(f"pyinstaller --noconsole --onefile --icon={keysenseico} {keysenseexe}")

    if os.path.exists("./dist/"):

        print("-------------------- BUILD COMPLETED @ ./dist/ --------------------")


def remove_built():

    print("REMOVING OLD BUILD")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print(f"REMOVED: {build_dir}")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
        print(f"REMOVED: {dist_dir}")

    if os.path.exists(build):
        os.remove(build)
        print(f"REMOVED: {build}")


def keysense_built():

    global build_dir, dist_dir, build
    build_dir, dist_dir, build = "./build/", "./dist/", "./main.spec"

    return (
        os.path.exists(build_dir) or os.path.exists(dist_dir) or os.path.exists(build)
    )


if __name__ == "__main__":
    main()
