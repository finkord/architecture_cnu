def mask_card_number(card_number: str) -> str:
    """
    Mask all but the last 4 digits of a card number.
    Ensures compliance with NFR-S4 (Mask sensitive payment data).
    """
    if not card_number or len(card_number) < 4:
        return "****"
    
    return f"**** **** **** {card_number[-4:]}"
