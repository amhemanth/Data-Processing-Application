// UI Interaction Functions

// Tab Navigation (using Bootstrap)
// The tab switching is handled by Bootstrap's data-bs-toggle and data-bs-target attributes in the HTML.
// No custom JavaScript is needed for basic tab switching.

// Generic data processing function
async function processData(dataType, form) {
    const fileInput = form.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    if (!file) {
        alert(`Please select a ${dataType} file`);
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    // Get selected options
    const preprocessing = {};
    const augmentation = {};
    
    form.querySelectorAll(`input[id$="Preprocessing"]`).forEach(checkbox => {
        preprocessing[checkbox.name] = checkbox.checked;
    });
    
    form.querySelectorAll(`input[id$="Augmentation"]`).forEach(checkbox => {
        augmentation[checkbox.name] = checkbox.checked;
    });

    try {
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';

        // Upload file
        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const uploadResult = await uploadResponse.json();
        
        if (uploadResult.status === 'success') {
            // Process file
            const processResponse = await fetch('/preprocess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    preprocessing,
                    augmentation,
                    file_type: dataType === 'three-d' ? '3d' : dataType
                })
            });
            const processResult = await processResponse.json();
            
            if (processResult.status === 'success') {
                updatePreviews(dataType, processResult);
            } else {
                alert('Error processing file: ' + processResult.error);
            }
        } else {
            alert('Error uploading file: ' + uploadResult.error);
        }
    } catch (error) {
        console.error(`Error processing ${dataType}:`, error);
        alert(`Error processing ${dataType} file`);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Process ' + dataType.charAt(0).toUpperCase() + dataType.slice(1);
    }
}

// Preview Updates
function updatePreviews(dataType, result) {
    switch(dataType) {
        case 'text':
            updateTextPreviews(result);
            break;
        case 'image':
            updateImagePreviews(result);
            break;
        case 'audio':
            updateAudioPreviews(result);
            break;
        case 'three-d':
            update3DPreviews(result);
            break;
    }
}

function updateTextPreviews(result) {
    const previewContainer = document.getElementById('textPreviewContainer');
    if (!previewContainer) return;

    const previews = previewContainer.querySelectorAll('.text-preview');
    
    if (previews[0]) previews[0].textContent = result.original || 'No text available';
    if (previews[1]) previews[1].textContent = result.preprocessed || 'No preprocessed text available';
    if (previews[2]) previews[2].textContent = result.augmented || 'No augmented text available';
}

function updateImagePreviews(result) {
    const previewContainer = document.getElementById('imagePreviewContainer');
    if (!previewContainer) return;

    const previews = previewContainer.querySelectorAll('.img-preview');
    
    if (previews[0]) {
        previews[0].innerHTML = result.original ? 
            `<img src="${result.original}" alt="Original" class="img-preview">` : 
            'No image available';
    }
    if (previews[1]) {
        previews[1].innerHTML = result.preprocessed ? 
            `<img src="${result.preprocessed}" alt="Preprocessed" class="img-preview">` : 
            'No preprocessed image available';
    }
    if (previews[2]) {
        previews[2].innerHTML = result.augmented ? 
            `<img src="${result.augmented}" alt="Augmented" class="img-preview">` : 
            'No augmented image available';
    }
}

function updateAudioPreviews(result) {
    const previewContainer = document.getElementById('audioPreviewContainer');
    if (!previewContainer) return;

    const previews = previewContainer.querySelectorAll('.audio-preview');
    
    if (previews[0]) {
        previews[0].innerHTML = result.original ? 
            `<audio controls src="${result.original}" class="audio-player"></audio>
             <div id="originalWaveform" class="waveform"></div>
             <div id="originalSpectrogram" class="spectrogram"></div>` : 
            '<p>No audio available</p>';
        if (result.original) initializeWaveform('originalWaveform', result.original);
    }
    if (previews[1]) {
        previews[1].innerHTML = result.preprocessed ? 
            `<audio controls src="${result.preprocessed}" class="audio-player"></audio>
             <div id="preprocessedWaveform" class="waveform"></div>
             <div id="preprocessedSpectrogram" class="spectrogram"></div>` : 
            '<p>No preprocessed audio available</p>';
        if (result.preprocessed) initializeWaveform('preprocessedWaveform', result.preprocessed);
    }
    if (previews[2]) {
        previews[2].innerHTML = result.augmented ? 
            `<audio controls src="${result.augmented}" class="audio-player"></audio>
             <div id="augmentedWaveform" class="waveform"></div>
             <div id="augmentedSpectrogram" class="spectrogram"></div>` : 
            '<p>No augmented audio available</p>';
        if (result.augmented) initializeWaveform('augmentedWaveform', result.augmented);
    }
}

function update3DPreviews(result) {
    const viewers = {
        original: document.getElementById('originalModelViewer'),
        preprocessed: document.getElementById('preprocessedModelViewer'),
        augmented: document.getElementById('augmentedModelViewer')
    };

    // Clean up existing viewers
    Object.values(viewers).forEach(viewer => {
        if (viewer) {
            // Check if a canvas element exists within the viewer
            const canvas = viewer.querySelector('canvas');
            if (canvas) {
                // Attempt to dispose of the renderer if available (requires storing renderer instances)
                // For now, simply remove the canvas element
                canvas.remove();
            }
        }
    });

    // Update original viewer
    if (viewers.original) {
        if (result.original) {
            viewers.original.innerHTML = '';
            initializeModelViewer('originalModelViewer', result.original);
        } else {
            viewers.original.innerHTML = '<p>No 3D model available</p>';
        }
    }

    // Update preprocessed viewer
    if (viewers.preprocessed) {
        if (result.preprocessed) {
            viewers.preprocessed.innerHTML = '';
            initializeModelViewer('preprocessedModelViewer', result.preprocessed);
        } else {
            viewers.preprocessed.innerHTML = '<p>No preprocessed model available</p>';
        }
    }

    // Update augmented viewer
    if (viewers.augmented) {
        if (result.augmented) {
            viewers.augmented.innerHTML = '';
            initializeModelViewer('augmentedModelViewer', result.augmented);
        } else {
            viewers.augmented.innerHTML = '<p>No augmented model available</p>';
        }
    }
}

// 3D Model Viewer
function initializeModelViewer(containerId, modelUrl) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Clear container and show loading state
    container.innerHTML = '<div class="loading"></div>';

    // Create scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf8f9fa);

    // Create camera
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(5, 5, 5);
    camera.lookAt(0, 0, 0);

    // Create renderer
    const renderer = new THREE.WebGLRenderer({ 
        antialias: true,
        alpha: true 
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0xf8f9fa, 1);

    // Add lights
    const ambientLight = new THREE.AmbientLight(0x404040, 1);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    // Add controls
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 1;
    controls.maxDistance = 10;
    controls.maxPolarAngle = Math.PI;

    // Load model
    const loader = new THREE.OBJLoader();
    loader.load(
        modelUrl,
        function(object) {
            // Remove loading indicator
            container.innerHTML = '';
            container.appendChild(renderer.domElement);

            // Center and scale model
            const box = new THREE.Box3().setFromObject(object);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            object.position.sub(center);
            const maxDim = Math.max(size.x, size.y, size.z);
            const scale = 2 / maxDim;
            object.scale.multiplyScalar(scale);

            scene.add(object);

            // Position camera to view the entire model
            const distance = maxDim * 2;
            camera.position.set(distance, distance, distance);
            camera.lookAt(0, 0, 0);
            controls.update();
        },
        function(xhr) {
            // Progress updates if needed
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        function(error) {
            console.error('Error loading model:', error);
            container.innerHTML = '<p>Error loading 3D model</p>';
        }
    );

    // Handle window resize
    function onWindowResize() {
        if (!container) return;
        
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    }
    window.addEventListener('resize', onWindowResize);

    // Animation loop
    function animate() {
        if (!container) return;
        
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    // Cleanup function
    return function() {
        window.removeEventListener('resize', onWindowResize);
        if (container && renderer.domElement) {
            container.removeChild(renderer.domElement);
        }
        renderer.dispose();
    };
}

// Audio Waveform
function initializeWaveform(elementId, audioPath) {
    const container = document.getElementById(elementId);
    if (!container) return;

    const wavesurfer = WaveSurfer.create({
        container: container,
        waveColor: '#4a9eff',
        progressColor: '#1e88e5',
        cursorColor: '#1e88e5',
        barWidth: 2,
        barRadius: 3,
        cursorWidth: 1,
        height: 100,
        barGap: 3
    });

    wavesurfer.load(audioPath);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Form handlers
    const forms = {
        text: document.getElementById('textForm'),
        image: document.getElementById('imageForm'),
        audio: document.getElementById('audioForm'),
        'three-d': document.getElementById('threeDForm')
    };

    Object.entries(forms).forEach(([type, form]) => {
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                processData(type, this);
            });
        }
    });

    // Tab navigation (Bootstrap handles this via data attributes)
    // No custom click listeners are needed here.
    
    // Initial tab should be handled by Bootstrap's 'active' class in HTML.
    // If you need to programmatically activate a tab on load, use Bootstrap's JavaScript API:
    // var someTabTriggerEl = document.querySelector('#text-tab')
    // var tab = new bootstrap.Tab(someTabTriggerEl)
    // tab.show()

    // Add file input change handler for 3D model - shows loading indicator
    const threeDFileInput = document.getElementById('threeDFileInput');
    if (threeDFileInput) {
        threeDFileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const previewContainer = document.getElementById('threeDPreviewContainer');
                if (previewContainer) {
                    const originalPreview = previewContainer.querySelector('#originalModelViewer');
                    if (originalPreview) {
                        originalPreview.innerHTML = '<div class="loading"></div>';
                    }
                }
            }
        });
    }
}); 