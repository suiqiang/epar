"""存储数据的类，用于读取存储于文件中的明文、功耗等数据。
"""


import os
import numpy as np

class Data:
    """读取并存储文件中的明文或功耗数据
    """

    def __init__(self):
        """data只读，存放数据，files只读，读取的文件名称列表
        """
        self.__data = np.array([])
        self.__files = []

    def read_files(self, files, totype, columns=1):
        """读入files列表中的文件，存储在columns列的数组中。
        Keyword Arguments:
        columns -- (default -1)
        totype  -- (default 'float')
        files   -- (default [])
        """
        self.__files = files
        data_dir = []

        for fname in files:
            with open(fname, 'r') as file:
                #data_file = list(map(eval(totype), file.read().split()))
                data_file = [totype(i) for i in file.read().split()]
            data_dir.extend(data_file)

        #map(float, data_dir)
        num_total = len(data_dir)
        num_mod = divmod(num_total, columns)[1]
        """将数据存成columns列n行的数组，多出的数据舍去。
        """
        data_dir = np.array(data_dir)[0:(num_total - num_mod)]
        self.__data = data_dir.reshape(-1, columns)

    def read_dir(self, dirname, totype, columns=1):
        """读目录中的所有文件，存成columns列的数组。
        Keyword Arguments:
        dirname --
        columns -- (default -1)
        totype  -- (default 'float')
        """
        path_files = [''.join([dirname, x]) for x in os.listdir(dirname)]
        self.read_files(path_files, totype, columns)

    @property
    def data(self):
        """设置变量_data为只读
        """
        return self.__data


    @property
    def files(self):
        """设置变量__files为只读
        """
        return self.__files



if __name__ == '__main__':
    pass

    # POWER = Data()
    # POWER.read_dir('./data_repo/power/', float, 400,)

    # PLAIN = Data()
    # PLAIN.read_dir('./data_repo/plain/', int, 1)
