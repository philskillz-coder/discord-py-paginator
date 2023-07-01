from discord.ext.paginator import Paginator


class MemberPaginator(Paginator):
    # have a look at the readme for all the available options
    paginator_delete_when_finished = True
    paginator_delete_delay = 10  # 10 seconds
    paginator_not_allowed_message = "Sorry, its not for you!"

    page_number_button_label = "Page %s/%s"

    placeholder_button_enabled = False
