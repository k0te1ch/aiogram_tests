"""Invoices, payments and shipping"""

from aiogram import types

from .base import DatasetItem
from .chats import USER

INVOICE = DatasetItem(
    {
        "title": "Working Time Machine",
        "description": "Want to visit your great-great-great-grandparents? "
        "Make a fortune at the races? "
        "Shake hands with Hammurabi and take a stroll in the Hanging Gardens? "
        "Order our Working Time Machine today!",
        "start_parameter": "time-machine-example",
        "currency": "USD",
        "total_amount": 6250,
    },
    model=types.Invoice,
)

SHIPPING_ADDRESS = DatasetItem(
    {
        "country_code": "US",
        "state": "State",
        "city": "DefaultCity",
        "street_line1": "Central",
        "street_line2": "Middle",
        "post_code": "424242",
    },
    model=types.ShippingAddress,
)

SUCCESSFUL_PAYMENT = DatasetItem(
    {
        "currency": "USD",
        "total_amount": 6250,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
        "telegram_payment_charge_id": "_",
        "provider_payment_charge_id": "12345678901234_test",
    },
    model=types.SuccessfulPayment,
)

PRE_CHECKOUT_QUERY = DatasetItem(
    {
        "id": "262181558630368727",
        "from": USER,
        "currency": "USD",
        "total_amount": 6250,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
    },
    model=types.PreCheckoutQuery,
)

SHIPPING_QUERY = DatasetItem(
    {
        "id": "262181558684397422",
        "from": USER,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
        "shipping_address": SHIPPING_ADDRESS,
    },
    model=types.ShippingQuery,
)
