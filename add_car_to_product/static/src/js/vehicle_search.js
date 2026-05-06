document.addEventListener('DOMContentLoaded', function () {
    const manufacturerSelect = document.getElementById('vehicle_manufacturer_select');
    const modelSelect = document.getElementById('vehicle_model_select');

    if (!manufacturerSelect || !modelSelect) return;

    manufacturerSelect.addEventListener('change', async function () {
        const manufacturerId = this.value;
        const currentModelId = modelSelect.dataset.selected;

        modelSelect.innerHTML = '<option value="">All models</option>';

        if (!manufacturerId) return;

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
        const models = data.result || [];

        models.forEach(function (model) {
            const option = document.createElement('option');
            option.value = model.id;
            option.textContent = model.name;
            if (String(model.id) === String(currentModelId)) {
                option.selected = true;
            }
            modelSelect.appendChild(option);
        });
    });
});
