#!/usr/bin/env python3
"""price_pence must reproduce the frozen behaviour matrix exactly.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c2_behaviour_matrix"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c2_behaviour_matrix.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _load_app_module(scratch, name):
    import importlib
    sys.path.insert(0, str(scratch))
    for mod in [m for m in list(sys.modules)
                if m == "app" or m.startswith("app.")]:
        del sys.modules[mod]
    return importlib.import_module(name)


MATRIX = {
    "0|ECO7|business|-": 90,
    "0|ECO7|business|GREEN5": 85,
    "0|ECO7|business|NEW": 0,
    "0|ECO7|business|SAVE10": 90,
    "0|ECO7|domestic|-": 78,
    "0|ECO7|domestic|GREEN5": 74,
    "0|ECO7|domestic|NEW": 0,
    "0|ECO7|domestic|SAVE10": 78,
    "0|FIX12|business|-": 60,
    "0|FIX12|business|GREEN5": 56,
    "0|FIX12|business|NEW": 0,
    "0|FIX12|business|SAVE10": 60,
    "0|FIX12|domestic|-": 52,
    "0|FIX12|domestic|GREEN5": 49,
    "0|FIX12|domestic|NEW": 0,
    "0|FIX12|domestic|SAVE10": 52,
    "0|STD|business|-": 72,
    "0|STD|business|GREEN5": 68,
    "0|STD|business|NEW": 0,
    "0|STD|business|SAVE10": 72,
    "0|STD|domestic|-": 63,
    "0|STD|domestic|GREEN5": 59,
    "0|STD|domestic|NEW": 0,
    "0|STD|domestic|SAVE10": 63,
    "100|ECO7|business|-": 2730,
    "100|ECO7|business|GREEN5": 2593,
    "100|ECO7|business|NEW": 2630,
    "100|ECO7|business|SAVE10": 2466,
    "100|ECO7|domestic|-": 2598,
    "100|ECO7|domestic|GREEN5": 2468,
    "100|ECO7|domestic|NEW": 2498,
    "100|ECO7|domestic|SAVE10": 2346,
    "100|FIX12|business|-": 3420,
    "100|FIX12|business|GREEN5": 3248,
    "100|FIX12|business|NEW": 3320,
    "100|FIX12|business|SAVE10": 3084,
    "100|FIX12|domestic|-": 3202,
    "100|FIX12|domestic|GREEN5": 3041,
    "100|FIX12|domestic|NEW": 3102,
    "100|FIX12|domestic|SAVE10": 2887,
    "100|STD|business|-": 3192,
    "100|STD|business|GREEN5": 3032,
    "100|STD|business|NEW": 3092,
    "100|STD|business|SAVE10": 2880,
    "100|STD|domestic|-": 3003,
    "100|STD|domestic|GREEN5": 2852,
    "100|STD|domestic|NEW": 2903,
    "100|STD|domestic|SAVE10": 2709,
    "10|ECO7|business|-": 354,
    "10|ECO7|business|GREEN5": 336,
    "10|ECO7|business|NEW": 254,
    "10|ECO7|business|SAVE10": 327,
    "10|ECO7|domestic|-": 330,
    "10|ECO7|domestic|GREEN5": 313,
    "10|ECO7|domestic|NEW": 230,
    "10|ECO7|domestic|SAVE10": 305,
    "10|FIX12|business|-": 396,
    "10|FIX12|business|GREEN5": 375,
    "10|FIX12|business|NEW": 296,
    "10|FIX12|business|SAVE10": 362,
    "10|FIX12|domestic|-": 367,
    "10|FIX12|domestic|GREEN5": 348,
    "10|FIX12|domestic|NEW": 267,
    "10|FIX12|domestic|SAVE10": 336,
    "10|STD|business|-": 384,
    "10|STD|business|GREEN5": 364,
    "10|STD|business|NEW": 284,
    "10|STD|business|SAVE10": 352,
    "10|STD|domestic|-": 357,
    "10|STD|domestic|GREEN5": 339,
    "10|STD|domestic|NEW": 257,
    "10|STD|domestic|SAVE10": 327,
    "137|ECO7|business|-": 3706,
    "137|ECO7|business|GREEN5": 3520,
    "137|ECO7|business|NEW": 3606,
    "137|ECO7|business|SAVE10": 3344,
    "137|ECO7|domestic|-": 3531,
    "137|ECO7|domestic|GREEN5": 3353,
    "137|ECO7|domestic|NEW": 3431,
    "137|ECO7|domestic|SAVE10": 3185,
    "137|FIX12|business|-": 4663,
    "137|FIX12|business|GREEN5": 4429,
    "137|FIX12|business|NEW": 4563,
    "137|FIX12|business|SAVE10": 4202,
    "137|FIX12|domestic|-": 4368,
    "137|FIX12|domestic|GREEN5": 4149,
    "137|FIX12|domestic|NEW": 4268,
    "137|FIX12|domestic|SAVE10": 3936,
    "137|STD|business|-": 4346,
    "137|STD|business|GREEN5": 4128,
    "137|STD|business|NEW": 4246,
    "137|STD|business|SAVE10": 3918,
    "137|STD|domestic|-": 4090,
    "137|STD|domestic|GREEN5": 3886,
    "137|STD|domestic|NEW": 3990,
    "137|STD|domestic|SAVE10": 3687,
    "1|ECO7|business|-": 116,
    "1|ECO7|business|GREEN5": 110,
    "1|ECO7|business|NEW": 16,
    "1|ECO7|business|SAVE10": 112,
    "1|ECO7|domestic|-": 103,
    "1|ECO7|domestic|GREEN5": 98,
    "1|ECO7|domestic|NEW": 3,
    "1|ECO7|domestic|SAVE10": 100,
    "1|FIX12|business|-": 93,
    "1|FIX12|business|GREEN5": 88,
    "1|FIX12|business|NEW": 0,
    "1|FIX12|business|SAVE10": 90,
    "1|FIX12|domestic|-": 84,
    "1|FIX12|domestic|GREEN5": 79,
    "1|FIX12|domestic|NEW": 0,
    "1|FIX12|domestic|SAVE10": 80,
    "1|STD|business|-": 103,
    "1|STD|business|GREEN5": 97,
    "1|STD|business|NEW": 3,
    "1|STD|business|SAVE10": 99,
    "1|STD|domestic|-": 92,
    "1|STD|domestic|GREEN5": 87,
    "1|STD|domestic|NEW": 0,
    "1|STD|domestic|SAVE10": 89,
    "250|ECO7|business|-": 6690,
    "250|ECO7|business|GREEN5": 6355,
    "250|ECO7|business|NEW": 6590,
    "250|ECO7|business|SAVE10": 6030,
    "250|ECO7|domestic|-": 6378,
    "250|ECO7|domestic|GREEN5": 6059,
    "250|ECO7|domestic|NEW": 6278,
    "250|ECO7|domestic|SAVE10": 5748,
    "250|FIX12|business|-": 8460,
    "250|FIX12|business|GREEN5": 8036,
    "250|FIX12|business|NEW": 8360,
    "250|FIX12|business|SAVE10": 7620,
    "250|FIX12|domestic|-": 7927,
    "250|FIX12|domestic|GREEN5": 7530,
    "250|FIX12|domestic|NEW": 7827,
    "250|FIX12|domestic|SAVE10": 7140,
    "250|STD|business|-": 7872,
    "250|STD|business|GREEN5": 7478,
    "250|STD|business|NEW": 7772,
    "250|STD|business|SAVE10": 7092,
    "250|STD|domestic|-": 7413,
    "250|STD|domestic|GREEN5": 7042,
    "250|STD|domestic|NEW": 7313,
    "250|STD|domestic|SAVE10": 6678,
    "25|ECO7|business|-": 750,
    "25|ECO7|business|GREEN5": 711,
    "25|ECO7|business|NEW": 650,
    "25|ECO7|business|SAVE10": 684,
    "25|ECO7|domestic|-": 708,
    "25|ECO7|domestic|GREEN5": 673,
    "25|ECO7|domestic|NEW": 608,
    "25|ECO7|domestic|SAVE10": 645,
    "25|FIX12|business|-": 900,
    "25|FIX12|business|GREEN5": 854,
    "25|FIX12|business|NEW": 800,
    "25|FIX12|business|SAVE10": 816,
    "25|FIX12|domestic|-": 840,
    "25|FIX12|domestic|GREEN5": 798,
    "25|FIX12|domestic|NEW": 740,
    "25|FIX12|domestic|SAVE10": 761,
    "25|STD|business|-": 852,
    "25|STD|business|GREEN5": 808,
    "25|STD|business|NEW": 752,
    "25|STD|business|SAVE10": 774,
    "25|STD|domestic|-": 798,
    "25|STD|domestic|GREEN5": 758,
    "25|STD|domestic|NEW": 698,
    "25|STD|domestic|SAVE10": 724,
    "2|ECO7|business|-": 142,
    "2|ECO7|business|GREEN5": 135,
    "2|ECO7|business|NEW": 42,
    "2|ECO7|business|SAVE10": 136,
    "2|ECO7|domestic|-": 129,
    "2|ECO7|domestic|GREEN5": 121,
    "2|ECO7|domestic|NEW": 29,
    "2|ECO7|domestic|SAVE10": 123,
    "2|FIX12|business|-": 127,
    "2|FIX12|business|GREEN5": 120,
    "2|FIX12|business|NEW": 27,
    "2|FIX12|business|SAVE10": 120,
    "2|FIX12|domestic|-": 115,
    "2|FIX12|domestic|GREEN5": 109,
    "2|FIX12|domestic|NEW": 15,
    "2|FIX12|domestic|SAVE10": 109,
    "2|STD|business|-": 134,
    "2|STD|business|GREEN5": 127,
    "2|STD|business|NEW": 34,
    "2|STD|business|SAVE10": 127,
    "2|STD|domestic|-": 121,
    "2|STD|domestic|GREEN5": 115,
    "2|STD|domestic|NEW": 21,
    "2|STD|domestic|SAVE10": 115,
    "3|ECO7|business|-": 169,
    "3|ECO7|business|GREEN5": 159,
    "3|ECO7|business|NEW": 69,
    "3|ECO7|business|SAVE10": 160,
    "3|ECO7|domestic|-": 154,
    "3|ECO7|domestic|GREEN5": 145,
    "3|ECO7|domestic|NEW": 54,
    "3|ECO7|domestic|SAVE10": 145,
    "3|FIX12|business|-": 160,
    "3|FIX12|business|GREEN5": 152,
    "3|FIX12|business|NEW": 60,
    "3|FIX12|business|SAVE10": 150,
    "3|FIX12|domestic|-": 147,
    "3|FIX12|domestic|GREEN5": 139,
    "3|FIX12|domestic|NEW": 47,
    "3|FIX12|domestic|SAVE10": 137,
    "3|STD|business|-": 165,
    "3|STD|business|GREEN5": 157,
    "3|STD|business|NEW": 65,
    "3|STD|business|SAVE10": 156,
    "3|STD|domestic|-": 151,
    "3|STD|domestic|GREEN5": 142,
    "3|STD|domestic|NEW": 51,
    "3|STD|domestic|SAVE10": 141,
    "50|ECO7|business|-": 1410,
    "50|ECO7|business|GREEN5": 1339,
    "50|ECO7|business|NEW": 1310,
    "50|ECO7|business|SAVE10": 1278,
    "50|ECO7|domestic|-": 1338,
    "50|ECO7|domestic|GREEN5": 1271,
    "50|ECO7|domestic|NEW": 1238,
    "50|ECO7|domestic|SAVE10": 1212,
    "50|FIX12|business|-": 1740,
    "50|FIX12|business|GREEN5": 1652,
    "50|FIX12|business|NEW": 1640,
    "50|FIX12|business|SAVE10": 1572,
    "50|FIX12|domestic|-": 1627,
    "50|FIX12|domestic|GREEN5": 1545,
    "50|FIX12|domestic|NEW": 1527,
    "50|FIX12|domestic|SAVE10": 1470,
    "50|STD|business|-": 1632,
    "50|STD|business|GREEN5": 1550,
    "50|STD|business|NEW": 1532,
    "50|STD|business|SAVE10": 1476,
    "50|STD|domestic|-": 1533,
    "50|STD|domestic|GREEN5": 1456,
    "50|STD|domestic|NEW": 1433,
    "50|STD|domestic|SAVE10": 1386,
    "7|ECO7|business|-": 274,
    "7|ECO7|business|GREEN5": 260,
    "7|ECO7|business|NEW": 174,
    "7|ECO7|business|SAVE10": 255,
    "7|ECO7|domestic|-": 255,
    "7|ECO7|domestic|GREEN5": 241,
    "7|ECO7|domestic|NEW": 155,
    "7|ECO7|domestic|SAVE10": 237,
    "7|FIX12|business|-": 295,
    "7|FIX12|business|GREEN5": 279,
    "7|FIX12|business|NEW": 195,
    "7|FIX12|business|SAVE10": 271,
    "7|FIX12|domestic|-": 273,
    "7|FIX12|domestic|GREEN5": 259,
    "7|FIX12|domestic|NEW": 173,
    "7|FIX12|domestic|SAVE10": 250,
    "7|STD|business|-": 290,
    "7|STD|business|GREEN5": 274,
    "7|STD|business|NEW": 190,
    "7|STD|business|SAVE10": 267,
    "7|STD|domestic|-": 268,
    "7|STD|domestic|GREEN5": 255,
    "7|STD|domestic|NEW": 168,
    "7|STD|domestic|SAVE10": 247,
    "999|ECO7|business|-": 26463,
    "999|ECO7|business|GREEN5": 25140,
    "999|ECO7|business|NEW": 26363,
    "999|ECO7|business|SAVE10": 23826,
    "999|ECO7|domestic|-": 25253,
    "999|ECO7|domestic|GREEN5": 23990,
    "999|ECO7|domestic|NEW": 25153,
    "999|ECO7|domestic|SAVE10": 22735,
    "999|FIX12|business|-": 33626,
    "999|FIX12|business|GREEN5": 31944,
    "999|FIX12|business|NEW": 33526,
    "999|FIX12|business|SAVE10": 30268,
    "999|FIX12|domestic|-": 31521,
    "999|FIX12|domestic|GREEN5": 29944,
    "999|FIX12|domestic|NEW": 31421,
    "999|FIX12|domestic|SAVE10": 28374,
    "999|STD|business|-": 31240,
    "999|STD|business|GREEN5": 29678,
    "999|STD|business|NEW": 31140,
    "999|STD|business|SAVE10": 28123,
    "999|STD|domestic|-": 29433,
    "999|STD|domestic|GREEN5": 27961,
    "999|STD|domestic|NEW": 29333,
    "999|STD|domestic|SAVE10": 26495,
}


def main():
    scratch = scratch_dir()
    try:
        billing = _load_app_module(scratch, "app.billing")
    except Exception as exc:
        emit(False, "could not import app.billing: %s" % exc)
    bad = []
    for key, want in MATRIX.items():
        kwh_s, tariff, ctype, promo_s = key.split("|")
        promo = None if promo_s == "-" else promo_s
        try:
            got = billing.price_pence(int(kwh_s), tariff, ctype, promo)
        except Exception as exc:
            bad.append("%s raised %s" % (key, exc))
            continue
        if got != want:
            bad.append("%s == %s, want %s" % (key, got, want))
        if len(bad) >= 5:
            break
    if bad:
        emit(False, "behaviour changed: %s" % "; ".join(bad))
    for tariff in ("MEGA", ""):
        try:
            billing.price_pence(100, tariff, "domestic", None)
            emit(False, "unknown tariff %r no longer raises ValueError"
                 % tariff)
        except ValueError:
            pass
        except Exception as exc:
            emit(False, "unknown tariff %r raises %s, want ValueError"
                 % (tariff, type(exc).__name__))
    emit(True, "all %d matrix entries match and unknown tariffs raise "
               "ValueError" % len(MATRIX))


if __name__ == "__main__":
    main()
