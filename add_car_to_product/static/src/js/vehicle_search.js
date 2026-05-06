document.addEventListener('DOMContentLoaded', function () {
    const manufacturerSelect = document.getElementById('vehicle_manufacturer_select');
    const modelSelect = document.getElementById('vehicle_model_select');

    if (!manufacturerSelect || !modelSelect) return;

    manufacturerSelect.addEventListener('change', async function () {
        const manufacturerId = this.value;
        modelSelect.innerHTML = '<option value="">All models</option>';

        if (!manufacturerId) return;

        try {
            const response = await fetch('/add_car_to_product/get_vehicle_models', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: { manufacturer_id: manufacturerId },
                }),
            });
            const data = await response.json();
            (data.result || []).forEach(function (model) {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = model.name;
                modelSelect.appendChild(option);
            });
        } catch (e) {
            console.error('Failed to load vehicle models', e);
        }
    });
});
