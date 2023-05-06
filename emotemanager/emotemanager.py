import discord
import io
import aiohttp
import logging
from typing import TYPE_CHECKING

from redbot.core import commands
from redbot.core.bot import Red

log = logging.getLogger("ngL.emotemanager")


class EmoteManager(commands.Cog):
    """
    EmoteManager
    """

    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

    async def red_delete_data_for_user(self, **kwargs) -> None:
        """Nothing to delete"""
        return

    @commands.guild_only()
    @commands.hybrid_group(aliases=["em"])
    async def emotemanager(self, ctx: commands.Context):
        """Manage your emotes"""

    @emotemanager.command()
    @commands.has_permissions(manage_emojis=True)
    async def copy(self, ctx: commands.Context, emotes: commands.Range[str, 1, 64]) -> None:
        """
        Copy emotes to your server

        Just write the emote behind the command. You can copy multiple emotes at once.

        **Examples:**
        - `[p]em copy  <emote>`
        """

        # guild only check in group
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.Member)

        for emoji in emotes.split():
            emote = emoji.split(":")[2].replace(">", "")
            name = f"{ctx.guild.name}_{emoji.split(':')[1].replace('>', '')}"

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://cdn.discordapp.com/emojis/{emote}.png") as request:
                    if request.status == 200:
                        data = io.BytesIO(await request.read())
                        await ctx.guild.create_custom_emoji(name=name.lower(), image=data.read())
                    else:
                        continue

        await ctx.send(f"Successfully copied {len(emotes.split())} emotes.")
