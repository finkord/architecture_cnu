import re

def mask_card_number(card_number: str) -> str:
    """
    NFR-S4: Masks sensitive financial data.
    Extracts the last 4 digits and masks the rest.
    """
    if not card_number:
        return ""
    
    cleaned = re.sub(r'\D', '', card_number)
    
    if len(cleaned) < 4:
        return cleaned
        
    last_four = cleaned[-4:]
    return f"****-****-****-{last_four}"

def extract_last_four(card_number: str) -> str:
    """
    Extracts only the last four digits for storage matching NFR-S4.
    """
    if not card_number:
        return ""
    cleaned = re.sub(r'\D', '', card_number)
    if len(cleaned) < 4:
        return cleaned
    return cleaned[-4:]
