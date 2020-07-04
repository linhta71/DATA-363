"""
A Python script to illustrate manipulating the data without
retrieving the orignal dataset from the web.
"""

import retrieve_data
import reformat_data_lib as reform
import csv

def main():
    old_mtx = []
    with open("data/project_data_states.csv", mode = 'r') as old_file:
        reader = csv.reader(old_file)
        old_mtx = [row for row in reader]
    # old_mtx: list of list

    # Split location into location and state (split by delim of "."
    reform.split_column(old_mtx, 2, lambda x: ("City", "State"),
                        lambda s: (s[:-4], s[-2:]))
    retrieve_data.serialize_list(old_mtx, data_fname = "project_data_.csv")
    return (old_mtx)
    
if __name__ == "__main__":
    retval = main()
    print(retval)
