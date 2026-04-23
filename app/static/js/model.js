// /* app/static/js/model.js */

// // ================= MODEL MODULE =================

// // CHANGED: moved model-related state here
// export const ModelApp = {
//     model: null,
//     classNames: [],
//     classIndex: null
// };

// const MODEL_URL   = '/static/models/mobilenet-slsl-1/model.json';
// const CLASSES_URL = '/static/models/mobilenet-slsl-1/class_names.json';

// const INPUT_SIZE           = 128;
// const CONFIDENCE_THRESHOLD = 0.55;

// // CHANGED: moved initModel here
// export async function initModel(setRecogStatus) {
//     setRecogStatus('Loading model…');

//     const res = await fetch(CLASSES_URL);
//     if (!res.ok) throw new Error('Failed to load class_names.json');

//     const raw = await res.json();
//     ModelApp.classNames = raw.class_names;
//     ModelApp.classIndex = raw.class_index;

//     ModelApp.model = await tf.loadGraphModel(MODEL_URL);

//     tf.tidy(() => {
//         const dummy = tf.zeros([1, INPUT_SIZE, INPUT_SIZE, 3]);
//         const out = ModelApp.model.predict(dummy);
//         if (Array.isArray(out)) out.forEach(t => t.dispose());
//         else out.dispose();
//     });

//     setRecogStatus('Model ready — press ▶ to start');
// }

// // CHANGED: moved inference logic here
// export async function captureAndInfer(video, canvas, setRecogStatus, appendToTranscript) {
//     if (!video || !canvas || !video.videoWidth) {
//         setRecogStatus('Video not ready for capture');
//         return;
//     }

//     canvas.width  = INPUT_SIZE;
//     canvas.height = INPUT_SIZE;

//     const ctx = canvas.getContext('2d');
//     ctx.drawImage(video, 0, 0, INPUT_SIZE, INPUT_SIZE);

//     const tensor = tf.tidy(() => {
//         return tf.browser.fromPixels(canvas)
//             .toFloat()
//             .div(255.0)
//             .expandDims(0);
//     });

//     let predTensor   = null;
//     let extraTensors = [];

//     try {
//         const out = ModelApp.model.predict(tensor);

//         if (Array.isArray(out)) {
//             predTensor   = out[0];
//             extraTensors = out.slice(1);
//         } else {
//             predTensor = out;
//         }

//         const predictions = await predTensor.data();

//         let maxIdx = 0;
//         for (let i = 1; i < predictions.length; i++) {
//             if (predictions[i] > predictions[maxIdx]) maxIdx = i;
//         }

//         const confidence = predictions[maxIdx];
//         const letter     = ModelApp.classNames[maxIdx] ?? String(maxIdx);

//         if (confidence < CONFIDENCE_THRESHOLD) {
//             setRecogStatus(
//                 `No confident prediction (best: ${letter} @ ${(confidence * 100).toFixed(1)}%)`
//             );
//             return;
//         }

//         appendToTranscript(letter);
//         setRecogStatus(`Detected: ${letter} (${(confidence * 100).toFixed(1)}%)`);
        
//         return letter; // CHANGED: return value for UI update
//     } catch (err) {
//         console.error('Inference error:', err);
//         setRecogStatus('⚠ Inference error: ' + err.message);
//     } finally {
//         tensor.dispose();
//         if (predTensor) { try { predTensor.dispose(); } catch (_) {} }
//         extraTensors.forEach(t => { try { t.dispose(); } catch (_) {} });
//     }
// }