"""
Execption to throw if the given problem is not found
"""
class ProblemNotFoundException(Exception):
    def __init__(self, *arg):
        self.args = arg
    
