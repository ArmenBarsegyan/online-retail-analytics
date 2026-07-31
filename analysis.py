import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(host="localhost", dbname="retail", user="analyst", password="analyst")

overview = pd.read_sql(open("sql/01_overview.sql").read(), conn)
print(overview)
overview.to_csv("data/result_01_overview.csv", index=False)

monthly = pd.read_sql(open("sql/02_monthly_revenue.sql").read(), conn)
monthly.to_csv("data/result_02_monthly_revenue.csv", index=False)

plt.figure(figsize=(8, 4))
plt.plot(monthly["month"].astype(str), monthly["revenue"], marker="o")
plt.title("Выручка по месяцам")
plt.ylabel("Выручка, £")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png")
plt.close()

top_products = pd.read_sql(open("sql/03_top_products.sql").read(), conn)
top_products.to_csv("data/result_03_top_products.csv", index=False)

plt.figure(figsize=(7, 4))
names = top_products["description"].str.slice(0, 28)
plt.barh(names[::-1], top_products["revenue"][::-1])
plt.title("Топ-10 товаров по выручке")
plt.xlabel("Выручка, £")
plt.tight_layout()
plt.savefig("charts/top_products.png")
plt.close()

by_country = pd.read_sql(open("sql/04_revenue_by_country.sql").read(), conn)
by_country.to_csv("data/result_04_revenue_by_country.csv", index=False)
print(by_country)

conn.close()
