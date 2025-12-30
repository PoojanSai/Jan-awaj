def identify_department(text):
    text = text.lower()

    if "water" in text:
        return "Water Supply Department"
    if "electric" in text or "power" in text:
        return "Electricity Department"
    if "road" in text or "pothole" in text:
        return "Public Works Department"
    if "garbage" in text:
        return "Municipal Corporation"

    return "General Administration"
