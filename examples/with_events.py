import discord
from discord.ext.paginator import Paginator


class PaginatorWithEvents(Paginator):
    # Paginator specific events

    async def on_setup(self, *args, **kwargs):
        # This is called by Paginator.run (when the paginator is sent)
        # You could set up a database connection here, for example.
        # But I would rather do that in on_start because you're wasting resources if the paginator is not started.

        print("Setup")

    async def on_start(self, interaction: discord.Interaction):
        # This is called when the paginator is started
        # If you need a database connection, you should set it up here.

        print("Start")

    async def on_stop(self, interaction: discord.Interaction):
        # This is called when the paginator is stopped with the stop button NOT WHEN IT TIMES OUT
        # If you needed a database connection, you should close it here.

        print("Stop")
