class UnknownQuestionId(Exception):
    """Raised when failed to determine question id"""
    pass


class IncorrectQuestionId(Exception):
    """Raised when incorrect question_id param was given"""
    pass
