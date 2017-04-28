import os


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
    global renamed_files
    renamed_files = []
    global unsupported_files
    unsupported_files = []

    for keys, values in get_env().items():
        for value in values:
            file_name = value.split('.')
            if file_name[len(file_name)-1] in ['jpg', 'mp4']:  # checks if file extension is jpg or mp4
                name = file_name[0]
                name_parts = name.split('_')
                if name_parts[0] in ['img', 'IMG', 'vid', 'VID']:  # checks if file name starts with img or vid
                    supported_files.append((keys, value, name_parts[1]))  # adds file and its path to list of supported

                    if name_parts[1] not in unique_names:  # checks if date part of the name is unique
                        unique_names += (name_parts[1],)
                else:
                    renamed_files.append((keys, value))  # adds file and its path to list of renamed files
            else:
                if value == 'media sorter.py':
                    pass
                else:
                    unsupported_files.append((keys, value))  # adds file and its path to list of unsupported files

    if not os.path.exists(os.path.join(os.getcwd(), 'Sorted')):
        os.mkdir("Sorted")

    if not os.path.exists(os.path.join(os.getcwd(), 'Sorted', 'Renamed')):
        os.mkdir(os.path.join(os.getcwd(), 'Sorted', "Renamed"))

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

    for file in renamed_files:
        os.rename(os.path.join(file[0], file[1]), os.path.join(path, 'Renamed', file[1]))

if __name__ == '__main__':
    create_folders()
    move_files()
