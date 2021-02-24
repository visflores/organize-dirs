# Import Section ------------------------------------------------------------------------------------------------
import os
import shutil
from hurry.filesize import size, verbose
import numpy as np
from datetime import date
import organize_gui

# ---------------------------------------------------------------------------------------------------------------

# Parent Class.
''' The parent Class Organize has the main methods used by child classes. 

The methods create_dirs() and move_dirs() are implemented here without code. That methods will be override within the
child classes, according to your function.
'''


class Organize:
    def __init__(self, dir_path):
        self.__dir_path = dir_path

    @property
    def dir_path(self):
        return self.__dir_path

    @dir_path.setter
    def dir_path(self, dir):
        self.__dir_path = dir

    def create_dirs(self):
        pass

    def move_dirs(self):
        pass

    @staticmethod
    def drop_duplicates(list_of_something):
        dic = dict.fromkeys(list_of_something)
        return list(dic)

    def list_files(self):
        files = []
        with os.scandir(self.__dir_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    files.append(entry.name)
        return files


'''
The class organize_by_extension take files from a directory, read the extension of these files and move then to new
directories named according to the extension of each file.
'''


class organize_by_extension(Organize):
    def __init__(self, dir_path):
        super().__init__(dir_path)

    def get_extensions(self):
        extension = []
        no_ext = False
        for ext in self.list_files():
            ext = ext.lower().split('.')
            if len(ext) == 1:
                no_ext = True
            else:
                extension.append(ext[-1])
        return super().drop_duplicates(extension), no_ext

    def create_dirs(self):
        extension, no_ext = self.get_extensions()
        for entry in extension:
            os.mkdir(self.dir_path + '/' + entry)
        if no_ext:
            os.mkdir(self.dir_path + '/others')
            
    def move_dirs(self):
        for entry in self.list_files():
            ext = entry.split('.')
            if len(ext) == 1:
                shutil.move(self.dir_path + '/' + entry, self.dir_path + '/others')
            else:
                shutil.move(self.dir_path + '/' + entry, self.dir_path + '/' + ext[-1].lower())
        print("Archives moved!!!")


'''
The class organize_by_bytes extract the size of each file in a directory, create an interval, convert the interval in
Kibibytes and create new directories with each interval. The files are moved according tho their size to the
corresponding directory.
'''


class organize_by_bytes(Organize):
    def __init__(self, dir_path, type=None):
        super().__init__(dir_path)
        self.__type = type

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    def create_intervals(self):
        intervals = []
        quantiles = self.get_quantiles(self.get_bytes())
        for index in range(0, 3):
            if index >= 2:
                intervals.append(str('[{} to {}]'.format(size(quantiles[index], system=verbose),
                                                         size(quantiles[index + 1], system=verbose))))
            else:
                intervals.append(str('[{} to {})'.format(size(quantiles[index], system=verbose),
                                                         size(quantiles[index + 1], system=verbose))))
        return intervals

    def create_dirs(self):
        for dir in self.create_intervals():
            os.mkdir(self.dir_path + '/' + dir)

    def move_dirs(self):
        files = self.list_files()
        bytes = self.get_bytes()
        dirs = self.get_quantiles(bytes)
        intervals = self.create_intervals()
        for file, fsize in zip(files, bytes):
            if (fsize >= dirs[0]) and (fsize < dirs[1]):
                shutil.move(self.dir_path + '/' + file, self.dir_path + '/' + intervals[0])
            elif (fsize >= dirs[1]) and (fsize < dirs[2]):
                shutil.move(self.dir_path + '/' + file, self.dir_path + '/' + intervals[1])
            else:
                shutil.move(self.dir_path + '/' + file, self.dir_path + '/' + intervals[2])
        print("Archives moved!!")

    def get_quantiles(self, list_of_bytes):
        quantiles = np.quantile(list_of_bytes, q=[0.25, 0.5, 0.75, 1.0])
        return quantiles

    def get_bytes(self):
        bytes = []
        for archive in self.list_files():
            stat_info = os.stat(self.dir_path + '/' + archive)
            bytes.append(stat_info.st_size)
        return bytes


'''
The class organize_by_date check the date of most recent modification of a file, create new directories with that dates
and move these files to the corresponding directory.
'''


class organize_by_date(Organize):
    def __init__(self, dir_path):
        super().__init__(dir_path)

    def create_dirs(self):
        dirs_names = self.get_dates()
        for dir in dirs_names:
            os.mkdir(self.dir_path + '/' + dir)

    def move_dirs(self):
        for archive in self.list_files():
            stat_info = os.stat(self.dir_path + '/' + archive)
            t = date.fromtimestamp(stat_info.st_mtime)
            shutil.move(self.dir_path + '/' + archive, self.dir_path + '/' + t.__str__())
        print('Archives moved!!')

    def get_dates(self):
        dates = []
        for archive in self.list_files():
            stat_info = os.stat(self.dir_path + '/' + archive)
            t = date.fromtimestamp(stat_info.st_mtime)
            dates.append(t.__str__())
        return super().drop_duplicates(dates)



if __name__ == "__main__":
    organize_gui.main()
