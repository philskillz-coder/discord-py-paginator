# discord-py-paginator
A view paginator for [discord.py](https://github.com/Rapptz/discord.py)

## Installing
This library works with [discord.py](https://github.com/Rapptz/discord.py) v2.1.0a:

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
```python
from discord import Interaction, Embed
from discord.ext.paginator import paginator
from discord import Color

class MySimplePaginator(paginator.Paginator):
    _cached_page_count = None

    async def get_page_count(self, interaction: Interaction) -> int:
        self._cached_page_count = len(self.client.guilds)
        return self._cached_page_count

    async def page_update(self, interaction: Interaction, page: int):
        guild = self.client.guilds[page]

        await interaction.response.edit_message(
            embed=Embed(
                title="Guild %s" % guild.name,
                colour=Color.green()
            )
            .add_field(name="ID", value=str(guild.id))
            .add_field(name="Member count", value=str(guild.member_count))
            .set_author(name=f"Page {page + 1}/{self._cached_page_count}"),
            view=self  # !very important! 
        )
```

to send you paginator do the following:
`````python
my_paginator = MySimplePaginator(
   client=interaction.client,
   user=interaction.user
)

await interaction.response.send_message(
    content="My awesome guild paginator",
    view=await my_paginator.run()
)
`````

More examples can be found [here](https://github.com/philskillz-coder/discord-py-paginator/tree/main/examples)

## Config
You can configure your paginator subclass and instance via a config dict.
An example with config can be found in the examples folder

### All config options

| **CONFIG NAME**                      | **TYPE**        | **VALUES**                    | **EXPLANATION**                                                            | **INFO**                                                                                                                    
|--------------------------------------|-----------------|-------------------------------|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| ``paginator_delete_when_finished``   | ``bool``        | ``True``, ``False``           | _Delete the pagination message when stopped_                               | Only works if the paginator message is not ephemeral                                                                        |
| ``paginator_delete_delay``           | ``int``         | Any                           | _How long to wait after paginator stop to delete the message_              |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``start_button_enabled``             |                 |                               |                                                                            | **Option not changable**                                                                                                    |
| ``start_button_style``               | ``ButtonStyle`` | Any                           | _The style of the start button_                                            |                                                                                                                             |
| ``start_button_label``               | ``str``         | Any                           | _The label of the start button_                                            |                                                                                                                             |
| ``start_button_emoji``               | ``str``         | Any                           | _The emoji of the start button_                                            |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``stop_button_enabled``              |                 |                               |                                                                            | **Option not changable**                                                                                                    |
| ``stop_button_style``                | ``ButtonStyle`` | Any                           | _The style of the stop button_                                             |                                                                                                                             |
| ``stop_button_label``                | ``str``         | Any                           | _The label of the stop button_                                             |                                                                                                                             |
| ``stop_button_emoji``                | ``str``         | Any                           | _The emoji of the stop button_                                             |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``quick_navigation_button_enabled``  | ``bool``        | ``True``, ``False``           | _Is the quick navigation button enabled_                                   |                                                                                                                             |
| ``quick_navigation_button_style``    | ``ButtonStyle`` | Any                           | _The style of the  quick navigation button_                                |                                                                                                                             |
| ``quick_navigation_button_label``    | ``str``         | Any                           | _The label of the quick navigation button_                                 |                                                                                                                             |
| ``quick_navigation_button_emoji``    | ``str``         | Any                           | _The emoji of the quick navigation button_                                 |                                                                                                                             |
| ``quick_navigation_error_message``   | ``str``         | Any                           | _The message when quick navigation input is not a number_                  |                                                                                                                             |
| ``quick_navigation_error_ephemeral`` | ``bool``        | ``True``, ``False``           | _Whether the error message should be ephemeral or not_                     |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``first_element_button_enabled``     | ``bool``        | ``True``, ``False``           | _Whether the button to go to the first element should be enabled or not    |                                                                                                                             |
| ``first_element_button_style``       | ``ButtonStyle`` | Any                           | _The style of the first element button_                                    |                                                                                                                             |
| ``first_element_button_label``       | ``str``         | Any                           | _The label of the first element button_                                    |                                                                                                                             |
| ``first_element_button_emoji``       | ``str``         | Any                           | _The emoji of the first element button_                                    |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``prev_element_button_enabled``      | ``bool``        | ``True``, ``False``           | _Whether the button to go to the previous element should be enabled or not |                                                                                                                             |
| ``prev_element_button_style``        | ``ButtonStyle`` | Any                           | _The style of the previous element button_                                 |                                                                                                                             |
| ``prev_element_button_label``        | ``str``         | Any                           | _The label of the previous element button_                                 |                                                                                                                             |
| ``prev_element_button_emoji``        | ``str``         | Any                           | _The emoji of the previous element button_                                 |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``next_element_button_enabled``      | ``bool``        | ``True``, ``False``           | _Whether the button to go to the next element should be enabled or not     |                                                                                                                             |
| ``next_element_button_style``        | ``ButtonStyle`` | Any                           | _The style of the next element button_                                     |                                                                                                                             |
| ``next_element_button_label``        | ``str``         | Any                           | _The label of the next element button_                                     |                                                                                                                             |
| ``next_element_button_emoji``        | ``str``         | Any                           | _The emoji of the next element button_                                     |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``last_element_button_enabled``      | ``bool``        | ``True``, ``False``           | _Whether the button to go to the last element should be enabled or not     |                                                                                                                             |
| ``last_element_button_style``        | ``ButtonStyle`` | Any                           | _The style of the last element button_                                     |                                                                                                                             |
| ``last_element_button_label``        | ``str``         | Any                           | _The label of the last element button_                                     |                                                                                                                             |
| ``last_element_button_emoji``        | ``str``         | Any                           | _The emoji of the last element button_                                     |                                                                                                                             |
|                                      |                 |                               |                                                                            |                                                                                                                             |
| ``placeholder_button_enabled``       |                 |                               |                                                                            | **Option Not Changable**                                                                                                    |
| ``placeholder_button_style``         | ``ButtonStyle`` | Any                           | _The style of the last element button_                                     |                                                                                                                             |
| ``placeholder_button_label``         | ``str``         | Any                           | _The label of the last element button_                                     |                                                                                                                             |
| ``placeholder_button_emoji``         | ``str``         | Any                           | _The emoji of the last element button_                                     |                                                                                                                             |
