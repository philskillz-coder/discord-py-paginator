import discord
from discord.ext.paginator import InstantPaginator


# This is a paginator that will start without a start button
class MyInstantPaginator(InstantPaginator):
    async def get_page_count(self, interaction: discord.Interaction) -> int:
        return 10

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        return await self.edit_or_send( # this is a helper function
            interaction,
            embed=(
                discord.Embed(
                    title=f"Number {current_page}",
                )
            ),
            view=self
        )

