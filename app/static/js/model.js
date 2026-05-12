// /static/js/model.js

import {
    HandLandmarker,
    FilesetResolver,
} from 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs';

const MODEL_URL   = '/static/models/slsl_mp/model.json';
const CLASSES_URL = '/static/models/slsl_mp/class_names.json';
export const CONFIDENCE_THRESHOLD = 0.55;

export let model       = null;
export let classNames  = [];
export let classIndex  = {};
let handLandmarker     = null;

// ---------------------------------------------------------------------------
// Landmark normalisation — must match the Python training pipeline exactly:
//   1. Translate so wrist (landmark 0) is at origin
//   2. Scale so the farthest landmark from the origin = 1
//   Returns Float32Array of length 63 (21 landmarks × x,y,z)
// ---------------------------------------------------------------------------
function normalizeLandmarks(landmarks) {
    // landmarks: array of 21 {x, y, z} objects from MediaPipe
    const coords = landmarks.map(lm => [lm.x, lm.y, lm.z]);

    // Translate wrist to origin
    const [wx, wy, wz] = coords[0];
    const translated = coords.map(([x, y, z]) => [x - wx, y - wy, z - wz]);

    // Compute max distance from origin for scale normalisation
    let maxDist = 1e-6;
    for (const [x, y, z] of translated) {
        const d = Math.sqrt(x * x + y * y + z * z);
        if (d > maxDist) maxDist = d;
    }

    // Flatten to Float32Array
    const out = new Float32Array(63);
    let i = 0;
    for (const [x, y, z] of translated) {
        out[i++] = x / maxDist;
        out[i++] = y / maxDist;
        out[i++] = z / maxDist;
    }
    return out;
}

// ---------------------------------------------------------------------------
// Initialise MediaPipe Hand Landmarker + TF.js model
// ---------------------------------------------------------------------------
export async function initModel(setRecogStatus, onModelReady) {
    setRecogStatus('Loading hand landmarker…');

    // 1. MediaPipe Hand Landmarker (runs in browser via WASM)
    const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm'
    );
    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath:
                'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
            delegate: 'GPU',
        },
        numHands: 1,
        minHandDetectionConfidence: 0.3,
        minHandPresenceConfidence:  0.3,
        minTrackingConfidence:      0.3,
        runningMode: 'IMAGE',       // single-frame mode; switch to 'VIDEO' if calling per-frame
    });

    // 2. Class names
    setRecogStatus('Loading class names…');
    const res = await fetch(CLASSES_URL);
    if (!res.ok) throw new Error('Failed to load class_names.json');
    const raw = await res.json();
    classNames = raw.class_names;
    classIndex = raw.class_index;

    // 3. TF.js graph model
    setRecogStatus('Loading TF model…');
    model = await tf.loadGraphModel(MODEL_URL);

    // Warm-up with correct shape
    tf.tidy(() => {
        const dummy = tf.zeros([1, 63]);
        const out   = model.execute({ landmarks: dummy });
        if (Array.isArray(out)) out.forEach(t => t.dispose());
        else out.dispose();
    });

    setRecogStatus('Model ready — press ▶ to start');
    onModelReady();
}

// ---------------------------------------------------------------------------
// Capture one frame → extract landmarks → run classifier
// ---------------------------------------------------------------------------
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

    // --- Step 1: run Hand Landmarker on the live video frame ---
    let landmarks;
    try {
        const result = handLandmarker.detect(video);   // accepts HTMLVideoElement directly
        if (!result.landmarks || result.landmarks.length === 0) {
            setRecogStatus('No hand detected in frame');
            return;
        }
        landmarks = result.landmarks[0];               // first hand, array of 21 {x,y,z}
    } catch (err) {
        console.error('Landmark detection error:', err);
        setRecogStatus('Landmark error: ' + err.message);
        return;
    }

    // --- Step 2: normalise → [1, 63] tensor ---
    const featureVec = normalizeLandmarks(landmarks);  // Float32Array(63)

    let predTensor = null;
    const inputTensor = tf.tensor2d(featureVec, [1, 63]);
    try {
        // --- Step 3: run classifier ---
        const out = model.execute({ landmarks: inputTensor });
        predTensor = Array.isArray(out) ? out[0] : out;
        if (Array.isArray(out)) out.slice(1).forEach(t => t.dispose());

        const predictions = await predTensor.data();

        let maxIdx = 0;
        for (let i = 1; i < predictions.length; i++) {
            if (predictions[i] > predictions[maxIdx]) maxIdx = i;
        }

        const confidence = predictions[maxIdx];
        const letter     = classNames[maxIdx] ?? String(maxIdx);

        if (confidence < CONFIDENCE_THRESHOLD) {
            setRecogStatus(`No confident prediction (best: ${letter} @ ${(confidence * 100).toFixed(1)}%)`);
            return;
        }

        const letterEl = document.getElementById('detectedLetter');
        if (letterEl) letterEl.textContent = letter;

        appendToTranscript(letter);
        if (onLetterDetected) onLetterDetected(letter);
        setRecogStatus(`Detected: ${letter} (${(confidence * 100).toFixed(1)}%)`);

    } catch (err) {
        console.error('Inference error:', err);
        setRecogStatus('Inference error: ' + err.message);
    } finally {
        inputTensor.dispose();
        if (predTensor) { try { predTensor.dispose(); } catch (_) {} }
    }
}
