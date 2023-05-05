import discord
import logging
import random
from redbot.core import commands
from redbot.core.bot import Red

log = logging.getLogger("ngL.zcg")

class ZCG(commands.Cog):
    """
    Birthdays

    Set yours and get a message and role on your birthday!
    """

    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.vc_names = [
            "Bastis Zeugenstand",
            "Caros Goldfischglas",
            "Christians Parthenon",
            "Felix Backstabroom",
            "Grevens Tanzschule",
            "Jans Kartell",
            "Jules Theater",
            "Julians Kiosk",
            "Johnnys Richterzimmer",
            "Lukas Bolzplatz",
            "Manus Stilleecke",
            "Max Sexdungeon",
            "Nigls Verhörraum",
            "Nils Salzgrotte",
            "Peanuts Boxengasse",
        ]
        self.category_ids = [927963463144325200, 982625359356915752]
        self.mod_rid = 918480035709603860

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceChannel,
        after: discord.VoiceChannel,
    ):
        """
        Listens for voice state updates.
        :param member: The member that changed their voice state.
        :param before: The voice channel the member was in before the change.
        :param after: The voice channel the member is in after the change.
        """

        if after.channel is not None:
            # Interception of user/moderator actions (mute / unmute / etc)
            if after.channel is not None and before.channel is not None:
                if after.channel.id == before.channel.id:
                    return

            guild = self.bot.get_guild(after.channel.guild.id)
            category = guild.get_channel(after.channel.category_id)

            if after.channel.category_id in self.category_ids:
                if len(after.channel.members) == 1:
                    vc_name = random.choice(self.vc_names)
                    while vc_name == after.channel.name:
                        vc_name = random.choice(self.vc_names)
                    channel = await category.create_voice_channel(
                        name=vc_name, bitrate=vc.get_bitrate(guild), reason="Channel created"
                    )

                    # Add access to voice channels for mod role
                    try:
                        role = guild.get_role(self.mod_rid)
                        await channel.set_permissions(role, view_channel=True, connect=True, manage_channels=True)
                    except ValueError:
                        self.bot.logger.error(f"Role with ID {self.mod_rid} not found.")

        if before.channel is not None:
            before_channel = self.bot.get_channel(before.channel.id)

            if before_channel is not None and before_channel.category_id in self.category_ids:
                if len(before_channel.members) == 0:
                    await before_channel.delete(reason="Channel is empty")

        if after.channel is None:
            guild = self.bot.get_guild(before.channel.guild.id)
            category = guild.get_channel(before.channel.category_id)

            if before_channel.category_id in self.category_ids:
                if len(category.channels) == 0:
                    vc_name = random.choice(self.vc_names)
                    await category.create_voice_channel(
                        name=vc_name, bitrate=vc.get_bitrate(guild), reason="Channel was empty"
                    )

    async def red_delete_data_for_user(self, **kwargs) -> None:
        """Nothing to delete"""
        return
