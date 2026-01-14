from collections import defaultdict


def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)


def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {'total_sales': 0, 'transaction_count': 0})

    total = calculate_total_revenue(transactions)

    for t in transactions:
        r = t['Region']
        amt = t['Quantity'] * t['UnitPrice']
        region_data[r]['total_sales'] += amt
        region_data[r]['transaction_count'] += 1

    for r in region_data:
        region_data[r]['percentage'] = round((region_data[r]['total_sales'] / total) * 100, 2)

    return dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))


def top_selling_products(transactions, n=5):
    prod = defaultdict(lambda: [0, 0])

    for t in transactions:
        prod[t['ProductName']][0] += t['Quantity']
        prod[t['ProductName']][1] += t['Quantity'] * t['UnitPrice']

    result = [(k, v[0], v[1]) for k, v in prod.items()]
    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


def customer_analysis(transactions):
    cust = defaultdict(lambda: {'total_spent': 0, 'count': 0, 'products': set()})

    for t in transactions:
        c = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        cust[c]['total_spent'] += amt
        cust[c]['count'] += 1
        cust[c]['products'].add(t['ProductName'])

    result = {}
    for c, v in cust.items():
        result[c] = {
            'total_spent': v['total_spent'],
            'purchase_count': v['count'],
            'avg_order_value': round(v['total_spent'] / v['count'], 2),
            'products_bought': list(v['products'])
        }

    return dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))


def daily_sales_trend(transactions):
    daily = defaultdict(lambda: {'revenue': 0, 'transactions': 0, 'customers': set()})

    for t in transactions:
        d = t['Date']
        daily[d]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily[d]['transactions'] += 1
        daily[d]['customers'].add(t['CustomerID'])

    return dict(sorted(daily.items()))


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily.items(), key=lambda x: x[1]['revenue'])
    return peak[0], peak[1]['revenue'], peak[1]['transactions']


def low_performing_products(transactions, threshold=10):
    prod = defaultdict(lambda: [0, 0])

    for t in transactions:
        prod[t['ProductName']][0] += t['Quantity']
        prod[t['ProductName']][1] += t['Quantity'] * t['UnitPrice']

    result = [(k, v[0], v[1]) for k, v in prod.items() if v[0] < threshold]
    result.sort(key=lambda x: x[1])
    return result


from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order = total_revenue / total_transactions if total_transactions else 0

    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_success = sum(1 for t in enriched_transactions if t['API_Match'])
    enrichment_rate = (enriched_success / len(enriched_transactions)) * 100

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Records Processed: {len(enriched_transactions)}\n")
        f.write("="*50 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-"*50 + "\n")
        for region, data in region_data.items():
            f.write(f"{region} | ₹{data['total_sales']:,.2f} | {data['percentage']}% | {data['transaction_count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-"*50 + "\n")
        for i, p in enumerate(top_products, 1):
            f.write(f"{i}. {p[0]} | Qty: {p[1]} | Revenue: ₹{p[2]:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-"*50 + "\n")
        for i, (cid, cdata) in enumerate(list(customers.items())[:5], 1):
            f.write(f"{i}. {cid} | Spent: ₹{cdata['total_spent']:,.2f} | Orders: {cdata['purchase_count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        for date, d in daily_trend.items():
            f.write(f"{date} | ₹{d['revenue']:,.2f} | {d['transactions']} | {len(d['customers'])}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-"*50 + "\n")
        f.write(f"Peak Sales Day: {peak_day[0]} | ₹{peak_day[1]:,.2f} | {peak_day[2]} transactions\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for p in low_products:
                f.write(f"- {p[0]} | Qty: {p[1]} | Revenue: ₹{p[2]:,.2f}\n")
        else:
            f.write("No low performing products\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Enriched: {enriched_success}/{len(enriched_transactions)}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")
