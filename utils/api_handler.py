import requests


def fetch_all_products():
    try:
        res = requests.get('https://dummyjson.com/products?limit=100')
        res.raise_for_status()
        print("✓ API fetch successful")
        return res.json().get('products', [])
    except:
        print("API fetch failed")
        return []


def create_product_mapping(api_products):
    return {
    p['id']: {
        'title': p.get('title'),
        'category': p.get('category'),
        'brand': p.get('brand'),      # SAFE ACCESS
        'rating': p.get('rating')
    }
    for p in api_products
}


def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for t in transactions:
        pid = int(''.join(filter(str.isdigit, t['ProductID'])))
        product = product_mapping.get(pid)

        t = t.copy()
        if product:
            t.update({
                'API_Category': product['category'],
                'API_Brand': product['brand'],
                'API_Rating': product['rating'],
                'API_Match': True
            })
        else:
            t.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })

        enriched.append(t)

    save_enriched_data(enriched)
    return enriched


def save_enriched_data(data, filename='data/enriched_sales_data.txt'):
    headers = list(data[0].keys())
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('|'.join(headers) + '\n')
        for row in data:
            f.write('|'.join(str(row[h]) for h in headers) + '\n')
