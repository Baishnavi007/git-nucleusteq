const API_BASE = "http://localhost:8080";

async function loadOrders() {
    try {
        const token = localStorage.getItem("token");

        const res = await fetch(`${API_BASE}/orders/my`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        let orders = await res.json();

        // 🔥 SORT: latest first
        orders.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

        // 🔍 FILTER (optional)
        const filter = document.getElementById("statusFilter")?.value;
        if (filter) {
            orders = orders.filter(o => o.status === filter);
        }

        const container = document.getElementById("ordersContainer");
        container.innerHTML = "";

        if (orders.length === 0) {
            container.innerHTML = "<p class='text-gray-500'>No orders yet 😢</p>";
            return;
        }

        orders.forEach(order => {

            const div = document.createElement("div");
            div.className = "bg-white p-5 rounded-xl shadow";

            div.innerHTML = `
                <div class="flex justify-between items-start">

                    <div>
                        <h2 class="text-lg font-bold">
                            🍽️ ${order.restaurantName || "Restaurant"}
                        </h2>

                        <!-- 📅 DATE -->
                        <p class="text-sm text-gray-500 mt-1">
                            🕒 ${formatDate(order.createdAt)}
                        </p>

                        <!-- 📍 ADDRESS -->
                        <p class="text-sm text-gray-600 mt-1">
                            📍 ${order.address || "Address not available"}
                        </p>

                        <!-- 💰 AMOUNT -->
                        <p class="mt-2 font-medium">
                            💰 ₹${order.totalAmount}
                        </p>

                        <!-- 🚦 STATUS -->
                        <p class="mt-2">
                            Status:
                            <span class="px-2 py-1 text-white text-sm rounded ${getStatusColor(order.status)}">
                                ${order.status}
                            </span>
                        </p>
                    </div>

                </div>

                <!-- 🧾 ITEMS -->
                <div class="mt-3 border-t pt-2">
                    ${order.items.map(item => `
                        <p class="text-sm text-gray-700">
                            • ${item.itemName} × ${item.quantity}
                        </p>
                    `).join("")}
                </div>
            `;

            container.appendChild(div);
        });

    } catch (err) {
        console.error("Error loading orders:", err);
    }
}

// 🎨 STATUS COLORS
function getStatusColor(status) {
    switch(status) {
        case "PLACED": return "bg-gray-500";
        case "PENDING": return "bg-yellow-500";
        case "DELIVERED": return "bg-blue-500";
        case "COMPLETED": return "bg-green-500";
        case "CANCELLED": return "bg-red-500";
        default: return "bg-gray-400";
    }
}

// 📅 FORMAT DATE (nice readable)
function formatDate(dateStr) {
    const d = new Date(dateStr);

    return d.toLocaleString("en-IN", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit"
    });
}

// INIT
loadOrders();