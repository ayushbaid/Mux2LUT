"""
A class to emulate an LUT
"""
__author__ = 'ayush'


class Lut:
    """
    This class is used to define the structure of a mux as well as perform evaluations
    """

    def __init__(self, lut_table):
        """
        Initializes the structure of the LUT as well as the mappings

        :param lut_table: The mapping for the LUT as a list
        :return: None
        """

        self.num_of_inputs = len(lut_table)
        self.lut_table = lut_table

    def evaluate(self, inp):
        """
        Returns the value in the lut_table for the given input
        :param inp: input number
        :return: value
        """
        return self.lut_table[inp]
