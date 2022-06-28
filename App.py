from UTILS import *

def go_single():
    # Available options: Split, rotate, delete pages, add password
    print("")

def go_multiple():
    # Available options: Merge
    pass

if __name__ == '__main__':

    print_intro()

    files, labels, num_files = pick_files()

    if num_files == 1:
        # Available options: Split, rotate, delete pages, add password, convert to png
        convert_to_png(files[0])
        # go_single()
    else:
        # Available options: Merge
        go_multiple()