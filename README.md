# discord-py-paginator
[![wakatime](https://wakatime.com/badge/user/2480a8c6-ad22-414e-8414-755209ac465a/project/7d9961f6-dd80-4c4a-b88a-ebb69ef6183f.svg)](https://wakatime.com/badge/user/2480a8c6-ad22-414e-8414-755209ac465a/project/7d9961f6-dd80-4c4a-b88a-ebb69ef6183f) <br>
A view paginator for [discord.py](https://github.com/Rapptz/discord.py)</br></br>
This paginator is your best choice  if you want to display</br>
- large amounts of data (image gallery)
- Live generating data (any database)

**Keep in mind that this paginator is very complex and requires decent discord.py knowledge**</br>
**If you need any help regarding my paginator you can contact me [here](https://discord/APGDCfZbpW) (do _not_ ask in the discord.py server, they don't help with third-party libaries)**

# Issue reports
Issue reports are appreciated.
You can report one via
- the repositories [issues page](https://github.com/philskillz-coder/discord-py-paginator/issues)
- [Mail](mailto:github@theskz.dev?subject=Issue%20report%20for%20discord-py-paginator&body=Repository%20link%3A%0D%0Ahttps%3A%2F%2Fgithub.com%2Fphilskillz-coder%2Fdiscord-py-paginator)
- my [Discord Server](https://discord.gg/QjntPW9fHc)
- Discord direct message to `philskillz_`

thanks in advance.

# Changelog
<details>
  <summary>Click me</summary>
  
   ````
   # v2.1.0 -> v2.1.1:
   - Added feature for custom buttons
   
   # v2.0.6 -> v2.1.0:
   - Added feature for search button
   - Rewrite of the paginator class
   - Added more examples
   ````
</details>

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
   - Returns, how many pages you have. (~~If you have 'infinite' pages you can return ``None``~~ not possible yet)

## An example paginator class:

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
async def show_guilds(ctx: commands.Context):
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
- ``Paginator.on_setup`` (invoked when the paginator instance is created)
- ``Paginator.on_start`` (invoked when a user clicked the start button)
- ``Paginator.on_stop`` (invoked when a user clicked the stop button)

<br>

More examples can be found [here](https://github.com/philskillz-coder/discord-py-paginator/tree/main/examples)

## Config
You can configure your paginator subclass by setting the following class attributes:
An example with config can be found in the examples folder (not yet)


| **CONFIG NAME**                     | **TYPE**        | **VALUES**          | **EXPLANATION**                                                             | **INFO**                                             |
|-------------------------------------|-----------------|---------------------|-----------------------------------------------------------------------------|------------------------------------------------------|
| ``paginator_delete_when_finished``  | ``bool``        | ``True``, ``False`` | _Delete the pagination message when stopped_                                | Only works if the paginator message is not ephemeral |
| ``paginator_delete_delay``          | ``int``         | Any                 | _How long to wait after paginator stop to delete the message_               |                                                      |
| ``paginator_view_timeout``          | ``int``         | Any                 | _The view timeout_                                                          |                                                      |
| ``paginator_not_allowed_message``   | ``str``         | Any                 | _The message to send if a user isnt allowed to interact with the paginator_ |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``start_button_style``              | ``ButtonStyle`` | Any                 | _The style of the start button_                                             |                                                      |
| ``start_button_label``              | ``str``         | Any                 | _The label of the start button_                                             |                                                      |
| ``start_button_emoji``              | ``str``         | Any                 | _The emoji of the start button_                                             |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``stop_button_style``               | ``ButtonStyle`` | Any                 | _The style of the stop button_                                              |                                                      |
| ``stop_button_label``               | ``str``         | Any                 | _The label of the stop button_                                              |                                                      |
| ``stop_button_emoji``               | ``str``         | Any                 | _The emoji of the stop button_                                              |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``quick_navigation_button_enabled`` | ``bool``        | ``True``, ``False`` | _Is the quick navigation button enabled_                                    |                                                      |
| ``quick_navigation_button_style``   | ``ButtonStyle`` | Any                 | _The style of the  quick navigation button_                                 |                                                      |
| ``quick_navigation_button_label``   | ``str``         | Any                 | _The label of the quick navigation button_                                  |                                                      |
| ``quick_navigation_button_emoji``   | ``str``         | Any                 | _The emoji of the quick navigation button_                                  |                                                      |
| ``quick_navigation_error_message``  | ``str``         | Any                 | _The message when quick navigation input is not a number_                   |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``page_number_button_enabled``      | ``bool``        | ``True``, ``False`` | _Page number button enabled_                                                |                                                      |
| ``page_number_button_style``        | ``ButtonStyle`` | Any                 | _The style of the  page number button_                                      |                                                      |
| ``page_number_button_label``        | ``str``         | Any                 | _The label of the page number button_                                       |                                                      |
| ``page_number_button_emoji``        | ``str``         | Any                 | _The emoji of the page number button_                                       |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``search_button_enabled``    | ``bool``        | ``True``, ``False`` | _Is the search button enabled_                                              |                                                      |
| ``search_button_style``      | ``ButtonStyle`` | Any                 | _The style of the  search button_                                           |                                                      |
| ``search_button_label``      | ``str``         | Any                 | _The label of the search button_                                            |                                                      |
| ``search_button_emoji``      | ``str``         | Any                 | _The emoji of the search button_                                            |                                                      |
| ``search_button_error_message``     | ``str``         | Any                 | _The message when search input is not found_                                |                                                      ||                                     |                 |                     |                                                                             |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``first_element_button_enabled``    | ``bool``        | ``True``, ``False`` | _Whether the button to go to the first element should be enabled or not     |                                                      |
| ``first_element_button_style``      | ``ButtonStyle`` | Any                 | _The style of the first element button_                                     |                                                      |
| ``first_element_button_label``      | ``str``         | Any                 | _The label of the first element button_                                     |                                                      |
| ``first_element_button_emoji``      | ``str``         | Any                 | _The emoji of the first element button_                                     |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``prev_element_button_enabled``     | ``bool``        | ``True``, ``False`` | _Whether the button to go to the previous element should be enabled or not  |                                                      |
| ``prev_element_button_style``       | ``ButtonStyle`` | Any                 | _The style of the previous element button_                                  |                                                      |
| ``prev_element_button_label``       | ``str``         | Any                 | _The label of the previous element button_                                  |                                                      |
| ``prev_element_button_emoji``       | ``str``         | Any                 | _The emoji of the previous element button_                                  |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``next_element_button_enabled``     | ``bool``        | ``True``, ``False`` | _Whether the button to go to the next element should be enabled or not      |                                                      |
| ``next_element_button_style``       | ``ButtonStyle`` | Any                 | _The style of the next element button_                                      |                                                      |
| ``next_element_button_label``       | ``str``         | Any                 | _The label of the next element button_                                      |                                                      |
| ``next_element_button_emoji``       | ``str``         | Any                 | _The emoji of the next element button_                                      |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``last_element_button_enabled``     | ``bool``        | ``True``, ``False`` | _Whether the button to go to the last element should be enabled or not      |                                                      |
| ``last_element_button_style``       | ``ButtonStyle`` | Any                 | _The style of the last element button_                                      |                                                      |
| ``last_element_button_label``       | ``str``         | Any                 | _The label of the last element button_                                      |                                                      |
| ``last_element_button_emoji``       | ``str``         | Any                 | _The emoji of the last element button_                                      |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
| ``placeholder_button_enabled``      | ``bool``        | ``True``, ``False`` | _Whether placeholder buttons are used or not_                               |                                                      |
| ``placeholder_button_style``        | ``ButtonStyle`` | Any                 | _The style of the last element button_                                      |                                                      |
| ``placeholder_button_label``        | ``str``         | Any                 | _The label of the last element button_                                      |                                                      |
| ``placeholder_button_emoji``        | ``str``         | Any                 | _The emoji of the last element button_                                      |                                                      |
