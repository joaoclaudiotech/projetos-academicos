from pathlib import Path
from datetime import date, timedelta
import random
import duckdb
random.seed(11)
DB=Path(__file__).with_name('semana11.duckdb')
if DB.exists(): DB.unlink()
con=duckdb.connect(str(DB))
con.execute('create schema raw')
con.execute('create table raw.customers(customer_id integer, customer_name varchar, state varchar)')
con.execute('create table raw.products(product_id integer, product_name varchar, category varchar)')
con.execute('create table raw.orders(order_id integer, customer_id integer, product_id integer, total double, order_date date, status varchar)')
customers=[(i,f'Cliente {i:03d}', random.choice(['PI','CE','MA','PE','BA'])) for i in range(1,31)]
products=[(i,f'Produto {i:02d}', random.choice(['Casa','Livros','Eletronicos','Esporte'])) for i in range(1,13)]
con.executemany('insert into raw.customers values (?,?,?)', customers)
con.executemany('insert into raw.products values (?,?,?)', products)
statuses=[' Paid ','PAID','paid',' Pending ','PENDING','cancelled',' CANCELLED ','refunded']
start=date(2026,9,1)
rows=[]
for i in range(1,241):
    oid=None if i in (37,149) else i
    cid=random.randint(1,30); pid=random.randint(1,12)
    total=round(random.uniform(25,1800),2)
    day=start+timedelta(days=random.randint(0,29))
    status=random.choice(statuses)
    rows.append((oid,cid,pid,total,day,status))
con.executemany('insert into raw.orders values (?,?,?,?,?,?)', rows)
con.close()
print('BANCO PREPARADO ✅')
print('Arquivo:', DB.name)
print('raw.orders: 240 linhas (inclui 2 order_id nulos e status propositalmente despadronizados)')
print('raw.customers: 30 | raw.products: 12')
