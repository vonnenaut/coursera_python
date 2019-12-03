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
        time_left = get_time_remaining(state, duration)       

    # state.print_history()
    return state


def get_time_remaining(obj, duration):
    """
    Returns the time remaining for the given simulate_clicker 
    # object and total duration.
    """
    return duration - obj.get_time()
