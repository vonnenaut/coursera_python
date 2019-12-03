""" Test suite for yahtzee_player.py """
import poc_simpletest


def run_suite(format_function):
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # test format_function on various inputs
    suite.run_test(format_function(0), "0:00.0", "Test #1:")
    
    
    suite.report_results()