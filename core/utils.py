def format_rupiah(amount):
    try:
        return f"Rp {int(amount):,}".replace(",", ".")
    except Exception:
        return "Rp 0"
