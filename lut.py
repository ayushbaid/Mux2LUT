"""
A class to emulate an LUT
"""
__author__ = 'ayush'

import math


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
        num_of_select_inps = int(math.ceil(math.log2(mux_data_inps)))
        self.num_of_inputs = mux_data_inps + num_of_select_inps
        length = int(math.pow(2, self.num_of_inputs))
        temp = int(math.pow(2, num_of_select_inps))
        self.lut_map = [0] * length

        format_specifier = '{0:0%db}' % self.num_of_inputs
        for i in range(length):
            binary_rep = format_specifier.format(i)
            selected_index = i % temp
            self.lut_map[i] = int(binary_rep[mux_data_inps - selected_index - 1])  # offsetting for select lines

    def __init__(self, lut_map=None):
        """
        Initializes the structure of the LUT as well as the mappings

        :param lut_map: The mapping for the LUT as a list
        :return: None
        """
        if lut_map is None:
            self.num_of_inputs = 0
            self.lut_map = None
            return
        self.num_of_inputs = len(lut_map)
        self.lut_map = lut_map

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
        print('\n*****LUT mapping*****')
        print('Binary Index\t\tOutput')
        for i in range(len(self.lut_map)):
            print('%s\t\t%d' % (format_specifier.format(i), self.lut_map[i]))


if __name__ == '__main__':
    lut = Lut()
    lut.generate_mux_lut_map(4)
    lut.print_lut_map()
