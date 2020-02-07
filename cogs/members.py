import discord
from discord import Member
from discord.ext import commands
from lib.is_pinned import is_not_pinned


class MembersCommands(commands.Cog, name='Befehle für Jedermann'):
    def __init__(self, bot):
        self.bot = bot

    # Command - Userinfo
    @commands.command(name='userinfo')
    async def userinfo(self, ctx, args):
        """Userinfo <username> -> Zeigt ein paar Userinfos"""
        content = ctx.message.content
        channel = ctx.message.channel
        args = content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, ctx.message.guild.members)
            if member:
                embed = discord.Embed(title=f'UserInfo für {member.name}',
                                      description=f'Dies ist die UserInfo für den User {member.mention}',
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d.%m.%Y'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d.%m.%Y'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += f'{role.mention} \r\n'
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Footer')
                embed_message = await channel.send(embed=embed)
                # Add Reaction (UTF8 EMOJI)
                await embed_message.add_reaction('💖')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCommands(bot))
