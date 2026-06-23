/* ==========================================================
 * Owner Dashboard
 * ----------------------------------------------------------
 * Manages: restaurants (CRUD + status), categories (CRUD),
 *          menu items (CRUD + availability toggle).
 * ========================================================== */

const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

let selectedRestaurantId = null;
let selectedRestaurantName = "";

// ---------- INIT ----------
document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        alert("Session expired");
        window.location.href = "auth.html";
        return;
    }

    loadRestaurants();

    const imageInput = document.getElementById("restImage");
    const preview = document.getElementById("imagePreview");
    if (imageInput && preview) {
        imageInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.classList.remove("hidden");
                };
                reader.readAsDataURL(file);
            } else {
                preview.classList.add("hidden");
            }
        });
    }
});

// ---------- HELPERS ----------
function authHeaders(extra = {}) {
    return Object.assign({ "Authorization": "Bearer " + token }, extra);
}

async function safeJson(res) {
    try { return await res.json(); } catch (e) { return null; }
}

async function callApi(url, options = {}) {
    const res = await fetch(url, options);
    if (res.status === 204) {
        return null;
    }
    const isJson = (res.headers.get("content-type") || "").includes("application/json");
    const body = isJson ? await safeJson(res) : await res.text();

    if (!res.ok) {
        const message = (body && body.message) ? body.message
            : (typeof body === "string" && body) ? body
            : ("Request failed (" + res.status + ")");
        throw new Error(message);
    }
    return body;
}

function showError(err) {
    console.error(err);
    alert(err.message || "Something went wrong");
}

// ---------- RESTAURANTS ----------
async function loadRestaurants() {
    try {
        const data = await callApi(`${BASE_URL}/owner/restaurants`, {
            headers: authHeaders()
        });

        const list = document.getElementById("restaurantList");
        if (!list) return;
        list.innerHTML = "";

        (data || []).forEach(r => {
            const div = document.createElement("div");
            div.className =
                "p-3 border rounded-lg flex justify-between items-center hover:bg-gray-100";

            const nameSpan = document.createElement("span");
            nameSpan.innerText = r.name;
            nameSpan.className = "flex-1 cursor-pointer";
            nameSpan.onclick = () => selectRestaurant(r, div);

            const statusBtn = document.createElement("button");

statusBtn.className =
    r.status === "OPEN"
        ? "mr-2 px-3 py-1 bg-green-500 text-white rounded text-sm"
        : "mr-2 px-3 py-1 bg-gray-500 text-white rounded text-sm";

statusBtn.innerText = r.status || "OPEN";

statusBtn.onclick = async (e) => {

    e.stopPropagation();

    const newStatus =
        r.status === "OPEN"
            ? "CLOSED"
            : "OPEN";

    try {

        await updateRestaurantStatus(r.id, newStatus);

        r.status = newStatus;

        statusBtn.innerText = newStatus;

        statusBtn.className =
            newStatus === "OPEN"
                ? "mr-2 px-3 py-1 bg-green-500 text-white rounded text-sm"
                : "mr-2 px-3 py-1 bg-gray-500 text-white rounded text-sm";

    } catch (err) {

        showError(err);
    }
};
            const deleteBtn = document.createElement("button");
            deleteBtn.className =
                "ml-2 px-3 py-1 bg-red-500 text-white rounded hover:bg-red-700 text-sm";
            deleteBtn.innerText = "Delete";
            deleteBtn.onclick = (e) => {
                e.stopPropagation();
                deleteRestaurant(r.id);
            };

            div.appendChild(nameSpan);
            div.appendChild(statusBtn);
            div.appendChild(deleteBtn);
            list.appendChild(div);
        });
    } catch (err) {
        showError(err);
    }
}

async function addRestaurant() {
    const name = document.getElementById("restName").value.trim();
    const city = document.getElementById("restCity").value.trim();
    const desc = document.getElementById("restDesc").value.trim();
    const file = document.getElementById("restImage").files[0];

    if (!name || !city) {
        alert("Name and City are required");
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("city", city);
    formData.append("description", desc);
    if (file) formData.append("image", file);

    try {
        await callApi(`${BASE_URL}/owner/restaurants`, {
            method: "POST",
            headers: authHeaders(),
            body: formData
        });
        alert("Restaurant added");

        document.getElementById("restName").value = "";
        document.getElementById("restCity").value = "";
        document.getElementById("restDesc").value = "";
        document.getElementById("restImage").value = "";
        const preview = document.getElementById("imagePreview");
        if (preview) preview.classList.add("hidden");

        loadRestaurants();
    } catch (err) {
        showError(err);
    }
}

async function deleteRestaurant(id) {
    if (!confirm("Delete this restaurant? All categories and items will be removed.")) return;
    try {
        await callApi(`${BASE_URL}/owner/restaurants/${id}`, {
            method: "DELETE",
            headers: authHeaders()
        });
        if (selectedRestaurantId === id) {
            selectedRestaurantId = null;
            document.getElementById("defaultView")?.classList.remove("hidden");
            document.getElementById("restaurantView")?.classList.add("hidden");
        }
        loadRestaurants();
    } catch (err) {
        showError(err);
    }
}

async function updateRestaurantStatus(restaurantId, status) {

    try {

        await callApi(
            `${BASE_URL}/owner/restaurants/status?restaurantId=${restaurantId}&status=${status}`,
            {
                method: "POST",
                headers: authHeaders()
            }
        );

    } catch (err) {

        showError(err);
    }
}

function selectRestaurant(r, element) {
    selectedRestaurantId = r.id;
    selectedRestaurantName = r.name;

    document.querySelectorAll("#restaurantList > div")
        .forEach(el => el.classList.remove("bg-red-100"));
    element.classList.add("bg-red-100");

    const titleEl = document.getElementById("selectedRestaurantName");
    if (titleEl) titleEl.innerText = r.name;

    document.getElementById("defaultView")?.classList.add("hidden");
    document.getElementById("restaurantView")?.classList.remove("hidden");

    loadCategories();
}

// ---------- CATEGORIES ----------
async function addCategory() {
    const input = document.getElementById("categoryName");
    const name = input.value.trim();
    if (!name) { alert("Enter category name"); return; }
    if (!selectedRestaurantId) { alert("Select a restaurant first"); return; }

    try {
        await callApi(`${BASE_URL}/owner/category`, {
            method: "POST",
            headers: authHeaders({ "Content-Type": "application/json" }),
            body: JSON.stringify({ name, restaurantId: selectedRestaurantId })
        });
        input.value = "";
        loadCategories();
    } catch (err) {
        showError(err);
    }
}

async function loadCategories() {

    try {

        const data = await callApi(
            `${BASE_URL}/owner/categories?restaurantId=${selectedRestaurantId}`,
            {
                headers: authHeaders()
            }
        );

        const container =
            document.getElementById("categoryContainer");

        if (!container) {
            return;
        }

        container.innerHTML = "";

        (data || []).forEach(cat => {

            const wrapper = document.createElement("div");

            wrapper.className =
                "bg-white p-4 rounded shadow";

            wrapper.innerHTML = `

                <div class="flex justify-between items-center">

                    <!-- CATEGORY NAME -->
                    <div class="flex-1">

                        <!-- VIEW MODE -->
                        <div class="category-view cursor-pointer">

                            <h3 class="font-semibold text-lg text-gray-800">
                                ${escapeHtml(cat.name)}
                            </h3>

                        </div>

                        <!-- EDIT MODE -->
                        <div class="category-edit hidden">

                            <input
                                type="text"
                                value="${escapeHtml(cat.name)}"
                                class="border p-2 rounded text-sm category-input w-64"
                            >

                        </div>

                    </div>

                    <!-- ACTION BUTTONS -->
                    <div class="flex gap-3 items-center">

                        <button
                            class="add-item-btn text-blue-600 hover:text-blue-800 text-sm"
                        >
                            Add Item
                        </button>

                        <button
                            class="edit-category-btn text-indigo-500 hover:text-indigo-700 text-sm"
                        >
                            Edit
                        </button>

                        <button
                            class="save-category-btn hidden text-green-600 text-sm"
                        >
                            Save
                        </button>

                        <button
                            class="cancel-category-btn hidden text-gray-500 text-sm"
                        >
                            Cancel
                        </button>

                        <button
                            class="delete-category-btn text-red-500 hover:text-red-700 text-lg"
                            title="Delete"
                        >
                            &#x1F5D1;
                        </button>

                    </div>

                </div>

                <!-- ITEMS -->
                <div
                    id="items-${cat.id}"
                    class="mt-3 hidden space-y-2"
                ></div>

                <!-- ADD ITEM FORM -->
                <div
                    id="add-form-${cat.id}"
                    class="mt-3 hidden bg-gray-50 p-3 rounded"
                >

                    <div class="grid grid-cols-1 md:grid-cols-4 gap-2">

                        <input
                            class="border p-2 rounded"
                            placeholder="Name"
                            id="newItemName-${cat.id}"
                        >

                        <input
                            class="border p-2 rounded"
                            placeholder="Description"
                            id="newItemDesc-${cat.id}"
                        >

                        <input
                            class="border p-2 rounded"
                            type="number"
                            placeholder="Price"
                            id="newItemPrice-${cat.id}"
                        >

                        <button
                            class="bg-green-500 text-white rounded px-3 py-1"
                            id="saveItem-${cat.id}"
                        >
                            Save
                        </button>

                    </div>

                </div>
            `;

            // ---------- ELEMENTS ----------
            const categoryView =
                wrapper.querySelector(".category-view");

            const categoryEdit =
                wrapper.querySelector(".category-edit");

            const categoryInput =
                wrapper.querySelector(".category-input");

            const addItemBtn =
                wrapper.querySelector(".add-item-btn");

            const editCategoryBtn =
                wrapper.querySelector(".edit-category-btn");

            const saveCategoryBtn =
                wrapper.querySelector(".save-category-btn");

            const cancelCategoryBtn =
                wrapper.querySelector(".cancel-category-btn");

            const deleteBtn =
                wrapper.querySelector(".delete-category-btn");

            // ---------- TOGGLE ITEMS ----------
            categoryView.onclick = () => toggleItems(cat.id);

            // ---------- ADD ITEM ----------
            addItemBtn.onclick = (e) => {

                e.stopPropagation();

                toggleAddForm(cat.id);
            };

            // ---------- DELETE CATEGORY ----------
            deleteBtn.onclick = (e) => {

                e.stopPropagation();

                deleteCategory(cat.id);
            };

            // ---------- EDIT ----------
            editCategoryBtn.onclick = (e) => {

                e.stopPropagation();

                categoryView.classList.add("hidden");

                categoryEdit.classList.remove("hidden");

                editCategoryBtn.classList.add("hidden");

                saveCategoryBtn.classList.remove("hidden");

                cancelCategoryBtn.classList.remove("hidden");
            };

            // ---------- CANCEL ----------
            cancelCategoryBtn.onclick = (e) => {

                e.stopPropagation();

                categoryView.classList.remove("hidden");

                categoryEdit.classList.add("hidden");

                editCategoryBtn.classList.remove("hidden");

                saveCategoryBtn.classList.add("hidden");

                cancelCategoryBtn.classList.add("hidden");

                categoryInput.value = cat.name;
            };

            // ---------- SAVE ----------
            saveCategoryBtn.onclick = async (e) => {

                e.stopPropagation();

                const newName =
                    categoryInput.value.trim();

                if (!newName) {

                    alert("Category name required");

                    return;
                }

                await updateCategory(cat.id, newName);

                categoryView.innerHTML = `
                    <h3 class="font-semibold text-lg text-gray-800">
                        ${escapeHtml(newName)}
                    </h3>
                `;

                cat.name = newName;

                categoryView.classList.remove("hidden");

                categoryEdit.classList.add("hidden");

                editCategoryBtn.classList.remove("hidden");

                saveCategoryBtn.classList.add("hidden");

                cancelCategoryBtn.classList.add("hidden");
            };

            container.appendChild(wrapper);

            // ---------- SAVE ITEM ----------
            const saveBtn =
                document.getElementById(`saveItem-${cat.id}`);

            if (saveBtn) {

                saveBtn.onclick = () => addMenuItem(cat.id);
            }
        });

    } catch (err) {

        showError(err);
    }
}

async function updateCategory(categoryId, name) {

    try {

        await callApi(
            `${BASE_URL}/owner/category/${categoryId}`,
            {
                method: "PUT",

                headers: authHeaders({
                    "Content-Type": "application/json"
                }),

                body: JSON.stringify({
                    restaurantId: selectedRestaurantId,
                    name: name
                })
            }
        );

    } catch (err) {

        showError(err);
    }
}
async function deleteCategory(categoryId) {
    if (!confirm("Delete this category and all its items?")) return;
    try {
        await callApi(`${BASE_URL}/owner/category/${categoryId}`, {
            method: "DELETE",
            headers: authHeaders()
        });
        loadCategories();
    } catch (err) {
        showError(err);
    }
}

// ---------- MENU ITEMS ----------
function toggleAddForm(categoryId) {
    const form = document.getElementById(`add-form-${categoryId}`);
    if (form) form.classList.toggle("hidden");
}

async function toggleItems(categoryId) {
    const container = document.getElementById(`items-${categoryId}`);
    if (!container) return;

    if (!container.classList.contains("hidden")) {
        container.classList.add("hidden");
        return;
    }

    try {
        const items = await callApi(
            `${BASE_URL}/owner/menu?categoryId=${categoryId}`,
            { headers: authHeaders() }
        );

        container.innerHTML = "";

        if (!items || items.length === 0) {
            container.innerHTML = `<p class="text-gray-400 text-sm">No items yet.</p>`;
        } else {
            items.forEach(item => {
                const row = document.createElement("div");
                row.className = "flex justify-between items-center p-2 border rounded";

                row.innerHTML = `
                    <div class="item-view">
                        <span class="font-medium">${escapeHtml(item.name)}</span>
                        <span class="text-gray-500 text-sm">- ₹${item.price}</span>
                    </div>

                    <div class="item-edit hidden flex gap-2">
                        <input class="border p-1 rounded text-sm name-input" value="${escapeHtml(item.name)}"/>
                        <input class="border p-1 rounded text-sm desc-input" value="${escapeHtml(item.description || "")}"/>
                        <input class="border p-1 rounded text-sm price-input" type="number" value="${item.price}"/>
                    </div>

                    <div class="flex gap-2 items-center">
                        <label class="text-sm flex items-center gap-1">
                            <input type="checkbox" ${item.isAvailable !== false ? "checked" : ""} />
                            Available
                        </label>

                        <button class="edit-btn text-blue-500">Edit</button>
                        <button class="save-btn hidden text-green-500">Save</button>
                        <button class="cancel-btn hidden text-gray-500">Cancel</button>

                        <button class="delete-btn text-red-500">Delete</button>
                    </div>
                `;

                // ---------- ELEMENTS ----------
                const checkbox = row.querySelector("input[type='checkbox']");
                const editBtn = row.querySelector(".edit-btn");
                const saveBtn = row.querySelector(".save-btn");
                const cancelBtn = row.querySelector(".cancel-btn");
                const deleteBtn = row.querySelector(".delete-btn");

                const viewDiv = row.querySelector(".item-view");
                const editDiv = row.querySelector(".item-edit");

                // ---------- EVENTS ----------

                // Availability toggle
                checkbox.onchange = () => toggleAvailability(item.id, checkbox.checked);

                // Delete
                deleteBtn.onclick = () => deleteItem(item.id);

                // Edit click
                editBtn.onclick = () => {
                    viewDiv.classList.add("hidden");
                    editDiv.classList.remove("hidden");

                    editBtn.classList.add("hidden");
                    saveBtn.classList.remove("hidden");
                    cancelBtn.classList.remove("hidden");
                };

                // Cancel click
                cancelBtn.onclick = () => {
                    viewDiv.classList.remove("hidden");
                    editDiv.classList.add("hidden");

                    editBtn.classList.remove("hidden");
                    saveBtn.classList.add("hidden");
                    cancelBtn.classList.add("hidden");
                };

                // Save click
                saveBtn.onclick = async () => {
                    const name = row.querySelector(".name-input").value.trim();
                    const desc = row.querySelector(".desc-input").value.trim();
                    const price = parseFloat(row.querySelector(".price-input").value);

                    if (!name) return alert("Name required");
                    if (!price || price <= 0) return alert("Invalid price");

                    await updateMenuItem(item.id, name, desc, price);

                    // Update UI after save
                    viewDiv.innerHTML = `
                        <span class="font-medium">${escapeHtml(name)}</span>
                        <span class="text-gray-500 text-sm">- ₹${price}</span>
                    `;

                    viewDiv.classList.remove("hidden");
                    editDiv.classList.add("hidden");

                    editBtn.classList.remove("hidden");
                    saveBtn.classList.add("hidden");
                    cancelBtn.classList.add("hidden");
                };

                container.appendChild(row);
            });
        }

        container.classList.remove("hidden");

    } catch (err) {
        showError(err);
    }
}
async function updateMenuItem(itemId, name, description, price) {
    try {
        const url = `${BASE_URL}/owner/menu/update`
            + `?itemId=${itemId}`
            + `&name=${encodeURIComponent(name)}`
            + `&description=${encodeURIComponent(description)}`
            + `&price=${price}`;

        await callApi(url, {
            method: "PUT",
            headers: authHeaders()
        });

    } catch (err) {
        showError(err);
    }
}
async function addMenuItem(categoryId) {
    const name = document.getElementById(`newItemName-${categoryId}`).value.trim();
    const desc = document.getElementById(`newItemDesc-${categoryId}`).value.trim();
    const priceStr = document.getElementById(`newItemPrice-${categoryId}`).value;
    const price = parseFloat(priceStr);

    if (!name) return alert("Item name required");
    if (!price || price <= 0) return alert("Enter a valid price");

    try {
        const url = `${BASE_URL}/owner/menu/add?categoryId=${categoryId}`
            + `&name=${encodeURIComponent(name)}`
            + `&description=${encodeURIComponent(desc)}`
            + `&price=${price}`;
        await callApi(url, { method: "POST", headers: authHeaders() });

        document.getElementById(`newItemName-${categoryId}`).value = "";
        document.getElementById(`newItemDesc-${categoryId}`).value = "";
        document.getElementById(`newItemPrice-${categoryId}`).value = "";

        // Reopen items list to refresh
        const container = document.getElementById(`items-${categoryId}`);
        if (container) container.classList.add("hidden");
        toggleItems(categoryId);
    } catch (err) {
        showError(err);
    }
}

async function toggleAvailability(itemId, isAvailable) {
    try {
        await callApi(
            `${BASE_URL}/owner/menu/availability?itemId=${itemId}&isAvailable=${isAvailable}`,
            { method: "POST", headers: authHeaders() }
        );
    } catch (err) {
        showError(err);
    }
}

async function deleteItem(itemId) {
    if (!confirm("Delete this menu item?")) return;
    try {
        await callApi(`${BASE_URL}/owner/menu/${itemId}`, {
            method: "DELETE",
            headers: authHeaders()
        });
    } catch (err) {
        showError(err);
    }
}

// ---------- NAV ----------
function goToOrders() {
    window.location.href = "orders.html";
}

function logout() {
    localStorage.clear();
    window.location.href = "auth.html";
}

// ---------- UTIL ----------
function escapeHtml(text) {
    if (text == null) return "";
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}