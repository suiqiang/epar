"""
抗功耗攻击评估模块。
Data类，用于读取存储明文、功耗数据
Evalution类，攻击算法类。
"""

import os
import numpy as np
import math

#from app.object_module import ObjISbox

"""存储数据的类，用于读取存储于文件中的明文、功耗等数据。
"""


class Data:
    """读取并存储文件中的明文或功耗数据
    """

    def __init__(self):
        """data只读，存放数据，files只读，读取的文件名称列表
        """
        self._data = np.array([])
        self._files = []

    def read_files(self, files, totype, columns=1):
        """读入files列表中的文件，存储在columns列的数组中。
        Keyword Arguments:
        columns -- (default -1)
        totype  -- (default 'float')
        files   -- (default [])
        """
        self._files = files
        data_dir = []

        for fname in files:
            with open(fname, 'r') as file:
                data_file = [totype(i) for i in file.read().split()]
            data_dir.extend(data_file)

        num_total = len(data_dir)
        num_mod = divmod(num_total, columns)[1]
        """将数据存成columns列n行的数组，多出的数据舍去。
        """
        data_dir = np.array(data_dir)[0:(num_total - num_mod)]
        self._data = data_dir.reshape(-1, columns)

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
        return self._data


    @property
    def files(self):
        """设置变量_files为只读
        """
        return self._files


class AttackCorr:
    """抗相关系数攻击评估
    """

    def __init__(self):
        """result存放攻击结果数据。
        """
        self._mat_corr = np.array([])
        self._result = []

    def do_attack(self, obj_module, plain, power, sum_key):
        """对目标object抗攻击能力进行评估。
        Keyword Arguments:
        obj_module --
        data       --
        power      --
        """

        self._mat_corr = np.array([self._corr_onekey(obj_module,
                                                     power,
                                                     plain,
                                                     key)
                                   for key in range(sum_key)])

        abs_mat_corr = abs(self._mat_corr)
        self._result = np.where(abs_mat_corr == abs_mat_corr.max())[0]


    def plot_result(self, sum_key):
        """输入key的数目，如8位密钥为256
        """
        plt.plot(np.arange(sum_key), self._mat_corr)

    @staticmethod
    def _corr_onekey(obj, power_data, plain_data, key):
        """对key实施一轮攻击
        Keyword Arguments:
        obj_module -- 攻击目标
        plain      -- 明文，为Data的实例
        key        -- 某一个key,0-255
        """

        """明文对应某一密钥的输出密文的汉明距离
        """

        def haming_distance(plain_data, obj, key):
            """生成密钥key对应明文输出的汉明距离序列。
            """
            cipher_current = 0
            for plain_text in plain_data:
                cipher_last = cipher_current
                cipher_current = obj.gen_cipher(plain_text, key)
                yield np.binary_repr(
                    np.bitwise_xor(cipher_last, cipher_current)).count('1')

        haming = list(haming_distance(plain_data, obj, key))
        return np.corrcoef(haming, power_data.transpose())[0, 1:]


class EvaluationCorr:
    """相关系数评估
    """

    def __init__(self):
        "docstring"
        self._table = {'0.80': 0.84162123,
                       '0.85': 1.03643339,
                       '0.90': 1.28155157,
                       '0.95': 1.64485363,
                       '0.96': 1.75068607,
                       '0.97': 1.88079361,
                       '0.98': 2.05374891,
                       '0.99': 2.32634787}

        self._result = {}

    def do_evaluation(self, mat_corr, truekey):
        """
        Keyword Arguments:
        data_corr --
        truekey   --
        """
        self._result = dict([(k, self._evaluate(mat_corr, truekey, v))
                             for (k, v) in self._table.items()])

    @staticmethod
    def _evaluate(mat_corr, truekey, z_alpha):
        """
        Keyword Arguments:
        result_corr --
        truekey     --
        alpha       --
        """
        p_truekey = abs(mat_corr[truekey]).max()
        return 3 + 8*((z_alpha/math.log((1 + p_truekey)/(1 - p_truekey)))**2)


if __name__ == '__main__':


    POWER = Data()
    POWER.read_dir('./data_repo/power/', float, 400,)

    PLAIN = Data()
    PLAIN.read_dir('./data_repo/plain/', int, 1)

    OBJECTIVE = ObjISbox()
    ATTACK = AttackCorr()


    ATTACK.do_attack(OBJECTIVE, PLAIN.data[:100], POWER.data[:100, :], 256)

    EVALUATION = EvaluationCorr()
    EVALUATION.do_evaluation(ATTACK._mat_corr, 198)

    ATTACK.plot_result(256)
    plt.show()
