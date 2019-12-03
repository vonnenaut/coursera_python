def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """ 
    Input:  Sequences X and Y and scoring matrix M.
    Output:  Dynamic programming (DP) table S

    computes either a global alignment matrix or a local alignment matrix depending on the value of global_flag True -- Q. 8, False -- Q. 12
    """
    num_rows = len(seq_x)+1
    num_cols = len(seq_y)+1
    dp_table = [[0 for col in range(num_cols)] for row in range(num_rows)]

    for row in range(1,num_rows):
        if not global_flag and dp_table[row-1][0] < 0:
                dp_table[row-1][0] = 0
        dp_table[row][0] = dp_table[row-1][0] + scoring_matrix[seq_x[row-1]]['-']
        if not global_flag and dp_table[row][0] < 0:
            dp_table[row][0] = 0

    for col in range(1,num_cols):
        if not global_flag and dp_table[0][col-1] < 0:
            dp_table[0][col-1] = 0
        dp_table[0][col] = dp_table[0][col-1] + scoring_matrix['-'][seq_y[col-1]]
        if not global_flag and dp_table[0][col] < 0:
            dp_table[0][col] = 0

    for row in range(1,num_rows):
        for col in range(1,num_cols):
            dp_table[row][col] = max(dp_table[row-1][col-1]+scoring_matrix[seq_x[row-1]][seq_y[col-1]], dp_table[row-1][col]+scoring_matrix[seq_x[row-1]]['-'], dp_table[row][col-1]+scoring_matrix['-'][seq_y[col-1]])
            if not global_flag and dp_table[row][col] < 0:
                dp_table[row][col] = 0
    return dp_table