document.addEventListener('DOMContentLoaded', function() {
    
    const gpsBtn = document.getElementById('useGPS');
    if (gpsBtn) {
        gpsBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                gpsBtn.innerHTML = ' Locating...';
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        
                        // In production: reverse geocode to get address
                        document.querySelector('#id_location_address').value = 
                            `GPS: ${lat.toFixed(6)}, ${lng.toFixed(6)}`;
                        
                        gpsBtn.innerHTML = ' Location captured';
                        gpsBtn.classList.remove('btn-outline-primary');
                        gpsBtn.classList.add('btn-success');
                    },
                    function(error) {
                        alert('Unable to get your location. Please enter address manually.');
                        gpsBtn.innerHTML = ' Use my current location';
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }
    
    const voiceBtn = document.getElementById('voiceInput');
    if (voiceBtn && 'webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-ZA'; // South African English
        recognition.continuous = false;
        
        voiceBtn.addEventListener('click', function() {
            voiceBtn.innerHTML = '🎤 Listening...';
            recognition.start();
        });
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.querySelector('#id_description').value += transcript;
            voiceBtn.innerHTML = '🎤 Tap to speak (isiZulu/English)';
        };
        
        recognition.onerror = function(event) {
            alert('Voice recognition error. Please type your description.');
            voiceBtn.innerHTML = '🎤 Tap to speak (isiZulu/English)';
        };
    } else if (voiceBtn) {
        voiceBtn.disabled = true;
        voiceBtn.title = 'Voice input not supported in this browser';
    }
    
    const categoryOptions = document.querySelectorAll('.category-option');
    const categorySelect = document.querySelector('#id_category');
    
    categoryOptions.forEach(option => {
        option.addEventListener('click', function() {
            
            categoryOptions.forEach(opt => opt.classList.remove('selected'));
            
            this.classList.add('selected');
            
            if (categorySelect) {
                categorySelect.value = this.dataset.value;
            }
        });
    });
    
    const cameraBtn = document.getElementById('cameraBtn');
    const galleryBtn = document.getElementById('galleryBtn');
    const photoInput = document.querySelector('#id_photo');
    
    if (cameraBtn && photoInput) {
        cameraBtn.addEventListener('click', function() {
            photoInput.setAttribute('capture', 'camera');
            photoInput.click();
        });
    }
    
    if (galleryBtn && photoInput) {
        galleryBtn.addEventListener('click', function() {
            photoInput.removeAttribute('capture');
            photoInput.click();
        });
    }
    
    const form = document.getElementById('reportForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    }
});