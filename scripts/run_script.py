from modules.ui.page_objects.actions.all_actions_page import ATBAllActionsPage


def run():

    atb_page = ATBAllActionsPage()

    atb_page.open(ATBAllActionsPage.URL)

    atb_page.get_current_address_shop('Броди')