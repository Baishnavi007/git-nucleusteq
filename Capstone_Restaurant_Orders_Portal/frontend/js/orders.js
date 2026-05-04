const API_BASE = "http://localhost:8080";

let previousOrderCount = 0;

// ================= TIME FORMAT =================
function formatTime(dateStr) {
    const date = new Date(dateStr);

    return date.toLocaleString("en-IN", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit"
    });
}

// ================= NEW ORDER CHECK =================
function isRecent(orderTime) {
    const now = new Date();
    const orderDate = new Date(orderTime);

    return (now - orderDate) < 60000; // 1 min
}

// ================= LOAD ORDERS =================
async function loadOrders() {
    try {
        const token = localStorage.getItem("token");

        const res = await fetch(`${API_BASE}/owner/orders`, {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        let orders = await res.json();

        // 🔥 SORT LATEST FIRST
        orders.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

        const container = document.getElementById("ordersContainer");
        container.innerHTML = "";

       
        if (orders.length > previousOrderCount) {
            showToast("🔥 New Order Received!");
        }
        previousOrderCount = orders.length;

        orders.forEach(order => {
            const div = document.createElement("div");

            
            div.className = `
                p-5 rounded-xl shadow
                ${isRecent(order.createdAt) ? "bg-green-50 border border-green-300" : "bg-white"}
            `;

            div.innerHTML = `
                <div class="flex justify-between items-center">
                    <div>
                        <p class="font-bold text-lg">Order #${order.id}</p>
                        <p class="text-gray-600">₹${order.totalAmount}</p>

                        <p class="mt-1 text-sm">
                            👤 ${order.customerName || "N/A"}
                        </p>

                        <p class="text-sm text-gray-500">
                            📍 ${order.address || "N/A"}
                        </p>

                        <p class="text-xs text-gray-400">
                            🕒 ${formatTime(order.createdAt)}
                        </p>

                        <p class="mt-1">
                            Status:
                            <span class="px-2 py-1 rounded text-white text-sm ${getStatusColor(order.status)}">
                                ${order.status}
                            </span>
                        </p>
                    </div>

                    <select 
                        ${order.status === "COMPLETED" || order.status === "CANCELLED" ? "disabled" : ""}
                        onchange="updateStatus(${order.id}, this.value)"
                        class="border p-2 rounded-lg">
                        <option disabled selected>Update</option>
                        <option>PENDING</option>
                        <option>DELIVERED</option>
                        <option>COMPLETED</option>
                        <option>CANCELLED</option>
                    </select>
                </div>

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

// ================= UPDATE STATUS =================
async function updateStatus(orderId, status) {
    try {
        const token = localStorage.getItem("token");

        const res = await fetch(
            `${API_BASE}/owner/orders/status?orderId=${orderId}&status=${status}`,
            {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + token
                }
            }
        );

        
        if (!res.ok) {
            const errorData = await res.json();

            showToast(`❌ ${errorData.message || "Invalid status transition"}`);
            return;
        }

        showToast("✅ Status Updated");

        loadOrders();

    } catch (err) {
        console.error("Error updating status:", err);
        showToast("❌ Something went wrong");
    }
}
// ================= STATUS COLORS =================
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

// ================= TOAST =================
function showToast(message) {
    const toast = document.createElement("div");

    toast.innerText = message;
    toast.className = "fixed bottom-5 right-5 bg-black text-white px-5 py-3 rounded-lg shadow-lg";

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ================= INIT =================
loadOrders();
setInterval(loadOrders, 5000);