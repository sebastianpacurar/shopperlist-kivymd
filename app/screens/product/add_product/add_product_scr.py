import os

from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.components.components import MySnackbar, db
from app.utils import constants as const

placeholder_img = os.path.join(os.getcwd(), '..', 'images', 'placeholder_image.png')


class AddProdScreen(MDScreen):
    top_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prod_name = None
        self.prod_price = None
        self.prod_category = None
        self.prod_unit = None
        self.bind(on_kv_post=self.set_definitions)
        self.bind(on_pre_enter=self.init_data)
        self.bind(on_pre_leave=self.clean_up)

    def set_definitions(self, *args):
        self.prod_name = self.ids.product_name_text
        self.prod_price = self.ids.product_price_text
        self.prod_category = self.ids.product_category_text
        self.prod_unit = self.ids.product_unit_text

    def perform_product_add(self):
        main_app = MDApp.get_running_app()
        msg, db_result = 'Errors in fields', 0
        if not any([len(t) == 0 for t in
                    [self.prod_name.text, self.prod_price.text, self.prod_category.text, self.prod_unit.text]]):
            db_result = db.add_product(self.prod_name.text, self.prod_price.text, self.prod_category.text,
                                       self.prod_unit.text,
                                       placeholder_img)
            msg = f'{self.prod_name.text} added to {self.prod_category.text}'
            main_app.sm.get_screen(const.MANAGE_DATA_SCR).refresh_data()
        MySnackbar(msg, db_result)

    def init_data(self, *args):
        self.prod_name.error = False
        self.prod_price.error = False
        self.prod_category.error = False
        self.prod_unit.error = False

    def clean_up(self, *args):
        self.prod_name.text = ''
        self.prod_price.text = ''
        self.prod_category.text = ''
        self.prod_unit.text = ''
