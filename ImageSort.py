import os
from PIL import Image
import collections
import shutil

ImageInfo = collections.namedtuple('ImageInfo', 'name, path, resolution')
wallpaper_resolutions = ['1280x800', '1440x900', '1680x1050', '1920x1200', '2560x1600', '1024x576', '1152x648', '1280x720', '1366x768', '1600x900', '1920x1080', '2560x1440', '3840x2160']


def main():
    print_header()
    folder = get_folder_from_user()
    while not folder:
        print('ERROR: Invalid folder path')
        folder = get_folder_from_user()

    search_subfolder = query_search_subfolder()
    if does_wallpaper_exist(folder):
        wallpaper_path = os.path.join(folder, 'Wallpaper')
    else:
        wallpaper_path = os.path.join(folder, 'Wallpaper_Sorted')

    images = search_folder(folder, search_subfolder)
    total_images = len(list(images))

    if boolean_query("{} images found! Sort by resolution".format(str(total_images))):
        image_count = 0
        images = search_folder(folder, search_subfolder)
        for image in images:
            if image.resolution in wallpaper_resolutions:
                new_path = os.path.join(wallpaper_path, image.resolution)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                    try:
                        shutil.copy(image.path, os.path.join(new_path, image.name))
                        image_count += 1
                    except shutil.SameFileError:
                        continue
                else:
                    try:
                        shutil.copy(image.path, os.path.join(new_path, image.name))
                        image_count += 1
                    except shutil.SameFileError:
                        continue
        print("{} images sorted.".format(str(image_count)))
    else:
        print("Ok bye!")

    # image_count = 0
    # for image in images:
    #      image_count += 1
    #     print('------Image #{}-------'.format(str(image_count)))
    #     print('Path: ' + image.path)
    #     print('Name: ' + image.name)
    #     print('Resolution: ' + image.resolution)


def print_header():
    print('-----------------------')
    print('       ImageSorT')
    print('-----------------------')


def get_folder_from_user():
    folder = input("What folder would you like to sort? ")

    if not folder or not folder.strip():
        return None

    if not os.path.isdir(folder):
        return None

    return os.path.abspath(folder)


def does_wallpaper_exist(folder):
    contents = os.listdir(folder)
    if 'Wallpaper' in contents:
        if boolean_query("Would you like to use the existing Wallpaper folder at: {}".format(os.path.join(os.path.abspath(folder), 'Wallpaper'))):
            print("Using existing Wallpaper folder at: {}".format(os.path.join(os.path.abspath(folder), 'Wallpaper_Sorted')))
            return True
        else:
            print("Creating Wallpaper folder at: {}".format(os.path.join(os.path.abspath(folder), 'Wallpaper_Sorted')))
            try:
                os.mkdir(os.path.join(os.path.abspath(folder), 'Wallpaper_Sorted'))
                return False
            except FileExistsError:
                return False
    # comeback to this for custom folder name
    else:
        print("Creating Wallpaper folder at: {}".format(os.path.join(os.path.abspath(folder), 'Wallpaper_Sorted')))
        return False


def query_search_subfolder():
    query = input("Would you like to search subfolders? (y/n)").lower()
    while query:
        if query == 'y':
            return True
        elif query == 'n':
            return False
        else:
            print("ERROR: Wrong Input")
            query = input("Would you like to search subfolders? (y/n)").lower()


def boolean_query(query_text):
    query = input(query_text + '? (y/n): ').lower()
    while query:
        if query == 'y':
            return True
        elif query == 'n':
            return False
        else:
            print("ERROR: Wrong Input")
            query = input(query_text + '? (y/n): ').lower()


def search_image(filename):
    try:
        with Image.open(filename) as img:
            height, width = img.size
            resolution = str(height) + 'x' + str(width)
            images = ImageInfo(name=os.path.basename(filename), path=filename, resolution=resolution)
            yield images
    except OSError:
        return


def search_folder(folder, search_subfolders):
    items = os.listdir(folder)
    for item in items:
        full_path = os.path.join(folder, item)
        if os.path.isdir(full_path) and search_subfolders:
            yield from search_folder(full_path, search_subfolders)
        elif os.path.isdir(full_path) and not search_subfolders:
            continue
        else:
            yield from search_image(full_path)


if __name__ == '__main__':
    main()
