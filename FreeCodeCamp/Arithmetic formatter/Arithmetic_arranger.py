def check_errors(problems: list):
  '''
  function takes an array of problems and checks it
  for all necessary errors
  :return: string with error message, if any occured,
  or False if no errors revealed
  '''
  if len(problems) > 5:
    return 'Error: Too many problems.'
  for problem in problems:
    chars = problem.split()
    for char in chars:
      if char == '*' or char == '/':
        return "Error: Operator must be '+' or '-'."
      elif len(char) > 4:
        return 'Error: Numbers cannot be more than four digits.'
      elif not char.isdigit() and not char in '+-':
        return 'Error: Numbers must only contain digits.'
      else:
        pass
  return False


def calculate(a: str, b: str, operator: str):
  '''
  function takes two opperands a and b and operator,
  makes calculations,
  :return: string with resulted value
  '''
  if operator=='+':
    return str(int(a)+int(b))
  else:
    return str(int(a)-int(b))


def display(problems: list, answer: bool):
  '''
  function takes an array of problems and optional bool param 
  'answer', processes problems and formats them vertically and side-by-side
  :return: an array of strings, containing every level of 
  problems top-down
  '''
  # preparing a list with empty strings depending on optional param
  display = ['','',''] if not answer else ['','','','']
  for problem in problems:
    # split every problem on partials and define max length
    operand_1, operator, operand_2 = problem.split()
    longest = operand_1 if len(operand_1) > len(operand_2) else operand_2
    length = len(longest) + 2
    # add properly formatted partials to every level top-down
    display[0] +=  ' '*(length-len(operand_1)) + operand_1 + '    '
    display[1] += operator + ' '*(length-len(operand_2)-1) + operand_2 + '    '
    display[2] += '-'*length + '    '
    # if optional param 'answer' is True, adds level with answers
    if answer:
      result = calculate(operand_1, operand_2, operator)
      display[3] += ' '*(length-len(result)) + result + '    '
  # final string formatting for every level
  for i in range(len(display)):
    display[i] = display[i].rstrip()
    if i < len(display)-1:
      display[i] += '\n'
  # returns an array of formatted strings
  return display

def arithmetic_arranger(problems: list, answer=False):
  '''
  main function takes an array of problems and has optional bool param
  'answer' to show the result of calculations (False by default),
  processes problems,
  :return: string with error message or
  strings with properly rearranged problems
  '''
  error = check_errors(problems)
  if error:
    return error
  else:
    console = display(problems, answer)
    return ''.join(console)