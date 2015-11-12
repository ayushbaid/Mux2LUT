"""
The main script to fit a desired Mux into the given set of LUTs.
"""

from math import log2, ceil


class Fitter:
    def __init__(self, mux_size, lut_set):
        """
        This function initializes the basic parameters
        :param mux_size: The number of data inputs of the mux to be fitted
        :param lut_set: A dict containing the LUT size and the corresponding number of LUTs present
        :return: None
        """
        self.used_lut_list = list()  # list of (list of luts) according to layers used for creating the req. mux
        self.graph_edges = list()  # a list of directed edges, each edge is a tuple
        self.data_input_nodes = list()
        self.control_input_nodes = list()
        self.mux_size = mux_size
        self.lut_set = lut_set

        # LUT list contains the list of available LUT sizes in decreasing order of size
        self.lut_list = list()

        for lut_size, num_of_lut in self.lut_set.items():
            self.lut_list.extend([lut_size] * num_of_lut)

    def get_lut_list(self):
        return self.lut_list

    def init_graph(self):
        """
        This function defines the data and control nodes for the graph
        :return: None
        """
        # defining the initial nodes (0 to mux_size-1) as data nodes
        self.data_input_nodes = range(self.mux_size)

        # the further nodes are control input nodes
        self.control_input_nodes = self.mux_size + range(ceil(log2(self.mux_size)))

    @staticmethod
    def fit_layer(num_of_inputs, lut_list):
        """
        This function performs the fitting of a layer with a given number of inputs
        currently performing no optimization
        :param num_of_inputs: The number of inputs to that layer
        :param lut_list: the list of available LUTs
        :return: used_list
        """
        used_list = list()
        count = 0
        while count < num_of_inputs:
            try:
                lut_size = lut_list.pop()
            except IndexError:
                raise
            count = count + lut_size
            used_list.append(lut_size)

        return used_list

    def fit(self):
        """
        This function fits the complete MUX into LUTs layer by layer
        :return:
        """
        current_num_inputs = self.mux_size

        while current_num_inputs > 1:
            try:
                lut_layer = self.fit_layer(current_num_inputs, self.lut_list)
            except IndexError:
                print('LUTs insufficient')
                self.used_lut_list = None
                return
            current_num_inputs = len(lut_layer)
            self.used_lut_list.append(lut_layer)

    def pretty_print(self):
        """
        TODO
        Prints the fitting in a neat layer structure
        :return: None
        """
        if self.used_lut_list is None:
            return
        print('*********')
        print('Fitted layout')
        for layer_list in self.used_lut_list:
            for lut in layer_list:
                print(lut, end=' ')
            print('')


def execute_test():
    lut_set = {2: 1, 3: 2}
    fitter = Fitter(4, lut_set)
    lut_list = fitter.get_lut_list()
    print(lut_list)
    fitter.fit()
    fitter.pretty_print()


if __name__ == '__main__':
    execute_test()
