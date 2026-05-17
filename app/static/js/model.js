// import handlandmarker for javascript
import {
    HandLandmarker,
    FilesetResolver,
} from 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs';


// set the model file paths
const MODEL_URL = '/static/models/mlp2/model.json';
const CLASSES_URL = '/static/models/mlp2/class_names.json';

// confidence threshold - 80% as per FR23 but can be changed if necessary
export const CONFIDENCE_THRESHOLD = 0.8;

export let model = null;
export let classNames = [];
export let classIndex = {};
let handLandmarker = null;

function normalizeLandmarks(landmarks) {
    // landmarks: array of 21 x, y, z objects from MediaPipe

    // translate wrist to origin
    const wx = landmarks[0].x;
    const wy = landmarks[0].y;
    const wz = landmarks[0].z;

    const translated = landmarks.map(lm => [
        lm.x - wx,
        lm.y - wy,
        lm.z - wz,
    ]);

    // scale by norm of landmark 9 (middle finger MCP)
    const [l9x, l9y, l9z] = translated[9];
    const scale = Math.sqrt(l9x * l9x + l9y * l9y + l9z * l9z);

    // flatten to float32
    const out = new Float32Array(63);
    let i = 0;
    for (const [x, y, z] of translated) {
        out[i++] = scale > 1e-6 ? x / scale : x;
        out[i++] = scale > 1e-6 ? y / scale : y;
        out[i++] = scale > 1e-6 ? z / scale : z;
    }
    return out;
}


// initialize model
export async function initModel(setRecogStatus, onModelReady) {
    setRecogStatus('Loading hand landmarker…');

    // initiialize vision and handlandmarker - download from google since i didn't create the landmarker myself
    const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm'
    );
    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath:
                'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
            delegate: 'GPU'
        },
        numHands: 2,
        minHandDetectionConfidence: 0.3,
        minHandPresenceConfidence: 0.3,
        minTrackingConfidence: 0.3,
        runningMode: 'IMAGE' // needs work before changing to video
    });

    // fetch class names
    setRecogStatus('Loading class names…');
    const res = await fetch(CLASSES_URL);
    if (!res.ok) throw new Error('Failed to load class_names.json');
    const raw = await res.json();
    classNames = raw.class_names;
    classIndex = raw.class_index;

    // load tfjs model
    setRecogStatus('Loading TF model…');
    model = await tf.loadLayersModel(MODEL_URL);

    tf.tidy(() => {
        model.predict(tf.zeros([1, 126]));
    });

    setRecogStatus('Model ready — press ▶ to start');
    onModelReady();
}

// heart of the program - capture a frame when required, extract landmarks from it, append to detected letter and transcript
export async function captureAndInfer(setRecogStatus, appendToTranscript, onLetterDetected = null) {
    const video = document.getElementById('localVideo');

    if (!model || !handLandmarker) {
        setRecogStatus('Model not loaded! Please wait.');
        return;
    }
    if (!video || !video.videoWidth) {
        setRecogStatus('Video not ready for capture');
        return;
    }

    // run handlandmarker on the live frame
    let result;
    try {
        result = handLandmarker.detect(video);
        if (!result.landmarks || result.landmarks.length === 0) {
            setRecogStatus('No hand detected in frame');
            return;
        }

    } catch (err) {
        console.error('Landmark detection error:', err);
        setRecogStatus('Landmark error: ' + err.message);
        return;
    }

    // require exactly 2 hands, since all of our signs use 2 hands
    if (result.landmarks.length !== 2) {
        setRecogStatus('Need exactly 2 hands in frame');
        return;
    }

    // identify left and right hands by handedness label
    let leftLandmarks = null;
    let rightLandmarks = null;

    for (let h = 0; h < result.landmarks.length; h++) {
        const label = result.handednesses?.[h]?.[0]?.categoryName;
        if (label === 'Left') leftLandmarks = result.landmarks[h];
        if (label === 'Right') rightLandmarks = result.landmarks[h];
    }

    if (!leftLandmarks || !rightLandmarks) {
        setRecogStatus('Could not identify both hands');
        return;
    }

// normalize each hand independently
    const leftFeatures = normalizeLandmarks(leftLandmarks);  
    const rightFeatures = normalizeLandmarks(rightLandmarks); 

    // concatenate both hands
    const combined = new Float32Array(126);
    combined.set(leftFeatures, 0);
    combined.set(rightFeatures, 63);

    // single inference call per frame
    const inputTensor = tf.tensor2d(combined, [1, 126]);
    let predTensor = null;


// prediction
    try {
        predTensor = model.predict(inputTensor);
        const predictions = await predTensor.data();

        let maxIdx = 0;
        for (let i = 1; i < predictions.length; i++) {
            if (predictions[i] > predictions[maxIdx]) maxIdx = i;
        }

        const confidence = predictions[maxIdx];
        const letter = classNames[maxIdx] ?? String(maxIdx);

        // if not fully confident, display a small message anyway - mostly useful for testing
        if (confidence < CONFIDENCE_THRESHOLD) {
            setRecogStatus(`No confident prediction (best: ${letter} @ ${(confidence * 100).toFixed(1)}%)`);
            return;
        }

        // append to detected letter
        const letterEl = document.getElementById('detectedLetter');
        if (letterEl) letterEl.textContent = letter;

        appendToTranscript(letter);
        if (onLetterDetected) onLetterDetected(letter);
        setRecogStatus(`${letter} (${(confidence * 100).toFixed(1)}%)`);

    } catch (err) {
        console.error('Inference error:', err);
        setRecogStatus('Inference error: ' + err.message);
    } finally {
        inputTensor.dispose();
        if (predTensor) { try { predTensor.dispose(); } catch (_) { } }
    }
}
