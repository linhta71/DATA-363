from __future__ import print_function
import sys

def nop(*args):
    """
    This function does nothing, useful for passing in None func ptr.
    """
    return None
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
def split_column(matrix, column_index,
                 first_row_split_func = nop, split_func = nop):
    """
    matrix: Matrix([m][n] yields row m column n) the matrix that we want to do
        the operation on
    column_index: integer: the index of column (0-indexed) that the split will
        happen.
    first_row_split_func: func*: the function that takes in a string or expected
        value from the first row, returns a tuple of (left, right)
    split_func: func*: the function that takes in a string or expected value
        from rows that are not first, returns a tuple of (left, right)
        
    This function splits column at column_index in matrix into two rows,
    the values will be assigned as (left, right) of first_row_split_func for
    the first row, and of split_func for the other rows.
    """
    for r in range(len(matrix)):
        # spl_func is first row split if r == 0 (first row), normal split func
        # otherwise.
        spl_func = first_row_split_func if r == 0 else split_func
        left, right = spl_func(matrix[r][column_index])
        # Insert the @left to the inserted index
        matrix[r].insert(column_index, left)
        # Assign the right (which is storing unsplited string) to be @right
        matrix[r][column_index+1] = right
    return matrix[r]


def old_split_name_location(merged_name_loc):
    """
    merged_name_loc: str: string that contains both univ name and location
        like this: "University of California-IrvineIrvine. CA"
        
    This function splits name and location by finding capitalization anomaly
    and split at that cap. ab. index.

    Ex: str = University of California-IrvineIrvine. CA
                                             ^ weird cap? -> int i
    left = str[0:i]
    right = str[i:]
    This function fails for cases like "CUNY ..."
    """
    # list of chars that will reset the capitalization
    cap_reset = [' ', '.', '-']
    # for(int i = 1; i < len(merged_name_loc; i++)
    i = 1
    while (i < len(merged_name_loc)):
        if merged_name_loc[i] in cap_reset:
            # this index and the next index is ignored
            i += 2
            continue
        if merged_name_loc[i].isupper():
            # capitalization anomaly is detected at this i
            return (merged_name_loc[0:i], merged_name_loc[i:])
        i+= 1
    # capitalization anomaly is not found, cannot be splited.
    eprint("cap ano not found: %s" % merged_name_loc)
    return (merged_name_loc, "")
          
def split_name_location(merged_name_loc):
    """
    merged_name_loc: str: string that contains both univ name and location
        like this: "University of California-IrvineIrvine. CA"
        
    This function splits name and location by finding capitalization anomaly
    and split at that cap. ab. index (starts right to left)

    Ex: str = University of California-IrvineIrvine. CA
                                             ^ weird cap? -> int i
    left = str[0:i]
    right = str[i:]
    """
    STATE_ENTRY_LEN = len(". XX")
    cap_reset = {' ', '-', '.'}
    last_char_cap = False
    # for(int i = len(merged_name_loc) - STATE_ENTRY_LEN; i >= 1; i--)
    i = len(merged_name_loc) - STATE_ENTRY_LEN
    while i >= 1:
        if last_char_cap and not (merged_name_loc[i] in cap_reset):
            # Consecutive caps, anomaly found
            return (merged_name_loc[0:i+1], merged_name_loc[i+1:])
        last_char_cap = merged_name_loc[i].isupper()
        i -= 1
    
    # capitalization anomaly is not found, cannot be splited.
    eprint("cap ano not found: %s" % merged_name_loc)
    return (merged_name_loc, "")
def split_score(merged_score):
    """
    merged_score: str that looks like this: "1190/25"

    This function splits the score by delim = "/"
    """
    spl = merged_score.split("/")
    return (spl[0], spl[1])

def split_fr_college_name(*ignored_args):
    """
    This function returns ("College Name", "Location")
    """
    return ("College Name", "Location")

def split_fr_median_score(*ignored_args):
    """
    This function returns ("Median SAT", "Median ACT")
    """
    return ("Median SAT", "Median ACT")
