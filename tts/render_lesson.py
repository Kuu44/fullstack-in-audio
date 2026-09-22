"""Render one lesson markdown file to mp3 with edge-tts.

Voice and pace match the course contract: en-US-AndrewNeural at -14%.
Strips the tts:skip block, headings, and markdown chrome. [pause] becomes
a short silence. Exits nonzero if the result is under 28 minutes.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

VOICE = "en-US-AndrewNeural"
RATE = "-14%"
MIN_SECONDS = 28 * 60
SUBSTITUTIONS = (
    ("Patan Dhoka", "Pah-tahn Doe-kah"),
    ("Subhechha", "Soo-bhek-cha"),
    ("Niyalo", "Nee-yah-lo"),
    ("Mato", "Mah-toe"),
    ("FDE", "F D E"),
)


def spoken_text(markdown: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.S)
    text = re.sub(r"<!--\s*tts:skip\s*-->.*?<!--\s*/tts:skip\s*-->", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^#+\s+.*$", "", text, flags=re.M)
    text = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("*", "").replace("`", "")
    for source, target in SUBSTITUTIONS:
        text = text.replace(source, target)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def word_count(text: str) -> int:
    spoken = text.replace("[pause]", " ")
    return len(re.findall(r"\b[\w']+\b", spoken))


def chunks(text: str, limit: int = 1800) -> list[str]:
    parts: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if len(block) <= limit:
            parts.append(block)
            continue
        sentence = re.split(r"(?<=[.!?])\s+", block)
        current = ""
        for piece in sentence:
            if current and len(current) + len(piece) + 1 > limit:
                parts.append(current)
                current = piece
            else:
                current = f"{current} {piece}".strip()
        if current:
            parts.append(current)
    return parts


def silence(path: Path, ms: int = 700) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=24000:cl=mono",
            "-t",
            f"{ms / 1000:.3f}",
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


async def render_piece(text: str, path: Path) -> None:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            await asyncio.wait_for(
                edge_tts.Communicate(text, VOICE, rate=RATE).save(str(path)),
                timeout=90,
            )
            return
        except Exception as error:
            last_error = error
            print(f"retry {attempt + 1}: {error}", flush=True)
            await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to render: {text[:80]}") from last_error


def duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


async def render(source: Path, dest: Path) -> None:
    text = spoken_text(source.read_text(encoding="utf-8"))
    count = word_count(text)
    minutes = count / 146
    print(f"spoken words: {count}", flush=True)
    print(f"estimate: {minutes:.1f} min at 146 wpm", flush=True)
    if "--dry-run" in sys.argv:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        silence_path = folder / "pause.mp3"
        silence(silence_path)
        files: list[Path] = []
        index = 0
        for part in chunks(text):
            bits = re.split(r"\s*\[pause\]\s*", part)
            for bit_index, bit in enumerate(bits):
                bit = bit.strip()
                if bit:
                    out = folder / f"{index:04d}.mp3"
                    print(f"render {index:04d} ({len(bit)} chars)", flush=True)
                    await render_piece(bit, out)
                    files.append(out)
                    index += 1
                if bit_index < len(bits) - 1:
                    files.append(silence_path)

        listing = folder / "list.txt"
        listing.write_text(
            "".join(f"file '{path.as_posix()}'\n" for path in files),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(listing),
                "-c:a",
                "libmp3lame",
                "-q:a",
                "4",
                str(dest),
            ],
            check=True,
            capture_output=True,
        )

    seconds = duration_seconds(dest)
    print(f"duration: {seconds / 60:.1f} min", flush=True)
    if seconds < MIN_SECONDS:
        print("under 28 minutes", file=sys.stderr)
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=False)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit("ffmpeg and ffprobe are required")
    if args.dry_run:
        text = spoken_text(args.source.read_text(encoding="utf-8"))
        count = word_count(text)
        print(f"spoken words: {count}")
        print(f"estimate: {count / 146:.1f} min at 146 wpm")
        return
    if args.out is None:
        sys.exit("--out is required unless --dry-run")
    asyncio.run(render(args.source, args.out))


if __name__ == "__main__":
    main()
