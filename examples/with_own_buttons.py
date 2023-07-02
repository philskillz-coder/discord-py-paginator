import discord
from discord import ui
from discord.ext.paginator import Paginator


class MemberPaginator(Paginator):
    async def on_start(self, interaction: discord.Interaction):
        # set extra button to enabled
        self.extra.disabled = False

    @ui.button(
        label="Extra",
        disabled=True,  # disabled at first, will get enabled when started (see above)
        style=discord.ButtonStyle.success,
        row=3
    )
    async def extra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content="Extra!",
            ephemeral=True
        )
