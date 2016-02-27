def test_continuous_integration_works():
  import quotapolicyd.citest
  assert quotapolicyd.citest.add(1, 2) == 3
