from flask import Flask, jsonify, request, Response
from pathlib import Path
from datetime import datetime, timezone, date
import sqlite3, re, secrets, json, os, hmac

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "saffron_smoke.db"
app = Flask(__name__)
MENU = [
  {
    "id": 1,
    "name": "Charred Paneer Tikka",
    "category": "Small plates",
    "price": 280,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?auto=format&fit=crop&w=1000&q=90",
    "description": "Smoky paneer, house spices, mint chutney and a squeeze of lime."
  },
  {
    "id": 2,
    "name": "Crispy Lotus Stem",
    "category": "Small plates",
    "price": 260,
    "rating": "4.7",
    "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=90",
    "description": "Crisp lotus stem tossed in a sweet, tangy chilli glaze."
  },
  {
    "id": 3,
    "name": "Tandoori Broccoli",
    "category": "Small plates",
    "price": 290,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=90",
    "description": "Charred broccoli, hung curd marinade and toasted almonds."
  },
  {
    "id": 4,
    "name": "Pepper Garlic Prawns",
    "category": "Small plates",
    "price": 420,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=1000&q=90",
    "description": "Juicy prawns, cracked pepper, garlic butter and lime."
  },
  {
    "id": 5,
    "name": "Burrata & Heirloom Tomato",
    "category": "Small plates",
    "price": 390,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=90",
    "description": "Creamy burrata, ripe tomatoes, basil oil and sourdough."
  },
  {
    "id": 6,
    "name": "Saffron Butter Chicken",
    "category": "Mains",
    "price": 420,
    "rating": "5.0",
    "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=1000&q=90",
    "description": "A rich, silky tomato gravy finished with cream and fragrant spices."
  },
  {
    "id": 7,
    "name": "Smoked Dal Makhani",
    "category": "Mains",
    "price": 340,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1000&q=90",
    "description": "Slow-cooked black lentils, a hint of smoke and cultured butter."
  },
  {
    "id": 8,
    "name": "Paneer Lababdar",
    "category": "Mains",
    "price": 360,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=1000&q=90",
    "description": "Soft paneer in a velvety tomato-cashew gravy."
  },
  {
    "id": 9,
    "name": "Coastal Fish Curry",
    "category": "Mains",
    "price": 480,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1000&q=90",
    "description": "Market fish simmered with coconut, tamarind and coastal spices."
  },
  {
    "id": 10,
    "name": "Fire-Roasted Pizza",
    "category": "Mains",
    "price": 390,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?auto=format&fit=crop&w=1000&q=90",
    "description": "Crisp edges, slow-roasted tomato, basil and creamy mozzarella."
  },
  {
    "id": 11,
    "name": "Truffle Mushroom Pasta",
    "category": "Mains",
    "price": 360,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=1000&q=90",
    "description": "Silky pasta, golden mushrooms, parmesan and a hint of truffle."
  },
  {
    "id": 12,
    "name": "Charcoal Chicken Biryani",
    "category": "Mains",
    "price": 390,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=1000&q=90",
    "description": "Fragrant basmati, slow-cooked chicken, herbs and warming spices."
  },
  {
    "id": 13,
    "name": "Garden Herb Rice Bowl",
    "category": "Mains",
    "price": 320,
    "rating": "4.7",
    "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=90",
    "description": "Seasonal vegetables, herbed rice, crunchy seeds and lemon dressing."
  },
  {
    "id": 14,
    "name": "Saffron Pulao",
    "category": "Mains",
    "price": 250,
    "rating": "4.7",
    "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1000&q=90",
    "description": "Basmati rice perfumed with saffron, fried onions and whole spices."
  },
  {
    "id": 15,
    "name": "Garlic Naan",
    "category": "Mains",
    "price": 70,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1000&q=90",
    "description": "Tandoor-baked naan brushed with garlic butter and coriander."
  },
  {
    "id": 16,
    "name": "Chocolate Lava Cake",
    "category": "Desserts",
    "price": 240,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=1000&q=90",
    "description": "Warm chocolate cake with a molten centre and vanilla cream."
  },
  {
    "id": 17,
    "name": "Berry Cheesecake",
    "category": "Desserts",
    "price": 260,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=1000&q=90",
    "description": "Creamy cheesecake, berry compote and a buttery biscuit base."
  },
  {
    "id": 18,
    "name": "Gulab Jamun Cheesecake",
    "category": "Desserts",
    "price": 280,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=1000&q=90",
    "description": "A playful fusion of cardamom, cream cheese and warm syrup."
  },
  {
    "id": 19,
    "name": "Pistachio Kulfi",
    "category": "Desserts",
    "price": 190,
    "rating": "4.7",
    "image": "https://images.unsplash.com/photo-1501446529957-6226bd447c46?auto=format&fit=crop&w=1000&q=90",
    "description": "Slow-set kulfi with pistachio, cardamom and saffron."
  },
  {
    "id": 20,
    "name": "Mango Mint Cooler",
    "category": "Drinks",
    "price": 150,
    "rating": "4.7",
    "image": "https://images.unsplash.com/photo-1513558161293-cd2a0e3e3c1c?auto=format&fit=crop&w=1000&q=90",
    "description": "Ripe mango, fresh mint and sparkling citrus over ice."
  },
  {
    "id": 21,
    "name": "Cold Brew Tonic",
    "category": "Drinks",
    "price": 170,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1000&q=90",
    "description": "Slow-steeped coffee, bright citrus and a crisp tonic finish."
  },
  {
    "id": 22,
    "name": "Rose & Lime Spritz",
    "category": "Drinks",
    "price": 160,
    "rating": "4.8",
    "image": "https://images.unsplash.com/photo-1513558161293-cd2a0e3e3c1c?auto=format&fit=crop&w=1000&q=90",
    "description": "Rose syrup, fresh lime, mint and sparkling water."
  },
  {
    "id": 23,
    "name": "Masala Chai",
    "category": "Drinks",
    "price": 90,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?auto=format&fit=crop&w=1000&q=90",
    "description": "Freshly brewed tea simmered with ginger and warming spices."
  },
  {
    "id": 24,
    "name": "Filter Coffee",
    "category": "Drinks",
    "price": 100,
    "rating": "4.9",
    "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1000&q=90",
    "description": "South Indian filter coffee, rich and aromatic."
  }
]

def get_db():
    db = sqlite3.connect(DB_PATH, timeout=15)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS cart_events (id INTEGER PRIMARY KEY AUTOINCREMENT,dish_id INTEGER NOT NULL,dish_name TEXT NOT NULL,quantity INTEGER NOT NULL,created_at TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY AUTOINCREMENT,reference TEXT NOT NULL UNIQUE,name TEXT NOT NULL,email TEXT NOT NULL,phone TEXT NOT NULL,guests INTEGER NOT NULL,reservation_date TEXT NOT NULL,reservation_time TEXT NOT NULL,notes TEXT NOT NULL DEFAULT '',status TEXT NOT NULL DEFAULT 'requested',created_at TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT,reference TEXT NOT NULL UNIQUE,name TEXT NOT NULL,phone TEXT NOT NULL,order_type TEXT NOT NULL,items_json TEXT NOT NULL,subtotal INTEGER NOT NULL,notes TEXT NOT NULL DEFAULT '',status TEXT NOT NULL DEFAULT 'received',created_at TEXT NOT NULL)")
        # Safe additive migrations for existing databases.
        order_cols={r['name'] for r in db.execute('PRAGMA table_info(orders)').fetchall()}
        for col,definition in [("tax","INTEGER NOT NULL DEFAULT 0"),("total","INTEGER NOT NULL DEFAULT 0"),("table_number","TEXT NOT NULL DEFAULT ''"),("payment_status","TEXT NOT NULL DEFAULT 'unpaid'")]:
            if col not in order_cols: db.execute(f'ALTER TABLE orders ADD COLUMN {col} {definition}')
        res_cols={r['name'] for r in db.execute('PRAGMA table_info(reservations)').fetchall()}
        if 'table_number' not in res_cols: db.execute("ALTER TABLE reservations ADD COLUMN table_number TEXT NOT NULL DEFAULT ''")
        db.execute("CREATE TABLE IF NOT EXISTS inquiries (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL,message TEXT NOT NULL,created_at TEXT NOT NULL)")

@app.after_request
def cors(response):
    # The frontend uses same-origin Apache proxying; this is retained for direct API testing.
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.get('/')
def root():
    return jsonify({'service':'Saffron & Smoke API','status':'ok','docs':'/docs','health':'/api/health'})

@app.get('/api/health')
def health():
    return jsonify({'status':'ok','service':'saffron-smoke-backend','menu_items':len(MENU)})

@app.get('/api/menu')
def menu():
    return jsonify({'items':MENU,'count':len(MENU),'currency':'INR'})

@app.route('/api/cart-events', methods=['GET','POST','OPTIONS'])
def cart_events():
    if request.method == 'OPTIONS': return ('',204)
    if request.method == 'GET':
        with get_db() as db:
            rows=db.execute('SELECT id,dish_id,dish_name,quantity,created_at FROM cart_events ORDER BY id DESC LIMIT 100').fetchall()
        return jsonify({'events':[dict(x) for x in rows],'count':len(rows)})
    data=request.get_json(silent=True) or {}
    try: dish_id=int(data.get('dish_id',0)); quantity=int(data.get('quantity',1))
    except (TypeError,ValueError): return jsonify({'error':'dish_id and quantity must be integers'}),400
    dish=next((x for x in MENU if x['id']==dish_id),None)
    if not dish: return jsonify({'error':'Dish not found'}),404
    if not 1 <= quantity <= 20: return jsonify({'error':'quantity must be between 1 and 20'}),400
    created=datetime.now(timezone.utc).isoformat()
    with get_db() as db:
        cur=db.execute('INSERT INTO cart_events(dish_id,dish_name,quantity,created_at) VALUES(?,?,?,?)',(dish_id,dish['name'],quantity,created))
    return jsonify({'message':'Cart action saved','event_id':cur.lastrowid,'dish':dish['name'],'quantity':quantity}),201

@app.route('/api/reservations', methods=['POST','OPTIONS'])
def create_reservation():
    if request.method == 'OPTIONS': return ('',204)
    data=request.get_json(silent=True) or {}
    name=str(data.get('name','')).strip(); email=str(data.get('email','')).strip().lower(); phone=str(data.get('phone','')).strip()
    notes=str(data.get('notes','')).strip(); res_date=str(data.get('date','')).strip(); res_time=str(data.get('time','')).strip()
    try: guests=int(data.get('guests',0))
    except (ValueError,TypeError): return jsonify({'error':'Guests must be a number.'}),400
    if len(name)<2 or len(name)>100: return jsonify({'error':'Enter a name between 2 and 100 characters.'}),400
    if len(email)>160 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email): return jsonify({'error':'Enter a valid email address.'}),400
    if len(phone)<7 or len(phone)>20 or not re.fullmatch(r'[+()\d\s.-]{7,20}',phone): return jsonify({'error':'Enter a valid phone number.'}),400
    if not 1 <= guests <= 12: return jsonify({'error':'Reservations are available for 1 to 12 guests online.'}),400
    if len(notes)>500: return jsonify({'error':'Special requests must be 500 characters or fewer.'}),400
    try:
        chosen_date=date.fromisoformat(res_date); chosen_time=datetime.strptime(res_time,'%H:%M').time()
    except ValueError: return jsonify({'error':'Choose a valid date and time.'}),400
    if chosen_date <= date.today(): return jsonify({'error':'Please choose a future date.'}),400
    if chosen_time.hour < 11 or chosen_time.hour > 22 or (chosen_time.hour == 22 and chosen_time.minute != 0) or chosen_time.minute not in (0,30):
        return jsonify({'error':'Reservations are available from 11:00 to 22:00, on the hour or half-hour.'}),400
    reference='SS-'+secrets.token_hex(3).upper(); created=datetime.now(timezone.utc).isoformat()
    try:
        with get_db() as db:
            db.execute('INSERT INTO reservations(reference,name,email,phone,guests,reservation_date,reservation_time,notes,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(reference,name,email,phone,guests,res_date,res_time,notes,created))
    except sqlite3.Error:
        app.logger.exception('Could not save reservation')
        return jsonify({'error':'We could not save your reservation right now. Please try again.'}),500
    return jsonify({'message':'Reservation request saved. Staff must confirm the table.','reference':reference,'reservation':{'name':name,'date':res_date,'time':res_time,'guests':guests,'status':'requested'}}),201

@app.get('/api/reservations/availability')
def reservation_availability():
    res_date=request.args.get('date','').strip()
    try:
        if date.fromisoformat(res_date) <= date.today(): raise ValueError()
    except ValueError: return jsonify({'error':'Provide a future date in YYYY-MM-DD format.'}),400
    with get_db() as db:
        rows=db.execute("SELECT reservation_time,COUNT(*) AS requests FROM reservations WHERE reservation_date=? AND status='requested' GROUP BY reservation_time ORDER BY reservation_time",(res_date,)).fetchall()
    return jsonify({'date':res_date,'requests_by_time':[dict(r) for r in rows],'note':'Request counts only; staff must confirm actual table availability.'})

@app.route('/api/orders', methods=['POST','OPTIONS'])
def create_order():
    if request.method == 'OPTIONS': return ('',204)
    data=request.get_json(silent=True) or {}
    name=str(data.get('name','')).strip(); phone=str(data.get('phone','')).strip(); order_type=str(data.get('order_type','pickup')).strip(); notes=str(data.get('notes','')).strip(); table_number=str(data.get('table_number','')).strip()
    raw_items=data.get('items')
    if len(name)<2 or len(name)>100: return jsonify({'error':'Enter a name between 2 and 100 characters.'}),400
    if len(phone)<7 or len(phone)>20 or not re.fullmatch(r'[+()\d\s.-]{7,20}',phone): return jsonify({'error':'Enter a valid phone number.'}),400
    if order_type not in ('pickup','dine-in'): return jsonify({'error':'Choose pickup or dine-in.'}),400
    if order_type == 'dine-in' and table_number not in ('T1','T2','T3','T4','T5','T6'): return jsonify({'error':'Choose a table for dine-in.'}),400
    if order_type == 'pickup': table_number = ''
    if len(notes)>500: return jsonify({'error':'Notes must be 500 characters or fewer.'}),400
    if not isinstance(raw_items,list) or not raw_items or len(raw_items)>30: return jsonify({'error':'Add between 1 and 30 cart lines.'}),400
    validated=[]; subtotal=0
    for row in raw_items:
        try: dish_id=int(row.get('dish_id',0)); qty=int(row.get('quantity',0))
        except (AttributeError,TypeError,ValueError): return jsonify({'error':'Each cart line needs a valid dish_id and quantity.'}),400
        dish=next((x for x in MENU if x['id']==dish_id),None)
        if not dish: return jsonify({'error':f'Unknown menu item {dish_id}.'}),400
        if not 1 <= qty <= 20: return jsonify({'error':'Each quantity must be between 1 and 20.'}),400
        line={'dish_id':dish_id,'name':dish['name'],'quantity':qty,'unit_price':dish['price'],'line_total':dish['price']*qty}
        subtotal += line['line_total']; validated.append(line)
    tax=round(subtotal*0.05); total=subtotal+tax; reference='ORD-'+secrets.token_hex(3).upper(); created=datetime.now(timezone.utc).isoformat()
    try:
        with get_db() as db:
            db.execute('INSERT INTO orders(reference,name,phone,order_type,items_json,subtotal,notes,created_at,tax,total,table_number,payment_status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(reference,name,phone,order_type,json.dumps(validated),subtotal,notes,created,tax,total,table_number,'unpaid'))
    except sqlite3.Error:
        app.logger.exception('Could not save order')
        return jsonify({'error':'We could not save your order request. Please try again.'}),500
    return jsonify({'message':'Order request received. This demo does not process payment; the restaurant must confirm availability.','reference':reference,'order':{'order_type':order_type,'table_number':table_number,'items':validated,'subtotal':subtotal,'tax':tax,'total':total,'payment_status':'unpaid','status':'received'}}),201

@app.get('/api/orders/<reference>')
def order_status(reference):
    with get_db() as db:
        row=db.execute('SELECT reference,name,phone,order_type,table_number,items_json,subtotal,tax,total,payment_status,status,notes,created_at FROM orders WHERE reference=?',(reference.upper(),)).fetchone()
    if not row: return jsonify({'error':'Order reference not found.'}),404
    result=dict(row); result['items']=json.loads(result.pop('items_json'))
    return jsonify(result)

@app.route('/api/contact', methods=['POST','OPTIONS'])
def contact():
    if request.method == 'OPTIONS': return ('',204)
    data=request.get_json(silent=True) or {}
    name=str(data.get('name','')).strip(); email=str(data.get('email','')).strip().lower(); message=str(data.get('message','')).strip()
    if len(name)<2 or len(name)>100: return jsonify({'error':'Enter your name.'}),400
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email): return jsonify({'error':'Enter a valid email address.'}),400
    if len(message)<5 or len(message)>2000: return jsonify({'error':'Message must be between 5 and 2000 characters.'}),400
    with get_db() as db:
        cur=db.execute('INSERT INTO inquiries(name,email,message,created_at) VALUES(?,?,?,?)',(name,email,message,datetime.now(timezone.utc).isoformat()))
    return jsonify({'message':'Your message has been saved. The restaurant team can follow up.','inquiry_id':cur.lastrowid}),201

def admin_authorized():
    expected=os.environ.get('ADMIN_TOKEN','')
    supplied=request.headers.get('Authorization','').removeprefix('Bearer ').strip()
    return bool(expected) and hmac.compare_digest(supplied, expected)

@app.get('/api/admin/summary')
def admin_summary():
    if not admin_authorized(): return jsonify({'error':'Admin authentication required.'}),401
    with get_db() as db:
        orders=[dict(r) for r in db.execute('SELECT reference,name,phone,order_type,table_number,subtotal,tax,total,payment_status,status,created_at,items_json FROM orders ORDER BY id DESC LIMIT 200').fetchall()]
        reservations=[dict(r) for r in db.execute('SELECT reference,name,email,phone,guests,reservation_date,reservation_time,notes,status,created_at FROM reservations ORDER BY id DESC LIMIT 200').fetchall()]
        inquiries=[dict(r) for r in db.execute('SELECT id,name,email,message,created_at FROM inquiries ORDER BY id DESC LIMIT 100').fetchall()]
    for order in orders: order['items']=json.loads(order.pop('items_json'))
    return jsonify({'orders':orders,'reservations':reservations,'inquiries':inquiries,'counts':{'orders':len(orders),'reservations':len(reservations),'inquiries':len(inquiries)}})

@app.post('/api/admin/orders/<reference>/status')
def admin_order_status(reference):
    if not admin_authorized(): return jsonify({'error':'Admin authentication required.'}),401
    data=request.get_json(silent=True) or {}; status=str(data.get('status','')).strip()
    if status not in ('received','accepted','preparing','ready','completed','cancelled'): return jsonify({'error':'Invalid order status.'}),400
    with get_db() as db:
        cur=db.execute('UPDATE orders SET status=? WHERE reference=?',(status,reference.upper()))
    if not cur.rowcount: return jsonify({'error':'Order not found.'}),404
    return jsonify({'message':'Order status updated.','reference':reference.upper(),'status':status})

@app.post('/api/admin/reservations/<reference>/status')
def admin_reservation_status(reference):
    if not admin_authorized(): return jsonify({'error':'Admin authentication required.'}),401
    data=request.get_json(silent=True) or {}; status=str(data.get('status','')).strip()
    if status not in ('requested','confirmed','rejected','cancelled','completed'): return jsonify({'error':'Invalid reservation status.'}),400
    with get_db() as db:
        cur=db.execute('UPDATE reservations SET status=? WHERE reference=?',(status,reference.upper()))
    if not cur.rowcount: return jsonify({'error':'Reservation not found.'}),404
    return jsonify({'message':'Reservation status updated.','reference':reference.upper(),'status':status})

OPENAPI = {
 "openapi":"3.0.3","info":{"title":"Saffron & Smoke API","version":"2.0.0","description":"Menu, reservation requests, order requests, and contact inquiries. Demo orders do not process payments."},
 "servers":[{"url":"/","description":"Current backend server"}],
 "paths":{
  "/":{"get":{"summary":"API overview","responses":{"200":{"description":"Service overview"}}}},
  "/api/health":{"get":{"summary":"Health check","responses":{"200":{"description":"Backend is running"}}}},
  "/api/menu":{"get":{"summary":"List the full menu","responses":{"200":{"description":"Menu items, count and currency"}}}},
  "/api/cart-events":{"get":{"summary":"List recent demo cart events","responses":{"200":{"description":"Recent events"}}},"post":{"summary":"Record add-to-basket event","responses":{"201":{"description":"Event recorded"},"400":{"description":"Invalid payload"}}}},
  "/api/reservations":{"post":{"summary":"Request a table reservation","description":"Stores a reservation request; it is not automatically confirmed.","requestBody":{"required":True,"content":{"application/json":{"schema":{"type":"object","required":["name","email","phone","guests","date","time"],"properties":{"name":{"type":"string"},"email":{"type":"string","format":"email"},"phone":{"type":"string"},"guests":{"type":"integer","minimum":1,"maximum":12},"date":{"type":"string","format":"date"},"time":{"type":"string","example":"19:00"},"notes":{"type":"string","maxLength":500}}}}}},"responses":{"201":{"description":"Request saved"},"400":{"description":"Validation error"}}}},
  "/api/reservations/availability":{"get":{"summary":"Counts of reservation requests for a future date","parameters":[{"name":"date","in":"query","required":True,"schema":{"type":"string","format":"date"}}],"responses":{"200":{"description":"Request counts (not a guarantee of availability)"}}}},
  "/api/orders":{"post":{"summary":"Submit an order request","description":"Server-calculates prices and stores the order. No payment is processed.","requestBody":{"required":True,"content":{"application/json":{"schema":{"type":"object","required":["name","phone","items"],"properties":{"name":{"type":"string"},"phone":{"type":"string"},"order_type":{"type":"string","enum":["pickup","dine-in"]},"items":{"type":"array","items":{"type":"object","required":["dish_id","quantity"],"properties":{"dish_id":{"type":"integer"},"quantity":{"type":"integer"}}}},"notes":{"type":"string"}}}}}},"responses":{"201":{"description":"Order request received"},"400":{"description":"Validation error"}}}},
  "/api/orders/{reference}":{"get":{"summary":"Look up order status by reference","parameters":[{"name":"reference","in":"path","required":True,"schema":{"type":"string"}}],"responses":{"200":{"description":"Order status and items"},"404":{"description":"Reference not found"}}}},
  "/api/contact":{"post":{"summary":"Send a contact inquiry","responses":{"201":{"description":"Inquiry saved"},"400":{"description":"Validation error"}}}}
 }
}

@app.get('/openapi.json')
def openapi(): return jsonify(OPENAPI)

@app.route('/docs')
@app.route('/docs/')
def docs():
    page="<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Saffron & Smoke API Docs</title><link rel='stylesheet' href='https://unpkg.com/swagger-ui-dist@5/swagger-ui.css'></head><body><div id='swagger-ui'></div><script src='https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js'></script><script>window.onload=()=>SwaggerUIBundle({url:'/openapi.json',dom_id:'#swagger-ui',deepLinking:true});</script></body></html>"
    return Response(page,mimetype='text/html')

init_db()
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000)
