# discord-py-paginator
A view paginator for [discord.py](https://github.com/Rapptz/discord.py)</br></br>
<p style="text-align: center">

   [![wakatime](https://wakatime.com/badge/user/2480a8c6-ad22-414e-8414-755209ac465a/project/7d9961f6-dd80-4c4a-b88a-ebb69ef6183f.svg)](https://wakatime.com/badge/user/2480a8c6-ad22-414e-8414-755209ac465a/project/7d9961f6-dd80-4c4a-b88a-ebb69ef6183f) <br>
   <img src="https://img.shields.io/github/languages/top/philskillz-coder/discord-py-paginator">
   <img src="https://img.shields.io/github/stars/philskillz-coder/discord-py-paginator">
   <img src="https://img.shields.io/github/forks/philskillz-coder/discord-py-paginator">
   <br>
   <img src="https://img.shields.io/github/last-commit/philskillz-coder/discord-py-paginator">
   <img src="https://img.shields.io/github/license/philskillz-coder/discord-py-paginator">
   <br>
   <img src="https://img.shields.io/github/issues/philskillz-coder/discord-py-paginator">
   <img src="https://img.shields.io/github/issues-closed/philskillz-coder/discord-py-paginator">
   <br>
   <br>
   <img src="https://repobeats.axiom.co/api/embed/14e0edd1541b4f98e45020228ee1ba2a9d3b5311.svg">
</p>

## Table of Contents
- [Install](#install)
- [Usage](#usage)
- [Example](#example)
- [Changelog](#changelog)
- [Issue reports](#issue-reports)
- [Config](#config)

This paginator is your best choice  if you want to display</br>
- large amounts of data (image gallery)
- Live generating data (any database)

**Keep in mind that this paginator is very complex and requires decent discord.py knowledge**</br>
**If you need any help regarding my paginator you can contact me [here](https://discord/APGDCfZbpW) (do _not_ ask in the discord.py server, they don't help with third-party libaries)**

# Install
This library is tested with [discord.py](https://github.com/Rapptz/discord.py) v2.3.1:

```sh
pip install git+https://github.com/philskillz-coder/discord-py-paginator
```

## Usage
Step by step:<br/>
1. Create a class with ``paginator.Paginator`` as its parent
2. Create the ``Paginator.page_update`` method:</br>
   - In this method you get the interaction object and the current page passed.
   - In this method you can use the interaction object as in your commands.
3. Create the ``Paginator.get_page_count`` method (or set the ``static_page_count`` variable):</br>
   - In this method you get the interaction object passed.
   - Returns, how many pages you have. If you no page limit, return ``None`` or dont implement this method.


## Example
#### An example paginator class:
`````python
from discord.ext.paginator import paginator

class GuildPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)

    async def page_update(self, interaction: Interaction, current_page: int):
        guild = self.client.guilds[current_page]

        return await interaction.response.edit_message(
            content=f"Guild {current_page + 1}/{await self.get_page_count(interaction)}",
            embed=(
                Embed(
                    title="Guild",
                    colour=Color.green()
                )
                .add_field(name="Name", value=guild.name)
                .add_field(name="ID", value=str(guild.id))
                .add_field(name="Member count", value=str(guild.member_count), inline=False)
            ),
            view=self
        )


@bot.command(
    name="guilds",
    description="Show all the guilds"
)
async def show_guilds(ctx):
    await ctx.send(
        content="The bot guilds",
        view=await GuildPaginator(
            ctx.bot,
            ctx.author
        ).run()
    )
`````
<br>

additionally you implement these methods
- ``Paginator.page_validator`` (custom page number validator)
- ``Paginator.search_page`` (search for the first occurrence of a value on a page)
- ``Paginator.on_setup`` (invoked when the paginator instance is created)
- ``Paginator.on_start`` (invoked when a user clicked the start button)
- ``Paginator.on_stop`` (invoked when a user clicked the stop button)

<br>

Examples on all methods and features can be found in the [examples folder](./examples)

## Changelog
<details>
  <summary>Click me</summary>
  
   ````
   # v2.1.5 -> v2.1.6:
   - Added InstantPaginator (without start button)
   - Added more examples
   
   # v2.1.4 -> v2.1.5:
   - Added page_validator method
   
   # v2.1.3 -> v2.1.4:
   - Added kwargs to the Paginator class (passed to view)
   
   # v2.1.2 -> v2.1.3:
   - Added new config option _button_hidden
   - Merged InfinitePaginator into Paginator (Paginator is now infinite by default)
    
   # v2.1.1 -> v2.1.2:
   - Added InfinitePaginator
   ````
</details>

## Issue reports
Issue reports are appreciated.
You can report one via
- the repositories [issues page](https://github.com/philskillz-coder/discord-py-paginator/issues)
- [Mail](mailto:philipp.nikos@gmail.com?subject=Issue%20report%20for%20discord-py-paginator&body=Repository%20link%3A%0D%0Ahttps%3A%2F%2Fgithub.com%2Fphilskillz-coder%2Fdiscord-py-paginator)
- my [Discord Server](https://discord.gg/APGDCfZbpW)
- Discord direct message to `philskillz_`

thanks in advance.

## Config
All config options can be found in [config.md file](config.md)<br>
Examples can be found in [examples folder](./examples)
