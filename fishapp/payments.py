from django.http import HttpResponse, HttpRequest
from django_daraja.mpesa.core import MpesaClient


def pay_and_push(request: HttpRequest, phone: str, amount: int):
    cl = MpesaClient()
    phone_number = phone
    amount = amount
    account_reference = "reference"
    transaction_desc = "Description"
    # replace with ngrok url; mine, lost access
    callback_url = "https://api.darajambili.com/express-payment"
    response = cl.stk_push(
        phone_number, amount, account_reference, transaction_desc, callback_url
    )
    return HttpResponse(response)
