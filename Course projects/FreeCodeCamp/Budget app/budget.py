class Category:
  '''
  Class creates a budget category and main operations for it:
  deposit, withdraw and transfer. Also there are supporting
  functions like get_balance and check_funds. When printed,
  shows ledger statement.
  '''
  def __init__(self, category):
      self.category = category
      self.ledger = []
      self.balance = 0


  def __repr__(self):
    return f'{self.category}'

  
  def __len__(self):
    return len(self.category)

  
  def __str__(self) -> str:
    '''
    Prints ledger statement with all operations and total
    '''
    display = []
    display.append(self.category.capitalize().center(30, '*'))
    for operation in self.ledger:
      description = operation['description'][:23]
      amount = f"{operation['amount']:.2f}"[:7]
      str = description + ' '*(30 - len(description) - len(amount)) + amount
      display.append(str)
    display.append(f'Total: {self.balance}')
    return '\n'.join(display)


  def deposit(self, amount: [int, float], description: str=''):
    operation = {'amount': amount, 'description': description}
    self.ledger.append(operation)
    self.balance += amount


  def withdraw(self, amount: [int, float], description: str='') -> bool:
    operation = {'amount':-1*(amount), 'description': description}
    operation_status = False
    if self.check_funds(amount):
      self.ledger.append(operation)
      self.balance -= amount
      operation_status = True

    return operation_status


  def get_balance(self) -> int:
    return self.balance

  
  def transfer(self, amount: [int, float], category: object) -> bool:
    operation_status = False
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.__repr__()}")
      category.deposit(amount, f"Transfer from {self.category}")
      operation_status = True

    return operation_status


  def check_funds(self, amount: [int, float]):
    return True if self.balance >= amount else False


def create_spend_chart(categories: list) -> str:
  '''
  Function creates a vertical bar chart. Takes a list of categories 
  as an argument and shows the percentage spent in each category 
  (down to the nearest 10 persents)
  '''
  # count withdrawals for each category and calculate total sum of expences
  expenses = []
  sum = 0
  for category in categories:
    expense = category.ledger[0]['amount'] - category.balance
    expenses.append(expense)
    sum += expense

  # count persentage for expenses in each category down to the nearest 10 persents
  persentage = []
  for expense in expenses:
    expense = (round((expense/sum)*100))//10*10
    persentage.append(expense)
  
  # prepare variables for a bar chart
  number_of_categories = len(categories)
  width = number_of_categories*3 + 5
  
  chart = ['Percentage spent by category']

  # create upper part of the chart: vertical axe 0 - 100 and bars for each
  # category according to their persentage expenditure
  pers = 100
  upper_chart = ''
  for i in range(11):
    upper_chart += f'{pers:>3}| '
    for j in range(number_of_categories):
      a = 'o' if pers <= persentage[j] else ''
      upper_chart += f'{a:<3}'
    upper_chart += '\n' if pers != 0 else ''
    pers -= 10

  chart.append(upper_chart)

  # add dash
  chart.append('    ' + '-'*(width-4))

  # create lower part of the chart with
  # each category name written vertically below the bar
  length = len(max(categories, key=len))
  lower_chart = ''
  for i in range(length):
    lower_chart += '     '
    for category in categories:
      category = category.__repr__()
      try:
        syl = category[i]
      except IndexError:
        syl = ' '
      lower_chart += f'{syl}  '
    lower_chart += '\n' if i != (length-1) else ''

  chart.append(lower_chart)

  return '\n'.join(chart)
