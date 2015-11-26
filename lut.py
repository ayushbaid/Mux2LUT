import math

import numpy as np

"""
A class to emulate an LUT
"""
__author__ = 'ayush'


class Lut:
    """
    This class is used to define the structure of a mux as well as perform evaluations
    """

    def generate_mux_lut_map(self, mux_data_inps):
        """
        Generates a lut mapping for MUX of given #(data inps)
        Format of the index's binary representation is {dn,....,d1,d0,...sm,...s1,s0}
        where dj is data inp #j and sj in select inp #j
        :param mux_data_inps: The number of data inputs for the MUX
        :return:
        """
        num_of_select = int(math.ceil(math.log2(mux_data_inps)))
        temp2 = int(math.pow(2, mux_data_inps + num_of_select))  # number of entries for the mux

        temp = int(math.pow(2, num_of_select))

        format_specifier = '{0:0%db}' % self.num_of_inputs
        for i in range(temp2):
            binary_rep = format_specifier.format(i)
            selected_index = i % temp
            self.lut_map[i] = int(binary_rep[- selected_index - 1 - num_of_select])  # offsetting for select lines

    def __init__(self, lut_size, input_nodes, select_lines, output_node):
        """
        Initializes the structure of the LUT as well as the mappings

        :param lut_size: the number of inputs for the LUT
        :param input_nodes: the list of input node labels
        :param select_lines: the list of select lines (LSB->MSB)
        :param output_node: the output node label
        :return: None
        """

        self.num_of_inputs = lut_size
        length = int(math.pow(2, self.num_of_inputs))

        L = input_nodes.shape[1]
        # deleting dummy inputs from input node labels
        # deleting useless output_nodes_labels
        dummy_label = [2] * L
        dummy_nodes = list()
        for i in range(input_nodes.shape[0]):
            if np.array_equal(input_nodes[i, :], dummy_label):
                dummy_nodes.append(i)

        self.input_nodes = np.delete(input_nodes, dummy_nodes, 0)

        self.select_lines = select_lines
        self.output_node = output_node

        self.lut_map = [0] * length
        self.generate_mux_lut_map(input_nodes.shape[0])

    def evaluate(self, inp):
        """
        Returns the value in the lut_table for the given input
        :param inp: input number
        :return: value
        """
        return self.lut_map[inp]

    def print_lut_map(self):
        """
        Prints the mapping of the LUT
        :return: None
        """

        format_specifier = '{0:0%db}' % self.num_of_inputs
        print('LUT mapping - ')
        print('Binary Index\t\tOutput')
        for i in range(len(self.lut_map)):
            print('%s\t\t%d' % (format_specifier.format(i), self.lut_map[i]))

    def print_labels(self):
        print('LUT input nodes - ')
        print(self.input_nodes)
        print('LUT select lines - ')
        print(self.select_lines)


if __name__ == '__main__':
    lut = Lut()
    lut.generate_mux_lut_map(4)
    lut.print_lut_map()
