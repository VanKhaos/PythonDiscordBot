from discord.ext import commands

from lib.is_pinned import is_not_pinned


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='clear')
    @commands.is_owner()
    async def clear(self, ctx, args):
        author = ctx.message.author
        content = ctx.message.content
        channel = ctx.message.channel
        if author.permissions_in(channel).manage_messages:
            args = content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await channel.purge(limit=count, check=is_not_pinned)
                    await channel.send('{} Nachrichten gelöscht'.format(len(deleted) - 1))

    @commands.command(name='discords')
    @commands.is_owner()
    async def discords(self, ctx):
        for server in self.bot.guilds:
            await ctx.send(f'Ich bin auf folgenden Server: {server.name}')
            # DEBUG LOG
            print(server.name)


def setup(bot):
    bot.add_cog(OwnerCog(bot))
