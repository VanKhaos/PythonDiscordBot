from discord.ext import commands


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""
