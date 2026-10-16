const API_BASE_URL = (window.API_BASE_URL || "").replace(/\/$/, "");
const fallbackDishes = [
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
];
const grid = document.getElementById("dish-grid");
const search = document.getElementById("search");
const toast = document.getElementById("toast");
let dishes = [...fallbackDishes];
let category = "All";
const cart = new Map();
let toastTimer;
const money = value => new Intl.NumberFormat("en-IN", {style:"currency", currency:"INR", maximumFractionDigits:0}).format(value);
function notify(text) { toast.textContent=text; toast.classList.add("show"); clearTimeout(toastTimer); toastTimer=setTimeout(()=>toast.classList.remove("show"),3200); }
async function api(path, options={}) {
  let response;
  try { response = await fetch(`${API_BASE_URL}${path}`, {headers:{"Accept":"application/json", ...(options.body?{"Content-Type":"application/json"}:{})}, ...options}); }
  catch (error) { throw new Error("The website cannot reach its API. Check the frontend Apache proxy and backend service/security group."); }
  const contentType=response.headers.get("content-type")||"";
  const result=contentType.includes("application/json") ? await response.json() : {};
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
  return result;
}
async function loadMenu() {
  try { const data=await api("/api/menu"); if(Array.isArray(data.items)&&data.items.length){dishes=data.items;renderMenu();notify(`Full menu loaded · ${data.count} dishes from the kitchen`);} }
  catch(error) { console.error(error); renderMenu(); notify("Showing the saved menu preview. Live API connection needs attention."); }
}
function renderMenu() {
  const q=search.value.trim().toLowerCase();
  const visible=dishes.filter(d=>(category==="All"||d.category===category)&&(`${d.name} ${d.description} ${d.category}`).toLowerCase().includes(q));
  if(!visible.length){grid.innerHTML='<p class="empty-cart">No dishes found. Try another search.</p>';return;}
  grid.innerHTML=visible.map(d=>`<article class="dish-card"><div class="dish-photo"><img src="${d.image}" alt="${d.name}" loading="lazy" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80'"><span class="dish-tag">${d.category}</span></div><div class="dish-info"><div class="dish-title-row"><h3>${d.name}</h3><span class="dish-price">${money(d.price)}</span></div><p>${d.description}</p><div class="dish-footer"><span class="dish-rating">★ ${d.rating} · Chef's pick</span><button class="add-button" data-id="${d.id}">${cart.get(Number(d.id))?`Added (${cart.get(Number(d.id))})`:'+ Add'}</button></div></div></article>`).join("");
  grid.querySelectorAll(".add-button").forEach(button=>button.addEventListener("click",()=>{const id=Number(button.dataset.id);cart.set(id,Math.min(20,(cart.get(id)||0)+1));renderMenu();renderCart();notify("Added to your basket");}));
}
function renderCart(){
  const target=document.getElementById("cart-items"); if(!target)return;
  const lines=[...cart.entries()].map(([id,quantity])=>({dish:dishes.find(d=>Number(d.id)===id),quantity})).filter(x=>x.dish);
  const count=lines.reduce((sum,x)=>sum+x.quantity,0); const subtotal=lines.reduce((sum,x)=>sum+x.dish.price*x.quantity,0);
  document.getElementById("cart-count-label").textContent=`${count} item${count===1?'':'s'}`;document.getElementById("cart-subtotal").textContent=money(subtotal);document.getElementById("cart-tax").textContent=money(Math.round(subtotal*0.05));document.getElementById("cart-total").textContent=money(subtotal+Math.round(subtotal*0.05));
  target.innerHTML=lines.length?lines.map(({dish,quantity})=>`<div class="cart-line"><img src="${dish.image}" alt="" loading="lazy"><div class="cart-line-info"><strong>${dish.name}</strong><span>${money(dish.price)} each</span><div class="quantity-controls"><button type="button" data-action="minus" data-id="${dish.id}" aria-label="Remove one ${dish.name}">−</button><span>${quantity}</span><button type="button" data-action="plus" data-id="${dish.id}" aria-label="Add one ${dish.name}">+</button><button type="button" class="remove-line" data-action="remove" data-id="${dish.id}">Remove</button></div></div><strong>${money(dish.price*quantity)}</strong></div>`).join(""):'<p class="empty-cart">Your basket is waiting for something delicious. Add a dish from the menu above.</p>';
  target.querySelectorAll("button[data-action]").forEach(btn=>btn.addEventListener("click",()=>{const id=Number(btn.dataset.id),action=btn.dataset.action;if(action==='remove')cart.delete(id);else if(action==='minus'){const n=(cart.get(id)||0)-1;n>0?cart.set(id,n):cart.delete(id);}else cart.set(id,Math.min(20,(cart.get(id)||0)+1));renderCart();renderMenu();}));
  document.getElementById("place-order-button").disabled=!lines.length;
}
document.querySelectorAll(".filter").forEach(button=>button.addEventListener("click",()=>{document.querySelector(".filter.active")?.classList.remove("active");button.classList.add("active");category=button.dataset.category;renderMenu();}));
search.addEventListener("input",renderMenu);

const orderTypeSelect=document.getElementById("order-type");
const tableWrap=document.getElementById("table-number-wrap");
orderTypeSelect?.addEventListener("change",()=>{const dineIn=orderTypeSelect.value==="dine-in";tableWrap.hidden=!dineIn;document.getElementById("table-number").required=dineIn;});
const reservationDateInput=document.getElementById("reservation-date");
const reservationForm=document.getElementById("reservation-form");
const reservationStatus=document.getElementById("reservation-status");
function setMinReservationDate(){if(reservationDateInput){const d=new Date();d.setDate(d.getDate()+1);reservationDateInput.min=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,'0')+"-"+String(d.getDate()).padStart(2,'0');}}
setMinReservationDate();
reservationForm?.addEventListener("submit",async event=>{event.preventDefault();const button=reservationForm.querySelector('button[type="submit"]');const fields=new FormData(reservationForm);const payload={name:String(fields.get('name')||'').trim(),email:String(fields.get('email')||'').trim(),phone:String(fields.get('phone')||'').trim(),guests:Number(fields.get('guests')),date:String(fields.get('date')||''),time:String(fields.get('time')||''),notes:String(fields.get('notes')||'').trim()};reservationStatus.className='reservation-status';reservationStatus.textContent='Sending your reservation request…';button.disabled=true;try{const result=await api('/api/reservations',{method:'POST',body:JSON.stringify(payload)});reservationStatus.className='reservation-status success';reservationStatus.textContent=`Reservation request received · ${result.reference}`;const rr=document.getElementById('reservation-receipt');rr.hidden=false;rr.innerHTML=`<h3>Reservation request saved</h3><p><b>Reference:</b> ${result.reference}</p><p>${payload.date} at ${payload.time} · ${payload.guests} guest(s)</p><p><b>Status:</b> Awaiting restaurant confirmation</p><p>Keep this reference to follow up with the restaurant.</p>`;reservationForm.reset();setMinReservationDate();notify('Reservation request saved');}catch(error){reservationStatus.className='reservation-status error';reservationStatus.textContent=`Could not save request: ${error.message}`;}finally{button.disabled=false;}});

document.getElementById("checkout-form")?.addEventListener("submit",async event=>{event.preventDefault();const form=event.currentTarget,button=document.getElementById('place-order-button'),status=document.getElementById('order-status');const items=[...cart.entries()].map(([dish_id,quantity])=>({dish_id,quantity}));if(!items.length){status.className='reservation-status error';status.textContent='Add at least one dish first.';return;}const fields=new FormData(form);const payload={name:String(fields.get('name')||'').trim(),phone:String(fields.get('phone')||'').trim(),order_type:String(fields.get('order_type')||'pickup'),table_number:String(fields.get('table_number')||''),notes:String(fields.get('notes')||'').trim(),items};button.disabled=true;status.className='reservation-status';status.textContent='Sending your order request…';try{const result=await api('/api/orders',{method:'POST',body:JSON.stringify(payload)});status.className='reservation-status success';status.textContent=`Order request received · ${result.reference}`;const receipt=document.getElementById('order-receipt');receipt.hidden=false;receipt.innerHTML=`<h3>Order receipt</h3><p><b>Order:</b> ${result.reference}</p><p><b>Type:</b> ${result.order.order_type==='dine-in'?'Dine in · '+(result.order.table_number||'table pending'):'Takeaway / pickup'}</p><div>${result.order.items.map(i=>`<p>${i.quantity} × ${i.name} <span>${money(i.line_total)}</span></p>`).join('')}</div><hr><p>Subtotal <span>${money(result.order.subtotal)}</span></p><p>GST (5% demo rate) <span>${money(result.order.tax)}</span></p><h3>Total <span>${money(result.order.total)}</span></h3><p>Payment status: <b>Unpaid · pay at restaurant</b></p><p>Order status: <b>Received, awaiting restaurant acceptance</b></p>`;cart.clear();renderCart();renderMenu();form.reset();tableWrap.hidden=true;document.getElementById('table-number').required=false;notify(`Order request ${result.reference} saved`);}catch(error){status.className='reservation-status error';status.textContent=`Could not place order: ${error.message}`;}finally{button.disabled=false;}});

renderMenu();renderCart();loadMenu();


document.getElementById("contact-form")?.addEventListener("submit",async event=>{event.preventDefault();const form=event.currentTarget,button=document.getElementById("contact-submit"),status=document.getElementById("contact-status"),fields=new FormData(form);button.disabled=true;status.textContent="Sending your message…";try{const result=await api("/api/contact",{method:"POST",body:JSON.stringify({name:String(fields.get("name")||"").trim(),email:String(fields.get("email")||"").trim(),message:String(fields.get("message")||"").trim()})});status.className="contact-status success";status.textContent=result.message;form.reset();notify("Message saved");}catch(error){status.className="contact-status error";status.textContent=`Could not send message: ${error.message}`;}finally{button.disabled=false;}});
