import os
import sqlite3
import mysql.connector
from decimal import Decimal
from decouple import config

from db.queries import QueriesSqlite, QueriesMysql
from app.utils import constants as const

SQLITE = 'sqlite'
MYSQL = 'mysql'


def get_sqlite_db_path():
    curr_dir = os.path.dirname(__file__)
    rel_path = os.path.join(curr_dir, '..', 'db', 'shopping_list_db.db')
    return os.path.normpath(rel_path)


class Database:
    def __init__(self, rdbms):
        self.queries = None
        self.rdbms = rdbms

    def set_conn(self):
        match self.rdbms:
            case 'sqlite':
                self.queries = QueriesSqlite(self.rdbms)
                return sqlite3.connect(get_sqlite_db_path())
            case 'mysql':
                self.queries = QueriesMysql(self.rdbms)
                return mysql.connector.connect(
                    host=config('DB_HOST'),
                    user=config('DB_USER'),
                    password=config('DB_PASSWORD'),
                    database='shopping_list_db'
                )

    def get_all_products(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_products())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_product(self, product_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_product_details(), (product_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_all_shop_lists(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_lists())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_shop_lists_for_active_user(self, user_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_lists_for_user(), (user_id,))
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_categories(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_categories())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_units(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_product_units())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def filter_product_names(self, search_param):
        like_query = search_param + '%'
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_product_based_on_name(), (like_query,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def filter_product_names_which_are_not_in_list(self, list_id, search_param):
        like_query = search_param + '%'
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_products_which_are_not_in_list(), (list_id, like_query,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def filter_categories(self, search_param):
        like_query = search_param + '%'
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_category(), (like_query,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def filter_units(self, search_param):
        like_query = search_param + '%'
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_unit(), (like_query,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_active_user(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.check_if_any_user_active())
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_login_user(self, name, password):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            cursor.execute(self.queries.check_if_user_stored(), (name, password))
            entry = cursor.fetchone()

            if entry:
                user_data = {
                    'id': entry[0],
                    'name': entry[1],
                    'email': entry[2]
                }
                try:
                    cursor.execute(self.queries.set_user_online_status(), (user_data['name'],))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return user_data

    def get_shop_list(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list(), (list_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list_checked_unchecked(self, list_id, checked):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list_checked_unchecked(), (list_id, checked))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list_all_count(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list_count(), (list_id,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def get_filtered_list_by_category_count(self, list_id, category_name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_list_by_category_count(), (list_id, category_name))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def get_shop_list_filtered(self, list_id, category_name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_list_by_category(), (list_id, category_name))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list_checked_unchecked_filtered(self, list_id, checked, category_name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_list_checked_unchecked_by_category(), (list_id, checked, category_name))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list_checked_unchecked_count(self, list_id, checked):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list_checked_unchecked_count(), (list_id, checked))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def get_filtered_list_checked_unchecked_by_category_count(self, list_id, checked, category_name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_list_checked_unchecked_by_category_count(), (list_id, checked, category_name))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def toggle_product_bought(self, shop_list_id, product_id, value):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.toggle_bought_status(), (value, shop_list_id, product_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def update_item_quantity(self, value, list_id, product_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.change_item_quantity(), (value, list_id, product_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def remove_product_from_shop_list(self, list_id, product_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.remove_item_from_list(), (list_id, product_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def update_shop_list_name(self, value, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.set_list_name(), (value, list_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def delete_shop_list(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.delete_list(), (list_id,))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def user_logout(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.unset_user_online_status(), (name,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()

    def user_auto_login(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            user = cursor.execute(self.queries.check_if_any_user_active()).fetchone()
            if user:
                user_data = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
        finally:
            cursor.close()
            conn.close()
        return user_data

    def add_user(self, user, email, password):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            check_one = cursor.execute(self.queries.check_if_user_email_exists(), (email,)).fetchone()
            check_two = cursor.execute(self.queries.check_if_user_name_exists(), (user,)).fetchone()
            if check_one or check_two:
                print('Error: User or email already exists')
            else:
                try:
                    cursor.execute(self.queries.create_user(), (user, email, password))
                    conn.commit()
                    user = cursor.execute(self.queries.check_if_user_stored(), (user, password)).fetchone()
                    user_data = {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2]
                    }
                except Exception as e:
                    conn.rollback()
                    print(e)
        finally:
            cursor.close()
            conn.close()
        return user_data

    def add_shopping_list(self, name, user_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res, row_id = False, None
        try:
            cursor.execute(self.queries.insert_into_shopping_list(), (name, user_id))
            conn.commit()
            res = True
            row_id = cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res, row_id, const.LIST_SCR

    def get_product_category_id(self, category_name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_category_id(), (category_name,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def add_product(self, name, price, category, unit, img_path):
        conn = self.set_conn()
        cursor = conn.cursor()
        res, row_id = False, None
        try:
            cursor.execute(self.queries.get_category_id(), (category,))
            category_id = cursor.fetchone()[0]

            cursor.execute(self.queries.get_unit_id(), (unit,))
            unit_id = cursor.fetchone()[0]

            if self.rdbms == MYSQL:
                price = Decimal(price)

            cursor.execute(self.queries.insert_into_product(), (name, price, unit_id, category_id, img_path))
            conn.commit()
            res = True
            row_id = cursor.lastrowid
        except Exception as e:
            conn.rollback()
            print(f'Exception when adding product: {e}')
        finally:
            cursor.close()
            conn.close()
        return res, row_id, const.PROD_SCR

    def add_product_in_list(self, list_id, product_id, unit_id, category_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.insert_into_shop_list_product(), (list_id, product_id, unit_id, category_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def add_category(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        res, row_id = False, None
        try:
            cursor.execute(self.queries.insert_into_category(), (name,))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def get_category_products(self, category_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_products_of_category_type(), (category_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_category_name(self, value, category_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.set_category_name(), (value, category_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def delete_category(self, category_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.delete_category(), (category_id,))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def add_unit(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        res, row_id = False, None
        try:
            cursor.execute(self.queries.insert_into_unit(), (name,))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def get_unit_products(self, unit_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_products_of_unit_type(), (unit_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def update_unit_name(self, value, unit_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.set_unit_name(), (value, unit_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def delete_unit(self, unit_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.delete_unit(), (unit_id,))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res
