document.getElementById('tripForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("¡Formulario interceptado correctamente!");

    const modeloInput = document.getElementById('modelo').value.trim();
    const payload = {
        consumo_medio: parseFloat(document.getElementById('consumo_medio').value),
        capacidad_tanque: parseFloat(document.getElementById('capacidad_tanque').value),
        distancia_recorrida: parseFloat(document.getElementById('distancia_recorrida').value),
        combustible_restante: parseFloat(document.getElementById('combustible_restante').value),
        precio_gasolina: parseFloat(document.getElementById('precio_gasolina').value),
        electrico: document.getElementById('electrico').checked
    };

    if (modeloInput !== "") {
        payload.modelo = modeloInput;
    }

    console.log("Datos a enviar:", payload);

    try {
        const response = await fetch('/api/v1/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log("Respuesta del servidor recibida, status:", response.status);

        if (!response.ok) {
            const errData = await response.json();
            console.error("Error devuelto por la API:", errData);
            throw new Error(JSON.stringify(errData.detail) || 'Error en la API');
        }

        const data = await response.json();
        console.log("Datos procesados correctamente:", data);

        const box = document.getElementById('resultBox');
        const content = document.getElementById('resultContent');
        
        box.classList.remove('hidden');
        content.innerHTML = `
            <p><strong>Veredicto:</strong> <span class="text-cyan-300 uppercase">${data.veredicto}</span></p>
            <p><strong>Score de Eficiencia:</strong> <span class="text-emerald-400 font-bold">${data.score_eficiencia} / 100</span></p>
            <p class="bg-slate-900 p-2.5 rounded border border-slate-800 text-slate-200"><em>${data.mensaje}</em></p>
            <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800 text-xs text-slate-400">
                <p>Litros Consumidos: <span class="text-white">${data.litros_consumidos} L</span></p>
                <p>Litros Restantes: <span class="text-white">${data.litros_restantes} L</span></p>
                <p>Autonomía Restante: <span class="text-white">${data.autonomia_restante !== null ? data.autonomia_restante + ' km' : 'N/A (Eléctrico)'}</span></p>
                <p>Dinero Gastado: <span class="text-white">${data.dinero_gastado} €</span></p>
            </div>
        `;
    } catch (error) {
        console.error("Error en el catch:", error);
        const box = document.getElementById('resultBox');
        const content = document.getElementById('resultContent');
        box.classList.remove('hidden');
        content.innerHTML = `<p class="text-red-400"><strong>Error:</strong> ${error.message}</p>`;
    }
});