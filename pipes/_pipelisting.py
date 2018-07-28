class BasePipe:
    pass


class Pipes:
    @classmethod
    def has(cls, other):
        return other in (
            cls.OutToFile,
            cls.OutToIn,
            cls.OutToFileA,
            cls.And,
            cls.AndS,
            cls.Or,
            cls.Cat,
            cls.CatOneLine,
        )

    class OutToIn(BasePipe):
        """
        redirects stdout to stdin
        """
        token = '|'

    class OutToFile(BasePipe):
        """
        redirects stdout to file
        """
        token = '>'

    class OutToFileA(BasePipe):
        """
        appends to file
        """
        token = '>>'

    class And(BasePipe):
        """
        chains 2 commands
        """
        token = '&'

    class AndS(BasePipe):
        """
        does following commands only if previous is successfull
        """
        token = '&&'

    class Or(BasePipe):
        """
        run next command only if previous fails
        """
        token = '||'

    class Cat(BasePipe):
        """
        sends data from file into command
        """
        token = '<'

    class CatOneLine(BasePipe):
        """
        sends one line of the file into command.
        """
        token = '<<'
