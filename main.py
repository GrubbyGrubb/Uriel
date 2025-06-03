import os
import importlib.util
import pandas as pd
import tkinter as tk
from gui.interface import UrielGUI

def load_scrapers():
    manifest_path = "scraper_manifest.txt"
    if not os.path.exists(manifest_path):
        return []
    with open(manifest_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def run_scrapers(input_path, output_path, selected_scrapers, log_callback, progress_callback):
    if not input_path or not output_path:
        log_callback("❌ Input or output path missing.")
        return

    # Load SKUs
    try:
        if input_path.endswith(".csv"):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)
    except Exception as e:
        log_callback(f"💥 Failed to read input file: {e}")
        return

    if "Part Number" not in df.columns:
        log_callback("❌ 'Part Number' column not found in input file.")
        return

    skus = df["Part Number"].dropna().unique().tolist()
    log_callback(f"📦 Loaded {len(skus)} SKUs from file.")
    log_callback(f"🔍 Running {len(selected_scrapers)} scraper(s): {', '.join(selected_scrapers)}")

    total_tasks = len(skus) * len(selected_scrapers)
    completed = 0
    results = []

    for sku in skus:
        for scraper_name in selected_scrapers:
            try:
                module_path = os.path.join("scrapers", scraper_name, "scraper.py")
                spec = importlib.util.spec_from_file_location(scraper_name, module_path)
                scraper = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(scraper)

                result = scraper.scrape(sku)
                results.append(result)

                log_callback(f"✅ {scraper_name} | {sku} => {result['price'] or 'No price'}")
            except Exception as e:
                results.append({
                    "supplier": scraper_name,
                    "sku": sku,
                    "price": None,
                    "currency": "AUD",
                    "status": f"fail: {str(e)}"
                })
                log_callback(f"🔥 ERROR: {scraper_name} failed on {sku}: {e}")

            completed += 1
            progress_callback((completed / total_tasks) * 100)

    log_callback(f"🎯 Scraping complete. {len(results)} results collected.")
    
    # Save to Excel
    try:
        out_df = pd.DataFrame(results)
        out_df.to_excel(output_path, index=False)
        log_callback(f"💾 Results written to {output_path}")
    except Exception as e:
        log_callback(f"❌ Failed to write output file: {e}")

if __name__ == "__main__":
    scraper_list = load_scrapers()

    def on_start(input_path, output_path, selected_scrapers):
        run_scrapers(
            input_path,
            output_path,
            selected_scrapers,
            gui.log,
            gui.update_progress
        )

    root = tk.Tk()
    gui = UrielGUI(root, scraper_list, on_start)
    root.mainloop()
