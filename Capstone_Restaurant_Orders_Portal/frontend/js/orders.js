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

    return (now - orderDate) < 60000; 
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
    <div class="flex justify-between items-start">
        
        <!-- LEFT SECTION -->
        <div class="space-y-1">
            <p class="font-semibold text-lg text-gray-800">
                Order #${order.id}
            </p>

            <!-- Restaurant Highlight -->
            <p class="text-sm font-medium text-indigo-600">
                🍽️ ${order.restaurantName || "Unknown Restaurant"}
            </p>

            <p class="text-gray-700 font-medium">
                ₹${order.totalAmount}
            </p>

            <p class="text-sm text-gray-600">
                👤 ${order.customerName || "N/A"}
            </p>

            <p class="text-sm text-gray-500">
                📍 ${order.address || "N/A"}
            </p>

            <p class="text-xs text-gray-400">
                🕒 ${formatTime(order.createdAt)}
            </p>

            <!-- STATUS BADGE -->
            <p class="mt-2">
                <span class="px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(order.status)} text-white">
                    ${order.status}
                </span>
            </p>
        </div>

        <!-- RIGHT SECTION -->
        <div>
            <select 
                ${order.status === "COMPLETED" || order.status === "CANCELLED" ? "disabled" : ""}
                onchange="updateStatus(${order.id}, this.value)"
                class="border border-gray-300 bg-white px-3 py-2 rounded-lg text-sm shadow-sm hover:border-gray-400">
                
                <option disabled selected>Update</option>
                <option>PENDING</option>
                <option>DELIVERED</option>
                <option>COMPLETED</option>
                <option>CANCELLED</option>
            </select>
        </div>
    </div>

    <!-- ITEMS -->
    <div class="mt-4 border-t pt-3 space-y-1">
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