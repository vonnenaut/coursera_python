# Compute and print tens and ones digit of an integer in [0,100).

###################################################
# Digits function
# Student should enter function on the next lines.
def calc_tens(number):
    tens = number//10
    return tens

def calc_ones(number):
    ones = number%10
    return ones

def print_digits(number):
    tens = str(calc_tens(number))
    ones = str(calc_ones(number))
    print "The tens digit is %s, and the ones digit is %s." % (tens, ones)


    
###################################################
# Tests
# Student should not change this code.
    
print_digits(42)
print_digits(99)
print_digits(5)


###################################################
# Expected output
# Student should look at the following comments and compare to printed output.

#The tens digit is 4, and the ones digit is 2.
#The tens digit is 9, and the ones digit is 9.
#The tens digit is 0, and the ones digit is 5.
