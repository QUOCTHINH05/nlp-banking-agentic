# Simulated policy / FAQ data keyed by intent label

POLICIES = {
    "activate_my_card": "To activate your card, please call our hotline or use our mobile app.",
    "age_limit": "Our banking services are available to individuals aged 18 and above.",
    "card_arrival": "Card delivery typically takes 5-7 business days after activation.",
    "change_pin": "You can change your PIN at any ATM or through our mobile app.",
    "exchange_rate": "Our current exchange rates can be found on our website or mobile app. Currently, 1 USD = 0.85 EUR, 1 USD = 26373 VND.",
    "lost_or_stolen_card": "If your card is lost or stolen, please report it immediately to our hotline to prevent unauthorized use.",
    "passcode_forgotten": "If you've forgotten your passcode, please visit the nearest branch with valid ID for assistance.",
    "request_refund": "To request a refund, please contact our customer service with your transaction details.",
    "terminate_account": "To terminate your account, please visit the nearest branch with valid ID for assistance.",
    "transfer_timing": "Domestic transfers typically take 1-2 business days, while international transfers may take 3-5 business days.",
    "dispute_transaction": "To dispute a transaction, please contact our fraud department with your transaction ID and supporting evidence within 60 days.",
    "check_balance": "You can check your account balance through our mobile app, online banking portal, or by calling our hotline.",
    "update_contact_info": "To update your contact information, please visit our nearest branch with valid ID or use our online banking portal.",
    "apply_for_credit_line": "To apply for a credit line, please visit our nearest branch or use our mobile app to submit your application with required documents.",
    "cancel_subscription": "To cancel any subscription service, please contact our customer service or visit our online portal to manage your subscriptions.",
    "report_suspicious_activity": "If you notice suspicious activity on your account, please contact our fraud team immediately at our 24/7 hotline.",
    "request_overdraft_protection": "To request overdraft protection, please visit our nearest branch or call our customer service to discuss your options.",
    "check_transaction_history": "You can view your complete transaction history in our mobile app or online banking portal anytime.",
    "apply_for_new_card": "To apply for a new card, please visit our nearest branch with valid ID or use our mobile app to submit your application.",
    "update_beneficiary": "To add or update beneficiaries for fund transfers, please visit our branch or use the online banking portal for secure updates."
}

DEFAULT_POLICY = (
    "For further assistance, please contact our 24/7 support hotline or visit the nearest branch."
)

KNOWN_INTENTS = list(POLICIES.keys())
