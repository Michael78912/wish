import sys

class StdAbsorber:
    def __init__(self, file):
        self.file = file
        self.str = ''

    def set_file(self):
        self.old = getattr(sys, self.file)
        setattr(sys, self.file, self)

    def reset(self):
        setattr(sys, self.file, self.old)

    def write(self, item):
        self.str += item

    def flush(self):
        pass

    def close(self):
        pass

    def read(self):
        return self.str


class StdinSender:
    def __init__(self, data):
        self.data = data
    def set(self):
        self.old = sys.stdin
        sys.stdin = self

    def reset(self):
        sys.stdout = self.old

    def read(self):
        return self.data

    def readline(self, num):
        return self.data.split('\n')[num]

    def close(self):
        pass

    def flush(self):
        pass
