# Config
Many examples can be found in the [Example folder](examples)

## Basic config usage
You can configure your paginator subclass by setting config attributes like this
```python
class ThePaginator(Paginator):
    # ATTRIBUTE_NAME = VALUE
    paginator_delete_when_finished = True
    stop_button_emoji = "\U0001f6d1"  # 🛑
    quick_navigation_button_enabled = False
```

## All config options
| **ATTRIBUTE NAME**                  | **TYPE**        | **VALUES**          | **EXPLANATION**                                                             | **INFO**                                             |
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
| ``search_button_button_enabled``    | ``bool``        | ``True``, ``False`` | _Is the search button enabled_                                              | Default: ``True``                                    |
| ``search_button_button_style``      | ``ButtonStyle`` | Any                 | _The style of the  search button_                                           |                                                      |
| ``search_button_button_label``      | ``str``         | Any                 | _The label of the search button_                                            |                                                      |
| ``search_button_button_emoji``      | ``str``         | Any                 | _The emoji of the search button_                                            |                                                      |
| ``search_button_error_message``     | ``str``         | Any                 | _The message when search input is not found_                                |                                                      |
|                                     |                 |                     |                                                                             |                                                      |
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