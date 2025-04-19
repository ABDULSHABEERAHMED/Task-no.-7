import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
''')

cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('Apple', 10, 0.5),
        ('Banana', 20, 0.3),
        ('Orange', 15, 0.4),
        ('Mango', 5, 1.0),
        ('Banana', 10, 0.3),
        ('Apple', 5, 0.5),
    ]
    cursor.executemany('INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)', sample_data)
    conn.commit()

query = '''
    SELECT product, 
           SUM(quantity) as total_quantity, 
           SUM(quantity * price) as total_revenue
    FROM sales
    GROUP BY product
'''
df = pd.read_sql_query(query, conn)

print("Sales Summary:")
print(df)

plt.figure(figsize=(8, 5))
plt.bar(df['product'], df['total_revenue'], color='skyblue')
plt.xlabel('Product')
plt.ylabel('Total Revenue ($)')
plt.title('Revenue by Product')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

conn.close()
