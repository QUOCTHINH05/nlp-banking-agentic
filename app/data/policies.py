# Simulated policy / FAQ data keyed by intent label

POLICIES = {
    "activate_my_card": "To activate your card, please call our hotline or use our mobile app.",
    "age_limit": "Our banking services are available to individuals aged 18 and above.",
    "card_arrival": "Card delivery typically takes 5-7 business days after activation.",
    "change_pin": "You can change your PIN at any ATM or through our mobile app.",
    "exchange_rate": "Our current exchange rates can be found on our website or mobile app.",
    "lost_or_stolen_card": "If your card is lost or stolen, please report it immediately to our hotline to prevent unauthorized use.",
    "passcode_forgotten": "If you've forgotten your passcode, please visit the nearest branch with valid ID for assistance.",
    "request_refund": "To request a refund, please contact our customer service with your transaction details.",
    "terminate_account": "To terminate your account, please visit the nearest branch with valid ID for assistance.",
    "transfer_timing": "Domestic transfers typically take 1-2 business days, while international transfers may take 3-5 business days."
}

DEFAULT_POLICY = (
    "For further assistance, please contact our 24/7 support hotline or visit the nearest branch."
)

KNOWN_INTENTS = list(POLICIES.keys())
