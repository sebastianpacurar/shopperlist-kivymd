from kivymd.uix.snackbar import MDSnackbarButtonContainer, MDSnackbarActionButtonText, MDSnackbarSupportingText
from kivy.metrics import sp, dp
from kivy.properties import StringProperty, ColorProperty, NumericProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton
from kivymd.uix.list import MDListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.navigationbar import MDNavigationItemIcon

from db.database import Database, SQLITE
from app.utils import constants as const

# This is where the DB gets instantiated
db = Database(SQLITE)


class RV(MDRecycleView):
    pass


class EditableTwoLineItemList(MDListItem):
    itm_icon = StringProperty()
    headline = StringProperty()
    supporting = StringProperty()


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


class PasswordField(MDTextField):
    hint_txt = StringProperty()


class AddShoppingListContent(MDBoxLayout):
    pass


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
        MDSnackbar(
            MDSnackbarSupportingText(text=self.text),
            y=dp(24),
            orientation='horizontal',
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.color,
        ).open()


class MySnackbar(MDSnackbar):
    text = StringProperty('')

    # def show(self):
    #     MDSnackbar(
    #         MDSnackbarSupportingText(text=self.text),
    #         MDSnackbarButtonContainer(
    #             MDSnackbarActionButton(
    #                 MDSnackbarActionButtonText(
    #                     text='Action button'
    #                 ),
    #             ),
    #             pos_hint={'center_y': 0.5}
    #         ),
    #         y=dp(24),
    #         orientation='horizontal',
    #         pos_hint={'center_x': .5, 'y':0},
    #         background_color=self.color,
    #     ).open()

    def __init__(self, message, db_res, **kwargs):
        super().__init__(**kwargs)
        self.main_app = MDApp.get_running_app()
        self.text = message
        self.md_bg_color = const.RGB_SUCCESS if db_res else const.RGB_ERROR
        self.show()

        if db_res:
            response, val_id, screen_name = db_res
            if response and screen_name:
                func = None
                match screen_name:
                    case const.LIST_SCR:
                        func = lambda _: (self.main_app.change_screen_to_list_scr(val_id), self.dismiss_sb())
                    case const.PROD_SCR:
                        func = lambda _: (self.main_app.change_screen_to_prod_scr(val_id), self.dismiss_sb())

                item = MDSnackbarActionButton(
                    text='View',
                    theme_text_color='Custom',
                    text_color='white',
                    font_size=sp(17.5),
                    on_release=func
                )

            self.add_widget(item)

    def show(self):
        MDSnackbar(
            MDSnackbarSupportingText(
                text='Single-line snackbar with action',
            ),
            MDSnackbarButtonContainer(
                MDSnackbarActionButton(
                    MDSnackbarActionButtonText(
                        text='Action button'
                    ),
                ),
                pos_hint={'center_y': 0.5}
            ),
            y=dp(24),
            orientation='horizontal',
            pos_hint={'center_x': .5},
            background_color=self.color,
        ).open()

    def dismiss_sb(self):
        self.dismiss()


class DropdownHandler(MDDropdownMenu):
    change_screen_func = ObjectProperty

    def __init__(self):
        super().__init__(
            width_mult=4,
            radius=[12, 12, 12, 12],
            elevation=4,
        )
        self.parent_caller = None
        self.main_app = MDApp.get_running_app()

    def on_dismiss(self):
        super().on_dismiss()
        # TODO
        # if isinstance(self.caller, MDListItemTrailingIcon):
        #     self.parent_caller.bg_color = self.theme_cls.bg_darkest

    def toggle(self, widget):
        data = None
        menu_items = []
        self.caller = widget

        # trigger items belonging to a specific table column
        if isinstance(widget, MDTextField):
            self.hor_growth = 'left'
            self.ver_growth = 'down'
            self.position = 'center'

            if widget.hint_text == 'Category':
                data = db.get_product_categories()
            elif widget.hint_text == 'Unit':
                data = db.get_product_units()

            for entry in data:
                menu_items.append(
                    {
                        'viewclass': 'OneLineListItem',
                        'text': entry[1],
                        'on_release': lambda item=entry: self.on_dropdown_item_select(widget, item)
                    }
                )
        # trigger items which trigger options from the ActionTopAppBarButton
        elif isinstance(widget, MDNavigationItemIcon):

            menu_items = [
                {
                    'viewclass': 'OneLineListItem',
                    'text': 'Add product',
                    'on_release': lambda screen=const.ADD_PROD_SCR: (
                        self.main_app.change_screen_and_update_bar(screen),
                        self.dismiss()
                    )
                },
                {
                    'viewclass': 'OneLineListItem',
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
            self.caller = widget.children[0].children[0]
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
