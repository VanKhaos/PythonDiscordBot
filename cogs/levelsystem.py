import asyncio
import discord
from discord.ext import commands
import json

from discord.utils import get

from config.discord_config import cat_bot_id


class Levels(commands.Cog, name='LevelSystem'):
    def __init__(self, bot):
        self.bot = bot

        with open('data/lvl_users.json', 'r') as f:
            self.users = json.load(f)

        self.bot.loop.create_task(self.save_users())

    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open('data/lvl_users.json', 'w') as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(5)

    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]['exp']
        cur_lvl = self.users[author_id]['level']
        cur_rank = self.users[author_id]['rank']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            self.users[author_id]['level'] += 1
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            # DEBUG print(f'BOT MSG: {channel} - {author}: {content}')
            return

        author_id = str(message.author.id)
        role_id = message.guild.roles

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['level'] = 1
            self.users[author_id]['exp'] = 0
        if role_id == cat_bot_id:
            self.users[author_id]['exp'] += 1
        else:
            # Keine EXP an Bots
            self.users[author_id]['exp'] += 0
            # DEBUG print(f'BOT MSG: {channel} - {author}: {content}')

        if self.lvl_up(author_id):
            await message.channel.send(
                f'{message.author.mention} has leveld up to {self.users[author_id]["level"]}')

    @commands.command()
    async def levels(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        author_id = str(member.id)
        if not author_id in self.users:
            await ctx.channel.send('User hat noch kein Level')
        else:
            embed = discord.Embed(color=0x22a7f0, timestamp=ctx.message.created_at)
            embed.set_author(name=f'{member.display_name} - Level {self.users[author_id]["level"]}',
                             icon_url=member.avatar_url)
            embed.add_field(name='Level', value=self.users[author_id]['level'])
            embed.add_field(name='EXP', value=self.users[author_id]['exp'])
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
