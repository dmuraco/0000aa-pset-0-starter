#!/usr/bin/env python3


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """

    some_str = str(some_int)
    out_int = int(some_str[-8:])

    return out_int



def optimized_fibonacci(fib):
    """Calculates a fibonacci value for a given number

    :param int some_int: the number
    :rtype: int
    """
    accum = 0
    past1 = 1
    past2 = 1

    for value in range(fib):
        past2 = past1
        past1 = accum
        accum = past2 + past1

    return accum



class SummableSequence(object):
    def __init__(self, *initial):
        self.my_lst = list(initial)


    def __call__(self, i):
        """Calculates a fibonacci value for a given number

        :param int i: the sequence length
        :rtype: int
        """

        start = len(self.my_lst) - 2

        for z in range(start, i-1):
            self.my_lst.append(sum(self.my_lst))
            self.my_lst.pop(0)
        return self.my_lst[-1]


if __name__ == "__main__":

    print("f optimized fib ", last_8(optimized_fibonacci(100000)))
    #
    #
    # new_seq = SummableSequence(0, 1)
    # print("fib seq[-8:]:", last_8(new_seq(8)))

    # f(100,000) = 28746875
    # im passing 78790626
    #
    # new_seq = SummableSequence(0, 1)
    # print("fib seq 999999[-8:]:", last_8(new_seq(99999)))
    #
    # new_seq = SummableSequence(0, 1)
    # print("fib seq 100000[-8:]:", last_8(new_seq(100000)))
    #
    # new_seq = SummableSequence(0, 1)
    # print("fib seq 100001[-8:]:", last_8(new_seq(100001)))


    # new_seq = SummableSequence(1, 2, 3)
    # print("new_seq(5):", last_8(new_seq(5)))
    #
    # new_seq = SummableSequence(5, 7, 11)
    # print("new_seq(5) 5,7,11:", last_8(new_seq(5)))
    #
    #
    # new_seq = SummableSequence(5, 7, 11)
    # print("new_seq(99998)[-8:]:", last_8(new_seq(99998)))  # 64224133
    #
    # new_seq = SummableSequence(5, 7, 11)
    # print("new_seq(99999)[-8:]:", last_8(new_seq(99999)))  # 64224133
    #
    new_seq = SummableSequence(5, 7, 11)
    print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))  # 64224133
    #
    # new_seq = SummableSequence(5, 7, 11)
    # print("new_seq(100001)[-8:]:", last_8(new_seq(100001)))  # 87834603
    #
    # new_seq = SummableSequence(5, 7, 11)
    # print("new_seq(100002)[-8:]:", last_8(new_seq(100002)))  # 87834603