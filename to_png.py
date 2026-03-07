#!/usr/bin/env python3
"""Convert a pystat HTML report to a single tall PNG screenshot."""

import argparse
import os
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description="Convert pystat HTML report to PNG")
    parser.add_argument("input", nargs="?", default="pystat_report.html",
                        help="Input HTML file (default: pystat_report.html)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output PNG file (default: <input>.png)")
    parser.add_argument("--width", type=int, default=1024,
                        help="Viewport width in pixels (default: 1024)")
    parser.add_argument("--scale", type=float, default=2.0,
                        help="Device scale factor for sharpness (default: 2.0)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found")
        exit(1)

    output = args.output or os.path.splitext(args.input)[0] + ".png"
    url = "file://" + os.path.abspath(args.input)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": 800},
            device_scale_factor=args.scale,
        )
        page.goto(url, wait_until="networkidle")

        # Wait for Chart.js canvases to render
        page.wait_for_timeout(1000)

        # Get full page height
        height = page.evaluate("document.querySelector('.wrap').scrollHeight")
        page.set_viewport_size({"width": args.width, "height": height + 40})
        page.wait_for_timeout(500)

        page.screenshot(path=output, full_page=True)
        browser.close()

    size_mb = os.path.getsize(output) / (1024 * 1024)
    print(f"Saved {output} ({size_mb:.1f} MB, {args.width * args.scale:.0f}x{height * args.scale:.0f}px)")


if __name__ == "__main__":
    main()
