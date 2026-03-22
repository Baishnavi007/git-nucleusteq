document.addEventListener("DOMContentLoaded", function () {

// Default products
const defaultProducts = [
    { id: 1, name: "Laptop", price: 55000, stock: 5, category: "electronics" },
    { id: 2, name: "Phone", price: 20000, stock: 10, category: "electronics" },
    { id: 3, name: "T-Shirt", price: 500, stock: 20, category: "clothing" },
    { id: 4, name: "Jeans", price: 1500, stock: 8, category: "clothing" },
    { id: 5, name: "Book", price: 300, stock: 0, category: "books" },
    { id: 6, name: "Notebook", price: 100, stock: 15, category: "books" },
    { id: 7, name: "Headphones", price: 2000, stock: 3, category: "accessories" },
    { id: 8, name: "Charger", price: 800, stock: 12, category: "accessories" }
];

// Main product array
let products = [];

// Filtered products
let filteredProducts = [];

// Temporary load
products = defaultProducts;
filteredProducts = [...products];

// Render products
function renderProducts() {

    const container = document.getElementById("productsContainer");

    container.innerHTML = "";

    for (let i = 0; i < filteredProducts.length; i++) {

        const product = filteredProducts[i];

        const card = document.createElement("div");

        card.innerHTML = `
            <h3>${product.name}</h3>
            <p>Category: ${product.category}</p>
            <p>Price: ₹${product.price}</p>
            <p>Stock: ${product.stock}</p>
        `;

        container.appendChild(card);
    }
}

// Analytics
function updateAnalytics() {

    const totalProducts = document.getElementById("totalProducts");
    const totalValue = document.getElementById("totalValue");
    const outOfStock = document.getElementById("outOfStock");

    let total = 0;
    let value = 0;
    let outStock = 0;

    for (let i = 0; i < products.length; i++) {

        total++;
        value += products[i].price * products[i].stock;

        if (products[i].stock === 0) {
            outStock++;
        }
    }

    totalProducts.textContent = total;
    totalValue.textContent = value;
    outOfStock.textContent = outStock;
}

// Load categories
function loadCategories() {

    const categoryDropdown = document.getElementById("categoryFilter");

    const categories = [];

    for (let i = 0; i < products.length; i++) {

        const category = products[i].category;

        if (!categories.includes(category)) {
            categories.push(category);
        }
    }

    for (let i = 0; i < categories.length; i++) {

        const option = document.createElement("option");
        option.value = categories[i];
        option.textContent = categories[i];

        categoryDropdown.appendChild(option);
    }
}

// Apply filters
function applyFilters() {

    const searchInput = document.getElementById("search").value.toLowerCase();
    const category = document.getElementById("categoryFilter").value;
    const lowStockChecked = document.getElementById("lowStock").checked;

    filteredProducts = [];

    for (let i = 0; i < products.length; i++) {

        const product = products[i];

        let matchesSearch = product.name.toLowerCase().includes(searchInput);

        let matchesCategory = (category === "all") || (product.category === category);

        let matchesStock = !lowStockChecked || (product.stock < 5);

        if (matchesSearch && matchesCategory && matchesStock) {
            filteredProducts.push(product);
        }
    }

    renderProducts();
    updateAnalytics();
}

// Event listeners
document.getElementById("search").addEventListener("input", applyFilters);
document.getElementById("categoryFilter").addEventListener("change", applyFilters);
document.getElementById("lowStock").addEventListener("change", applyFilters);

// Initial load
loadCategories();
renderProducts();
updateAnalytics();

});