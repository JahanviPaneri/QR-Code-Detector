import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Allow imports from backend utilities
ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / 'backend'
sys.path.append(str(BACKEND_DIR))

from url_features import FEATURE_COLUMNS, extract_features  # noqa: E402


def train(dataset_path: Path, output_path: Path) -> None:
    df = pd.read_csv(dataset_path)
    if 'label' not in df.columns or 'url' not in df.columns:
        raise ValueError('Dataset must contain "url" and "label" columns.')

    feature_frame = df['url'].apply(extract_features).to_list()
    X = pd.DataFrame(feature_frame)[FEATURE_COLUMNS]
    y = df['label']

    model = RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    )
    model.fit(X, y)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    print(f'Saved RandomForest model to {output_path}')


def main():
    parser = argparse.ArgumentParser(
        description='Export the RandomForest QR threat model joblib artifact.'
    )
    parser.add_argument(
        '--dataset',
        type=Path,
        default=Path('QR codes') / 'dataset_feat_engg.csv',
        help='Path to the CSV file containing url + label columns.',
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('backend') / 'artifacts' / 'qr_random_forest.joblib',
        help='Where to store the trained model artifact.',
    )

    args = parser.parse_args()
    dataset_path: Path = (Path(__file__).resolve().parent / args.dataset).resolve()
    output_path: Path = ROOT / args.output

    if not dataset_path.exists():
        raise FileNotFoundError(
            f'Dataset not found at {dataset_path}. Generate it via the notebook first.'
        )

    train(dataset_path, output_path)


if __name__ == '__main__':
    main()

