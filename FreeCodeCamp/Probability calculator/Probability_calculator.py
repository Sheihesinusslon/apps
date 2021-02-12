import copy
import random
from collections import Counter

class Hat:
  '''
  Class takes a variable number of arguments that specify the number of balls of each color that are in the hat. It saves all balls as
  a list of strings in instance variable 'contents'.
  '''
  def __init__(self, **kwargs):
    contents = []
    for k, v in kwargs.items():
      for i in range(v):
        contents.append(k)
    self.contents = contents


  def draw(self, num_draw: int):
    '''
    Method accepts an argument indicating the number of balls to draw from the hat. It randomly picks balls, removes them from the hat and returns final selection as a list of strings.
    '''
    # If the number of balls to draw exceeds the available quantity, return all the balls
    if num_draw > len(self.contents):
      return self.contents
    
    selection = []
    for i in range(num_draw):
      pick = random.choice(self.contents)
      self.contents.remove(pick)
      selection.append(pick)
    return selection
    


def experiment(hat: object, expected_balls: dict, num_balls_drawn: int, num_experiments: int) -> float:
  '''
  :param hat: A hat object containing balls
  :param expected_balls: An object indicating the exact group of balls to attempt to draw from the hat for the experiment
  :param num_balls_drawn: The number of balls to draw out of the hat in each experiment
  :param num_experiments: The number of experiments to perform
  :returns: a probability as M/N, where M - number of times when expected selection of balls showed up in actual selection, N - number of experiments performed
  '''
  count = 0
  for i in range(num_experiments):
    # copy object, draw balls and turn selection into a dict
    h = copy.deepcopy(hat)
    actual_balls = Counter(h.draw(num_balls_drawn))
    # try to compare random selection with expexted balls
    try:
      # if all expected balls in the selection, count experiment as successful 
      compare = [actual_balls[color] >= expected_balls[color] for color in expected_balls.keys()]
      if all(compare):
        count += 1
      # if balls with some color are not in the selection, skip this experiment
    except KeyError:
      pass

  return count / num_experiments
