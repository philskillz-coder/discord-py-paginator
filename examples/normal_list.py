from abc import ABC

from discord import app_commands, Embed, Color, Interaction
from discord.ext.paginator import paginator


class ColorPaginator(paginator.Paginator, ABC):
    pass
    
@app_commands.command(
    name="colors",
    description="Show some colors"
)
async def show_colors(interaction: Interaction):
    await interaction.response.send_message(
        content="Nice colors",
        view=await ColorPaginator.from_list(
            interaction.client,
            interaction.user,
            data=[
                {
                    "content": "The color red",
                    "embed": Embed(title="Red", color=Color.red()),
                },
                {
                    "content": "The color green",
                    "embed": Embed(title="Green", color=Color.green()),
                },
                {
                    "content": "The color blue",
                    "embed": Embed(title="Blue", color=Color.blue()),
                }
            ]
        ).run()
    )
