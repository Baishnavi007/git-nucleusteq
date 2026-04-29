const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// Session check
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

            div.innerHTML = `
                <img src="https://source.unsplash.com/300x200/?food,restaurant" />
                <div class="info">
                    <h3>${r.name}</h3>
                    <p>${r.city || "Available Everywhere"}</p>
                    <span class="rating">⭐ 4.${Math.floor(Math.random()*5)}</span>
                </div>
            `;

            
            div.onclick = () => {
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

// CALL THIS ALSO
document.addEventListener("DOMContentLoaded", () => {
    loadRestaurants();
    loadWallet(); // 👈 ADD THIS
});

// ---------- NAVIGATION ----------
function goToWallet() {
    window.location.href = "wallet.html";
}

// ---------- LOGOUT ----------
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}