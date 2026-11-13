"""Crea le versioni web (webp) delle immagini usate nel sito, dentro img/."""
import hashlib
import os
import re
import subprocess

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _name(src, suffix):
    base = os.path.splitext(os.path.basename(src))[0]
    base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:40]
    h = hashlib.md5(src.encode()).hexdigest()[:6]
    return f"{base}-{h}{suffix}.webp"


def web_image(src, slug, max_w=2000, max_h=2000, suffix=""):
    """Ritorna (percorso web, larghezza, altezza)."""
    out_dir = os.path.join(ROOT, "img", slug)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, _name(src, suffix))
    rel = os.path.relpath(out, ROOT)
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(os.path.join(ROOT, src)):
        with Image.open(out) as im:
            return rel, im.width, im.height
    with Image.open(os.path.join(ROOT, src)) as im:
        im.draft("RGB", (max_w, max_h))
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((max_w, max_h), Image.LANCZOS)
        im.save(out, "WEBP", quality=80, method=5)
        return rel, im.width, im.height


def web_video(src, slug):
    out_dir = os.path.join(ROOT, "img", slug)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.splitext(os.path.basename(src))[0] + ".mp4")
    if not os.path.exists(out):
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, src),
            "-an", "-vf", "scale='min(1280,iw)':-2", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "28", "-movflags", "+faststart", "-pix_fmt", "yuv420p", out,
        ], check=True)
    poster, _, _ = web_image_from_video(out, slug)
    return os.path.relpath(out, ROOT), poster


def web_image_from_video(video, slug):
    out = os.path.splitext(video)[0] + "-poster.webp"
    if not os.path.exists(out):
        tmp = out + ".png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3", "-i", video, "-frames:v", "1", tmp], check=True)
        with Image.open(tmp) as im:
            im.convert("RGB").save(out, "WEBP", quality=78)
        os.remove(tmp)
    with Image.open(out) as im:
        return os.path.relpath(out, ROOT), im.width, im.height
