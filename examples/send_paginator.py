from typing import Optional

import discord
from discord.ext import commands
from discord.ext.paginator import Paginator

class MemberPaginator(Paginator):
    def __init__(self, client: commands.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

    async def get_page_count(self, interaction: discord.Interaction) -> int:
        return interaction.guild.member_count

    async def search_page(self, interaction: discord.Interaction, query: str) -> Optional[int]:
        for i, member in enumerate(interaction.guild.members):
            if query in member.name:
                print(i, member.name)
                return i

        return None

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        member = interaction.guild.members[current_page]

        return await interaction.response.edit_message(
            content=f"Member {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                discord.Embed(
                    title=str(member),
                    colour=discord.Color.green()
                )
                .add_field(name="ID", value=str(member.id))
                .add_field(name="Created at", value=str(member.created_at), inline=False)
                .add_field(name="Joined at", value=str(member.joined_at), inline=False)
                .add_field(name="Roles", value=", ".join([role.name for role in member.roles]))
            ),
            view=self
        )


# As a chat command
@bot.command(
    name="members"
)
async def show_members(ctx: commands.Context):
    await ctx.send(
        content="The guild members",
        view=await MemberPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )


# As a slash command
@bot.tree.command(
    name="members"
)
async def show_members(interaction: discord.Interaction):
    await interaction.response.send_message(
        content="The guild members",
        view=await MemberPaginator(
            interaction.client,
            interaction.user
        ).run()
    )
