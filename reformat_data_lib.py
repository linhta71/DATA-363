from __future__ import print_function
import sys
import traceback

def nop(*args):
    """
    This function does nothing, useful for passing in None func ptr.
    """
    return None
def eprint(*args, **kwargs):
    """
    The exact same semantics as Python's print, but this prints to standard error
    """
    print(*args, file=sys.stderr, **kwargs)

def process_matrix(matrix, process_func, column_indices=None, row_indices=None):
    """
    matrix: Matrix([m][n] yields row m column n) the matrix that we want to do
        the operation on
    process_func: function pointer that takes in value at specified column and row
        as input and return the output of the processing given that input.
    column_indices: collection of matrix column indices that we want to process.
        None means all columns
    row_indices: collection of matrix row indices that we want to process.
        None means all rows (except first row)

    This function rewrites values from specified columns and rows with the
        result of process_func.
    For example: process_matrix(dataset, add_one, 5) performs add_one on all
        values of column 5 (perform add_one in column of est. price without aid
        in our dataset)
    """
    # Set to "all" if None
    if row_indices is None:
        row_indices = range(1, len(matrix))
    if column_indices is None:
        column_indices = range(len(matrix[0]))
    # Perform process_func on all declared indices
    for r in row_indices:
        for c in column_indices:
            matrix[r][c] = process_func(matrix[r][c])
    return matrix

def make_number(noisy_str):
    """
    noisy_str: string that contains leading and trailing non-digit characters
    
    This function attempts to remove as many leading and trailing non-digit
        characters (with exceptions like '-' on prefix) to make a valid float
        string. (Does not support hexadecimal or binary string format,
        space and whitespace will mess up the function).

        "$72.000" -> 72.00
    """
    try:
        # Find first and last digit (to determine leading and trailing chars
        digit_i = [i for i,c in enumerate(noisy_str) if c.isdigit()]
        if len(digit_i) == 0:
            # not a number, return whatever was passed in
            return noisy_str
        dot_i = [i for i,c in enumerate(noisy_str) if c == '.']
        num_end = digit_i[-1] + 1
        num_begin = digit_i[0]
        if num_begin > 0 and noisy_str[num_begin - 1] == '-':
            # number is negative
            num_begin -= 1
        floatified_str = ""
        if len(dot_i) > 1:
            # More than one dot, the string probably uses '.' to separate thousands
            # ignore the dots.
            cstr = []
            for i in range(num_end, num_begin):
                if i in dot_i:
                    continue
                cstr.append(noisy_str[i])
            floatified_str = "".join(cstr)
        else:
            # No interuption just make the substring.
            floatified_str = noisy_str[num_begin:num_end]
        # Check for trailing "%"
        if num_end < len(noisy_str) and noisy_str[num_end] == '%':
            # Is percentage, convert it to float then divide it by 100
            floatified_str = str(float(floatified_str)/100)
        return floatified_str
    except Exception as e:
        eprint("Error parsing \"%s\" returning \"NA\"" % noisy_str)
        traceback.print_exc()
        return "NA"
    
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
