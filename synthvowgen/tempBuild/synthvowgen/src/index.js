import path from "path";
import _formants from "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/CSV2/timit-vowels_formant_estimation_subset_8k.json";
import { exportSignal } from "./lib/makeVowel";
import * as fs from "fs";
let exportFolder = "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/AUDIO/synth_vows_new_subset";
const pyMakewavHelper = "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/synthvowgen/src/helper/makewav";
if (!fs.existsSync(exportFolder)) {
    fs.mkdirSync(exportFolder);
}
const data = _formants;
const formants = data.data;
for (let i = 0; i < formants.length; i++) {
    let f = formants[i];
    let fName = `${f.vowel_type}_${f.idx}_${f.person}_${f.sex}_${Math.round(f.pitch_org_praat)}`;
    let fArr = [
        f.f1_mean_org_praat,
        f.f2_mean_org_praat,
        f.f3_mean_org_praat,
        f.f4_mean_org_praat,
    ];
    let expPath = path.join(exportFolder, fName);
    console.log(fName, `; ${formants.length - i - 1} remaining`);
    exportSignal(f.pitch_org_praat, fArr, expPath, pyMakewavHelper);
}
//# sourceMappingURL=index.js.map