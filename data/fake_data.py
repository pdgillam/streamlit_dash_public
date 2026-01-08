import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional


def get_sample(n: int = 5, seed: Optional[int] = None) -> pd.DataFrame:
    """Return a tiny sample DataFrame used for examples.

    Columns: timestamp, category, text, value, score, status
    """
    return generate_fake_data(n=n, seed=seed)


def generate_fake_data(n: int = 100, start_date: Optional[pd.Timestamp] = None, end_date: Optional[pd.Timestamp] = None, seed: Optional[int] = None) -> pd.DataFrame:
    """Generate deterministic fake dataset with required columns.

    - timestamp: evenly spaced between start_date and end_date (or last 30 days)
    - category: choices A/B/C
    - text: short synthetic text
    - value: integers
    - score: floats
    - status: 'open' or 'closed'
    """
    rng = np.random.RandomState(seed)

    if end_date is None:
        end = pd.to_datetime(datetime.utcnow())
    else:
        end = pd.to_datetime(end_date)
    if start_date is None:
        start = end - pd.Timedelta(days=30)
    else:
        start = pd.to_datetime(start_date)

    if n <= 1:
        timestamps = [start]
    else:
        timestamps = pd.date_range(start=start, end=end, periods=n)

    categories = rng.choice(["A", "B", "C"], size=n)
    text = [f"text-{i}" for i in range(n)]
    value = rng.randint(0, 100, size=n)
    score = rng.rand(n)
    status = rng.choice(["open", "closed"], size=n, p=[0.3, 0.7])

    df = pd.DataFrame({
        "timestamp": timestamps,
        "category": categories,
        "text": text,
        "value": value,
        "score": score,
        "status": status,
    })
    return df

