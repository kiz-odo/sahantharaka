// E-commerce Website JavaScript

// Sample product data
const products = [
    {
        id: 1,
        name: "Wireless Bluetooth Headphones",
        price: 89.99,
        category: "electronics",
        rating: 4.5,
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
        description: "High-quality wireless headphones with noise cancellation and long battery life."
    },
    {
        id: 2,
        name: "Smart Fitness Watch",
        price: 199.99,
        category: "electronics",
        rating: 4.3,
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop",
        description: "Advanced fitness tracking with heart rate monitor and GPS."
    },
    {
        id: 3,
        name: "Premium Cotton T-Shirt",
        price: 29.99,
        category: "clothing",
        rating: 4.7,
        image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop",
        description: "Comfortable and stylish cotton t-shirt available in multiple colors."
    },
    {
        id: 4,
        name: "Denim Jeans",
        price: 79.99,
        category: "clothing",
        rating: 4.4,
        image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop",
        description: "Classic denim jeans with perfect fit and durability."
    },
    {
        id: 5,
        name: "Modern Coffee Table",
        price: 299.99,
        category: "home",
        rating: 4.6,
        image: "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?w=400&h=300&fit=crop",
        description: "Elegant coffee table perfect for modern living rooms."
    },
    {
        id: 6,
        name: "Garden Plant Pots Set",
        price: 49.99,
        category: "home",
        rating: 4.2,
        image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop",
        description: "Beautiful ceramic plant pots for indoor and outdoor gardening."
    },
    {
        id: 7,
        name: "Professional Basketball",
        price: 39.99,
        category: "sports",
        rating: 4.8,
        image: "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=300&fit=crop",
        description: "Official size basketball perfect for indoor and outdoor play."
    },
    {
        id: 8,
        name: "Yoga Mat Premium",
        price: 59.99,
        category: "sports",
        rating: 4.5,
        image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop",
        description: "Non-slip yoga mat with carrying strap for all types of yoga."
    },
    {
        id: 9,
        name: "Laptop Stand",
        price: 45.99,
        category: "electronics",
        rating: 4.1,
        image: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop",
        description: "Adjustable laptop stand for better ergonomics and cooling."
    },
    {
        id: 10,
        name: "Wireless Mouse",
        price: 34.99,
        category: "electronics",
        rating: 4.4,
        image: "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop",
        description: "Ergonomic wireless mouse with precision tracking."
    },
    {
        id: 11,
        name: "Casual Blazer",
        price: 129.99,
        category: "clothing",
        rating: 4.6,
        image: "https://images.unsplash.com/photo-1593030761757-71cae45ad0dd?w=400&h=300&fit=crop",
        description: "Versatile blazer perfect for both casual and formal occasions."
    },
    {
        id: 12,
        name: "Running Shoes",
        price: 119.99,
        category: "sports",
        rating: 4.7,
        image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop",
        description: "Lightweight running shoes with excellent cushioning and support."
    }
];

// Global variables
let cart = [];
let currentUser = null;
let filteredProducts = [...products];
let currentPage = 1;
const productsPerPage = 8;

// DOM elements
const productsGrid = document.getElementById('productsGrid');
const cartModal = document.getElementById('cartModal');
const cartIcon = document.getElementById('cartIcon');
const closeCart = document.getElementById('closeCart');
const cartItems = document.getElementById('cartItems');
const cartCount = document.getElementById('cartCount');
const cartTotal = document.getElementById('cartTotal');
const clearCart = document.getElementById('clearCart');
const checkoutBtn = document.getElementById('checkoutBtn');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const sortSelect = document.getElementById('sortSelect');
const priceRange = document.getElementById('priceRange');
const priceValue = document.getElementById('priceValue');
const loadMoreBtn = document.getElementById('loadMoreBtn');
const quickViewModal = document.getElementById('quickViewModal');
const closeQuickView = document.getElementById('closeQuickView');
const quickViewBody = document.getElementById('quickViewBody');
const userModal = document.getElementById('userModal');
const userBtn = document.getElementById('userBtn');
const closeUser = document.getElementById('closeUser');
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const userInfo = document.getElementById('userInfo');
const userName = document.getElementById('userName');
const logoutBtn = document.getElementById('logoutBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');
const contactForm = document.getElementById('contactForm');
const newsletterForm = document.getElementById('newsletterForm');

// Initialize the website
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
    setupEventListeners();
    loadProducts();
    loadCartFromStorage();
    updateCartDisplay();
});

// Initialize website
function initializeWebsite() {
    // Load user from localStorage
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateUserDisplay();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Cart events
    cartIcon.addEventListener('click', openCart);
    closeCart.addEventListener('click', closeCartModal);
    clearCart.addEventListener('click', clearCartItems);
    checkoutBtn.addEventListener('click', checkout);
    
    // Search and filter events
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') performSearch();
    });
    sortSelect.addEventListener('change', applyFilters);
    priceRange.addEventListener('input', function() {
        priceValue.textContent = `$${this.value}`;
        applyFilters();
    });
    
    // Load more products
    loadMoreBtn.addEventListener('click', loadMoreProducts);
    
    // Quick view events
    closeQuickView.addEventListener('click', closeQuickViewModal);
    
    // User modal events
    userBtn.addEventListener('click', openUserModal);
    closeUser.addEventListener('click', closeUserModal);
    loginBtn.addEventListener('click', showLoginForm);
    registerBtn.addEventListener('click', showRegisterForm);
    logoutBtn.addEventListener('click', logout);
    
    // Form submissions
    contactForm.addEventListener('submit', handleContactSubmit);
    newsletterForm.addEventListener('click', handleNewsletterSubmit);
    
    // Category filtering
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            filterByCategory(category);
        });
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === cartModal) closeCartModal();
        if (e.target === quickViewModal) closeQuickViewModal();
        if (e.target === userModal) closeUserModal();
    });
}

// Load products
function loadProducts() {
    const startIndex = 0;
    const endIndex = productsPerPage;
    const productsToShow = filteredProducts.slice(startIndex, endIndex);
    
    displayProducts(productsToShow);
    updateLoadMoreButton();
}

// Display products
function displayProducts(productsToShow) {
    if (currentPage === 1) {
        productsGrid.innerHTML = '';
    }
    
    productsToShow.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
}

// Create product card
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
    
    card.innerHTML = `
        <img src="${product.image}" alt="${product.name}" class="product-image">
        <div class="product-info">
            <h3 class="product-title">${product.name}</h3>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <div class="product-rating">
                <span class="stars">${stars}</span>
                <span>${product.rating}</span>
            </div>
            <div class="product-actions">
                <button class="add-to-cart" onclick="addToCart(${product.id})">Add to Cart</button>
                <button class="quick-view" onclick="showQuickView(${product.id})">Quick View</button>
            </div>
        </div>
    `;
    
    return card;
}

// Load more products
function loadMoreProducts() {
    currentPage++;
    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = startIndex + productsPerPage;
    const productsToShow = filteredProducts.slice(startIndex, endIndex);
    
    displayProducts(productsToShow);
    updateLoadMoreButton();
}

// Update load more button
function updateLoadMoreButton() {
    const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
    if (currentPage >= totalPages) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'block';
    }
}

// Search functionality
function performSearch() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        filteredProducts = [...products];
    } else {
        filteredProducts = products.filter(product => 
            product.name.toLowerCase().includes(searchTerm) ||
            product.description.toLowerCase().includes(searchTerm) ||
            product.category.toLowerCase().includes(searchTerm)
        );
    }
    
    currentPage = 1;
    loadProducts();
    showToast(`Found ${filteredProducts.length} products`);
}

// Apply filters
function applyFilters() {
    const sortBy = sortSelect.value;
    const maxPrice = parseFloat(priceRange.value);
    
    let filtered = products.filter(product => product.price <= maxPrice);
    
    // Apply sorting
    switch (sortBy) {
        case 'price-low':
            filtered.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filtered.sort((a, b) => b.price - a.price);
            break;
        case 'name':
            filtered.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'rating':
            filtered.sort((a, b) => b.rating - a.rating);
            break;
    }
    
    filteredProducts = filtered;
    currentPage = 1;
    loadProducts();
}

// Filter by category
function filterByCategory(category) {
    if (category === 'all') {
        filteredProducts = [...products];
    } else {
        filteredProducts = products.filter(product => product.category === category);
    }
    
    currentPage = 1;
    loadProducts();
    showToast(`Showing ${filteredProducts.length} products in ${category}`);
    
    // Update active navigation
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        document.querySelector(`[href="#${category}"]`).classList.add('active');
}

// Cart functionality
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }
    
    saveCartToStorage();
    updateCartDisplay();
    showToast(`${product.name} added to cart`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCartToStorage();
    updateCartDisplay();
    showToast('Item removed from cart');
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(productId);
    } else {
        saveCartToStorage();
        updateCartDisplay();
    }
}

function clearCartItems() {
    cart = [];
    saveCartToStorage();
    updateCartDisplay();
    showToast('Cart cleared');
}

function updateCartDisplay() {
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update cart items display
    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        cartTotal.textContent = '$0.00';
        return;
    }
    
    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
                <h4 class="cart-item-title">${item.name}</h4>
                <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                <div class="cart-item-quantity">
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
            </div>
            <button class="remove-item" onclick="removeFromCart(${item.id})">&times;</button>
        </div>
    `).join('');
    
    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotal.textContent = `$${total.toFixed(2)}`;
}

function saveCartToStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function loadCartFromStorage() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
}

// Modal functions
function openCart() {
    cartModal.style.display = 'block';
}

function closeCartModal() {
    cartModal.style.display = 'none';
}

function showQuickView(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
    
    quickViewBody.innerHTML = `
        <div class="quick-view-product">
            <img src="${product.image}" alt="${product.name}" class="quick-view-image">
            <div class="quick-view-details">
                <h2>${product.name}</h2>
                <div class="quick-view-price">$${product.price.toFixed(2)}</div>
                <div class="product-rating">
                    <span class="stars">${stars}</span>
                    <span>${product.rating}</span>
                </div>
                <p class="quick-view-description">${product.description}</p>
                <button class="add-to-cart" onclick="addToCart(${product.id}); closeQuickViewModal();">Add to Cart</button>
            </div>
        </div>
    `;
    
    quickViewModal.style.display = 'block';
}

function closeQuickViewModal() {
    quickViewModal.style.display = 'none';
}

function openUserModal() {
    userModal.style.display = 'block';
}

function closeUserModal() {
    userModal.style.display = 'none';
}

// User authentication functions
function showLoginForm() {
    userInfo.style.display = 'none';
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    
    const loginForm = document.createElement('div');
    loginForm.innerHTML = `
        <form id="loginForm" class="user-form">
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <button type="button" onclick="showUserActions()">Back</button>
        </form>
    `;
    
    document.querySelector('.user-body').appendChild(loginForm);
    
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        login();
    });
}

function showRegisterForm() {
    userInfo.style.display = 'none';
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    
    const registerForm = document.createElement('div');
    registerForm.innerHTML = `
        <form id="registerForm" class="user-form">
            <input type="text" placeholder="Full Name" required>
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <button type="submit">Register</button>
            <button type="button" onclick="showUserActions()">Back</button>
        </form>
    `;
    
    document.querySelector('.user-body').appendChild(registerForm);
    
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        register();
    });
}

function showUserActions() {
    userInfo.style.display = 'none';
    loginBtn.style.display = 'block';
    registerBtn.style.display = 'block';
    
    const forms = document.querySelectorAll('.user-form');
    forms.forEach(form => form.remove());
}

function login() {
    // Simulate login
    currentUser = {
        name: 'Demo User',
        email: 'demo@example.com'
    };
    
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    updateUserDisplay();
    closeUserModal();
    showToast('Login successful');
}

function register() {
    // Simulate registration
    currentUser = {
        name: 'New User',
        email: 'newuser@example.com'
    };
    
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    updateUserDisplay();
    closeUserModal();
    showToast('Registration successful');
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    updateUserDisplay();
    showToast('Logout successful');
}

function updateUserDisplay() {
    if (currentUser) {
        userName.textContent = currentUser.name;
        userInfo.style.display = 'block';
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
    } else {
        userInfo.style.display = 'none';
        loginBtn.style.display = 'block';
        registerBtn.style.display = 'block';
    }
}

// Checkout function
function checkout() {
    if (cart.length === 0) {
        showToast('Your cart is empty');
        return;
    }
    
    if (!currentUser) {
        showToast('Please login to checkout');
        openUserModal();
        return;
    }
    
    // Simulate checkout process
    showToast('Processing checkout...');
    
    setTimeout(() => {
        cart = [];
        saveCartToStorage();
        updateCartDisplay();
        closeCartModal();
        showToast('Order placed successfully! Thank you for your purchase.');
    }, 2000);
}

// Form handlers
function handleContactSubmit(e) {
    e.preventDefault();
    showToast('Message sent successfully! We\'ll get back to you soon.');
    e.target.reset();
}

function handleNewsletterSubmit(e) {
    e.preventDefault();
    showToast('Thank you for subscribing to our newsletter!');
    e.target.reset();
}

// Utility functions
function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function scrollToProducts() {
    document.getElementById('products').scrollIntoView({
        behavior: 'smooth'
    });
}

// Add some CSS for user forms
const style = document.createElement('style');
style.textContent = `
    .user-form {
        display: grid;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .user-form input {
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        font-family: inherit;
    }
    
    .user-form button {
        padding: 0.75rem;
        border: none;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: var(--transition);
    }
    
    .user-form button[type="submit"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    .user-form button[type="submit"]:hover {
        background-color: var(--secondary-color);
    }
    
    .user-form button[type="button"] {
        background-color: var(--background-light);
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }
    
    .user-form button[type="button"]:hover {
        background-color: var(--border-color);
    }
`;
document.head.appendChild(style);