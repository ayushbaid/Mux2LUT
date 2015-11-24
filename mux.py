"""
A class to emulate a mux
"""
__author__ = 'ayush'

import math

import numpy as np


class Mux:
    """
    This class is used to define the structure of a mux as well as perform evaluations
    """

    def __init__(self, num_of_data_inputs, num_of_control_inputs):
        """
        Initializes the structure of the mux

        :param num_of_data_inputs:
        :param num_of_control_inputs:
        :return: None
        """
        self.num_of_data_inputs = num_of_data_inputs
        self.num_of_control_inputs = num_of_control_inputs

    def evaluate(self, data_inputs, control_inputs):
        """
        Evaluates the output of the mux given a list of data inputs and control inputs each

        :param data_inputs: list of data inputs
        :param control_inputs: list of control inputs
        :return: the result of the lut
        """
        input_number = 0

        # calculate the #data input to be selected
        for i in range(self.num_of_control_inputs):
            input_number += pow(2, self.num_of_control_inputs - i - 1) * \
                            control_inputs[i]

        return data_inputs[input_number]

    @staticmethod
    def get_mux_params(input_labels, mux_size):
        """
        Generates the select lines and the output node label if the given inputs can be fitted into the mux of the
        given size.

        2 is considered as don't care
        :param input_labels: 2D numpy matrix where each row is a label of the
        corr. input node
        :param mux_size: the number of data inputs for the mux
        :return:
        """

        k = math.log2(mux_size)  # number of select lines

        # Mux can be fit if there are <= k columns which have both zeros and
        # ones. (don't cares considered both
        # zeros and ones)

        a = np.size(input_labels, 1)

        is_similar = [True] * a  # is_similar[i] represents if the ith column has all similar entries
        columns_list = list()  # list of columns having both zeros and ones
        # the labels are from MSB to LSB
        for i in range(a):
            is_one_exists = not np.where(input_labels[:, a - 1 - i] == 1)[0].size == 0
            is_zero_exists = not np.where(input_labels[:, a - 1 - i] == 0)[0].size == 0
            is_dontcare_exists = not np.where(input_labels[:, a - 1 - i] == 2)[0].size == 0

            if is_one_exists is True:
                if is_zero_exists is True or is_dontcare_exists is True:
                    columns_list.append(i)
                    is_similar[i] = False
            elif is_zero_exists is True and is_dontcare_exists is True:
                columns_list.append(i)
                is_similar[i] = False

        if len(columns_list) > k:  # Mux cannot be fit for a given set of params
            return None

        # the select lines are corresponding to the indices in columns_list

        # for the output node label, convert the selected columns to don't care. All other columns have each entry
        # similar and hence pick the first one
        output_node_label = np.empty(a)

        for i in range(a):
            if is_similar[i]:
                output_node_label[i] = input_labels[0, i]
            else:
                output_node_label[i] = 2
        return columns_list, output_node_label


if __name__ == '__main__':
    # testing get_mux_params function
    input_labels = np.array([[1, 0, 2], [1, 1, 2]])
    mux_size = 2

    op = Mux.get_mux_params(input_labels, mux_size)
    if op is None:
        print('Mux fit not possible')
        exit()
    print(op[0])
    print(op[1])
