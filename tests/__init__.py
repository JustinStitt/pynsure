import unittest


def main():
    test_suite = unittest.TestLoader().discover("tests", pattern="test*.py")
    unittest.TextTestRunner(verbosity=2).run(test_suite)
