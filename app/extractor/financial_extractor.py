import re

def extract_merchant(description: str):

    if not description:
        return "unknown"

    desc = description.strip()

    # Handle UPI format
    if desc.startswith("UPI/"):
        parts = desc.split("/")

        if len(parts) > 3:
            merchant = parts[3].strip().lower()
            return merchant

    # fallback logic
    desc = desc.lower()

    # remove numbers
    desc = re.sub(r"\d+", "", desc)

    words = desc.split()

    return " ".join(words[:2])