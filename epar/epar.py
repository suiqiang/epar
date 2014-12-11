"""
抗功耗攻击评估模块。
Data类，用于读取存储明文、功耗数据
Evalution类，攻击算法类。
"""

import os
import numpy as np
import pandas as pd
import math
import struct
import matplotlib.pyplot as plt

# from object_module import ObjISbox

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

    def read_files(self, files, etype, ftype='c', columns=1):
        """读入files列表中的文件，存储在columns列的数组中。
        Keyword Arguments:
        columns -- (default 1)
        etype   -- (default )读取文件中数据的类型，如整形，浮点
        files   -- (default [])
        ftype   -- (default )读取文件的类型，如二进制（b），字符型（c）
        """
        self._files = files
        data_dir = []

        for fname in files:
            if 'c' == ftype:
                with open(fname, 'r') as file:
                    data_file = [etype(i) for i in file.read().split()]
            else:
                with open(fname, 'rb') as file:
                    check = (1023, 1023, 1023, 1023, 1023, 1023, 1023,
                             1023, 1023, 1023, 1023, 1023, 0, 0, 0, 0)
                    if check == struct.unpack('16H', file.read(32)):
                        data = file.read()
                        num_data = divmod(len(data), 2)[0]
                        data_file = list(struct.unpack(''.join([str(num_data), 'H']), data))
                    else:
                        raise UserWarning(''.join(['文件', fname, '未通过较验']))

            data_dir.extend(data_file)

        num_total = len(data_dir)
        num_mod = divmod(num_total, columns)[1]
        """将数据存成columns列n行的数组，多出的数据舍去。
        """
        data_dir = np.array(data_dir)[0:(num_total - num_mod)]
        self._data = data_dir.reshape(-1, columns)


    def read_dir(self, dirname, etype, ftype, columns=1):
        """读目录中的所有文件，存成columns列的数组。
        Keyword Arguments:
        dirname --
        columns -- (default -1)
        etype   -- (default 'float')
        """
        path_files = [''.join([dirname, x]) for x in os.listdir(dirname)]
        self.read_files(path_files, etype, ftype, columns)


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

    def do_attack(self, obj_module, plain, power, bits_key):
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
                                   for key in range(2**bits_key)])

        abs_mat_corr = abs(self._mat_corr)
        self._result = np.where(abs_mat_corr == abs_mat_corr.max())[0]


    def plot_result(self, bits_key):
        """输入key的数目，如8位密钥为256
        """
        plt.plot(range(2**bits_key), self._mat_corr)

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



class AttackMean:
    """抗均值差攻击
    """

    def __init__(self):
        """result存放攻击结果数据。
        """
        self._mat_mean = []
        self._result = []

    def do_attack(self, obj_module, plain, power, bits_key):
        """对目标object抗攻击能力进行评估。
        Keyword Arguments:
        obj_module --
        data       --
        power      --
        """

        self._mat_mean = np.array([self._mean_onekey(obj_module,
                                            power,
                                            plain,
                                            key,
                                            bits_key)
                          for key in range(2**bits_key)])

        df_mat_mean = pd.DataFrame(self._mat_mean,
                                   index=(range(2**bits_key)),
                                   columns=range(bits_key))

        """每个位对应的前五个最大值的密钥，共40个（8位，每位5个）。
        """
        result_top5 = []
        for i in range(bits_key):
            result_top5.extend(list(df_mat_mean.sort(i, ascending=False).index[0:5]))

        """将密钥由numpy.int64变为字符型，因为json不识别numpy.int64
        """
        result_top5 = [str(i) for i in result_top5]

        """统计密钥出现的次数
        """
        result = {}
        for i in result_top5:
            result[i] = result.get(i, 0) + 1

        """按密钥出现的次数进行排序
        """
        self._result = sorted(result.items(), key=lambda d: d[1], reverse=True)

        # abs_mat_mean = abs(self._mat_mean)
        # self._result = np.array([np.where(i == i.max())[0] for i in self._mat_mean.transpose()]).reshape(bits_key)
        # self._result = np.array([np.where(i == i.max())[0] for i in df_mat_mean])


    def plot_result(self, bits_key):
        """输入key的数目，如8位密钥为256
        """
        plt.plot(range(2**bits_key), self._mat_mean[:, 2])

    @staticmethod
    def _mean_onekey(obj, power_data, plain_data, key, bits_key):
        """对key实施一轮攻击
        Keyword Arguments:
        obj_module -- 攻击目标
        plain      -- 明文，为Data的实例
        key        -- 某一个key,0-255
        """

        """明文对应某一密钥的输出密文的汉明距离
        """
        cipher_text = [np.binary_repr(obj.gen_cipher(plain_text, key), bits_key)
                       for plain_text in plain_data]

        df_data = pd.DataFrame(power_data, index=cipher_text)

        all_cipher = [np.binary_repr(i, bits_key) for i in range(2**bits_key)]


        result = []
        for i in range(7, -1, -1):
            df_data_1 = df_data.loc[[x for x in all_cipher if x[i] == '1']]
            df_data_0 = df_data.loc[[x for x in all_cipher if x[i] == '0']]
            df_data_diff = np.array(df_data_1.mean() - df_data_0.mean())
            result.append(abs(df_data_diff).max())

        return np.array(result)


if __name__ == '__main__':


    PLAIN = Data()
    PLAIN.read_dir('./data_repo/plain/', int, 'c', 1)

    POWER = Data()
    POWER.read_dir('./data_repo/power/', float, 'c', 400)

    OBJECTIVE = ObjISbox()

    ATTACKCORR = AttackCorr()
    ATTACKCORR.do_attack(OBJECTIVE, PLAIN.data[:1000], POWER.data[:1000, :], 8)
    EVALUATION = EvaluationCorr()
    EVALUATION.do_evaluation(ATTACKCORR._mat_corr, 198)
    ATTACKCORR.plot_result(8)


    ATTACKMEAN = AttackMean()
    ATTACKMEAN.do_attack(OBJECTIVE, PLAIN.data[:2000], POWER.data[:2000, :], 8)
    ATTACKMEAN.plot_result(8)

    plt.show()
