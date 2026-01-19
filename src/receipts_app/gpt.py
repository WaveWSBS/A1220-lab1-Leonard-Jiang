# gpt.py
import json
from openai import OpenAI

CATEGORIES = ["Meals", "Transport", "Lodging", "Office Supplies", 
"Entertainment", "Other"]

def extract_receipt_info(image_b64):
    """Extract structured receipt fields from a base64-encoded image.

    Args:
        image_b64 (str): Base64-encoded receipt image data.

    Returns:
        dict: Parsed JSON with keys "date", "amount", "vendor", "category".

    Assumptions:
        The OpenAI API key is set and the model returns valid JSON.
    """
    prompt = f"""
You are an information extraction system.
Extract ONLY the following fields from the receipt image:

date: the receipt date as a string
amount: the total amount paid as it appears on the receipt
vendor: the merchant or vendor name
category: one of [{", ".join(CATEGORIES)}]

Return EXACTLY one JSON object with these four keys and NOTHING ELSE.
Do not include explanations, comments, or formatting.
Do not wrap the JSON in markdown.
If a field cannot be determined, use null.

The output must be valid JSON.
"""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        seed=43,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]
    )
    data = json.loads(response.choices[0].message.content)
    return normalize_amount_field(data)


def normalize_amount_field(data):
    """Normalize the "amount" field by stripping "$" and converting to float.

    Args:
        data (dict): Parsed receipt data from the language model.

    Returns:
        dict: Updated data with "amount" as a float when possible.

    Assumptions:
        The "amount" field is a number-like string or null.
    """
    amount = data.get("amount")
    if amount is None:
        return data
    if isinstance(amount, str):
        amount = amount.replace("$", "").strip()
    try:
        data["amount"] = float(amount)
    except (TypeError, ValueError):
        pass
    return data
