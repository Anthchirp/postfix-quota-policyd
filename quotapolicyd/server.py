class Server():
  def __init__(self, *args, **kwargs):
    self.opened = False
    self.closed = False

  def __enter__(self):
    self.opened = True
    return self

  def __exit__(self, *args):
    self.closed = True

  def listen(self):
    pass
