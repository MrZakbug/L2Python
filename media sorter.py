import os
import PIL.Image


def get_env():
    """
    Creates a dictionary of all dirs and files in current directory
    :return: dictionary
    """

    dirs_files = {}

    for item in os.walk(os.getcwd()):
        file_list = []
        directory = str(item[0])
        for i in item[2]:
            file_list.append(i)
        dirs_files[directory] = file_list
    return dirs_files


def create_folders():
    """
    Creates folders (one for each day picture/pictures were taken)
    :return: NONE
    """
    global unique_names
    unique_names = ()
    global supported_files
    supported_files = []
    global video_files
    video_files = []
    global unsupported_files
    unsupported_files = []

    for keys, values in get_env().items():
        for value in values:
            file_name = value.split('.')
            if file_name[len(file_name)-1] in ['jpg', 'JPG']:  # checks if file extension is jpg
                img = PIL.Image.open(value)
                exif_data = img._getexif()[34853][29].replace(':', '-')
                print(exif_data)
                supported_files.append((keys, value, exif_data))  # adds file and its path to list of supported

                if exif_data not in unique_names:  # checks if date part of the name is unique
                    unique_names += (exif_data,)

            elif file_name[len(file_name) - 1] in ['mp4', 'MP4']:
                video_files.append((keys, value))  # adds file and its path to list of renamed files

            else:
                if keys == os.getcwd():  # if file in main directory and not img nor mp4
                    pass
                else:
                    unsupported_files.append((keys, value))  # adds file and its path to list of unsupported files

    if not os.path.exists(os.path.join(os.getcwd(), 'Sorted')):
        os.mkdir("Sorted")

    if not os.path.exists(os.path.join(os.getcwd(), 'Sorted', 'Video')):
        os.mkdir(os.path.join(os.getcwd(), 'Sorted', "Video"))

    if not os.path.exists(os.path.join(os.getcwd(), 'Sorted', 'Unsupported')):
        os.mkdir(os.path.join(os.getcwd(), 'Sorted', "Unsupported"))

    for n in unique_names:
        new_path = os.path.join(os.getcwd(), 'Sorted', n)
        if not os.path.exists(new_path):
            os.mkdir(new_path)

    return None


def move_files():
    """
    Moves files to proper directories
    :return: None
    """
    path = os.path.join(os.getcwd(), 'Sorted')

    for file in supported_files:
        os.rename(os.path.join(file[0], file[1]), os.path.join(path, file[2], file[1]))

    for file in unsupported_files:
        os.rename(os.path.join(file[0], file[1]), os.path.join(path, 'Unsupported', file[1]))

    for file in video_files:
        os.rename(os.path.join(file[0], file[1]), os.path.join(path, 'Video', file[1]))

if __name__ == '__main__':
    get_env()
    create_folders()
    # move_files()
