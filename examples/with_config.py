from discord import app_commands, Embed, Color, Interaction
from discord.ext.paginator import paginator
from typing import Dict, Any

class GuildPaginator(paginator.Paginator):
    CONFIG = {
        "quick_navigation_button_enabled": False  # this paginator never uses quick nav by default
    }

    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)

    async def get_page_content(self, interaction: Interaction, page: int) -> Dict[str, Any]:
        # this method should return the arguments used for interaction.response.edit_message
        # e.g. {'content': 'hello'} means the message content will be edited to hello

        guild = self.client.guilds[page]
        # this cannot throw a index error because page is between 0 and the guild count

        return {
            "content": f"Guild {page+1}/{await self.get_page_count(interaction)}",
            "embed": (
                Embed(
                    title="Guild",
                    colour=Color.green()
                )
                .add_field(name="Name", value=guild.name)
                .add_field(name="ID", value=str(guild.id))
                .add_field(name="Member count", value=str(guild.member_count), inline=False)
            ),
            "ephemeral": True
        }


@app_commands.command(
    name="guilds_0",
    description="Show all the guilds"
)
async def guild_default_config(interaction: Interaction):
    await interaction.response.send_message(
        content="The bot guilds",
        view=await GuildPaginator(
            interaction.client,
            interaction.user
        ).run()  # in this case the config does not get overwritten so quick nav is not used
    )


@app_commands.command(
    name="guilds_1",
    description="Show all the guilds"
)
async def guild_overwrite_config(interaction: Interaction):
    await interaction.response.send_message(
        content="The bot guilds",
        view=await GuildPaginator(
            interaction.client,
            interaction.user,
            config={
                "quick_navigation_button_enabled": True
            }
        ).run()  # this instance of the GuildPaginator uses quick nav
    )


import discord
from discord.ext.paginator import paginator

my_paginator = paginator.Paginator.from_list(
    client,
    user,
    config={
        "paginator_ephemeral": True,
        "quick_navigation_button_enabled": False
    },
    data=[
        {
            "embed": discord.Embed(title=guild.name, description=f"This guild has {guild.member_count} members"),
        } for guild in client.guilds
    ]
)