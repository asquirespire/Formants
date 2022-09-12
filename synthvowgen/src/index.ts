import path from "path";
import _formants from "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/CSV2/timit-vowels_formant_estimation_subset_8k.json";
import { exportSignal } from "./lib/makeVowel";
import * as fs from "fs";

// var t = {
// 	schema: {
// 		fields: [
// 			{ name: "slno", type: "integer" },
// 			{ name: "idx", type: "integer" },

// 			{ name: "person", type: "string" },
// 			{ name: "sex", type: "string" },

// 			{ name: "vowel_type", type: "string" },

// 			{ name: "pitch_org_praat", type: "number" },
// 			{ name: "f1_mean_org_praat", type: "number" },
// 			{ name: "f2_mean_org_praat", type: "number" },
// 			{ name: "f3_mean_org_praat", type: "number" },
// 			{ name: "f4_mean_org_praat", type: "number" },
// 		],
// 		primaryKey: ["slno"],
// 		pandas_version: "0.20.0",
// 	},
// };
interface Data {
	schema: {
		fields: Array<{ name: string; type: string }>;
		primaryKey: Array<string>;
		pandas_version: string;
	};
	data: Array<{
		slno: number;
		idx: number;

		person: string;
		sex: string;

		vowel_type: string;

		pitch_org_praat: number;
		f1_mean_org_praat: number;
		f2_mean_org_praat: number;
		f3_mean_org_praat: number;
		f4_mean_org_praat: number;
	}>;
}

let exportFolder =
	"/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/AUDIO/synth_vows_sample";
const pyMakewavHelper =
	"/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/synthvowgen/src/helper/makewav";

if (!fs.existsSync(exportFolder)) {
	fs.mkdirSync(exportFolder);
}

const data: Data = _formants;
const formants = data.data;

for (let i = 0; i < formants.length; i++) {
	let f = formants[i];

	let fName = `${f.vowel_type}_${f.idx}_${f.person}_${f.sex}_${Math.round(
		f.pitch_org_praat
	)}`;

	let fArr = [
		f.f1_mean_org_praat,
		f.f2_mean_org_praat,
		f.f3_mean_org_praat,
		f.f4_mean_org_praat,
	];

	let expPath = path.join(exportFolder, fName);

	console.log(fName, `; ${formants.length - i - 1} remaining`);

	exportSignal(f.pitch_org_praat, fArr, expPath, pyMakewavHelper);

	// if (i > 5) break;
}
