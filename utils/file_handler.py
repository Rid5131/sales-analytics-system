def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
                return [line.strip() for line in lines[1:] if line.strip()]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("❌ File not found:", filename)
            return []
    return []


def parse_transactions(raw_lines):
    transactions = []
    for line in raw_lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts
        pname = pname.replace(',', '')
        qty = qty.replace(',', '')
        price = price.replace(',', '')

        try:
            transactions.append({
                'TransactionID': tid,
                'Date': date,
                'ProductID': pid,
                'ProductName': pname,
                'Quantity': int(qty),
                'UnitPrice': float(price),
                'CustomerID': cid,
                'Region': region
            })
        except:
            continue
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid, invalid = [], 0

    regions = sorted({t['Region'] for t in transactions if t['Region']})
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions if t['Quantity'] > 0]

    print("Regions:", ", ".join(regions))
    print(f"Amount Range: ₹{min(amounts)} - ₹{max(amounts)}")

    for t in transactions:
        if (
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C') or
            not t['Region']
        ):
            invalid += 1
            continue

        amount = t['Quantity'] * t['UnitPrice']

        if region and t['Region'] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'final_count': len(valid)
    }

    return valid, invalid, summary
