let audioCtx = null;

export const initAudio = () => {
  if (!audioCtx) {
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
      console.error("Audio context creation failed:", e);
    }
  }
  if (audioCtx?.state === 'suspended') {
    audioCtx.resume();
  }
};

export const playTone = (freq, type = 'sine', dur = 0.2) => {
  if (!audioCtx) return;
  try {
    const o = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.setValueAtTime(0.3, audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + dur);
    o.connect(g);
    g.connect(audioCtx.destination);
    o.start();
    o.stop(audioCtx.currentTime + dur);
  } catch (e) {
    console.error("Tone play error:", e);
  }
};

export const playSFX = (type) => {
  if (!audioCtx) return;
  
  switch (type) {
    case 'click':
      playTone(400, 'sine', 0.1);
      break;
    case 'start':
      playTone(400, 'square', 0.1);
      setTimeout(() => playTone(600, 'square', 0.2), 100);
      break;
    case 'win':
      [440, 554, 659].forEach((f, i) => {
        setTimeout(() => playTone(f, 'triangle', 0.3), i * 100);
      });
      break;
    case 'hit':
      playTone(100, 'sawtooth', 0.3);
      break;
    default:
      break;
  }
};

export const speakWord = (text) => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  }
};
