# discord-py-paginator
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
- Discord direct message to `Philskillz_#0266`

thanks in advance.

# Install
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
*Example in readme removed because it was too complex.<br> Contact me for help or look in the examples*

<br>

To send you paginator do the following:
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
<br>

additionally you implement these methods
- ``Paginator.on_setup`` (invoked when the paginator instance is created)
- ``Paginator.on_start`` (invoked when a user clicked the start button)
- ``Paginator.on_stop`` (invoked when a user clicked the stop button)

<br>

More examples can be found [here](https://github.com/philskillz-coder/discord-py-paginator/tree/main/examples) (currently no examples, i will add some)

## Config
You can configure your paginator subclass and instance via a config dict.
An example with config can be found in the examples folder

### All config options

| **CONFIG NAME**                      | **TYPE**        | **VALUES**          | **EXPLANATION**                                                            | **INFO**                                             
|--------------------------------------|-----------------|---------------------|----------------------------------------------------------------------------|------------------------------------------------------|
| ``paginator_delete_when_finished``   | ``bool``        | ``True``, ``False`` | _Delete the pagination message when stopped_                               | Only works if the paginator message is not ephemeral |
| ``paginator_delete_delay``           | ``int``         | Any                 | _How long to wait after paginator stop to delete the message_              |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``start_button_enabled``             |                 |                     |                                                                            | **Option not changable**                             |
| ``start_button_style``               | ``ButtonStyle`` | Any                 | _The style of the start button_                                            |                                                      |
| ``start_button_label``               | ``str``         | Any                 | _The label of the start button_                                            |                                                      |
| ``start_button_emoji``               | ``str``         | Any                 | _The emoji of the start button_                                            |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``stop_button_enabled``              |                 |                     |                                                                            | **Option not changable**                             |
| ``stop_button_style``                | ``ButtonStyle`` | Any                 | _The style of the stop button_                                             |                                                      |
| ``stop_button_label``                | ``str``         | Any                 | _The label of the stop button_                                             |                                                      |
| ``stop_button_emoji``                | ``str``         | Any                 | _The emoji of the stop button_                                             |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``quick_navigation_button_enabled``  | ``bool``        | ``True``, ``False`` | _Is the quick navigation button enabled_                                   |                                                      |
| ``quick_navigation_button_style``    | ``ButtonStyle`` | Any                 | _The style of the  quick navigation button_                                |                                                      |
| ``quick_navigation_button_label``    | ``str``         | Any                 | _The label of the quick navigation button_                                 |                                                      |
| ``quick_navigation_button_emoji``    | ``str``         | Any                 | _The emoji of the quick navigation button_                                 |                                                      |
| ``quick_navigation_error_message``   | ``str``         | Any                 | _The message when quick navigation input is not a number_                  |                                                      |
| ``quick_navigation_error_ephemeral`` | ``bool``        | ``True``, ``False`` | _Whether the error message should be ephemeral or not_                     |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``first_element_button_enabled``     | ``bool``        | ``True``, ``False`` | _Whether the button to go to the first element should be enabled or not    |                                                      |
| ``first_element_button_style``       | ``ButtonStyle`` | Any                 | _The style of the first element button_                                    |                                                      |
| ``first_element_button_label``       | ``str``         | Any                 | _The label of the first element button_                                    |                                                      |
| ``first_element_button_emoji``       | ``str``         | Any                 | _The emoji of the first element button_                                    |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``prev_element_button_enabled``      | ``bool``        | ``True``, ``False`` | _Whether the button to go to the previous element should be enabled or not |                                                      |
| ``prev_element_button_style``        | ``ButtonStyle`` | Any                 | _The style of the previous element button_                                 |                                                      |
| ``prev_element_button_label``        | ``str``         | Any                 | _The label of the previous element button_                                 |                                                      |
| ``prev_element_button_emoji``        | ``str``         | Any                 | _The emoji of the previous element button_                                 |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``next_element_button_enabled``      | ``bool``        | ``True``, ``False`` | _Whether the button to go to the next element should be enabled or not     |                                                      |
| ``next_element_button_style``        | ``ButtonStyle`` | Any                 | _The style of the next element button_                                     |                                                      |
| ``next_element_button_label``        | ``str``         | Any                 | _The label of the next element button_                                     |                                                      |
| ``next_element_button_emoji``        | ``str``         | Any                 | _The emoji of the next element button_                                     |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``last_element_button_enabled``      | ``bool``        | ``True``, ``False`` | _Whether the button to go to the last element should be enabled or not     |                                                      |
| ``last_element_button_style``        | ``ButtonStyle`` | Any                 | _The style of the last element button_                                     |                                                      |
| ``last_element_button_label``        | ``str``         | Any                 | _The label of the last element button_                                     |                                                      |
| ``last_element_button_emoji``        | ``str``         | Any                 | _The emoji of the last element button_                                     |                                                      |
|                                      |                 |                     |                                                                            |                                                      |
| ``placeholder_button_enabled``       | ``bool``        | ``True``, ``False`` | _Whether placeholder buttons are used or not_                              |                                                      |
| ``placeholder_button_style``         | ``ButtonStyle`` | Any                 | _The style of the last element button_                                     |                                                      |
| ``placeholder_button_label``         | ``str``         | Any                 | _The label of the last element button_                                     |                                                      |
| ``placeholder_button_emoji``         | ``str``         | Any                 | _The emoji of the last element button_                                     |                                                      |
