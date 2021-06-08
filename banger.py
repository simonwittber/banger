import numbers


class Banger:
    def __init__(self, beats):
        self.__dict__.update(dict(
            beats = beats,
            tick = 0,
            children = {},
            enabled = True))

    def list(self, ind=0):
        indent = "  " * ind
        print("%sBanger(%s):"%(indent, self.beats))
        for k,v in self.__dict__["children"].items():
            if isinstance(v, Banger):
                v.list(ind + 1)
            else:
                print("%s- %s (%s)"%(indent,k,v))


    def __next__(self):
        d = self.__dict__
        d["tick"] += 1
        children = d["children"]
        beats = d["beats"]
        if d["tick"] % beats == 0:
            for i in children:
                fn = children[i]
                if isinstance(fn, Banger):
                    next(fn)
                else:
                    try:
                        if fn is not None: fn()
                    except Exception as e:
                        print("Error in %s (%s)"%(fn,e))
                        children[i] = None
        return beats

    def __setitem__(self, key, value):
        print("Error, you cannot set on this object.")

    def __getitem__(self, key):
        children = self.__dict__.get("children")
        if key in children:
            return children[key]
        if isinstance(key, numbers.Number):
            banger = children[key] = Banger(key)
            return banger

    def __delitem__(self, key):
        del self.children[key]

    def __setattr__(self, key, value):
        self.children[key] = value
        #self.__setitem__(key, value)

    def __delattr__(self, key):
        self.__delitem__(key)

    def __getattr__(self, key):
        self.__getitem__(key)

