# Patch Django BaseContext.__copy__ to support Python 3.14+
try:
    from django.template.context import BaseContext
    from copy import copy

    def safe_copy(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__ = copy(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = safe_copy
except ImportError:
    pass
