class CaselessDict:
    def __init__(self, inDict=None, lowerfunc=None):
        self.dict = {}

        if inDict:
            for key in inDict:
                k = self._lower(key)
                self.dict[k] = (key, inDict[key])

        self.keyList = self.dict.keys()
        self.lowerfunc = lowerfunc

    def _lower(self, key):
        if self.lowerfunc:
            return self.lowerfunc(key)

        if hasattr(key, "lower") and callable(key.lower):
            return key.lower()

        return key

    def __iter__(self):
        self.iterPosition = 0
        return self

    def next(self):
        if self.iterPosition >= len(self.keyList):
            raise StopIteration
        x = self.dict[self.keyList[self.iterPosition]][0]
        self.iterPosition += 1
        return x

    def __getitem__(self, key):
        k = self._lower(key)
        return self.dict[k][1]

    def __delitem__(self, key):
        k = self._lower(key)
        del self.dict[k]

    def __setitem__(self, key, value):
        k = self._lower(key)
        self.dict[k] = (key, value)
        self.keyList = self.dict.keys()

    def has_key(self, key):
        k = self._lower(key)
        return k in self.keyList

    def __len__(self):
        return len(self.dict)

    def keys(self):
        return [v[0] for v in self.dict.values()]

    def values(self):
        return [v[1] for v in self.dict.values()]

    def items(self):
        return self.dict.values()

    def __contains__(self, item):
        return self.dict.has_key(self._lower(item))

    def __repr__(self):
        items = ", ".join([("%r: %r" % (k,v)) if v != self else ("%r: {...}" % (k)) for k,v in self.items()])
        return "{%s}" % items

    def __str__(self):
        return repr(self)

if __name__ == "__main__":
    d = CaselessDict()
    d["self"] = d
    d["booger"] = "yucky"
    print d["SELF"] # Ohai