from discord.ext import commands


class AuthorizationError(commands.errors.CheckFailure):
    pass

class HackTheBotNotRegistered(commands.errors.CheckFailure):
    pass

class HackTheBotUnknownError(commands.errors.CheckFailure):
    pass
class HackTheBotInvalidTeamName(commands.errors.CheckFailure):
    pass