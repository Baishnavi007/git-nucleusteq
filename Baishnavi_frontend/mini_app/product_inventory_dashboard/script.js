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

// Temporary load (for now)
products = defaultProducts;
filteredProducts = [...products];

// Function to render products
function renderProducts() {

    const container = document.getElementById("productsContainer");

    // Clear previous data
    container.innerHTML = "";

    // Loop through products
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

// Initial render
renderProducts();

});