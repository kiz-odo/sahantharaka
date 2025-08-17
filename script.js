// E-commerce Website JavaScript

// Global variables
let products = [];
let cart = [];
let filteredProducts = [];

// DOM elements
const productsGrid = document.getElementById('productsGrid');
const cartBtn = document.getElementById('cartBtn');
const cartSidebar = document.getElementById('cartSidebar');
const cartOverlay = document.getElementById('cartOverlay');
const closeCart = document.getElementById('closeCart');
const cartItems = document.getElementById('cartItems');
const cartCount = document.getElementById('cartCount');
const totalAmount = document.getElementById('totalAmount');
const checkoutBtn = document.getElementById('checkoutBtn');
const searchBtn = document.getElementById('searchBtn');
const searchModal = document.getElementById('searchModal');
const closeSearch = document.getElementById('closeSearch');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const productModal = document.getElementById('productModal');
const closeModal = document.getElementById('closeModal');
const productModalBody = document.getElementById('productModalBody');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    setupEventListeners();
    loadCartFromStorage();
    updateCartDisplay();
});

// Event listeners setup
function setupEventListeners() {
    // Cart functionality
    cartBtn.addEventListener('click', openCart);
    closeCart.addEventListener('click', closeCartSidebar);
    cartOverlay.addEventListener('click', closeCartSidebar);
    checkoutBtn.addEventListener('click', handleCheckout);
    
    // Search functionality
    searchBtn.addEventListener('click', openSearchModal);
    closeSearch.addEventListener('click', closeSearchModal);
    searchInput.addEventListener('input', handleSearch);
    
    // Filtering and sorting
    categoryFilter.addEventListener('change', filterProducts);
    sortFilter.addEventListener('change', sortProducts);
    
    // Modal functionality
    closeModal.addEventListener('click', closeProductModal);
    
    // Close modals on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeCartSidebar();
            closeSearchModal();
            closeProductModal();
        }
    });
}

// Load products from JSON file
async function loadProducts() {
    try {
        const response = await fetch('products.json');
        products = await response.json();
        filteredProducts = [...products];
        displayProducts();
    } catch (error) {
        console.error('Error loading products:', error);
        // Fallback to sample products if JSON file is not available
        products = getSampleProducts();
        filteredProducts = [...products];
        displayProducts();
    }
}

// Sample products fallback
function getSampleProducts() {
    return [
        {
            id: 1,
            name: "Wireless Bluetooth Headphones",
            category: "electronics",
            price: 89.99,
            rating: 4.5,
            image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=200&fit=crop",
            description: "High-quality wireless headphones with noise cancellation and long battery life."
        },
        {
            id: 2,
            name: "Classic Cotton T-Shirt",
            category: "clothing",
            price: 24.99,
            rating: 4.2,
            image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=200&fit=crop",
            description: "Comfortable and stylish cotton t-shirt available in multiple colors."
        },
        {
            id: 3,
            name: "Programming Fundamentals Book",
            category: "books",
            price: 34.99,
            rating: 4.7,
            image: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=200&fit=crop",
            description: "Comprehensive guide to programming basics and best practices."
        },
        {
            id: 4,
            name: "Smart Home Assistant",
            category: "electronics",
            price: 129.99,
            rating: 4.6,
            image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=200&fit=crop",
            description: "Voice-controlled smart home assistant with AI capabilities."
        },
        {
            id: 5,
            name: "Garden Tool Set",
            category: "home",
            price: 49.99,
            rating: 4.3,
            image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=200&fit=crop",
            description: "Complete set of essential gardening tools for your home garden."
        },
        {
            id: 6,
            name: "Designer Jeans",
            category: "clothing",
            price: 79.99,
            rating: 4.4,
            image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=200&fit=crop",
            description: "Premium quality designer jeans with perfect fit and style."
        },
        {
            id: 7,
            name: "Cookbook Collection",
            category: "books",
            price: 44.99,
            rating: 4.8,
            image: "https://images.unsplash.com/photo-1589998059171-988d887df646?w=300&h=200&fit=crop",
            description: "Collection of delicious recipes from around the world."
        },
        {
            id: 8,
            name: "Coffee Maker",
            category: "home",
            price: 89.99,
            rating: 4.5,
            image: "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=300&h=200&fit=crop",
            description: "Automatic coffee maker with programmable settings and timer."
        }
    ];
}

// Display products in the grid
function displayProducts() {
    if (filteredProducts.length === 0) {
        productsGrid.innerHTML = '<div class="no-products"><h3>No products found</h3><p>Try adjusting your filters or search terms.</p></div>';
        return;
    }
    
    productsGrid.innerHTML = filteredProducts.map(product => `
        <div class="product-card" data-product-id="${product.id}">
            <img src="${product.image}" alt="${product.name}" class="product-image" onclick="openProductModal(${product.id})">
            <div class="product-info">
                <h3 class="product-title" onclick="openProductModal(${product.id})">${product.name}</h3>
                <p class="product-category">${product.category}</p>
                <div class="product-rating">
                    <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                    <span>${product.rating}</span>
                </div>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

// Filter products by category
function filterProducts() {
    const selectedCategory = categoryFilter.value;
    
    if (selectedCategory === '') {
        filteredProducts = [...products];
    } else {
        filteredProducts = products.filter(product => product.category === selectedCategory);
    }
    
    displayProducts();
}

// Sort products
function sortProducts() {
    const sortBy = sortFilter.value;
    
    switch (sortBy) {
        case 'name':
            filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'price-low':
            filteredProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filteredProducts.sort((a, b) => b.price - a.price);
            break;
        case 'rating':
            filteredProducts.sort((a, b) => b.rating - a.rating);
            break;
    }
    
    displayProducts();
}

// Search functionality
function handleSearch() {
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
    
    displayProducts();
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
    
    updateCartDisplay();
    saveCartToStorage();
    showNotification(`${product.name} added to cart!`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartDisplay();
    saveCartToStorage();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(productId);
    } else {
        updateCartDisplay();
        saveCartToStorage();
    }
}

function updateCartDisplay() {
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update cart items
    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart"><p>Your cart is empty</p></div>';
        totalAmount.textContent = '$0.00';
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
                <button class="remove-item" onclick="removeFromCart(${item.id})">Remove</button>
            </div>
        </div>
    `).join('');
    
    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    totalAmount.textContent = `$${total.toFixed(2)}`;
}

// Cart sidebar controls
function openCart() {
    cartSidebar.classList.add('active');
    cartOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCartSidebar() {
    cartSidebar.classList.remove('active');
    cartOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Search modal controls
function openSearchModal() {
    searchModal.classList.add('active');
    searchInput.focus();
}

function closeSearchModal() {
    searchModal.classList.remove('active');
    searchInput.value = '';
    // Reset search results
    filteredProducts = [...products];
    displayProducts();
}

// Product modal functionality
function openProductModal(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    productModalBody.innerHTML = `
        <div class="product-modal-details">
            <div class="product-modal-image">
                <img src="${product.image}" alt="${product.name}">
            </div>
            <div class="product-modal-info">
                <h2>${product.name}</h2>
                <p class="product-modal-category">${product.category}</p>
                <div class="product-modal-rating">
                    <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                    <span>${product.rating} out of 5</span>
                </div>
                <div class="product-modal-price">$${product.price.toFixed(2)}</div>
                <p class="product-modal-description">${product.description}</p>
                <button class="add-to-cart-btn" onclick="addToCart(${product.id}); closeProductModal();">
                    Add to Cart
                </button>
            </div>
        </div>
    `;
    
    productModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeProductModal() {
    productModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Checkout functionality
function handleCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Simple checkout simulation
    alert(`Thank you for your order!\nTotal: $${total.toFixed(2)}\n\nThis is a demo website. In a real application, you would be redirected to a payment gateway.`);
    
    // Clear cart after checkout
    cart = [];
    updateCartDisplay();
    saveCartToStorage();
    closeCartSidebar();
}

// Utility functions
function showNotification(message) {
    // Create a simple notification
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #27ae60;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 3000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function scrollToProducts() {
    document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
}

// Local storage functions
function saveCartToStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function loadCartFromStorage() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .product-modal-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        align-items: start;
    }
    
    .product-modal-image img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 10px;
    }
    
    .product-modal-info h2 {
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .product-modal-category {
        color: #7f8c8d;
        text-transform: uppercase;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .product-modal-rating {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .product-modal-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e74c3c;
        margin-bottom: 1rem;
    }
    
    .product-modal-description {
        color: #666;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .empty-cart {
        text-align: center;
        padding: 2rem;
        color: #7f8c8d;
    }
    
    .no-products {
        text-align: center;
        padding: 3rem;
        color: #7f8c8d;
    }
    
    .no-products h3 {
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    @media (max-width: 768px) {
        .product-modal-details {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(style);