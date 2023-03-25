import arrow as dt
import pytest
from arrow import Arrow


@pytest.fixture()
def now() -> Arrow:
    return dt.now()


def test_now(now: Arrow):
    assert "+08:00" == now.format("ZZ")

    us = dt.now("US/Pacific")
    assert "-07:00" == us.format("ZZ")

    utcnow = dt.utcnow()
    assert "+00:00" == utcnow.format("ZZ")


def test_timestamp(now):
    ts = now.timestamp()
    assert 1.6 * 10**9 < ts < 1.7 * 10**9, f"{ts=}"
    assert isinstance(ts, float), f"{type(ts)=}"


def test_format(now):
    s = now.format()
    assert s.startswith("20")
    assert len(s) == len("2023-01-01 00:00:00+08:00"), f"{s=}"


def test_format_manual(now):
    s = now.format("YYYY-MM-DD HH:mm:ss")
    s2 = now.format()
    assert s2.startswith(s), f"{s=},{s2=}"


def test_from_timestamp(now: Arrow):
    ts = now.timestamp()
    assert dt.get(ts).timestamp() == ts
    assert dt.get(int(ts)).timestamp() == int(ts)


def test_from_str(now: Arrow):
    s = now.format()
    assert dt.get(s).format() == s

    f = "YYYY-MM-DD HH:mm:ss"
    s = now.format(f)
    assert dt.get(s).format(f) == s
    assert dt.get(s, f).format(f) == s


def test_shift(now: Arrow):
    tomorrow = now.shift(days=1)

    assert (tomorrow - now).days == 1, f"{(tomorrow - now).days=}"


def test_zone(now: Arrow):
    ac = now.to("America/Chicago")
    assert "-05:00" == ac.format("ZZ")

    utc = ac.to("+00:00")
    assert "+00:00" == utc.format("ZZ")

    utc = ac.to("utc")
    assert "+00:00" == utc.format("ZZ")

    local = ac.to("local")
    assert "+08:00" == local.format("ZZ")


def test_human(now: Arrow):
    assert now.humanize() == "just now", f"{now.humanize()=}"
    assert now.humanize(locale="zh") == "刚才", f"{now.humanize(locale='zh')=}"


def test_floor(now: Arrow):
    floor = now.floor("hour")
    assert floor.minute == 0 and floor.second == 0, f"{floor=}"


def test_ceil(now: Arrow):
    ceil = now.ceil("day")
    assert ceil.hour == 23 and ceil.minute == 59 and ceil.second == 59, f"{ceil=}"
