





# pseudocode (True, Q. 8):

#     m <--|X|;   n <-- |Y|;    
#     S[0,0] <-- 0;

#     for i <-- 1 to m do
#         S[i,0] <--- S[i-1,0] + Msub(Xsub(i-1), -)

#     for j <-- 1 to n do
#         S[0,j] <-- S[0,j-1] + Msub(-,Ysub(j-1))

#     for i <-- 1 to m do
#         for j <-- 1 to n do
#             S[i,j] <-- max(S[i-1,j-1] + Msub(Xsub(i-1),Ysub(j-1)), S[i-1,j] + Msub(Xsub(i-1),-), S[i,j-1] + Msub(-,Ysub(j-1))
#     return S

#     pseudocode (False, Q. 12) -- same but then converts negative values to zero. i.e,
# In Questions 12-15, we will make simple modifications to ComputeGlobalAlignmentScores and ComputeAlignment that yield an efficient algorithm for the Local Pairwise Alignment Problem.

# In this question, we will focus on modifying ComputeGlobalAlignmentScores to compute a matrix of local alignment scores. Our modification is as follows: Whenever Algorithm ComputeGlobalAlignmentScores (in Question 8) computes a value to assign to S[i,j], if the computed value is negative, the algorithm instead assigns 0 to S[i,j]. The result of this computation is the local alignment matrix for the two sequences. No other modification is done.

# As an example, consider two strings X=AA and Y=TAAT   over the alphabet Σ={A,C,T,G}    and the scoring matrix M given by:

#     Mσ,σ=10 for every σ∈Σ.
#     Mσ,σ′=4 for every σ,σ′∈Σ and σ≠σ′.
#     Mσ,−=M−,σ=−6 for every σ∈Σ.

# Given the two sequences X and Y and the scoring matrix M, what values would the modified algorithm assign to the entries S[0,2], S[2,0] and S[2,2] of the local alignment matrix S?

# Enter your answer below as three numbers separated by spaces.