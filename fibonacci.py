#!/usr/bin/env python3


def last_8(some_int):
    """Return the last 8 digits of an int

    :param int some_int: the number
    :rtype: int
    """

    some_str = str(some_int)
    out_int = int(some_str[-8:])

    return out_int



def optimized_fibonacci(f):

    accum = 0
    past1 = 1
    past2 = 1

    for z in range(f):
        past2 = past1
        past1 = accum
        accum = past2 + past1

    return accum



class SummableSequence(object):
    def __init__(self, *initial):
        self.my_lst = list(initial)


    def __call__(self, i):
        print("inside call")
        print(self.my_lst)

        for z in range(i):
            # print(self.my_lst)
            # print((sum(self.my_lst)))
            self.my_lst.append(sum(self.my_lst))
            self.my_lst.pop(0)

        return (self.my_lst.pop())


if __name__ == "__main__":

    print("f(100000)[-8:]", last_8(optimized_fibonacci(100000)))

    new_seq = SummableSequence(5, 7, 11)
    print("new_seq(100000)[-8:]:", last_8(new_seq(100000)))

    new_seq = SummableSequence(0, 1)
    print("new_seq(100000)[-8:]:", last_8(new_seq(45)))

    # print("new_seq(2)[-8:]:", last_8(new_seq(2)))