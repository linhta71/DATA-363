"""
Main entry. Run this python script to update the data.
"""

import retrieve_data
import reformat_data_lib as reform

def upd_col_char_to_earnings():
    """
        Update the college characteristics to earnings .csv file.

        Returns the post-processed matrix.
    """
    # Retrieve data
    data = retrieve_data.get_matrix()

    # Reprocess data
    print("Post-processing data")
    COLLEGE_NAME_COL = 1
    SAT_ACT_COL = 2
    # split the college name and location
    reform.split_column(data, COLLEGE_NAME_COL, reform.split_fr_college_name,
                        reform.split_name_location)
    # split sat and act score
    # since we added a column to the left of SAT_ACT_COL, increment by 1
    SAT_ACT_COL += 1
    reform.split_column(data, SAT_ACT_COL, reform.split_fr_median_score,
                        reform.split_score)

    # remove symbols like % or $ in number data (from Median SAT columns to
    # Early career earnings)
    reform.process_matrix(data, reform.make_number, range(3,10))
    # Save it as project_data.csv
    retrieve_data.serialize_list(data, data_fname = "project_data.csv")
    return data

def main():
    mtx_col_earn = upd_col_char_to_earnings()
    return (mtx_col_earn)
    
if __name__ == "__main__":
    retval = main()
    print(retval)
