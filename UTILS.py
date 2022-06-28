import pdf2image, PyPDF2, time, sys, tkinter, tkinter.filedialog
import os

project_path = "/home/suman/Mergenest/"

num_tabs = 0
decor_width = 32

def print(*args, sep = ' ', end = '\n', flush = False):
    string = sep.join(map(str, args)) + end
    for ch in string:
        sys.stdout.write(ch)
        sys.stdout.flush()

def wait(duration = 0.5):
    time.sleep(duration)

def indent():
    print(num_tabs * '\t', end = "|\n", flush = True)
    print(num_tabs * '\t', end = "|", flush = True)

def decor():
    print('*' * decor_width)

def increase_indent(seed = 1):
    global num_tabs
    num_tabs += seed

def decrease_indent(seed = 1):
    global num_tabs
    num_tabs -= seed

def increase_decor(seed = 8):
    global decor_width
    decor_width += seed

def decrease_decor(seed = 8):
    global decor_width
    decor_width -= seed

def zero_based_index(page_nums: list) -> list:
    return [page_num - 1 for page_num in page_nums]

def one_based_index(page_nums: list) -> list:
    return [page_num + 1 for page_num in page_nums]

def print_intro() -> None:
    os.system("clear")
    file_path = project_path + "Introduction.txt"
    print(open(file_path, 'r').read())
    time.sleep(1)

def absolute_label(path: str) -> str:
    return path.split('/')[-1]

def pick_files() -> tuple:
    print("Please select files...")
    wait(1)
    files = tkinter.filedialog.askopenfilenames()
    labels = list(map(absolute_label, files))
    num_files = len(files)
    print()

    if any([not file.endswith('.pdf') for file in labels]):
        raise AssertionError("Unsupported files found. Expected extension: .pdf")

    if num_files == 0:
        print("Please pick at least one file")
        return pick_files()
    else:
        print("Selected files:", labels)
        return files, labels, num_files


def read_file(file_name: str) -> PyPDF2.PdfFileReader:
    indent()
    print("Reading {} ...".format(file_name), end = "", flush = True)
    wait()
    reader = PyPDF2.PdfFileReader(file_name)
    print(" Done", flush = True)
    indent()
    decor()
    return reader

def write_file(writer: PyPDF2.PdfFileWriter, destination: str) -> None:
    indent()
    print("Saving {} ...".format(destination), end = "", flush = True)
    wait()
    with open(destination, 'wb') as fp:
        writer.write(fp)
    print(" Done", flush = True)
    indent()
    decor()

def convert_to_png(file_name: str) -> None:
    label = absolute_label(file_name)
    folder_name = label.split('.')[0]
    try:
        os.makedirs(folder_name)
    except:
        pass
    indent()
    print("Converting Pages of " + label + " to PNG images ...", end = "", flush = True)
    wait()
    images = pdf2image.convert_from_path(file_name)
    for index, image in enumerate(images):
        destination = folder_name + '/' + 'Page ' + str(index + 1) + '.png'
        image.save(destination, 'PNG')
    print(" Done", flush = True)

def merge_files(files: list, destination_file_name) -> None:
    all_files = '(' + ', '.join(list(map(absolute_label, files))) + ')'
    indent()
    print("Merging {} ...".format(all_files), end = "", flush = True)
    wait()
    merger = PyPDF2.PdfFileMerger()
    for file in files:
        merger.append(file)
    print(" Done", flush = True)

    indent()
    print("Saving {} ...".format(destination_file_name), end = "", flush = True)
    wait()
    merger.write(destination_file_name)
    print(" Done", flush = True)
    merger.close()

def add_password(file_name: str, password: str, destination_file: str) -> None:
    reader = read_file(file_name)
    writer = PyPDF2.PdfFileWriter()
    for page in reader.pages:
        writer.addPage(page)

    indent()
    print("Adding password to {} ...".format(file_name), end = "", flush = True)
    wait()
    writer.encrypt(password)
    print(" Done", flush = True)
    print()

    write_file(writer, destination_file)

def rotate_pages(file_name: str, pages: list, destination: str, angle = 90):
    indent()
    print("Rotating pages {} ...".format(one_based_index(pages)), flush = True)
    wait()

    increase_indent()
    reader = read_file(file_name)
    pages = set(pages)
    writer = PyPDF2.PdfFileWriter()
    total_pages = reader.getNumPages()
    if any(page >= total_pages or page < 0 for page in pages):
        raise ValueError('Page numbers out of range')
    
    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)
        if page_num in pages:
            page.rotateClockwise(angle)
        writer.addPage(page)

    write_file(writer, destination)

    decrease_indent()
    
    indent()
    print("Done", flush = True)

def delete_pages(file_name: str, reader: PyPDF2.PdfFileReader, page_nums: list, destination: str) -> None:
    indent()
    print("Deleting pages {} ...".format(one_based_index(page_nums)), flush = True)
    wait()
    indent()
    present = [i for i in range(reader.getNumPages()) if i not in set(page_nums)]
    print("{} will now have the pages {}".format(destination, one_based_index(present)), flush = True)
    increase_indent()
    indent()
    print("Source: {}".format(file_name), flush = True)
    indent()
    print("Destination: {}".format(destination), flush = True)
    total_pages = reader.getNumPages()    
    page_nums = set(page_nums)
    writer = PyPDF2.PdfFileWriter()
    for page_num in range(total_pages):
        if page_num not in page_nums:
            writer.addPage(reader.getPage(page_num))

    write_file(writer, destination)
    decrease_indent()


def split_pdf(file_name: str, split_at: tuple, file_1: str, file_2: str) -> None:
    indent()
    print("Splitting {} in between {} ...".format(file_name, split_at), flush = True)
    increase_indent(1)
    reader = read_file(file_name)
    total_pages = reader.getNumPages()
    if split_at[0] < 0 or split_at[1] >= total_pages or split_at[1] - split_at[0] != 1:
        raise ValueError('Invalid split range')
    
    delete_list1 = list(range(split_at[1], total_pages))
    delete_list2 = list(range(0, split_at[1]))

    delete_pages(file_name, reader, delete_list1, file_1)
    wait()
    delete_pages(file_name, reader, delete_list2, file_2)
    decrease_indent(1)

if __name__ == '__main__':
    increase_decor(32)
    decor()
    decrease_decor(32)
    file = "Passport.pdf"
    rotate_pages(file, [0], "Rotated.pdf")