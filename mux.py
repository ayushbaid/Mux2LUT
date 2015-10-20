"""
A class to emulate a mux
"""
__author__ = 'ayush'


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
        :return:
        """
        result = 0
        inpNumber = 0

        # calculate the #data input to be selected
        for i in range(self.num_of_control_inputs):
            inpNumber += pow(2, self.num_of_control_inputs - i - 1) * control_inputs[i]

        return data_inputs[inpNumber]
