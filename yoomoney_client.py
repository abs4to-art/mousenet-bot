import hashlib
import hmac
from urllib.parse import parse_qs

from yoomoney import Quickpay

from config import YOOMONEY_RECEIVER, YOOMONEY_REDIRECT_URI, YOOMONEY_NOTIFICATION_SECRET


class YooMoneyClient:
    def __init__(self) -> None:
        self.receiver = YOOMONEY_RECEIVER
        self.redirect_uri = YOOMONEY_REDIRECT_URI

    def create_payment_link(
        self, amount: float, label: str, description: str = ""
    ) -> str:
        quickpay = Quickpay(
            receiver=self.receiver,
            quickpay_form="shop",
            targets=description or "Оплата заказа",
            paymentType="SB",
            sum=amount,
            label=label,
            redirect_uri=self.redirect_uri,
        )
        return quickpay.base_url

    def verify_notification(self, body: str, sig_header: str) -> bool:
        secret = YOOMONEY_NOTIFICATION_SECRET
        if not secret:
            return True
        expected = hmac.new(
            secret.encode(), body.encode(), hashlib.sha1
        ).hexdigest()
        return hmac.compare_digest(expected, sig_header)

    def parse_notification(self, body: str) -> dict:
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()}
