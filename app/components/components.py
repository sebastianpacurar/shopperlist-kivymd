from kivymd.uix.appbar import MDActionTopAppBarButton
from kivymd.uix.bottomsheet import MDBottomSheetDragHandle
from kivymd.uix.dialog import MDDialog, MDDialogContentContainer
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.snackbar import MDSnackbarButtonContainer, MDSnackbarActionButtonText, MDSnackbarSupportingText, \
    MDSnackbarCloseButton
from kivy.metrics import sp, dp
from kivy.properties import StringProperty, ColorProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton
from kivymd.uix.list import MDListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from db.database import Database, SQLITE, MYSQL
from app.utils import constants as const

# This is where the DB gets instantiated
db = Database(SQLITE)


class RV(MDRecycleView):
    pass


class SimpleTextField(MDTextField):
    hint_txt = StringProperty()
    helper_txt = StringProperty()


class PasswordField(MDRelativeLayout):
    field_mode = StringProperty('outlined')
    hint_txt = StringProperty()
    is_hidden = BooleanProperty(False)  # used in toggle_visibility when clicking eye icon
    skip = BooleanProperty(False)  # used to cancel save_text_value during on_text after setting/unsetting text to symbols
    text_value = StringProperty()  # the actual literal value
    masked_text = StringProperty()  # the literal value masked

    # set text_value and masked_text vars. triggered on set_text
    def save_text_value(self, *args):
        args[0].text = args[0].text.replace(' ', '')  # prevent whitespaces
        if len(args[0].text) > 0:
            if not self.skip or (len(args[0].text) == 1 and self.is_hidden):  # update vars only if not marked as skip and if is first element while is_hidden is True
                if len(args[0].text) < len(self.text_value):  # trigger if erase/delete event occurs
                    diff = len(self.text_value) - len(args[0].text)  # TODO: handle multi-select delete
                    self.text_value = self.text_value[:-diff]
                elif args[0].text[-1] != '*':  # if last typed element is not a star, add it to text_value var
                    self.text_value += args[0].text[-1]
                self.masked_text = '*' * len(self.text_value)

            if self.is_hidden:  # if is_hidden is on, change the text, and mark as Skipped, to prevent re-trigger of save_text_value func
                args[0].text = self.masked_text
                self.skip = True
            if self.skip:  # skip happens only once, after eye icon is toggled
                self.skip = False
        else:  # if field is empty, then reset vars
            self.masked_text = ''
            self.text_value = ''

    # enable/disable masked pass. set skip to prevent re-trigger of save_text_value, when resetting text_field text value
    def toggle_visibility(self, *args):
        icon_btn = args[0]
        self.is_hidden = not self.is_hidden
        self.skip = not self.skip
        if self.is_hidden:
            icon_btn.icon = 'eye-off'
            args[1].text = self.masked_text
        else:
            icon_btn.icon = 'eye'
            args[1].text = self.text_value


# TODO: update names for Editable list items below
class EditableOneLineItemList(MDListItem):
    itm_id = StringProperty()
    text = StringProperty()
    itm_icon = StringProperty()


class EditableTwoLineItemList(MDListItem):
    itm_id = StringProperty()
    headline = StringProperty()
    supporting = StringProperty()
    itm_icon = StringProperty()
    sheet_func = ObjectProperty()


class EditableThreeLineItemList(MDListItem):
    itm_icon = StringProperty()
    headline = StringProperty()
    supporting = StringProperty()
    tertiary = StringProperty()


class ProdItemWithImg(MDListItem):
    img_path = StringProperty()
    headline = StringProperty()


class TwoLineProdImgListItem(MDListItem):
    headline = StringProperty()
    supporting = StringProperty()
    prod_id = NumericProperty()
    img_path = StringProperty()
    itm_icon = StringProperty()
    image_func = ObjectProperty()
    icon_func = ObjectProperty()


class SelectSignInSignUpButton(MDButton):
    text = StringProperty()


class BottomSheetSelectionLineItem(MDListItem):
    text = StringProperty()


class BottomSheetHandleContainer(MDBottomSheetDragHandle):
    title = StringProperty()


class DynamicDialog(MDDialog):
    confirm = ObjectProperty()
    headline = StringProperty()
    supporting = StringProperty()
    accept_txt = StringProperty()
    cancel_txt = StringProperty()
    should_refresh = BooleanProperty(False)

    def on_dismiss(self):
        super().on_dismiss()
        if self.should_refresh:
            main_sm = MDApp.get_running_app().sm
            if main_sm.current == const.COLLECTION_SCR:
                main_sm.get_screen(const.COLLECTION_SCR).refresh_data()


class AddShoppingListContent(MDDialogContentContainer):
    pass


class RenameShoppingListContent(MDDialogContentContainer):
    list_id = StringProperty()


class DeleteShoppingListContent(MDDialogContentContainer):
    list_name = StringProperty()
    list_id = StringProperty()


class Spacer(MDBoxLayout):
    value = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.init_spacer)

    def init_spacer(self, *args):
        if self.orientation == 'vertical':
            self.size_hint_y = None
            self.height = self.value
        else:
            self.size_hint_x: None
            self.width = self.value


class SimpleSnackbar(MDSnackbar):
    text = StringProperty()
    color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDSnackbarSupportingText(text=self.text))
        self.y = dp(24)
        self.orientation = 'horizontal'
        self.pos_hint = {'center_x': 0.5, 'y': 0}
        self.background_color = self.color
        self.open()


class MySnackbar(MDSnackbar):
    text = StringProperty()

    def __init__(self, message, db_res, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.text = message
        self.background_color = const.RGB_SUCCESS if db_res else const.RGB_ERROR

        self.y = dp(24)
        self.orientation = 'horizontal'
        self.pos_hint = {'center_x': 0.5, 'y': 0}

        self.add_widget(MDSnackbarSupportingText(
            text=self.text,
            theme_text_color='Custom',
            theme_font_size='Custom',
            text_color='white',
            font_size=sp(15.5),
            bold=True
        ))

        bar_buttons = MDSnackbarButtonContainer(pos_hint={'center_y': .5})

        if isinstance(db_res, tuple):
            response, val_id, screen_name = db_res
            if response and screen_name:
                func = None
                match screen_name:
                    case const.LIST_SCR:
                        func = lambda _: (self.main_app.change_screen_to_list_scr(val_id), self.dismiss())
                    case const.PROD_SCR:
                        func = lambda _: (self.main_app.change_screen_to_prod_scr(val_id), self.dismiss())

                bar_buttons.add_widget(
                    MDSnackbarActionButton(
                        MDSnackbarActionButtonText(
                            text='View',
                            theme_text_color='Custom',
                            theme_font_size='Custom',
                            text_color='white',
                            font_size=sp(15.5),
                            bold=True,
                        ),
                        style='outlined',
                        theme_line_color='Custom',
                        line_color='white',
                        radius=(dp(5), dp(5), dp(5), dp(5)),
                        on_release=func
                    )
                )

        bar_buttons.add_widget(
            MDSnackbarCloseButton(
                icon='close',
                on_release=self.dismiss
            )
        )

        self.add_widget(bar_buttons)
        self.open()


class DropdownMenu(MDDropdownMenu):
    change_screen_func = ObjectProperty

    def __init__(self):
        super().__init__(
            width_mult=4,
            radius=[12, 12, 12, 12],
            elevation=4,
        )
        self.parent_caller = None
        self.main_app = MDApp.get_running_app()

    def drop(self, widget):
        data = None
        menu_items = []
        self.caller = widget

        # trigger items belonging to a specific table column
        if isinstance(widget, MDTextField):
            self.hor_growth = 'left'
            self.ver_growth = 'down'
            self.position = 'center'

            if widget.hint_txt == 'Category':
                data = db.get_product_categories()
            elif widget.hint_txt == 'Unit':
                data = db.get_product_units()

            for entry in data:
                menu_items.append(
                    {
                        'text': entry[1],
                        'on_release': lambda item=entry: self.on_dropdown_item_select(widget, item)
                    }
                )
        # trigger items which trigger options from the ActionTopAppBarButton
        elif isinstance(widget, MDActionTopAppBarButton):
            menu_items = [
                {
                    'text': 'Add product',
                    'on_release': lambda screen=const.ADD_PROD_SCR: (
                        self.main_app.change_screen_and_update_bar(screen),
                        self.dismiss()
                    )
                },
                {
                    'text': 'Add Data',
                    'on_release': lambda screen=const.ADD_DATA_SCR: (
                        self.main_app.change_screen_and_update_bar(screen),
                        self.dismiss()
                    )
                },
            ]

        elif isinstance(widget, TwoLineProdImgListItem):
            # TODO
            # widget.bg_color = self.theme_cls.primary_light
            self.parent_caller = widget
            self.caller = widget.children[0]
            prod_id = self.parent_caller.prod_id

            menu_items = [
                {
                    'text': 'View',
                    'on_release': lambda target=prod_id: (
                        self.main_app.change_screen_to_prod_scr(target),
                        self.dismiss()
                    )

                },
                {
                    'text': 'Delete',
                    'on_release': lambda target=prod_id: (
                        print('delete me?'),
                        self.dismiss()
                    )
                }
            ]

        self.items = menu_items
        self.open()

    def on_dropdown_item_select(self, text_input, content):
        ''' perform menu_item selection and update the caller text value '''
        text_input.text = str(content[1])
        self.dismiss()
