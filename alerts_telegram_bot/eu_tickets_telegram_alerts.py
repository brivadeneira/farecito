"""
Telegram ticket alerts
"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_alert_to_telegram_channel(
    from_city_name: str,
    departure_city_uuid: str,
    to_city_name: str,
    arrival_city_uuid: str,
    price: float,
    departure_date: str,
    seats_available: int,
):
    ticket_url = f"https://shop.flixbus.com/search?departureCity={departure_city_uuid}"
    ticket_url += f"&{arrival_city_uuid}&rideDate={departure_date}"

    msg = f"""
    🎟 A cheap ticket for you!
    🚌 from {from_city_name} to {to_city_name}
    🪙 FOR JUST {price} EUROS!
    📆 Schedule your next trip on {departure_date}
    🏃 Hurry up! just {seats_available} remaining seats
    {ticket_url}
    """

    bot_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    send_msg_url = f"sendMessage?chat_id=@farecito_eu&text={msg}"
    _ = requests.post(f"{bot_url}/{send_msg_url}")
