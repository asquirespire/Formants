import * as WindowFunctions from "dsp-collection/signal/WindowFunctions";
import * as Fft from "dsp-collection/signal/Fft";
import * as DspUtils from "dsp-collection/utils/DspUtils";
export function openSaveAsDialog(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const element = document.createElement("a");
    element.href = url;
    element.download = fileName;
    const clickEvent = new MouseEvent("click");
    element.dispatchEvent(clickEvent);
    setTimeout(() => URL.revokeObjectURL(url), 60000);
    document.dummySaveAsElementHolder = element;
}
export async function catchError(f, ...args) {
    try {
        const r = f(...args);
        if (r instanceof Promise) {
            await r;
        }
    }
    catch (error) {
        console.log(error);
        alert("Error: " + error);
    }
}
export function createAudioBufferFromSamples(samples, sampleRate, audioContext) {
    const buffer = audioContext.createBuffer(1, samples.length, sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < samples.length; i++) {
        data[i] = samples[i];
    }
    return buffer;
}
export function fadeAudioSignalInPlace(samples, fadeMargin, windowFunction) {
    const d = Math.min(samples.length, 2 * fadeMargin);
    for (let i = 0; i < d / 2; i++) {
        const w = windowFunction(i / d);
        samples[i] *= w;
        samples[samples.length - 1 - i] *= w;
    }
}
export function genSpectrum(samples, windowFunctionId) {
    const evenSamples = samples.subarray(0, 2 * Math.floor(samples.length / 2));
    const windowedSamples = WindowFunctions.applyWindowById(evenSamples, windowFunctionId);
    const complexSpectrum = Fft.fftRealSpectrum(windowedSamples);
    const logSpectrum = genLogSpectrum(complexSpectrum);
    return logSpectrum;
}
function genLogSpectrum(complexSpectrum) {
    const n = complexSpectrum.length;
    const a = new Float64Array(n);
    for (let i = 0; i < n; i++) {
        a[i] = DspUtils.convertAmplitudeToDb(complexSpectrum.getAbs(i));
    }
    return a;
}
export function findMaxFunctionValue(f, xVals) {
    let max = -Infinity;
    for (const x of xVals) {
        if (!isNaN(x)) {
            max = Math.max(max, f(x));
        }
    }
    return max;
}
//# sourceMappingURL=utils.js.map