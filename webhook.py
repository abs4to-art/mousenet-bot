import logging

from aiohttp import web

from database import get_order_by_label, confirm_order

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.post("/callback")
async def yoomoney_callback(request: web.Request) -> web.Response:
    yoomoney = request.app["yoomoney"]
    bot = request.app["bot"]

    body = await request.text()
    sig = request.headers.get("Content-SHA1", "")

    if not yoomoney.verify_notification(body, sig):
        return web.Response(status=403, text="Invalid signature")

    data = yoomoney.parse_notification(body)

    notification_type = data.get("notification_type", "")
    if notification_type != "payment_notification":
        return web.Response(status=200, text="OK")

    label = data.get("label", "")
    if not label:
        return web.Response(status=200, text="OK")

    order = get_order_by_label(label)
    if order and order["status"] == "pending":
        confirm_order(order["id"])

        try:
            await bot.send_message(
                order["user_id"],
                f"✅ <b>Оплата получена!</b>\n\n"
                f"Заказ #{order['id']} на тариф «{order['tariff']}» подтверждён.\n"
                "Администратор скоро свяжется с вами для настройки.",
            )
        except Exception as e:
            logger.warning("Failed to notify user %d: %s", order["user_id"], e)

    return web.Response(status=200, text="OK")


@routes.get("/health")
async def health_check(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})
