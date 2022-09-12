import * as KlattSyn from "klatt-syn";
import * as Utils from "./utils";
import * as WindowFunctions from "dsp-collection/signal/WindowFunctions";
import { getMyAudioParms } from "./vowelParams";
import * as fs from "fs";
import * as cp from "child_process";
function synthesizeSignal(appParms) {
    let signal;
    let rate;
    signal = KlattSyn.generateSound(appParms.mParms, appParms.fParmsA);
    rate = appParms.mParms.sampleRate;
    Utils.fadeAudioSignalInPlace(signal, appParms.fadingDuration * rate, WindowFunctions.hannWindow);
    return signal;
}
export function exportSignal(pitch, formants, dstfile, pyMakewavHelper) {
    if (fs.existsSync(`${dstfile}.wav`))
        return;
    let rate = 16000;
    let duration = 1.7;
    let signal;
    const params = getMyAudioParms(rate, duration, pitch, formants, [76, 102, 72], [0, -8, -15]);
    signal = synthesizeSignal(params);
    if (!signal) {
        console.log("signal synthesis failed: ", dstfile);
        return;
    }
    fs.writeFileSync(dstfile, signal.toString(), "utf-8");
    cp.execSync(`${pyMakewavHelper} ${dstfile}`);
}
//# sourceMappingURL=makeVowel.js.map