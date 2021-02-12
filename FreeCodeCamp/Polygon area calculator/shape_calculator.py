class Rectangle:
  ''' 
  Class that creates an instance of Rectangle
  with given params 'width' and 'height' 
  '''
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height


  def __str__(self):
    return f'Rectangle(width={self.width}, height={self.height})'

  
  def set_width(self, width: int):
    self.width = width

  
  def set_height(self, height: int):
    self.height = height


  def get_area(self) -> int:
    return self.width * self.height

  
  def get_perimeter(self) -> int:
    return (2*self.width + 2*self.height)


  def get_diagonal(self) -> int:
    return (self.width ** 2 + self.height ** 2) ** .5


  def get_picture(self) -> str:
    ''' 
    Returns a string that represents the shape using lines of "*" 
    '''
    h = self.height
    w = self.width
    if h > 50 or w > 50:
      return 'Too big for picture.'
    else:
      shape = []
      for i in range(h):
        shape.append('*' * w)
      return ('\n'.join(shape))+'\n'


  def get_amount_inside(self, figure: object) -> int:
    '''
    Returns the number of times the passed in shape of the figure could fit inside the shape (with no rotations)
    '''
    return self.get_area() // figure.get_area() 


class Square(Rectangle):
  '''
  Subclass of Rectangle as a rectangle with width=height
  '''
  def __init__(self, side, width=None, height=None):
    super().__init__(width, height)
    self.width = side
    self.height = side


  def __str__(self):
    return f'Square(side={self.width})'


  def set_side(self, side: int):
    self.width = side
    self.height = side

  
  def set_width(self, width: int):
    super().set_width(width)
    self. height = width

  
  def set_height(self, height: int):
    super().set_height(height)
    self. width = height
