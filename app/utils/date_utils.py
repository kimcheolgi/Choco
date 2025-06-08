from datetime import datetime, date, timedelta, timezone
from pytz import timezone


class D:
    def __init__(self, *args):
        self.utc_now = datetime.utcnow()
        self.datetime_kst = datetime.now(timezone('Asia/Seoul'))
        self.timedelta = 0

    @classmethod
    def datetime(cls, diff: int=9) -> datetime:
        return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

    @classmethod
    def date(cls, diff: int=9) -> date:
        return cls.datetime(diff=diff).date()

    @classmethod
    def date_num(cls, diff: int=9) -> int:
        return int(cls.date(diff=diff).strftime('%Y%m%d'))

    @classmethod
    def datetime_str(cls, diff: int=9) -> datetime:
        return (cls().utc_now + timedelta(hours=diff)).strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def datetime_str_day(cls, diff: int=9) -> datetime:
        return (cls().utc_now + timedelta(hours=diff)).strftime("%Y-%m-%d")

    @classmethod
    def datetime_msec_str(cls, diff: int=9) -> datetime:
        return (cls().utc_now + timedelta(hours=diff)).strftime("%Y%m%d%H%M%S%04d")

    @classmethod
    def datetime_stamp(cls, diff: int=9):
        return int((cls().utc_now + timedelta(hours=diff)).timestamp())
