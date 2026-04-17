/* ================= TF MODULE =================
   WHY THIS FILE EXISTS:
   - Separates ML logic from WebRTC + UI logic
   - Makes model loading reusable
   - Keeps call.js focused on call + signaling only
================================================ */

const TFConfig = {
    MODEL_URL: '/static/models/mobilenet-slsl-1/model.json',
    CLASSES_URL: '/static/models/mobilenet-slsl-1/class_names.json',
    INPUT_SIZE: 128,
    CONFIDENCE_THRESHOLD: 0.55
};

// Holds model state privately inside module
const TFState = {
    model: null,
    classNames: []
};

/* -------------------------------------------------
   LOAD MODEL + CLASSES
   WHY:
   - Centralizes model loading logic
   - Avoids duplicate fetch/load in main file
------------------------------------------------- */
export async function loadModel(setStatusCallback) {
    setStatusCallback?.('Loading model…');

    // Load class names
    const res = await fetch(TFConfig.CLASSES_URL);
    if (!res.ok) throw new Error('Failed to load class_names.json');

    const raw = await res.json();

    // WHY: ensures consistent array format regardless of JSON shape
    TFState.classNames = Array.isArray(raw) ? raw : Object.values(raw);

    // Load TensorFlow graph model
    TFState.model = await tf.loadGraphModel(TFConfig.MODEL_URL);

    /* WHY: warm-up inference avoids first-request lag during real use */
    tf.tidy(() => {
        const dummy = tf.zeros([1, TFConfig.INPUT_SIZE, TFConfig.INPUT_SIZE, 3]);
        const out = TFState.model.predict(dummy);

        // WHY: prevent memory leaks from warmup tensors
        if (Array.isArray(out)) out.forEach(t => t.dispose());
        else out.dispose();
    });

    setStatusCallback?.('Model ready');
    return true;
}

/* -------------------------------------------------
   RUN INFERENCE FROM VIDEO FRAME
   WHY:
   - isolates ML pipeline from UI code
   - makes testing easier
------------------------------------------------- */
export async function runInference(video, canvas, setStatusCallback) {
    if (!TFState.model) {
        setStatusCallback?.('Model not loaded');
        return null;
    }

    if (!video || !canvas || !video.videoWidth) {
        setStatusCallback?.('Video not ready');
        return null;
    }

    canvas.width = TFConfig.INPUT_SIZE;
    canvas.height = TFConfig.INPUT_SIZE;

    const ctx = canvas.getContext('2d');

    /* WHY:
       - we intentionally DO NOT mirror here
       - model expects training-aligned orientation */
    ctx.drawImage(video, 0, 0, TFConfig.INPUT_SIZE, TFConfig.INPUT_SIZE);

    // Convert image → tensor
    const tensor = tf.tidy(() => {
        return tf.browser.fromPixels(canvas)
            .toFloat()
            .div(255.0)
            .expandDims(0);
    });

    let predTensor = null;
    let extraTensors = [];

    try {
        const out = TFState.model.predict(tensor);

        // WHY: handle both single-output and multi-output models
        if (Array.isArray(out)) {
            predTensor = out[0];
            extraTensors = out.slice(1);
        } else {
            predTensor = out;
        }

        const predictions = await predTensor.data();

        // Find max confidence index
        let maxIdx = 0;
        for (let i = 1; i < predictions.length; i++) {
            if (predictions[i] > predictions[maxIdx]) {
                maxIdx = i;
            }
        }

        const confidence = predictions[maxIdx];
        const letter = TFState.classNames[maxIdx] ?? String(maxIdx);

        // Filter low-confidence predictions
        if (confidence < TFConfig.CONFIDENCE_THRESHOLD) {
            setStatusCallback?.(
                `No confident prediction (${letter} @ ${(confidence * 100).toFixed(1)}%)`
            );
            return null;
        }

        return {
            letter,
            confidence
        };

    } catch (err) {
        setStatusCallback?.('Inference error: ' + err.message);
        throw err;
    } finally {
        /* WHY:
           - ensures GPU memory is freed every inference cycle */
        tensor.dispose();

        if (predTensor) {
            try { predTensor.dispose(); } catch (_) {}
        }

        extraTensors.forEach(t => {
            try { t.dispose(); } catch (_) {}
        });
    }
}

/* -------------------------------------------------
   OPTIONAL ACCESSORS (clean separation)
   WHY:
   - avoids exposing internal state directly
------------------------------------------------- */
export function getModel() {
    return TFState.model;
}

export function getClassNames() {
    return TFState.classNames;
}

export { TFConfig };