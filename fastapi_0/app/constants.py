def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()
    return property(fget, fset)


class _Constants(object):
    @constant
    def MODEL_EXTENTIONS():
        return ["pkl", "h5", "hdf5"]


CONSTANTS = _Constants()
