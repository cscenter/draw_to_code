class TestNotPassed(BaseException):
    pass


def check_eq(x, y):
    if x != y:
        print("Error: expected {}, got {}".format(str(x), str(y)))
        raise TestNotPassed


def check_almost_eq(x, y):
    if abs(x - y) > 0.0000001:
        print("Error: expected {}, got {}".format(str(x), str(y)))
        raise TestNotPassed
