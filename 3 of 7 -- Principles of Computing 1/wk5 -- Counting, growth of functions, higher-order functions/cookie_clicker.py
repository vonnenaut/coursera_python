"""
Cookie Clicker Simulator
"""

import simpleplot, math, codeskulptor
# import poc_simpletest

# Used to increase the timeout, if necessary
codeskulptor.set_timeout(30)  # adujst as needed

import poc_clicker_provided as provided

# Constants
# SIM_TIME = 10000000000.0
SIM_TIME = 50.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._time = 0.0
        self._current_cookies = 0.0
        self._total_cookies = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._time) + " Current Cookies: " + str(self.get_cookies()) + " CPS: " + str(self.get_cps()) + " Total Cookies: " + str(self._total_cookies) 

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_total_cookies(self):
        """
        Returns the total number of cookies produced
        """
        return self._total_cookies

    def add_cookies(self, amount):
        """
        Adds the specified amount to both the current and total cookies
        """
        self._current_cookies += amount
        self._total_cookies += amount

    def subtract_cookies(self, amount):
        """
        Subtracts the specified amount from the current cookies
        """
        self._current_cookies -= amount

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def add_cps(self, amount):
        """
        Adds the specified amount to the current cps
        """
        self._cps = float(self.get_cps()) + float(amount)

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def add_time(self, amount):
        """
        Adds to the total time passed in the simulation
        """
        self._time = self.get_time() + amount

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        _copy_history = self._history[:]
        return _copy_history

    def print_history(self):
        """
        Prints the history of purchases made during the simulation
        """
        for item in self.get_history():
            print item

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        # check whether we have enough cookies for an upgrade without waiting
        curr_cookies = self.get_cookies()

        if curr_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - curr_cookies) / float(self.get_cps()))

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        self.add_time(time)
        self.add_cookies(time * self.get_cps())

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        time = self.get_time()

        if self.get_cookies() >= cost:
            # before buying the item, check if we can buy multiples of the same
            # item and do so
            # transactions = int(math.floor(self.get_cookies() / cost))
            self.subtract_cookies(cost)
            self.add_cps(additional_cps)
            self._history.append((time, item_name,
                                 cost, self.get_total_cookies()))
        else:
            print "Cannot afford this item!"        
        

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_clone = build_info.clone()
    state = ClickerState()
    time_left = get_time_remaining(state, duration)

    while time_left > 0:
        # get item to purchase based on given strategy's
        # recommendation
        item = strategy(state.get_cookies(), state.get_cps(
        ), state.get_history(), time_left, build_clone)
        
        if item is None:
            state.wait(time_left)
            break

        cost = build_clone.get_cost(item)        
        time_to_wait = state.time_until(cost)

        if time_to_wait > time_left:
            # if time to wait is greater than  that remaining, 
            # wait out remainder of time, accumulating remaining 
            # cookies and end the loop
            state.wait(time_left)
            break
        else:
            state.wait(time_to_wait)
        state.buy_item(item, cost, build_clone.get_cps(item))
        # update cost increase after purchase of item
        try:
            build_clone.update_item(item)
        except KeyError:
            print "Key not found."

        # update time remaining
        time_left = get_time_remaining(state, duration)

    # check if any final purchases can be made after time is up
    if item != None and state.get_cookies() >= build_clone.get_cost(item):
        state.buy_item(item, cost, build_clone.get_cps(item))

    return state


def get_time_remaining(obj, duration):
    """
    Returns the time remaining for the given simulate_clicker 
    # object and total duration.
    """
    return duration - obj.get_time()


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    buy_options = build_info.build_items()
    cheapskate_option = None
    cheapskate_option_cost = 999999999

    for option in buy_options:
        cost = build_info.get_cost(option)
        if cost < cheapskate_option_cost:
            if cookies > cost or time_left * cps > cost:
                cheapskate_option = option
                cheapskate_option_cost = cost

    return cheapskate_option
   


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    buy_options = build_info.build_items()
    snob_option = None
    snob_option_cost = 0

    for option in buy_options:
        cost = build_info.get_cost(option)
        if cost > snob_option_cost:
            if cookies > cost or time_left * cps > cost:
                snob_option = option
                snob_option_cost = cost
        
    return snob_option   


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies',
    # [history], True)


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)


# # TESTS
# def run_suite():
#     """
#     Some informal testing code
#     """

#     # create a TestSuite object
#     suite = poc_simpletest.TestSuite()

#     # create a ClickerState instance
#     state = ClickerState()

    # # test str
    # suite.run_test(state.__str__(), "Time: 0.0 Current Cookies: 0.0 CPS: 1.0 Total Cookies: 0.0 History: [(0.0, None, 0.0, 0.0)]", "Test #1:")

    # # test add_cookies and get_cookies
    # state.add_cookies(50)
    # suite.run_test(state.get_cookies(), 50, "Test #2:")

    # # test add_time and get_time
    # state.add_time(155)
    # suite.run_test(state.get_time(), 155, "Test #3:")

    # # test get_cps
    # reset_state(state)
    # state.add_cps(10.0)
    # state.wait(50)
    # suite.run_test(state.get_cps(), 11.0, "Test #4:")

    # # test get_history
    # suite.run_test(state.get_history(), state.get_history(), "Test #5:")

    # # test time_until
    # print "---Test #6---"
    # reset_state(state)
    # suite.run_test(state.time_until(501.5), 502.0, "Test #6:")

    # # test wait
    # print "\n\n"
    # print "---Test #7---"
    # reset_state(state)
    # state.wait(500)
    # suite.run_test(state.get_cookies(), 500.0, "Test #7:")
    # print "state.time:", state.get_time(), "\n"

    # # test get_cookies #2
    # print "\n\n"
    # print "---Test #8---"
    # reset_state(state)
    # # print "state:", state
    # state.wait(40)
    # print "time:", state.get_time()
    # suite.run_test(state.get_cookies(), 40.0, "Test #8:")

    # print "\n\n"
    # print "---Test #9---"
    # reset_state(state)
    # state.wait(100)
    # state.buy_item("grandma", 100, 5.0)
    # suite.run_test(state.get_cps(), 6.0, "Test #9:")

    # print "\n\n"
    # print "---Test #10---"
    # reset_state(state)
    # state.wait(100)
    # print state
    # state.buy_item("grandma", 100.0, 5.0)
    # print state
    # suite.run_test(state.get_cookies(), 0.0, "Test #10:")
 
    # print "Resetting state."
    # reset_state(state)
    # print state

    # # Owl Test Troubleshooting
    # obj = ClickerState()
    # print "cps:", obj.get_cps()
    # print "Waiting."
    # obj.wait(402.0)
    # print "Buying item."
    # obj.buy_item('item', 2.0, 9.0)
    # print "cps:", obj.get_cps()
    # suite.run_test(obj.time_until(450.0), 5.0, "Test #11:")
    # print obj

#     suite.run_test(simulate_clicker(provided.BuildInfo(), 500.0, strategy_cursor_broken), "Time: 500.0 Current Cookies: 28.0735995433 CPS: 2.7 Total Cookies: 1004.2", "test #12:")

#     suite.run_test(simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none), "Time: 5000.0 Current Cookies: 5000.0 CPS: 1.0 Total Cookies: 5000.0 History: [(0.0, None, 0.0, 0.0)]", "Test #12:")

    # suite.run_test(simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0, strategy_cursor_broken), "Time: 16.0 Current Cookies: 13.9125 CPS: 151.0 Total Cookies: 66.0",  "Test #13:")

#     suite.run_test(simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none), "Time: 5000.0 Current Cookies: 5000.0 CPS: 1.0 Total Cookies: 5000.0 History: [(0.0, None, 0.0, 0.0)]", "Test #13:")

#     suite.report_results()


# def reset_state(instance):
#     instance._cps = 1.0
#     instance._total_cookies = 0.0
#     instance._current_cookies = 0.0
#     instance._history = [(0.0, None, 0.0, 0.0)]
#     instance._time = 0.0

# run_suite()
# # run()
