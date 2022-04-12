from discord import app_commands, Embed, Color, Interaction
from discord.ext.paginator import paginator
from typing import Dict, Any

class GuildPaginator(paginator.Paginator):
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
            )
        }
    
@app_commands.command(
    name="guilds",
    description="Show all the guilds"
)
async def show_guilds(interaction: Interaction):
    await interaction.response.send_message(
        content="The bot guilds",
        view=await GuildPaginator(interaction.client, interaction.user).run()
    )