from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from app.keyboards.user.account import UserPanel, UserPanelAction


class ChargeMethods(str, Enum):
    yookassa = "yookassa"


class ChargePanel(InlineKeyboardBuilder):
    class Callback(CallbackData, prefix="payment"):
        method: ChargeMethods

    def __init__(self, settings: dict[str, bool], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.button(
            text="💳 Банковская карта",
            callback_data=self.Callback(method=ChargeMethods.yookassa),
        )
        self.adjust(1)


class SelectPayAmount(InlineKeyboardBuilder):
    class Callback(CallbackData, prefix="payslctam"):
        amount: int
        free: int = 0
        method: ChargeMethods

    def __init__(self, method: ChargeMethods, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        amount_list = [100, 250, 500, 1000, 2500, 5000]
        for amount in amount_list:
            free = int(
                0
                if (not config.PAYMENTS_DISCOUNT_ON)
                or (amount < config.PAYMENTS_DISCOUNT_ON)
                else amount * (config.PAYMENTS_DISCOUNT_ON_PERCENT / 100)
            )
            self.button(
                text=f"{amount:,} руб."
                if not free
                else f"{amount:,} руб. (+{free:,} bonus)",
                callback_data=self.Callback(amount=amount, free=free, method=method),
            )
        self.button(text="Своя сумма", callback_data=self.Callback(amount=0, method=method))
        self.button(text="Назад", callback_data=UserPanel.Callback(action=UserPanelAction.charge))
        self.adjust(2, 2, 2, 1, 1)


class PayYooUrl(InlineKeyboardBuilder):
    def __init__(self, url: str, inv_id: int = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.button(text="Оплатить", url=url)
        if inv_id:
            self.button(text="Проверить статус / Повторить", callback_data=f"check_yoo_payment:{inv_id}")
        self.button(
            text="К суммам",
            callback_data=SelectPayAmount.Callback(amount=0, method=ChargeMethods.yookassa),
        )
        self.adjust(1, 1)
