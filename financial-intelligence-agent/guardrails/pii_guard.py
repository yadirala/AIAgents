import re

patterns = {
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
}

def redact_pii(text):
    for key, pattern in patterns.items():
        text = re.sub(pattern, f'[{key.upper()}]', text)
    return text

if __name__ == "__main__":
    test = "My email is john@example.com and SSN is 123-45-6789 and card 4111-1111-1111-1111"
    print(redact_pii(test))