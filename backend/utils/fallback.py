DEFAULT_COMPLAINT = "General civic issue reported by citizen."

def fallback_text(text):
    return text if text else DEFAULT_COMPLAINT


