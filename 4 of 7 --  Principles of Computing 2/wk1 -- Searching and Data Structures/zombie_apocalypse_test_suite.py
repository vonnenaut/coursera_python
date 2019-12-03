"""
Testing Zombie Apocalypse mini-project
"""
import poc_simpletest
import zombie_apocalypse

def run_suite(format_function):
	"""
    Some informal testing code
    """
    # create a TestSuite object
    	suite = poc_simpletest.TestSuite()
    	apoc = zombie_apocalypse

    	if format_function == num_zombies:
    		suite.run_test(apoc.num_zombies(), "0", "Test #1:")

    	elif format_function == add_zombie:
    		print "Testing add_zombie:"
    		apoc.add_zombie(0,0)
    		apoc.add_zombie(5,2)
    		suite.run_test(apoc.num_zombies, "2", "Test #2:")

    	suite.report_results()

print "Beginning testing."
print "Testing num_zombies:"
run_suite(num_zombies)