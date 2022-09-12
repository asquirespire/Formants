import * as KlattSyn from "klatt-syn";
const defaultMainParms = {
    sampleRate: 44100,
    glottalSourceType: 1,
};
const defaultFrameParms = {
    duration: 3,
    f0: 247,
    flutterLevel: 0.25,
    openPhaseRatio: 0.7,
    breathinessDb: -25,
    tiltDb: 0,
    gainDb: NaN,
    agcRmsLevel: 0.18,
    nasalFormantFreq: NaN,
    nasalFormantBw: NaN,
    oralFormantFreq: [520, 1006, 2831, 3168, 4135, 5020],
    oralFormantBw: [76, 102, 72, 102, 816, 596],
    cascadeEnabled: true,
    cascadeVoicingDb: 0,
    cascadeAspirationDb: -25,
    cascadeAspirationMod: 0.5,
    nasalAntiformantFreq: NaN,
    nasalAntiformantBw: NaN,
    parallelEnabled: false,
    parallelVoicingDb: 0,
    parallelAspirationDb: -25,
    parallelAspirationMod: 0.5,
    fricationDb: -30,
    fricationMod: 0.5,
    parallelBypassDb: -99,
    nasalFormantDb: NaN,
    oralFormantDb: [0, -8, -15, -19, -30, -35],
};
const defaultAppParms = {
    mParms: defaultMainParms,
    fParmsA: [defaultFrameParms],
    fadingDuration: 0.05,
    windowFunctionId: "hann",
};
function decodeGlottalSourceType(s) {
    const i = KlattSyn.glottalSourceTypeEnumNames.indexOf(s);
    if (i < 0) {
        throw new Error(`Unknown glottal source type "${s}".`);
    }
    return i;
}
export function getMyAudioParms(sampleRate, duration, pitch, formants, formantsBw, formantsDb) {
    const appParms = defaultAppParms;
    const mParms = defaultMainParms;
    appParms.mParms = mParms;
    mParms.sampleRate = sampleRate;
    mParms.glottalSourceType = decodeGlottalSourceType("natural");
    const fParms = defaultFrameParms;
    appParms.fParmsA = [fParms];
    fParms.duration = duration;
    fParms.f0 = pitch;
    fParms.oralFormantFreq = formants;
    fParms.oralFormantBw = formantsBw;
    fParms.oralFormantDb = formantsDb;
    return appParms;
}
//# sourceMappingURL=vowelParams.js.map