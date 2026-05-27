/* ================================================
SIGANME EN TIKTOK ARGOS2B
PHARMATECH | NEUROSCIENCE DIVISION
    ================================================ */
// ========================
// CART STATE
// ========================
let carrito = [];
let total = 0;
// ========================
// MODAL FUNCTIONS
// ========================
function openModal(title, text) {
    document.getElementById("modalTitle").innerHTML = title;
    document.getElementById("modalText").innerHTML = text;
    document.getElementById("customModal").classList.add("active");
}
function closeModal() {
    document.getElementById("customModal").classList.remove("active");
}
// ========================
// CART FUNCTIONS
// ========================
function agregarCarrito(nombre, precio) {
    carrito.push({ nombre, precio });
    total += precio;
    actualizarCarrito();
    openModal("Producto agregado", nombre + " añadido al carrito.");
}
function actualizarCarrito() {
    const carritoContenido = document.getElementById("carritoContenido");
    carritoContenido.innerHTML = "";
    carrito.forEach((producto, index) => {
        carritoContenido.innerHTML += `
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                background:#27272a;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                transition:0.3s;
            ">
                <span>${producto.nombre}</span>
                <div>
                    ₡${producto.precio.toLocaleString()}
                    <button
                        onclick="eliminarProducto(${index})"
                        style="
                            margin-left:10px;
                            background:#dc2626;
                            border:none;
                            color:white;
                            padding:5px 10px;
                            border-radius:5px;
                            cursor:pointer;
                            font-weight:bold;
                            transition:0.3s;
                        ">X</button>
                </div>
            </div>
        `;
    });
    document.getElementById("totalCarrito").innerText = "₡" + total.toLocaleString();
}
function eliminarProducto(index) {
    total -= carrito[index].precio;
    carrito.splice(index, 1);
    actualizarCarrito();
}
// ========================
// PAYMENT FUNCTIONS
// ========================
function finalizarCompra() {
    if (carrito.length === 0) {
        openModal("Carrito vacío", "Agrega productos primero.");
        return;
    }
    const metodo = document.getElementById("metodoPago").value;
    let metodoHTML = "";
    if (metodo === "sinpe") {
        metodoHTML = `
            <strong>SINPE Móvil</strong><br><br>
            Número: 8888-8888
        `;
    } else if (metodo === "transferencia") {
        metodoHTML = `
            <strong>Transferencia Bancaria</strong><br><br>
            Banco Nacional<br>
            Cuenta: 123456789
        `;
    } else {
        metodoHTML = `
            <strong>Pago con Tarjeta</strong><br><br>
            <input type="text" placeholder="Número de tarjeta" style="width:100%;padding:10px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Nombre del titular" style="width:100%;padding:10px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="CVV" style="width:100%;padding:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
        `;
    }
    let formulario = `
        <div style="text-align:left;">
            <h3 style="color:#a855f7;margin-bottom:20px;">
                Información de Envío
            </h3>
            <input type="text" placeholder="Nombre completo" style="width:100%;padding:12px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Provincia" style="width:100%;padding:12px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Cantón" style="width:100%;padding:12px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Código Postal" style="width:100%;padding:12px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Dirección Exacta" style="width:100%;padding:12px;margin-bottom:10px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <input type="text" placeholder="Teléfono" style="width:100%;padding:12px;margin-bottom:20px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <h3 style="color:#a855f7;margin-bottom:15px;">
                Verificación Médica
            </h3>
            <input type="password" id="credencial" placeholder="Ingrese código de verificación" style="width:100%;padding:12px;margin-bottom:20px;border:none;border-radius:8px;background:#3f3f46;color:white;">
            <div style="background:#27272a;padding:15px;border-radius:10px;margin-bottom:20px;">
                ${metodoHTML}
            </div>
            <h3 style="margin-bottom:20px;">
                Total: ₡${total.toLocaleString()}
            </h3>
            <button onclick="procesarCompraFinal()" class="btn-primary" style="width:100%;">
                Confirmar Compra
            </button>
        </div>
    `;
    openModal("Procesar Compra", formulario);
}
function procesarCompraFinal() {
    const credencial = document.getElementById("credencial").value;
    if (credencial !== "2345") {
        openModal("Credencial inválida", "El código de verificación médica es incorrecto.");
        return;
    }
    openModal(
        "Compra Exitosa",
        `<div style="text-align:center;padding:30px;">
            <div style="font-size:90px;color:#22c55e;margin-bottom:20px;">✔️</div>
            <h2 style="color:#22c55e;margin-bottom:15px;">Compra Exitosa</h2>
            <p style="font-size:1rem;line-height:1.7;color:#d4d4d8;">
                Su solicitud fue procesada correctamente.
            </p>
        </div>`
    );
    carrito = [];
    total = 0;
    actualizarCarrito();
}
// ========================
// PORTAL SEGURO
// ========================
function abrirPortalSeguro() {
    const clave = prompt("Ingrese clave de acceso:");
    if (clave === "12345") {
        openModal("Acceso autorizado", "Bienvenido al Portal Seguro de NeuroScience Division.");
    } else {
        openModal("Acceso denegado", "Clave de acceso incorrecta.");
    }
}
// ========================
// FLOATING ASSISTANT
// ========================
const assistant = document.getElementById('assistant');
const chatPanel = document.getElementById('chatPanel');
let offsetX, offsetY;
let isDragging = false;
let hasDragged = false;
let startX, startY;
let chatOpen = false;
let welcomeShown = false;
// Toggle chat panel open/close
function toggleChat() {
    chatOpen = !chatOpen;
    if (chatOpen) {
        chatPanel.classList.add('open');
        if (!welcomeShown) {
            addBotMessage("¡Hola! Soy el asistente de <strong>PharmaTech</strong>. ¿En qué puedo ayudarte hoy?");
            welcomeShown = true;
        }
        setTimeout(() => {
            document.getElementById('chatInput').focus();
        }, 350);
    } else {
        chatPanel.classList.remove('open');
    }
}
// Mouse events for drag + click detection
assistant.addEventListener('mousedown', (e) => {
    isDragging = true;
    hasDragged = false;
    startX = e.clientX;
    startY = e.clientY;
    offsetX = e.clientX - assistant.offsetLeft;
    offsetY = e.clientY - assistant.offsetTop;
    assistant.classList.add('dragging');
    e.preventDefault();
});
document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const dx = Math.abs(e.clientX - startX);
    const dy = Math.abs(e.clientY - startY);
    if (dx > 5 || dy > 5) {
        hasDragged = true;
    }
    assistant.style.left = (e.clientX - offsetX) + 'px';
    assistant.style.top = (e.clientY - offsetY) + 'px';
    assistant.style.right = 'auto';
    assistant.style.bottom = 'auto';
    if (chatOpen) {
        chatPanel.style.left = (e.clientX - offsetX - 330) + 'px';
        chatPanel.style.top = (e.clientY - offsetY - 570) + 'px';
        chatPanel.style.right = 'auto';
        chatPanel.style.bottom = 'auto';
    }
});
document.addEventListener('mouseup', () => {
    if (isDragging && !hasDragged) {
        toggleChat();
    }
    isDragging = false;
    assistant.classList.remove('dragging');
});
// Touch events for mobile
assistant.addEventListener('touchstart', (e) => {
    const touch = e.touches[0];
    isDragging = true;
    hasDragged = false;
    startX = touch.clientX;
    startY = touch.clientY;
    offsetX = touch.clientX - assistant.offsetLeft;
    offsetY = touch.clientY - assistant.offsetTop;
    assistant.classList.add('dragging');
}, { passive: true });
document.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    const touch = e.touches[0];
    const dx = Math.abs(touch.clientX - startX);
    const dy = Math.abs(touch.clientY - startY);
    if (dx > 5 || dy > 5) {
        hasDragged = true;
    }
    assistant.style.left = (touch.clientX - offsetX) + 'px';
    assistant.style.top = (touch.clientY - offsetY) + 'px';
    assistant.style.right = 'auto';
    assistant.style.bottom = 'auto';
    if (chatOpen) {
        chatPanel.style.left = (touch.clientX - offsetX - 330) + 'px';
        chatPanel.style.top = (touch.clientY - offsetY - 570) + 'px';
        chatPanel.style.right = 'auto';
        chatPanel.style.bottom = 'auto';
    }
}, { passive: true });
document.addEventListener('touchend', () => {
    if (isDragging && !hasDragged) {
        toggleChat();
    }
    isDragging = false;
    assistant.classList.remove('dragging');
});
// ========================
// CHAT FUNCTIONS
// ========================
function addUserMessage(text) {
    const messages = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'msg user';
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}
function addBotMessage(html) {
    const messages = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'msg bot';
    div.innerHTML = html;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
}
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    addUserMessage(text);
    input.value = '';
    const thinking = addBotMessage(
        '<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span> Procesando...'
    );
    try {
        const res = await fetch('/preguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: text })
        });
        const data = await res.json();
        thinking.innerHTML = data.respuesta;
    } catch (error) {
        console.error("Error de conexión con el núcleo de IA:", error);
        thinking.innerHTML = "No se pudo conectar con el servidor. Asegúrate de que el backend esté corriendo.";
    }
}
// Enter key to send message
document.getElementById('chatInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
