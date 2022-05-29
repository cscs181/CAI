class BotException(Exception):
    pass


class BotMutedException(BotException):
    pass


class LimitException(Exception):
    pass


class AtAllLimitException(LimitException):
    pass


class GroupMsgLimitException(LimitException):
    pass
