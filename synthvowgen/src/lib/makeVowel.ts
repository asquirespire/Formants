import * as KlattSyn from "klatt-syn";
import * as Utils from "./utils";
import * as WindowFunctions from "dsp-collection/signal/WindowFunctions";
import { AppParms, getMyAudioParms } from "./vowelParams";
import * as fs from "fs";
import * as cp from "child_process";

function synthesizeSignal(appParms: AppParms): Float64Array {
	let signal: Float64Array | undefined;
	let rate: number;

	signal = KlattSyn.generateSound(appParms.mParms, appParms.fParmsA);
	rate = appParms.mParms.sampleRate;

	Utils.fadeAudioSignalInPlace(
		signal,
		appParms.fadingDuration * rate,
		WindowFunctions.hannWindow
	);

	return signal;
}

export function exportSignal(
	pitch: number,
	formants: Array<number>,
	dstfile: string,
	pyMakewavHelper: string
) {
	if (fs.existsSync(`${dstfile}.wav`)) return;

	let rate: number = 16000;
	let duration: number = 1.7;
	let signal: Float64Array | undefined;

	const params = getMyAudioParms(
		rate, // fs
		duration, // dur
		pitch, // pitch
		// [300, 870, 2240, 0, 0, 0], // formants freqs
		formants, // formants freqs
		// [76, 102, 72, 102, 816, 596], // formants bw
		[76, 102, 72], // formants bw
		// [0, -8, -15, -19, -30, -35] // formants db
		[0, -8, -15] // formants db
	);

	signal = synthesizeSignal(params);

	if (!signal) {
		console.log("signal synthesis failed: ", dstfile);
		return;
	}

	fs.writeFileSync(dstfile, signal.toString(), "utf-8");

	cp.execSync(`${pyMakewavHelper} ${dstfile}`);
}
