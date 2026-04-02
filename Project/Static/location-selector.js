// Dynamic municipality/ward loading based on province selection
document.addEventListener('DOMContentLoaded', function() {
    const provinceSelect = document.getElementById('id_province');
    const municipalitySelect = document.getElementById('id_municipality');
    const wardSelect = document.getElementById('id_ward');
    
    if (provinceSelect) {
        provinceSelect.addEventListener('change', function() {
            const provinceId = this.value;
            
            // Load municipalities
            fetch(`/api/municipalities/?province=${provinceId}`)
                .then(response => response.json())
                .then(data => {
                    municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
                    data.forEach(mun => {
                        const option = new Option(mun.name, mun.id);
                        municipalitySelect.add(option);
                    });
                    // Reset ward dropdown
                    if (wardSelect) {
                        wardSelect.innerHTML = '<option value="">Select Ward (Optional)</option>';
                        wardSelect.disabled = true;
                    }
                });
        });
    }
    
    if (municipalitySelect) {
        municipalitySelect.addEventListener('change', function() {
            const munId = this.value;
            if (wardSelect && munId) {
                fetch(`/api/wards/?municipality=${munId}`)
                    .then(response => response.json())
                    .then(data => {
                        wardSelect.innerHTML = '<option value="">Select Ward (Optional)</option>';
                        data.forEach(ward => {
                            const option = new Option(`Ward ${ward.number}`, ward.id);
                            wardSelect.add(option);
                        });
                        wardSelect.disabled = false;
                    });
            } else if (wardSelect) {
                wardSelect.innerHTML = '<option value="">Select Ward (Optional)</option>';
                wardSelect.disabled = true;
            }
        });
    }
});