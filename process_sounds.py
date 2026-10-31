import os
import glob
import wave
import struct
import math
import shutil

backup_dir = 'Sounds/backup_originals'
os.makedirs(backup_dir, exist_ok=True)

files = sorted(glob.glob('Sounds/YT*.wav'))
print(f'Found {len(files)} files to process:')
for f in files:
    print(' ', f)

# Step 1: Backup original files
for f in files:
    dest = os.path.join(backup_dir, os.path.basename(f))
    if not os.path.exists(dest):
        shutil.copy2(f, dest)
print('Backup to Sounds/backup_originals completed.\n')

def soft_limit(samples, threshold=0.92):
    out = []
    for x in samples:
        ax = abs(x)
        if ax <= threshold:
            out.append(x)
        else:
            excess = (ax - threshold) / (1.0 - threshold)
            compressed = threshold + (1.0 - threshold) * math.tanh(excess)
            out.append(math.copysign(min(0.999, compressed), x))
    return out

tgt_rms = -14.0
loaded = []

for f in files:
    w = wave.open(f, 'rb')
    n = w.getnframes()
    ch = w.getnchannels()
    fr = w.getframerate()
    sw = w.getsampwidth()
    d = w.readframes(n)
    w.close()

    raw = struct.unpack(f'<{n*ch}h', d)

    # 1. Convert to mono by averaging channels
    if ch == 2:
        mono = [(raw[i*2] + raw[i*2+1]) / (2.0 * 32768.0) for i in range(n)]
    else:
        mono = [float(x) / 32768.0 for x in raw]

    # 2. Measure perceived loudness (150ms shot blast window)
    pk = max(abs(x) for x in mono)
    onset = [i for i, x in enumerate(mono) if abs(x) > 0.05 * pk][0]
    win = mono[onset:min(n, onset + int(0.15 * fr))]
    rms = (sum(x*x for x in win) / len(win)) ** 0.5
    current_rms_db = 20 * math.log10(rms)
    gain = 10 ** ((tgt_rms - current_rms_db) / 20.0)

    # 3. Apply gain and smooth soft limiter (prevents harsh digital clipping)
    scaled = [x * gain for x in mono]
    limited = soft_limit(scaled, threshold=0.92)

    # 4. Find peak sample index
    lim_pk = max(abs(x) for x in limited)
    pk_idx = [i for i, x in enumerate(limited) if abs(x) == lim_pk][0]

    loaded.append({
        'file': f,
        'fr': fr,
        'samples': limited,
        'pk_idx': pk_idx,
        'lim_pk': lim_pk,
        'gain_db': 20 * math.log10(gain),
    })

# Step 5: Find the latest peak index across all files to align max amplitudes
target_pk_idx = max(item['pk_idx'] for item in loaded)
print(f'Aligning all max amplitudes to sample index: {target_pk_idx} ({target_pk_idx / 44100.0 * 1000:.2f} ms)\n')

# Step 6: Prepend silence and write back mono 16-bit WAV
for item in loaded:
    silence_len = target_pk_idx - item['pk_idx']
    aligned = [0.0] * silence_len + item['samples']

    # Verify peak index matches target exactly
    new_pk = max(abs(x) for x in aligned)
    new_pk_idx = [i for i, x in enumerate(aligned) if abs(x) == new_pk][0]
    assert new_pk_idx == target_pk_idx, f"Mismatch in {item['file']}: {new_pk_idx} vs {target_pk_idx}"

    # Convert to 16-bit PCM integer
    pcm16 = [int(round(max(-1.0, min(1.0, x)) * 32767.0)) for x in aligned]
    out_bytes = struct.pack(f'<{len(pcm16)}h', *pcm16)

    out_w = wave.open(item['file'], 'wb')
    out_w.setnchannels(1)
    out_w.setsampwidth(2)
    out_w.setframerate(item['fr'])
    out_w.writeframes(out_bytes)
    out_w.close()

    print(f"Wrote {item['file']}: mono, added {silence_len:4d} smp silence ({silence_len/item['fr']*1000:4.1f}ms), peak at {new_pk_idx} ({new_pk_idx/item['fr']*1000:.2f}ms), gain={item['gain_db']:+5.1f}dB")

print('\nAll files successfully processed and written!')
