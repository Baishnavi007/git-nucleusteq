const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

let selectedRestaurantId = null;

// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        alert("Session expired");
        window.location.href = "auth.html";
        return;
    }
    loadRestaurants();
});


// ================= API LAYER =================
const api = {

    getRestaurants: () =>
        fetch(`${BASE_URL}/owner/restaurants`, {
            headers: { Authorization: "Bearer " + token }
        }).then(res => res.json()),

    addRestaurant: (data) =>
        fetch(`${BASE_URL}/owner/restaurants`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token
            },
            body: JSON.stringify(data)
        }),

    getCategories: (restaurantId) =>
        fetch(`${BASE_URL}/owner/categories?restaurantId=${restaurantId}`, {
            headers: { Authorization: "Bearer " + token }
        }).then(res => res.json()),

    addCategory: (data) =>
        fetch(`${BASE_URL}/owner/category`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token
            },
            body: JSON.stringify(data)
        }),

    getItems: (categoryId) =>
        fetch(`${BASE_URL}/owner/menu?categoryId=${categoryId}`, {
            headers: { Authorization: "Bearer " + token }
        }).then(res => res.json()),

    addItem: (categoryId, name, desc, price) =>
        fetch(`${BASE_URL}/owner/menu/add?categoryId=${categoryId}&name=${name}&description=${desc}&price=${price}`, {
            method: "POST",
            headers: { Authorization: "Bearer " + token }
        }),

    toggleItem: (id, status) =>
        fetch(`${BASE_URL}/owner/menu/availability?itemId=${id}&isAvailable=${status}`, {
            method: "POST",
            headers: { Authorization: "Bearer " + token }
        }),

    updateItem: (id, name, desc, price) =>
        fetch(`${BASE_URL}/owner/menu/update?itemId=${id}&name=${name}&description=${desc}&price=${price}`, {
            method: "PUT",
            headers: { Authorization: "Bearer " + token }
        }),

    deleteItem: (id) =>
        fetch(`${BASE_URL}/owner/menu/delete?itemId=${id}`, {
            method: "DELETE",
            headers: { Authorization: "Bearer " + token }
        })
};


// ================= RESTAURANTS =================
async function loadRestaurants() {
    const data = await api.getRestaurants();

    const list = document.getElementById("restaurantList");
    list.innerHTML = "";

    data.forEach(r => {
        const div = document.createElement("div");
        div.className = "p-3 border rounded-lg cursor-pointer hover:bg-red-50";
        div.innerText = r.name;

        div.onclick = () => selectRestaurant(r, div);

        list.appendChild(div);
    });
}

function selectRestaurant(r, element) {
    selectedRestaurantId = r.id;

    document.querySelectorAll("#restaurantList div")
        .forEach(el => el.classList.remove("bg-red-100"));

    element.classList.add("bg-red-100");

    document.getElementById("selectedRestaurantName").innerText = r.name;

    document.getElementById("defaultView").classList.add("hidden");
    document.getElementById("restaurantView").classList.remove("hidden");

    loadCategories();
}


// ================= CATEGORY =================
async function addCategory() {
    const name = document.getElementById("categoryName").value.trim();

    if (!name) return alert("Enter category name");

    await api.addCategory({
        name,
        restaurantId: selectedRestaurantId
    });

    document.getElementById("categoryName").value = "";
    loadCategories();
}


// ================= CATEGORY LOAD =================
async function loadCategories() {
    const data = await api.getCategories(selectedRestaurantId);

    const container = document.getElementById("categoryContainer");
    container.innerHTML = "";

    data.forEach(cat => {
        const div = document.createElement("div");
        div.className = "bg-white rounded-xl shadow-md";

        div.innerHTML = `
            <div onclick="toggleCategory(${cat.id})"
                class="p-4 flex justify-between cursor-pointer">
                <h3>${cat.name}</h3>
                <span id="arrow-${cat.id}">▼</span>
            </div>

            <div id="content-${cat.id}" class="hidden p-4 border-t">

                <div class="flex gap-2 mb-3">
                    <input id="name-${cat.id}" placeholder="Item name" class="border p-2 rounded">
                    <input id="desc-${cat.id}" placeholder="Description" class="border p-2 rounded">
                    <input id="price-${cat.id}" placeholder="Price" class="border p-2 rounded">

                    <button onclick="addItem(${cat.id})"
                        class="bg-green-500 text-white px-3 rounded">
                        Add
                    </button>
                </div>

                <div id="items-${cat.id}"></div>
            </div>
        `;

        container.appendChild(div);

        loadItems(cat.id);
    });
}


// ================= ACCORDION =================
function toggleCategory(id) {
    document.querySelectorAll("[id^='content-']")
        .forEach(el => el.classList.add("hidden"));

    document.querySelectorAll("[id^='arrow-']")
        .forEach(el => el.innerText = "▼");

    document.getElementById(`content-${id}`).classList.remove("hidden");
    document.getElementById(`arrow-${id}`).innerText = "▲";
}


// ================= ITEMS =================
async function addItem(categoryId) {
    const name = document.getElementById(`name-${categoryId}`).value;
    const desc = document.getElementById(`desc-${categoryId}`).value;
    const price = document.getElementById(`price-${categoryId}`).value;

    if (!name || !price) return alert("Required fields missing");

    await api.addItem(categoryId, name, desc, price);

    loadItems(categoryId);
}


async function loadItems(categoryId) {
    const data = await api.getItems(categoryId);

    const container = document.getElementById(`items-${categoryId}`);
    container.innerHTML = "";

    data.forEach(item => {
        container.innerHTML += renderItem(item);
    });
}


// ================= ITEM UI =================
function renderItem(item) {
    return `
    <div class="bg-gray-50 p-3 rounded-lg mb-2">

        <div id="view-${item.id}" class="flex justify-between">

            <div>
                <p class="font-semibold">${item.name}</p>
                <p>₹${item.price}</p>
            </div>

            <div class="flex gap-2">

                <button onclick="showEdit(${item.id})">✏️</button>
                <button onclick="deleteItem(${item.id})">🗑️</button>

                <button onclick="toggle(${item.id}, ${!item.isAvailable})"
                    class="${item.isAvailable ? "bg-green-500" : "bg-gray-400"} text-white px-2 rounded">
                    ${item.isAvailable ? "In Stock" : "Out of Stock"}
                </button>
            </div>
        </div>

        <div id="edit-${item.id}" class="hidden mt-2 flex gap-2">
            <input id="n-${item.id}" value="${item.name}">
            <input id="d-${item.id}" value="${item.description || ""}">
            <input id="p-${item.id}" value="${item.price}">

            <button onclick="updateItem(${item.id})">Save</button>
            <button onclick="cancelEdit(${item.id})">Cancel</button>
        </div>
    </div>
    `;
}


// ================= ITEM ACTIONS =================
function showEdit(id) {
    document.getElementById(`view-${id}`).classList.add("hidden");
    document.getElementById(`edit-${id}`).classList.remove("hidden");
}

function cancelEdit(id) {
    document.getElementById(`view-${id}`).classList.remove("hidden");
    document.getElementById(`edit-${id}`).classList.add("hidden");
}

async function updateItem(id) {
    const name = document.getElementById(`n-${id}`).value;
    const desc = document.getElementById(`d-${id}`).value;
    const price = document.getElementById(`p-${id}`).value;

    await api.updateItem(id, name, desc, price);

    loadCategories();
}

async function deleteItem(id) {
    if (!confirm("Delete item?")) return;

    await api.deleteItem(id);

    loadCategories();
}

async function toggle(id, status) {
    await api.toggleItem(id, status);

    loadCategories();
}