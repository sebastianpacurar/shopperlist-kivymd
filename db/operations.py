from app.components.components import MySnackbar, db


def perform_list_add(*args):
    dialog = args[0]
    shop_list_name = args[1].text
    db_result, msg = 0, "List can't be empty!"
    if len(shop_list_name) > 0:
        db_result = db.add_shopping_list(shop_list_name, args[2])
        dialog.should_refresh = db_result
        msg = f'{shop_list_name} created'
        dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_update_list_name(*args):
    dialog, field, list_id = args
    name = field.text
    db_result = db.update_shop_list_name(name, list_id)
    msg = 'List name cannot be empty'
    if len(name) > 0:
        if db_result:
            dialog.should_refresh = db_result
            msg = f'{name} updated!'
            dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_delete_list(*args):
    dialog, name, list_id = args
    db_result = db.delete_shop_list(list_id)
    msg = f'Failed to remove {name}'
    dialog.should_refresh = db_result
    if db_result:
        dialog.should_refresh = db_result
        msg = f'{name} deleted successfully'
        dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_update_category_name(*args):
    dialog, field, category_id = args
    name = field.text
    db_result = db.update_category_name(name, category_id)
    msg = 'Category name cannot be empty'
    if len(name) > 0:
        if db_result:
            dialog.should_refresh = db_result
            msg = f'{name} updated!'
            dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_list_item_toggle(*args):
    list_id, product_id, val = args
    db_result = db.toggle_product_bought(list_id, product_id, val)
    if not db_result:
        print('error toggling product item')


def perform_quantity_update(*args):
    value, list_id, product_id, = args
    db_result = db.update_item_quantity(value, list_id, product_id)
    msg = 'Quantity updated'
    if not db_result:
        msg = 'error updating product'
    MySnackbar(msg, db_result)


def perform_list_item_remove(*args):
    dialog, list_id, product_id = args
    db_result = db.remove_product_from_shop_list(list_id, product_id)
    msg = f'Failed to remove item'
    dialog.should_refresh = db_result
    if db_result:
        dialog.should_refresh = db_result
        msg = f'Item removed successfully'
        dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_update_unit_name(*args):
    dialog, field, unit_id = args
    name = field.text
    db_result = db.update_unit_name(name, unit_id)
    msg = 'Category name cannot be empty'
    if len(name) > 0:
        if db_result:
            dialog.should_refresh = db_result
            msg = f'{name} updated!'
            dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_delete_category(*args):
    dialog, name, category_id = args
    db_result = db.delete_category(category_id)
    msg = f'Failed to {name}'
    dialog.should_refresh = db_result
    if db_result:
        dialog.should_refresh = db_result
        msg = f'{name} deleted successfully'
        dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_delete_unit(*args):
    dialog, name, unit_id = args
    db_result = db.delete_unit(unit_id)
    msg = f'Failed to delete {name}'
    dialog.should_refresh = db_result
    if db_result:
        dialog.should_refresh = db_result
        msg = f'{name} deleted successfully'
        dialog.dismiss()
    MySnackbar(msg, db_result)


def perform_add_prod_to_list(*args):
    list_id, product_id, unit_id, category_id = args
    db_result = db.add_product_in_list(list_id, product_id, unit_id, category_id)
    msg = 'Failed to add product to list'
    if db_result:
        msg = 'Product added to list'
    MySnackbar(msg, db_result)
