"""
The main script to fit a desired Mux into the given set of LUTs.

Assumptions:

1) LUTs only implement a 2^(n):1 MUX
"""

from math import log2, ceil

import numpy as np

from mux import Mux


class Fitter:
    # this maps the lut-size to the mux-size it can implement
    lut2mux_map = {3: 2, 4: 2, 5: 2, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 8, 12: 8}

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

        # mux_dict is the dict where keys are of possible mux-implementation  sizes in decreasing order of size.
        # Each key is mapped to the list of LUTS which are available to implement it. (Each such list will be sorted)
        self.mux_dict = dict()

        for lut_size, num_of_lut in self.lut_set.items():
            mux_for_lut = Fitter.lut2mux_map.get(lut_size)
            lut_list = self.mux_dict.get(mux_for_lut)
            if lut_list is None:
                lut_list = list()
            lut_list.extend([lut_size] * num_of_lut)
            self.mux_dict[mux_for_lut] = lut_list

        # sort the lut list for each mux
        for mux_size, lut_list in self.mux_dict.items():
            lut_list.sort()
            self.mux_dict[mux_size] = lut_list

    def get_mux_dict(self):
        return self.mux_dict

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
    def fit_layer(input_nodes_labels, mux_dict):
        """
        This function performs the fitting of a layer with a given number of inputs

        It starts with the highest mux-size that can be implemented and then checks if any sequential combination of
        inputs nodes can be fit into the mux. It proceeds to use this mux in the final layout and continue on the
        remaining inputs
        :param input_nodes_labels: 2D matrix where each row is the label for an input node
        :param mux_dict:
        :return: used_list: the LUTS used in this layer
        :return output_nodes_labels: 2D matrix for lables for the output nodes
        """

        output_nodes_labels = input_nodes_labels
        L = input_nodes_labels.shape[1]
        num_of_inputs = input_nodes_labels.shape[0]
        is_used = [False] * num_of_inputs
        used_list = list()
        count = 0

        available_muxes = sorted(mux_dict.keys())  # implementable mux-sizes in increasing order of the size

        deactivated_label = [-1] * L  # label to be used for deactivated output nodes
        dummy_input_label = [2] * L  # label for dummy input node

        # print(' Available muxes - %r' % available_muxes)
        while count < num_of_inputs:  # loop till we have not covered all inputs on some mux
            try:
                mux_size = available_muxes.pop()  # get the highest size mux available
                # print('fitting mux of size %d' % mux_size)
            except IndexError as e:
                # No muxes are available
                # just pass along the inputs through the layer
                # print(e.args)
                # print('no available mux')
                return used_list, output_nodes_labels

            # try to fit a subset of the inputs to the mux of given size
            mux_candidate_inputs = np.empty((mux_size, L))  # candidate nodes for fitting the mux
            # TODO: the for loop condition creates pain when large mux is available
            for i in range(0, num_of_inputs):
                k = i
                inp_count = 0
                used_inp_list = list()
                while inp_count < mux_size and k < num_of_inputs:
                    if is_used[k] is False:
                        mux_candidate_inputs[inp_count, :] = input_nodes_labels[k, :]
                        inp_count += 1
                        used_inp_list.append(k)
                    k += 1
                # print('input node labels - %r' % mux_candidate_inputs)
                while inp_count < mux_size:
                    mux_candidate_inputs[inp_count, :] = dummy_input_label
                    inp_count += 1
                # print('checking for inputs - %r' % used_inp_list)
                # print('input node labels - %r' % mux_candidate_inputs)
                # print('getting mux params')
                mux_params = Mux.get_mux_params(mux_candidate_inputs, mux_size)
                # print(mux_params)
                if mux_params is not None:
                    # print('mux op label')
                    # print(mux_params[1])
                    # hence implementable

                    # setting used flags for input nodes
                    for index in used_inp_list:
                        is_used[index] = True

                    lut_list = mux_dict.pop(mux_size)
                    if lut_list is None:
                        break
                    used_lut = lut_list.pop(0)  # get the smallest sized lut which can implement the required mux
                    used_list.append(used_lut)
                    output_nodes_labels[used_inp_list[0], :] = mux_params[1]
                    for j in range(1, len(used_inp_list)):
                        output_nodes_labels[used_inp_list[j], :] = deactivated_label

                    count += len(used_inp_list)
                    if len(lut_list) != 0:
                        # print('adding back the mux')
                        mux_dict[mux_size] = lut_list
                        available_muxes.append(mux_size)
                    break
            if count == num_of_inputs - 1:
                break

        # deleting useless output_nodes_labels
        deactivated_nodes = list()
        for i in range(num_of_inputs):
            if np.array_equal(output_nodes_labels[i, :], deactivated_label):
                deactivated_nodes.append(i)

        output_nodes_labels = np.delete(output_nodes_labels, deactivated_nodes, 0)

        return used_list, output_nodes_labels

    def fit(self):
        """
        This function fits the complete MUX into LUTs layer by layer
        :return:
        """

        current_num_inputs = self.mux_size
        L = ceil(log2(self.mux_size))
        format_specifier = '{0:0%db}' % L  # for converting decimal to binary
        input_node_labels = np.empty((self.mux_size, L))

        for i in range(self.mux_size):
            binary_rep = format_specifier.format(i)
            for j in range(L):
                input_node_labels[i, j] = binary_rep[j]

        layer_number = 0
        while current_num_inputs > 1:
            layer_number += 1
            print('\n\n*****fitting layer %d*****' % layer_number)
            lut_layer, output_label_nodes = self.fit_layer(input_node_labels, self.mux_dict)
            print('LUTs used - %r' % lut_layer)
            print('Output nodes labels - %r' % output_label_nodes)
            if len(lut_layer) == 0:
                # no fitting was done
                print('LUTs insufficient')
                self.used_lut_list = None
                return None
            current_num_inputs = output_label_nodes.shape[0]
            input_node_labels = output_label_nodes
            self.used_lut_list.append(lut_layer)

    def pretty_print(self):
        """
        TODO
        Prints the fitting in a neat layer structure
        :return: None
        """
        if self.used_lut_list is None:
            return
        print('\n##########')
        print('Fitted layout')
        for layer_list in self.used_lut_list:
            for lut in layer_list:
                print(lut, end=' ')
            print('')
        print('\n\n')


def execute_test():
    lut_set = {3: 2, 5: 2}
    fitter = Fitter(4, lut_set)
    fitter.fit()
    fitter.pretty_print()

    lut_set = {6: 1, 3: 5}
    fitter = Fitter(8, lut_set)
    fitter.fit()
    fitter.pretty_print()

    lut_set = {3: 2, 5: 2}
    fitter = Fitter(4, lut_set)
    fitter.fit()
    fitter.pretty_print()

    lut_set = {6: 5}
    fitter = Fitter(8, lut_set)
    fitter.fit()
    fitter.pretty_print()


if __name__ == '__main__':
    execute_test()
