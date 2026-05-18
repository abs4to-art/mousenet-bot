import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_PATH = "mousenet.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            referred_by INTEGER DEFAULT NULL,
            trial_used INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tariff TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_label TEXT DEFAULT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)

    cur.execute("PRAGMA table_info(orders)")
    cols = [row["name"] for row in cur.fetchall()]
    if "payment_label" not in cols:
        cur.execute("ALTER TABLE orders ADD COLUMN payment_label TEXT DEFAULT NULL")

    conn.commit()
    conn.close()
    logger.info("Database initialized")


def add_user(user_id: int, username: str | None, referred_by: int | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, referred_by) VALUES (?, ?, ?)",
        (user_id, username, referred_by),
    )
    conn.commit()
    conn.close()


def user_exists(user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def has_trial_used(user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT trial_used FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row and row["trial_used"] == 1:
        return True
    return False


def use_trial(user_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET trial_used = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_order(user_id: int, tariff: str, payment_label: str | None = None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (user_id, tariff, payment_label) VALUES (?, ?, ?)",
        (user_id, tariff, payment_label),
    )
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def get_pending_orders() -> list[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, tariff, created_at FROM orders WHERE status = 'pending' ORDER BY created_at DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_by_label(label: str) -> sqlite3.Row | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, tariff, status FROM orders WHERE payment_label = ?",
        (label,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_order(order_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, tariff, status FROM orders WHERE id = ?", (order_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def confirm_order(order_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'confirmed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()


def reject_order(order_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'rejected' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()


def get_referral_count(user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE referred_by = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row["cnt"] if row else 0


def get_all_users() -> list[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows
