/* Data */
const products = [
  { id: 'p1', name: 'Minimalist Backpack', price: 49.99, image: 'images/product1.jpg' },
  { id: 'p2', name: 'Wireless Headphones', price: 79.5, image: 'images/product2.jpg' },
  { id: 'p3', name: 'Ceramic Mug', price: 12.0, image: 'images/product3.jpg' },
  { id: 'p4', name: 'Mechanical Keyboard', price: 99.0, image: 'images/product4.jpg' },
  { id: 'p5', name: 'Classic T‑Shirt', price: 18.75, image: 'images/product5.jpg' },
  { id: 'p6', name: 'Running Shoes', price: 64.25, image: 'images/product6.jpg' },
];

/* Utilities */
const currency = new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' });
const byId = (id) => document.getElementById(id);

function getPlaceholderFor(productId) {
  return `https://picsum.photos/seed/${encodeURIComponent(productId)}/400/300`;
}

/* Cart State */
const CART_KEY = 'mini-ecommerce-cart-v1';
let cart = loadCart();

function loadCart() {
  try {
    const raw = localStorage.getItem(CART_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveCart() {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function getCartCount() {
  return Object.values(cart).reduce((sum, qty) => sum + qty, 0);
}

function getCartTotal() {
  return Object.entries(cart).reduce((sum, [productId, qty]) => {
    const product = products.find((p) => p.id === productId);
    return product ? sum + product.price * qty : sum;
  }, 0);
}

/* Cart operations */
function addToCart(productId, quantity = 1) {
  const nextQty = (cart[productId] ?? 0) + quantity;
  cart[productId] = nextQty;
  if (cart[productId] <= 0) delete cart[productId];
  saveCart();
  renderCart();
}

function setQuantity(productId, quantity) {
  if (quantity <= 0) delete cart[productId];
  else cart[productId] = quantity;
  saveCart();
  renderCart();
}

function removeFromCart(productId) {
  delete cart[productId];
  saveCart();
  renderCart();
}

/* Rendering */
function renderProducts() {
  const grid = byId('productsGrid');
  grid.innerHTML = '';

  products.forEach((product) => {
    const card = document.createElement('article');
    card.className = 'product-card';
    card.setAttribute('role', 'listitem');

    const img = document.createElement('img');
    img.className = 'product-media';
    img.alt = product.name;
    img.src = product.image;
    img.onerror = () => {
      img.onerror = null;
      img.src = getPlaceholderFor(product.id);
    };

    const body = document.createElement('div');
    body.className = 'product-body';

    const title = document.createElement('h3');
    title.className = 'product-title';
    title.textContent = product.name;

    const price = document.createElement('div');
    price.className = 'product-price';
    price.textContent = currency.format(product.price);

    const actions = document.createElement('div');
    actions.className = 'product-actions';

    const addBtn = document.createElement('button');
    addBtn.className = 'add-btn';
    addBtn.textContent = 'Add to Cart';
    addBtn.addEventListener('click', () => addToCart(product.id, 1));

    actions.appendChild(addBtn);
    body.appendChild(title);
    body.appendChild(price);
    body.appendChild(actions);

    card.appendChild(img);
    card.appendChild(body);

    grid.appendChild(card);
  });
}

function renderCart() {
  // Count and total
  const countEl = byId('cartCount');
  countEl.textContent = String(getCartCount());

  const totalEl = byId('cartTotal');
  totalEl.textContent = currency.format(getCartTotal());

  // Items
  const itemsEl = byId('cartItems');
  itemsEl.innerHTML = '';

  const entries = Object.entries(cart);
  if (entries.length === 0) {
    const empty = document.createElement('p');
    empty.style.color = '#64748b';
    empty.style.padding = '0.5rem 0.75rem';
    empty.textContent = 'Your cart is empty.';
    itemsEl.appendChild(empty);
    return;
  }

  entries.forEach(([productId, quantity]) => {
    const product = products.find((p) => p.id === productId);
    if (!product) return;

    const item = document.createElement('div');
    item.className = 'cart-item';
    item.setAttribute('role', 'listitem');

    const thumb = document.createElement('img');
    thumb.className = 'cart-thumb';
    thumb.alt = product.name;
    thumb.src = product.image;
    thumb.onerror = () => {
      thumb.onerror = null;
      thumb.src = getPlaceholderFor(product.id);
    };

    const meta = document.createElement('div');
    meta.className = 'cart-meta';

    const name = document.createElement('p');
    name.className = 'cart-name';
    name.textContent = product.name;

    const price = document.createElement('p');
    price.className = 'cart-price';
    price.textContent = currency.format(product.price);

    const qtyControls = document.createElement('div');
    qtyControls.className = 'qty-controls';

    const minus = document.createElement('button');
    minus.className = 'qty-btn';
    minus.setAttribute('aria-label', `Decrease quantity for ${product.name}`);
    minus.textContent = '−';
    minus.addEventListener('click', () => addToCart(product.id, -1));

    const qtyVal = document.createElement('div');
    qtyVal.className = 'qty-val';
    qtyVal.textContent = String(quantity);

    const plus = document.createElement('button');
    plus.className = 'qty-btn';
    plus.setAttribute('aria-label', `Increase quantity for ${product.name}`);
    plus.textContent = '+';
    plus.addEventListener('click', () => addToCart(product.id, 1));

    qtyControls.appendChild(minus);
    qtyControls.appendChild(qtyVal);
    qtyControls.appendChild(plus);

    const remove = document.createElement('button');
    remove.className = 'remove-btn';
    remove.textContent = 'Remove';
    remove.addEventListener('click', () => removeFromCart(product.id));

    meta.appendChild(name);
    meta.appendChild(price);
    meta.appendChild(qtyControls);

    item.appendChild(thumb);
    item.appendChild(meta);
    item.appendChild(remove);

    itemsEl.appendChild(item);
  });
}

/* Cart drawer toggle */
function openCart() {
  const drawer = byId('cartDrawer');
  const backdrop = byId('backdrop');
  drawer.hidden = false;
  backdrop.hidden = false;
  byId('cartToggle').setAttribute('aria-expanded', 'true');
}
function closeCart() {
  const drawer = byId('cartDrawer');
  const backdrop = byId('backdrop');
  drawer.hidden = true;
  backdrop.hidden = true;
  byId('cartToggle').setAttribute('aria-expanded', 'false');
}

function setupCartToggle() {
  const toggle = byId('cartToggle');
  const closeBtn = byId('cartClose');
  const backdrop = byId('backdrop');

  toggle.addEventListener('click', () => openCart());
  closeBtn.addEventListener('click', () => closeCart());
  backdrop.addEventListener('click', () => closeCart());

  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') closeCart();
  });
}

/* Init */
window.addEventListener('DOMContentLoaded', () => {
  renderProducts();
  renderCart();
  setupCartToggle();

  // Demo checkout
  byId('checkoutBtn').addEventListener('click', () => {
    alert('This is a front‑end demo. Implement real checkout on the server.');
  });
});