from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from software_system.backend.app.config import load_config
from software_system.backend.app.predictor import RoutedModelPredictor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI inference for encryption-method identification.")
    parser.add_argument("--input", help="Input CSV file.")
    parser.add_argument("--output", help="Output CSV file for batch predictions.")
    parser.add_argument("--record-json", help="Single record as a JSON object string.")
    parser.add_argument("--model-dir", help="Override primary model directory.")
    parser.add_argument("--fallback-model-dir", help="Override fallback model directory.")
    parser.add_argument("--include-probabilities", action="store_true", help="Include per-class probabilities.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    model_dir = Path(args.model_dir).resolve() if args.model_dir else config.model_dir
    fallback_model_dir = Path(args.fallback_model_dir).resolve() if args.fallback_model_dir else config.fallback_model_dir
    predictor = RoutedModelPredictor(
        primary_model_dir=model_dir,
        fallback_model_dir=fallback_model_dir,
        data_metadata_path=config.data_metadata_path,
    ).load()

    if args.record_json:
        record = json.loads(args.record_json)
        predictions = predictor.predict_records([record], include_probabilities=args.include_probabilities)
        print(json.dumps(predictions[0], ensure_ascii=False, indent=2))
        return

    if not args.input:
        raise SystemExit("Either --input or --record-json is required.")
    if not args.output:
        raise SystemExit("--output is required for CSV input.")

    input_path = Path(args.input)
    output_path = Path(args.output)
    csv_text = input_path.read_text(encoding="utf-8-sig")
    predictions = predictor.predict_csv_text(csv_text, include_probabilities=args.include_probabilities)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(predictions).to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote predictions: {output_path}")


if __name__ == "__main__":
    main()
