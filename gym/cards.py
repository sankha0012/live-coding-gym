from datetime import timedelta

INTERVALS = [1, 2, 4, 8, 16]  # days until a card in box 1..5 returns


def due(conn, cards, today):
    scheduled = {r["card_id"]: r["due"] for r in conn.execute("SELECT card_id, due FROM cards")}
    return [c for c in cards if scheduled.get(c["id"], "") <= today.isoformat()]


def record(conn, card_id, correct, today):
    row = conn.execute("SELECT box FROM cards WHERE card_id = ?", (card_id,)).fetchone()
    if correct:
        box = min((row["box"] if row else 0) + 1, len(INTERVALS))
        due_date = today + timedelta(days=INTERVALS[box - 1])
    else:
        box, due_date = 1, today
    conn.execute(
        "INSERT INTO cards (card_id, box, due) VALUES (?, ?, ?) "
        "ON CONFLICT(card_id) DO UPDATE SET box = excluded.box, due = excluded.due",
        (card_id, box, due_date.isoformat()),
    )
    conn.commit()
    return {"box": box, "due": due_date.isoformat()}
