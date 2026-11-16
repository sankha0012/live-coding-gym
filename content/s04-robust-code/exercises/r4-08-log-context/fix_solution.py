import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
log = logging.getLogger("orders")
log.addHandler(handler)
log.setLevel(logging.INFO)
orders = [{"order_id": "A-17", "qty": "3"}, {"order_id": "A-18", "qty": "three"},
          {"order_id": "A-19", "qty": None}]

def process_bad(order):
    try:
        return int(order["qty"])
    except (ValueError, TypeError) as exc:
        log.error("failed to parse quantity order_id=%s qty=%r error=%s",
                  order["order_id"], order["qty"], exc)

def process_good(order):
    try:
        return int(order["qty"])
    except (ValueError, TypeError) as exc:
        log.error("failed to parse quantity order_id=%s qty=%r error=%s",
                  order["order_id"], order["qty"], exc)

print("--- bad ---")
print([process_bad(o) for o in orders])
print("--- good ---")
print([process_good(o) for o in orders])
