import pandas as pd
import psycopg2

df = pd.read_csv("data/online_retail_raw.csv")

df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df.dropna(subset=["CustomerID"])
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

df["LineTotal"] = df["Quantity"] * df["UnitPrice"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%m/%d/%Y %H:%M")
df["CustomerID"] = df["CustomerID"].astype(int)

df = df.rename(columns={
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country",
    "LineTotal": "line_total",
})

print(len(df))

conn = psycopg2.connect(host="localhost", dbname="retail", user="analyst", password="analyst")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS orders")
cur.execute("""
    CREATE TABLE orders (
        invoice_no TEXT,
        stock_code TEXT,
        description TEXT,
        quantity INTEGER,
        invoice_date TIMESTAMP,
        unit_price NUMERIC,
        customer_id INTEGER,
        country TEXT,
        line_total NUMERIC
    )
""")

cols = ["invoice_no", "stock_code", "description", "quantity", "invoice_date",
        "unit_price", "customer_id", "country", "line_total"]

for row in df[cols].itertuples(index=False, name=None):
    cur.execute(
        "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        row,
    )

conn.commit()
