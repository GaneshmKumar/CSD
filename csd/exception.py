"""
Execption to throw if the given problem is not found
"""
class ProblemNotFoundException(Exception):
    def __init__(self, *arg):
        self.args = arg

"""
Execption to throw if the given language is not available
"""
class InvalidLanguageException(Exception):
    def __init__(self, *arg):
        self.args = arg

"""
Execption to throw if the given status is not available
"""
class InvalidStatusException(Exception):
    def __init_(self, *arg):
        self.args = arg
