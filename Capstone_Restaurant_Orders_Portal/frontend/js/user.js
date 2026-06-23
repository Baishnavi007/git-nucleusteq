const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

const DEFAULT_IMAGE = "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?q=80&w=2070&auto=format&fit=crop";

// ---------- SESSION CHECK ----------
if (!token) {
    alert("Session expired. Please login again.");
    window.location.href = "auth.html";
}

if (role !== "USER") {
    alert("Unauthorized access");
    window.location.href = "auth.html";
}

// ---------- LOAD ON START ----------
document.addEventListener("DOMContentLoaded", () => {
    loadRestaurants();
    loadWallet(); 
});

// ---------- FETCH ALL RESTAURANTS ----------
function loadRestaurants() {
    fetch(`${BASE_URL}/users/restaurants`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const container = document.getElementById("restaurantList");
        container.innerHTML = "";

        if (!data || data.length === 0) {
            container.innerHTML = "<p>No restaurants available 🍽️</p>";
            return;
        }

        data.forEach(r => {
            const div = document.createElement("div");
            div.className = "card";

            const imageUrl = r.imageUrl || DEFAULT_IMAGE;

            div.innerHTML = `
                <img src="${imageUrl}"
                onerror="this.src='${DEFAULT_IMAGE}'" />
                <div class="info">
    <h3>${r.name}</h3>

    <p>${r.city || "Available Everywhere"}</p>

    <span class="rating">
        ⭐ 4.${Math.floor(Math.random()*5)}
    </span>

    <br>

    ${
        r.status === "CLOSED"
        ? `<span style="color:red;font-weight:bold;">
                Currently Closed
           </span>`
        : `<span style="color:green;font-weight:bold;">
                Open
           </span>`
    }
</div>
            `;

            div.onclick = () => {

    if (r.status === "CLOSED") {

        alert("Restaurant is currently closed");

        return;
    }

    localStorage.setItem("restaurantId", r.id);

    window.location.href = "menu.html";
};

            container.appendChild(div);
        });
    })
    .catch(err => {
        console.error(err);
        alert("Failed to load restaurants");
    });
}

// ---------- LOAD WALLET ----------
function loadWallet() {
    fetch(`${BASE_URL}/users/profile`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("walletBalance").innerText = data.walletBalance || 0;
    })
    .catch(err => console.error(err));
}

// ----------  GO TO ORDERS ----------
function goToOrders() {
    window.location.href = "order-history.html";
}

// ---------- NAVIGATION ----------
function goToWallet() {
    window.location.href = "wallet.html";
}

// ---------- LOGOUT ----------
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}