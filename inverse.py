from itertools import izip, cycle

def inverse(text, key="somekey"):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in izip(text, cycle(key))])

if __name__ == "__main__":
    key = "abcdefg"
    orig = "ohai thar"

    print "Original: {0}\nKey: {1}".format(orig, key)

    in_ = inverse(orig, key)
    print "Inversed: {0}".format(repr(in_))

    out_ = inverse(in_, key)
    print "Inversed again: {0}".format(out_)