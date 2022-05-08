# discord-py-paginator
A view paginator for [discord.py](https://github.com/Rapptz/discord.py)

## Installing
This libary requires [discord.py](https://github.com/Rapptz/discord.py) v2.0:

```sh
pip install git+https://github.com/philskillz-coder/discord-py-paginator
```

## Usage
To make your own paginator simply subclass [paginator.Paginator](https://github.com/philskillz-coder/discord-py-paginator/blob/main/discord/ext/paginator/paginator.py?#L12) and overwrite the methods: <br/>
 - [get_page_count](https://github.com/philskillz-coder/discord-py-paginator/blob/main/discord/ext/paginator/paginator.py?#L270) ~ you can also pass ``static_page_count`` variable to the instructor of ``paginator.Paginator``
 - [get_page_content](https://github.com/philskillz-coder/discord-py-paginator/blob/main/discord/ext/paginator/paginator.py?#L300)

#### IMPORTANT: <br/>
Do not confuse ``get_page_count`` with ``acquire_page_count``! Only overwrite ``get_page_count`` <br/>
The same goes for ``get_page_content`` and ``acquire_page_content``

```python
from discord import Interaction, Embed
from discord.ext.paginator import paginator

class MyPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)
    
    async def get_page_content(self, interaction: Interaction, page: int):
        guild = self.client.guilds[page]
        return {
            "embed": Embed(
                title=guild.name,
                description=f"This guild has {guild.member_count} members."
            ),
            "ephemeral": True
        }

my_paginator = MyPaginator(client, user)
# or
my_paginator = MyPaginator(client, user, static_page_count=len(client.guilds))
```

or use the [from_list](https://github.com/philskillz-coder/discord-py-paginator/blob/main/discord/ext/paginator/paginator.py?#L162) method to create a paginator from a list of data.

````python
import discord
from discord.ext.paginator import paginator

my_paginator = paginator.Paginator.from_list(
    client,
    user,
    data=[
        {
            "embed": discord.Embed(title=guild.name, description=f"This guild has {guild.member_count} members"),
            "ephemeral": True,
        } for guild in client.guilds
])
````

to send you paginator do the following:
`````python
await interaction.response.send_message(
    content="A paginator",
    view=await my_paginator.run()
)
`````

More examples can be found [here](https://github.com/philskillz-coder/discord-py-paginator/tree/main/examples)

## Config
You can configurate your paginator subclass and instance via a config dict.
All config options can be found [here](https://github.com/philskillz-coder/discord-py-paginator/blob/main/discord/ext/paginator/paginator.py#L13).

### An example with config
By default this paginator will have ephemeral disabled, the instance though has ephemeral enabled.
````python
from discord import Interaction, Embed
from discord.ext.paginator import paginator

class MyPaginator(paginator.Paginator):
    CONFIG = {
        "paginator_ephemeral": False
    }
    
    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)
    
    async def get_page_content(self, interaction: Interaction, page: int):
        guild = self.client.guilds[page]
        return {
            "embed": Embed(
                title=guild.name,
                description=f"This guild has {guild.member_count} members."
            ),
            "ephemeral": True
        }


my_paginator = MyPaginator(
    client,
    user,
    config={
        "paginator_ephemeral": True
    }
    static_page_count=len(client.guilds),
)
````

### An example with config (based on static paginator)

This paginator will have the default config options overwritten with the specified config options
````python
import discord
from discord.ext.paginator import paginator

my_paginator = paginator.Paginator.from_list(
    client,
    user,
    static_data=[
        {
            "embed": discord.Embed(title=guild.name, description=f"This guild has {guild.member_count} members"),
        } for guild in client.guilds
    ],
    config={
        "paginator_ephemeral": True,
        "quick_navigation_button_enabled": False
    }
)
````

### All config options

| **CONFIG NAME**                      | **TYPE**        | **VALUES**                    | **EXPLANATION**                                                            | **INFO**                                                                                                                    
|--------------------------------------|-----------------|-------------------------------|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| ``paginator_ephemeral``              | ``bool``        | ``True``, ``False``, ``None`` | _Paginator response ephemeral_                                             | This config option overwrites the ``ephemeral`` option returned from ``get_page_content``. If ``None``, the not overwritten |
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
