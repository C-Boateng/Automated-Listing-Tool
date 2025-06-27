import ollama
from typing import List, Dict
from utils.config import LLM_MODEL

def create_chat_messages(attributes: Dict) -> List[Dict[str, str]]:
    examples = [
        {
            "attributes": {
                "product": "Basic T-Shirt Cotton Short Sleeve",
                "gender": "Women",
                "color": "Blue",
                "category": {
                    "vinted": "Women > Clothing > Tops & t-shirts > T-shirts",
                    "ebay": "Clothing, Shoes & Accessories > Women > Women's Clothing > Tops"
                },
                "size": "M",
                "condition": "2"
            },
            "vinted": {
                "title": "Blauw Bershka T-shirt",
                "description": "Mooi blauw T-shirt, maat M, amper gedragen, goede staat."
            },
            "ebay": {
                "title": "Women's Blue Cotton T-Shirt Short Sleeve Size M Good Condition",
                "description": "Premium women's blue cotton T-shirt, size M, in good condition. Slim fit, stretchy fabric, scoop neck, short sleeves. Perfect for casual wear or layering. Machine washable, no stains or tears. True to size, ideal for everyday comfort."
            }
        },
        {
            "attributes": {
                "product": "Sundress Summer Sleeveless",
                "gender": "Women",
                "color": "Red",
                "category": {
                    "vinted": "Women > Clothing > Dresses > Midi dresses",
                    "ebay": "Clothing, Shoes & Accessories > Women > Women's Clothing > Dresses"
                },
                "size": "S",
                "condition": "3"
            },
            "vinted": {
                "title": "Rode Zomerjurk",
                "description": "Prachtige rode jurk, maat S, zo goed als nieuw, perfect voor de zomer."
            },
            "ebay": {
                "title": "Women's Red Sleeveless Sundress Size S Like New",
                "description": "Stunning red sleeveless sundress, size S, in excellent condition. Lightweight, breathable fabric, ideal for summer outings or parties. Midi length, flattering fit. No damage or wear, machine washable. Perfect for vacations or special occasions."
            }
        },
        {
            "attributes": {
                "product": "H&M Denim Jeans",
                "gender": "Men",
                "color": "Blue",
                "category": {
                    "vinted": "Men > Clothing > Jeans > Slim jeans",
                    "ebay": "Clothing, Shoes & Accessories > Men > Men's Clothing > Jeans"
                },
                "size": "L",
                "condition": "3"
            },
            "vinted": {
                "title": "H&M Slim Jeans Blauw",
                "description": "Blauwe H&M jeans, maat L, zo goed als nieuw, comfortabele pasvorm."
            },
            "ebay": {
                "title": "Men's H&M Blue Denim Slim Fit Jeans Size L Like New",
                "description": "High-quality H&M men's blue denim jeans, size L, in excellent condition. Slim fit, durable fabric, perfect for casual or semi-formal settings. Five-pocket style, machine washable, no signs of wear. Ideal for everyday wear or dressing up."
            }
        },
        {
            "attributes": {
                "product": "Zara Wool Coat",
                "gender": "Women",
                "color": "Black",
                "category": {
                    "vinted": "Women > Clothing > Outerwear > Coats > Long coats",
                    "ebay": "Clothing, Shoes & Accessories > Women > Women's Clothing > Coats, Jackets & Vests"
                },
                "size": "XS",
                "condition": "1"
            },
            "vinted": {
                "title": "Zwart Zara Wollen Jas",
                "description": "Zwarte wollen jas, maat XS, in redelijke staat, warm en stijlvol."
            },
            "ebay": {
                "title": "Women's Zara Black Wool Coat Size XS Fair Condition",
                "description": "Elegant Zara women's black wool coat, size XS, in fair condition. Warm, stylish design with button closure, perfect for winter. Minor signs of wear, fully functional. Dry clean recommended. Ideal for professional or casual outfits."
            }
        },
        {
            "attributes": {
                "product": "Nike Running Shoes",
                "gender": "Men",
                "color": "Grey",
                "category": {
                    "vinted": "Men > Shoes > Sneakers > Running sneakers",
                    "ebay": "Clothing, Shoes & Accessories > Men > Men's Shoes > Athletic Shoes"
                },
                "size": "XL",
                "condition": "2"
            },
            "vinted": {
                "title": "Grijze Nike Schoenen",
                "description": "Nike hardloopschoenen, maat XL, goede staat, ideaal voor sporten."
            },
            "ebay": {
                "title": "Men's Nike Grey Running Shoes Size XL Good Condition",
                "description": "Men's Nike grey running shoes, size XL, in good condition. Lightweight, breathable mesh upper, cushioned sole for comfort. Perfect for running, gym, or casual wear. Minor wear on soles, cleaned and ready to use. True to size."
            }
        }
    ]

    messages = []

    # System Role Message
    system_content = """You are an expert at generating clothing and accessory listings for second-hand marketplaces Vinted and eBay.
    Given attributes (product (short item description), gender (Men or Women), color, Vinted category, eBay category, size (XS, S, M, L, XL), condition (1-3 stars, where 3=excellent, 2=good, 1=fair)), create concise, platform-specific listings.

    For Vinted:
    - Titles: In Dutch, trendy and catchy.
    - Descriptions: In Dutch, casual and engaging. Include product, color, size, and condition.

    For eBay:
    - Titles: In English, keyword-rich for searchability.
    - Descriptions: In English, detailed with fit, material, care instructions, and usage scenarios. Include product, color, size, and condition.

    Always try to include all provided attributes in the output. If some attributes are missing or inaccurate, don't mention it in your output. Generate only the titles and descriptions, using this strict format below (NO EXCEPTIONS):
    === Vinted ===
    Title: <vinted_title>
    Description: <vinted_description> =====

    === eBay ===
    Title: <ebay_title>
    Description: <ebay_description> =====
    """
    messages.append({"role": "system", "content": system_content})

    # Example Conversations
    for example in examples:
        ex_attributes = example["attributes"]
        user_example_content = f"""Please generate listings for the following attributes:
        Product: {ex_attributes['product']}
        Gender: {ex_attributes['gender']}
        Color: {ex_attributes['color']}
        Vinted Category: {ex_attributes['category']['vinted']}
        eBay Category: {ex_attributes['category']['ebay']}
        Size: {ex_attributes['size']}
        Condition: {ex_attributes['condition']}
        """
        messages.append({"role": "user", "content": user_example_content})

        assistant_example_content = f"""=== Vinted ===
        Title: {example['vinted']['title']}
        Description: {example['vinted']['description']} =====

        === eBay ===
        Title: {example['ebay']['title']}
        Description: {example['ebay']['description']} =====
        """
        messages.append({"role": "assistant", "content": assistant_example_content})

    # Final User Request
    final_user_content = f"""Now, please generate listings for the following item:
        Product: {attributes['product']}
        Gender: {attributes['gender']}
        Color: {attributes['color']}
        Vinted Category: {attributes['category']['vinted']}
        eBay Category: {attributes['category']['ebay']}
        Size: {attributes['size']}
        Condition: {attributes['condition']}
        """
    messages.append({"role": "user", "content": final_user_content})

    return messages

def generate_text(attributes: Dict) -> str:
    chat_messages = create_chat_messages(attributes)
    response = ollama.chat(model=LLM_MODEL, messages=chat_messages)
    return response['message']['content']