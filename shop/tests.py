# from django.test import TestCase

import var_dump as var_dump
from yookassa import Payment, Configuration
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt
from yookassa.domain.models.receipt_item import ReceiptItem
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

Configuration.account_id = 234633
Configuration.secret_key = 'test_CPQkt10rG9ghCn3WmNJh8QGISj7C5XNwj8LW_aP5WwU'

receipt = Receipt()
receipt.customer = {"phone": "79990000000", "email": "test@email.com"}
receipt.tax_system_code = 1
receipt.items = [
    ReceiptItem({
        "description": "Product 1",
        "quantity": 2.0,
        "amount": {
            "value": 250.0,
            "currency": Currency.RUB
        },
        "vat_code": 2
    }),
    {
        "description": "Product 2",
        "quantity": 1.0,
        "amount": {
            "value": 100.0,
            "currency": Currency.RUB
        },
        "vat_code": 2
    }
]

builder = PaymentRequestBuilder()
builder.set_amount({"value": 1200, "currency": Currency.RUB}) \
    .set_confirmation({"type": ConfirmationType.REDIRECT, "return_url": "https://merchant-site.ru/return_url"}) \
    .set_capture(False) \
    .set_description("Заказ №72") \
    .set_metadata({"orderNumber": "ololo"}) \
    .set_receipt(receipt)

request = builder.build()
# Можно что-то поменять, если нужно
request.client_ip = '1.2.3.4'
res = Payment.create(request)

# var_dump.var_dump(res)
print(res.json())
