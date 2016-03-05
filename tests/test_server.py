import mock
from quotapolicyd.server import Server
import time

def test_start_server():
  def callback(*args, **kwargs):
    pass

  with Server(callback=callback) as srv:
    srv.listen()
    server_reference = srv
    time.sleep(0.3)

  assert server_reference.opened
  assert server_reference.closed

