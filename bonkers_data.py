import json

with open(r"C:\Users\kishan.prajapati\Desktop\4 python\bonker (1).json", "r", encoding="utf-8") as f:
    data = json.load(f)

result = []

for item in data.get("products", []):

    handle = item.get("handle")
    product_name = next((
        item.get(k) for k in ["title", "name", "product_name", "product_title", "handle"]
        if item.get(k)
    ), None)

    vendor = item.get("vendor", "Bonkers")

    product_url = f"https://www.bonkerscorner.com/products/{handle}"

    variants = item.get("variants", [])

    variants_list = [
        {
            "variantName": item['name'].split("-")[1].replace(' ',''),
            "variantId": int(item.get("id") or item.get("variant_id")),
            "variantUrl": f"{product_url}?variant={item.get('id') or item.get('variant_id')}",
            "variantPrice": float(item.get("price")) / 100 if isinstance(item.get("price"), (int, float))
                            else float(item.get("price")) if item.get("price") else None
        }
        for item in variants
        if item.get("id") or item.get("variant_id")
    ]
    sizes = list({
        item['name'].split('-')[1].strip() for item in item['variants']
    })

    product_price = variants_list[0]["variantPrice"] 

    result.append({
        "productName": product_name,
        "vendor": vendor,
        "productUrl": product_url,
        "productPrice": product_price,
        "variantCount": len(variants_list),
        "variantOptions": [
            {
                "optionName": "Size",
                "optionValues": sizes
            }
        ],
        "variants": variants_list
    })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)



