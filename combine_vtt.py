#This code has been created with the use of AI

#Declare current path
from pathlib import Path
import re

#Specify common hallucinations
HALLUCINATION_TEXTS = {
    "you",
    "Thank you.",
    "Thanks for watching",
}

#Establish timestamp format, especially for those under one hour
timestamp_re = re.compile(
    r"(?:(\d{2}):)?(\d{2}):(\d{2})\.(\d{3})\s+-->\s+(?:(\d{2}):)?(\d{2}):(\d{2})\.(\d{3})"
)

def timestamp_to_ms(h, m, s, ms):
    h = int(h) if h is not None else 0
    return (
        h * 3600000 +
        int(m) * 60000 +
        int(s) * 1000 +
        int(ms)
    )

def format_ts(ms):
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"

# Collect VTT files in current directory
vtt_files = sorted(Path(".").glob("*.vtt"))

if not vtt_files:
    print("No .vtt files found.")
    exit(1)

# Prompt user for speaker names
speaker_map = {}

print("\nEnter speaker names (press Enter to keep filename):\n")

for vtt_file in vtt_files:
    default_name = vtt_file.stem
    user_input = input(
        f'Speaker name for "{vtt_file.name}" [{default_name}]: '
    ).strip()

    speaker_map[vtt_file] = user_input if user_input else default_name

raw_entries = []

# Parse all VTT files
for vtt_file in vtt_files:
    speaker = speaker_map[vtt_file]

    with vtt_file.open(encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    i = 0
    while i < len(lines):
        match = timestamp_re.match(lines[i])
        if match:
            start_ms = timestamp_to_ms(
                match.group(1),
                match.group(2),
                match.group(3),
                match.group(4),
            )

            i += 1
            text_lines = []
            while i < len(lines) and lines[i]:
                text_lines.append(lines[i])
                i += 1

            text = " ".join(text_lines).strip()
            if text:
                raw_entries.append((start_ms, speaker, text))
        else:
            i += 1

# Sort chronologically
raw_entries.sort(key=lambda x: x[0])

# --- Remove hallucinations ---
filtered_entries = []
last_by_speaker = {}

for start_ms, speaker, text in raw_entries:
    # Remove hallucinations in common hallucinations list above
    if text in HALLUCINATION_TEXTS:
        continue

    # If the current text is the same as the previous text, and its the same
    # speaker, remove it. It is probably a hallucination. The first instance
    # stays, the rest is removed.
    if last_by_speaker.get(speaker) == text:
        continue

    filtered_entries.append((speaker, start_ms, text))
    last_by_speaker[speaker] = text

# Write output files
with open("transcript.txt", "w", encoding="utf-8") as compact, \
     open("transcript_mediawiki.txt", "w", encoding="utf-8") as spaced:

    for speaker, start_ms, text in filtered_entries:
        line = f"{speaker}: [{format_ts(start_ms)}] {text}\n"
        compact.write(line)
        spaced.write(line + "\n")
