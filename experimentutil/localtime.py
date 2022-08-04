from datetime import datetime, timedelta, timezone


__all__ = [
    'now',
    'time_round'
]


def now(as_local: bool = True) -> datetime:
    """ Get timezone aware current date/time as UTC or local time.

    :param as_local: if True get datetime in local timezone, else in UTC
    :return: datetime
    """
    dt_utc = datetime.now(timezone.utc)

    if not as_local:
        return dt_utc

    return dt_utc.astimezone()


def time_round(t: datetime, nearest: timedelta) -> datetime:
    """ Round datetime to nearest interval defined as a timedelta.

    :param t: input datetime
    :param nearest: nearest timedelta to round to
    :return: datetime
    """
    t_utc = t.replace(tzinfo=timezone.utc)

    dt = (t_utc.timestamp() - round(t_utc.timestamp() / nearest.total_seconds()) * nearest.total_seconds())

    if t.tzinfo is not None:
        return (t.astimezone(timezone.utc) - timedelta(seconds=dt)).astimezone(t.tzinfo)
    else:
        return t - timedelta(seconds=dt)
