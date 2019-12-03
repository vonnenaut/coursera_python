


# Line 1: Xi−1+X′
# Line 2: Yj−1+Y′
# Line 3: Xi−1+X′
# Line 4: "−"+Y′
# Line 5: "−"+X′
# Line 6: Yj−1+Y′


# compute global alignment pseudocode
# sequences X and Y
# scoring matrix M
# dynamic programming table S


# i <-- |X|; j <-- |Y|;
# X' <-- epsilon;  Y' <-- epsilon;

# while i != 0 and j != 0 do
    # if S[i,j] = S[i-1,j-1] + Msub(Xsub(i-1),Ysub(j-1)) then
    #     X' <-- Xsub(i−1)+X′;
    #     Y' <-- Ysub(j−1)+Y′;
    #     i <-- i-1; j <-- j-1;
    # else
    #     if S[i,j] = S[i-1,j] + Msub(Xsub(i-1),-) then
    #         X' <-- Xsub(i−1)+X′;
    #         Y' <-- "−"+Y′;
    #         i <-- i-1;
    #     else
    #         X' <-- "−"+X′;
    #         Y' <-- Ysub(j−1)+Y′;
    #         j <-- j-1;

# while i != 0 do
#     X' <-- X sub(i-1) + X';  Y' <-- '-' + Y';
#     i <-- i-1;

# while j != 0 do
#     X' <-- "-" + X';  Y' <-- Ysub(j-1) + Y';
#     j <-- j-1;

# return (X',Y')



