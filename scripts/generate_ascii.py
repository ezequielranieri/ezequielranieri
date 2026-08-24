#!/usr/bin/env python3
"""
Generate ASCII art from an image using Pillow.
Usage: python scripts/generate_ascii.py <input_image> <output_text_file>
"""

import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def image_to_ascii(input_path: str, output_path: str, width: int = 58, char_aspect: float = 0.48) -> None:
    """Convert image to ASCII art and save as plain text."""
    # Load image in grayscale
    img = Image.open(input_path).convert("L")

    # Apply autocontrast (cutoff=2)
    img = ImageOps.autocontrast(img, cutoff=2)

    # Increase contrast by 1.3x
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)

    # Apply SHARPEN filter
    img = img.filter(ImageFilter.SHARPEN)

    # Resize to target width, proportional height with char_aspect factor
    orig_w, orig_h = img.size
    new_h = int(orig_h / orig_w * width * char_aspect)
    img = img.resize((width, new_h), Image.Resampling.LANCZOS)

    # Character ramp from light/sparse to dark/dense (10 chars, index 0-9)
    ramp = " .:-=+*#%@"

    # Map each pixel to a character: index = int(pixel / 255 * 9)
    pixels = img.load()
    ascii_lines = []
    for y in range(new_h):
        line = "".join(ramp[int(pixels[x, y] / 255 * 9)] for x in range(width))
        ascii_lines.append(line)

    # Save as plain text
    output = "\n".join(ascii_lines)
    Path(output_path).write_text(output, encoding="utf-8")
    print(f"ASCII art saved to {output_path} ({width}x{new_h} chars)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/generate_ascii.py <input_image> <output_text_file>")
        sys.exit(1)
    image_to_ascii(sys.argv[1], sys.argv[2])