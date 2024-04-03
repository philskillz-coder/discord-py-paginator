import discord
from discord.ext.paginator import Paginator
from typing import Optional

# This is a paginator with infinite pages
class MyInstantPaginator(Paginator):
    async def page_validator(self, interaction: discord.Interaction, page: int, max_page: Optional[int]) -> bool:
        # in here you could implement a custom page validation
        # for example numbers can not be negative

        # explanation:
        # We didn't set a page limit hence the paginator doesn't jump to the last page after jumping back from the first page,
        # so we need to implement a custom page validation to prevent the user from going to negative pages
        return page >= 0

    async def page_update(self, interaction: discord.Interaction, current_page: int):
        return await self.edit_or_send(  # this is a helper function
            interaction,
            embed=(
                discord.Embed(
                    title=f"Number {current_page}",
                )
            ),
            view=self
        )

