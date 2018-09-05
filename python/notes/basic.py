# Python scope order

# LEGB RULE
#   LOCAL
#   ENCLOSING
#   GLOBAL
#   BUILT IN

# Decorators
def hello(name='Jose'):
  print('the hello() func has been run')

  def greet():
    return "    This is inside the greet()"

  def welcome():
    return "    This is inside the welcome()"

  if name=="Jose":
    return greet
  else:
    return welcome

x = hello()
x()

def new_decorator(func):
  def wrap_func():
    print("some code before executing func")

    func()

    print("code here, after executing func()")

  return wrap_func

@new_decorator
def func_needs_decorator():
  print('Please decorate me')

#func_needs_decorator = new_decorator(func_needs_decorator)
func_needs_decorator()

