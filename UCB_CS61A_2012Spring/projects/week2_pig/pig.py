#!/usr/local/bin/python3

"""The Game of Pig"""

from dice import make_fair_die, make_test_die
from ucb import main, trace, log_current_line, interact

goal = 100  # The goal of pig is always to score 100 points.


# Taking turns

def roll(turn_total, outcome):
    """Performs the roll action, which adds outcome to turn_total, or loses the
    turn on outcome == 1.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll (the number generated by the die)

    Returns three values in order:
    - the number of points the player scores after the roll
      Note: If the turn is not over after this roll, this return value is 0.
            No points are scored until the end of the turn.
    - the player turn point total after the roll
    - a boolean; whether or not the player's turn is over
    
    >>> roll(7, 3)
    (0, 10, False)
    >>> roll(99, 1)
    (1, 0, True)
    """
    "*** YOUR CODE HERE ***"
    if outcome == 1:
        return 1, 0, True
    else:
        return 0, turn_total + outcome, False


def hold(turn_total, outcome):
    """Performs the hold action, which adds turn_total to the player's score.

    Arguments:
    turn -- number of points accumulated by the player so far during the turn
    outcome -- the outcome of the roll, ie. the number generated by the die

    Returns three values in order:
    - the number of points the player scores after holding
    - the player turn total after the roll (always 0)
    - a boolean; whether or not the player's turn is over
    
    >>> hold(99, 1)
    (99, 0, True)
    """
    "*** YOUR CODE HERE ***"
    return turn_total, 0, True


def take_turn(plan, dice=make_fair_die(), who='Paul Hilfinger',
              comments=False):
    """Simulate a single turn and return the points scored for the whole turn.

    Important: The d function should be called once, **and only once**, for
               every action taken!  Testing depends upon this fact.
    
    Arguments:
    plan -- a function that takes the turn total and returns an action function
    dice -- a function that takes no args and returns an integer outcome.
            Note: dice is non-pure!  Call it exactly once per action.
    who -- name of the current player
    comments -- a boolean; whether commentary is enabled
    """
    score_for_turn = 0  # Points scored in the whole turn
    "*** YOUR CODE HERE ***"
    turn_total = 0
    turn_is_over = False
    while not turn_is_over:
        action = plan(turn_total)
        outcome = dice()
        score_for_turn, turn_total, turn_is_over = action(turn_total, outcome)
        if comments:
            commentate(action, outcome, score_for_turn, turn_total,
                       turn_is_over, who)
    return score_for_turn


def take_turn_test():
    """Test the take_turn function using deterministic test dice."""
    plan = make_roll_until_plan(10)  # plan is a function (see problem 2)
    "*** YOUR CODE HERE ***"
    print(take_turn(plan, dice=make_fair_die()))  # deterministic
    # print(take_turn(plan, dice=make_test_die(4,6,1)))  # Not deterministic


# Commentating

def commentate(action, outcome, score_for_turn, turn_total, over, who):
    """Print descriptive comments about a game event.
    
    action -- the action function chosen by the current player
    outcome -- the outcome of the die roll
    score_for_turn -- the points scored in this turn by the current player
    turn_total -- the current turn total
    over -- a boolean that indicates whether the turn is over
    who -- the name of the current player 
    """
    print(who, describe_action(action))
    if action == roll:
        print(draw_number(outcome))
    if over:
        print(who, 'scored', score_for_turn, 'point(s) on this turn.')
    else:
        print(who, 'now has a turn total of', turn_total, 'point(s).')


def describe_action(action):
    """Generate a string that describes an action.

    action -- a function, which should be either hold or roll

    If action is neither the hold nor roll function, the description should
    announce that cheating has occurred.

    >>> describe_action(roll)
    'chose to roll.'
    >>> describe_action(hold)
    'decided to hold.'
    >>> describe_action(commentate)
    'took an illegal action!'
    """
    "*** YOUR CODE HERE ***"
    if action == roll:
        return 'chose to roll.'
    elif action == hold:
        return 'decided to hold.'
    else:
        return 'took an illegal action!'


def draw_number(n, dot='*'):
    """Return an ascii art representation of rolling the number n.

    >>> print(draw_number(5))
     -------
    | *   * |
    |   *   |
    | *   * |
     -------
    """
    "*** YOUR CODE HERE ***"
    pattern = [
        [1, 0, 0, 0],  # 1
        [0, 1, 0, 0],  # 2
        [1, 0, 1, 0],  # 3
        [0, 1, 1, 0],  # 4
        [1, 1, 1, 0],  # 5
        [0, 1, 1, 1],  # 6
    ]
    p = pattern[n-1]
    return draw_die(p[0], p[1], p[2], p[3], dot)


def draw_die(c, f, b, s, dot):
    """Return an ascii art representation of a die.

    c, f, b, & s are boolean arguments. This function returns a multi-line
    string of the following form, where the letters in the diagram are either
    filled if the corresponding argument is true, or empty if it is false.
    
     -------
    | b   f |
    | s c s |
    | f   b |
     -------    

    Note: The sides with 2 and 3 dots have 2 possible depictions due to
          rotation. Either representation is acceptable.

    Note: This function uses Python syntax not yet covered in the course.
    
    c, f, b, s -- booleans; whether to place dots in corresponding positions
    dot        -- A length-one string to use for a dot
    """
    border = ' -------'

    def draw(b):
        return dot if b else ' '

    c, f, b, s = map(draw, [c, f, b, s])
    top = ' '.join(['|', b, ' ', f, '|'])
    middle = ' '.join(['|', s, c,   s, '|'])
    bottom = ' '.join(['|', f, ' ', b, '|'])
    return '\n'.join([border, top, middle, bottom, border])


# Game simulator

# def play(strategy, opponent_strategy, comments=False):
#     """Simulate a game and return 0 if the first player wins and 1 otherwise.
    
#     strategy -- The strategy function for the first player (who plays first)
#     opponent_strategy -- The strategy function for the second player
#     """
#     who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
#     "*** YOUR CODE HERE ***"
#     dice_4 = make_fair_die(4)
#     dice_6 = make_fair_die(6)

#     if comments:
#         print("--- Start of the play. ---")
#     player1_score = 0
#     player2_score = 0
#     while True:
#         if comments:
#             print("Current score: %d vs %d" % (player1_score, player2_score))

#         dice = dice_4 if (player1_score + player2_score) % 7 == 0 else dice_6
#         player1_plan = strategy(player1_score, player2_score)
#         player1_score += take_turn(player1_plan, dice, who='player1')
#         if player1_score >= 100:
#             who = 0
#             break
#         else:
#             dice = dice_4 if (player1_score + player2_score) % 7 == 0 else dice_6
#             player2_plan = opponent_strategy(player2_score, player1_score)
#             player2_score += take_turn(player2_plan, dice, who='player2')
#             if player2_score >= 100:
#                 who = 1
#                 break

#     if comments:
#         print("\nPlayer %d won! Scored: %d\n---End of the play.---\n\n" % (who + 1,
#             [player1_score, player2_score][who]))

#     return who


def play(strategy, opponent_strategy, comments=False):
    """Simulate a game and return 0 if the first player wins and 1 otherwise.
    
    strategy -- The strategy function for the first player (who plays first)
    opponent_strategy -- The strategy function for the second player
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    dice_4 = make_fair_die(4)
    dice_6 = make_fair_die(6)

    if comments:
        print("--- Start of the play. ---")
    player1_score = 0
    player2_score = 0
    while True:
        if comments:
            print("Current score: %d vs %d" % (player1_score, player2_score))

        dice = dice_4 if (player1_score + player2_score) % 7 == 0 else dice_6

        player1_plan = strategy(player1_score, player2_score)
        player2_plan = opponent_strategy(player2_score, player1_score)

        player1_score += take_turn(player1_plan, dice, who='player1')
        if player1_score >= 100:
            who = 0
            break
        else:
            player2_score += take_turn(player2_plan, dice, who='player2')
            if player2_score >= 100:
                who = 1
                break

    if comments:
        print("\nPlayer %d won! Scored: %d\n---End of the play.---\n\n" % (who + 1,
            [player1_score, player2_score][who]))

    return who


def other(who):
    """Return the other player, for players numbered 0 and 1.
    
    >>> other(0)
    1
    >>> other(1)
    0
    """
    return (who + 1) % 2


# Basic Strategies

def make_roll_until_plan(turn_goal=20):
    """Return a plan to roll until turn total is at least turn_goal."""
    def plan(turn):
        if turn >= turn_goal:
            return hold
        else:
            return roll
    return plan


def make_roll_until_strategy(turn_goal):
    """Return a strategy to always adopt a plan to roll until turn_goal.
    
    A strategy is a function that takes two game scores as arguments and
    returns a plan (which is a function from turn totals to actions).
    """
    "*** YOUR CODE HERE ***"

    def strategy(player_score, opnt_score):
        plan = make_roll_until_plan(turn_goal)
        return plan
    return strategy


def make_roll_until_strategy_test():
    """Test that make_roll_until_strategy gives a strategy that returns correct
    roll-until plans."""
    strategy = make_roll_until_strategy(15)
    plan = strategy(0, 0)
    assert plan(14) == roll, 'Should have returned roll'
    assert plan(15) == hold, 'Should have returned hold'
    assert plan(16) == hold, 'Should have returned hold'


# Experiments (Phase 2)

def average_value(fn, num_samples, *args):
    """Compute the average value returned by fn over num_samples trials.
    
    >>> d = make_test_die(1, 3, 5, 7)
    >>> average_value(d, 100)
    4.0
    """
    "*** YOUR CODE HERE ***"
    avg = 0.0
    for i in range(num_samples):
        avg += fn(*args)
    return avg/num_samples


def averaged(fn, num_samples=6000):
    """Return a function that returns the average_value of fn when called.

    Note: To implement this function, you will have to use *args syntax, a new
          Python feature introduced in this project.  See the project
          description for details.

    >>> die = make_test_die(3, 1, 5, 7)
    >>> avg_die = averaged(die)
    >>> avg_die()
    4.0
    >>> avg_turn = averaged(take_turn)
    >>> avg_turn(make_roll_until_plan(4), die, 'The player', False)
    3.0

    In this last example, two different turn scenarios are averaged.  
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 (then holds on the 7), scoring 5.
    Thus, the average value is 3.0

    Note: If this last test is called with comments=True in take_turn, the
    doctests will fail because of the extra output.
    """
    "*** YOUR CODE HERE ***"
    def avg(*args):
        return average_value(fn, num_samples, *args)
    
    return avg


def compare_strategies(strategy, baseline=make_roll_until_strategy(20)):
    """Return the average win rate (out of 1) of strategy against baseline."""
    as_first = 1 - averaged(play)(strategy, baseline)
    as_second = averaged(play)(baseline, strategy)
    return (as_first + as_second) / 2  # Average the two results

def eval_strategy_range(make_strategy, lower_bound, upper_bound):
    """Return the best integer argument value for make_strategy to use against
    the roll-until-20 baseline, between lower_bound and upper_bound (inclusive).

    make_strategy -- A one-argument function that returns a strategy.
    lower_bound -- lower bound of the evaluation range
    upper_bound -- upper bound of the evaluation range
    """
    best_value, best_win_rate = 0, 0
    value = lower_bound
    while value <= upper_bound:
        strategy = make_strategy(value)
        win_rate = compare_strategies(strategy)
        print(value, 'win rate against the baseline:', win_rate) 
        if win_rate > best_win_rate:
            best_win_rate, best_value = win_rate, value
        value += 1
    return best_value

def run_strategy_experiments(make_strategy, lower_bound, upper_bound):
    """Run a series of strategy experiments and report results."""
    "*** YOUR CODE HERE ***"
    best_val = eval_strategy_range(make_strategy, lower_bound, upper_bound)
    print("Best parameter is %d" % best_val)
    return best_val



def make_die_specific_strategy(four_side_goal, six_side_goal=22):
    """Return a strategy that returns a die-specific roll-until plan.
    
    four_side_goal -- the roll-until goal whenever the turn uses a 4-sided die
    six_side_goal -- the roll-until goal whenever the turn uses a 6-sided die

    """
    "*** YOUR CODE HERE ***"
    def strategy(player_score, opnt_score):
        if (player_score + opnt_score) % 7 == 0:  # use 4-sided goal to avoid '1's
            plan = make_roll_until_plan(four_side_goal)
        else: # use 6-sided die
            plan = make_roll_until_plan(six_side_goal)
        return plan
    return strategy


def make_pride_strategy(margin, turn_goal=22):
    """Return a strategy that wants to finish a turn winning by at least margin.

    margin -- the size of the lead that the player requires
    turn_goal -- the minimum roll-until turn goal, even when winning
    """
    "*** YOUR CODE HERE ***"
    def strategy(player_score, opnt_score):
        margin_goal = max(turn_goal, opnt_score - player_score + margin)
        plan = make_roll_until_plan(margin_goal)
        return plan

    return strategy


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"

    turn_goal = 22

    # pride strategy
    pride_goal = opponent_score - score + 4
    turn_goal = max(turn_goal, pride_goal)

    # die specific strategy and pride strategy
    if (score + opponent_score) % 7 == 0:
        turn_goal = 10

    # give opponent more side-4 dices
    # residue = (turn_goal + score + opponent_score) % 7
    # if residue <= 3:
        # turn_goal1 = turn_goal - residue
    # else:
        # turn_goal1 = turn_goal + 7 - residue
    # while turn_goal > 22:
        # turn_goal -= 7

    # optimal end performance
    turn_goal = min(turn_goal, 100 - score)

    plan = make_roll_until_plan(turn_goal)
    return plan


def interactive_strategy(score, opponent_score):
    """Prints total game scores and returns an interactive plan.
    
    Note: this function uses Python syntax not yet covered in the course.
    """
    print('You have', score, 'and they have', opponent_score, 'total score')
    def plan(turn):
        if turn > 0:
            print('You now have a turn total of', turn, 'points')
        while True:
            response = input('(R)oll or (H)old?')
            if response.lower()[0] == 'r':
                return roll
            elif response.lower()[0] == 'h':
                return hold
            print('Huh?')
    return plan


@main
def run():
    #take_turn_test()

    # Uncomment the next line to play an interactive game
    # play(interactive_strategy, make_roll_until_strategy(20))

    # Uncomment the next line to test make_roll_until_strategy
    # make_roll_until_strategy_test()

    # run_strategy_experiments(make_roll_until_strategy, 10, 25) # best is 22
    # run_strategy_experiments(make_die_specific_strategy, 5, 25)
    # run_strategy_experiments(make_pride_strategy, 0, 10)

    # test final strategy
    win_rate = compare_strategies(final_strategy, baseline=make_roll_until_strategy(20))
    print("Final strategy win rate = %f" % win_rate)
