"""Validate uploaded flux waveforms before passing them to a model."""
import csv
import io

import numpy as np


def read_waveform_csv(data, resolution):
    """Return one period in tesla at the selected model's resolution."""
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValueError('Save the CSV using UTF-8 encoding.') from exc
    try:
        rows = list(csv.reader(io.StringIO(text), strict=True))
    except csv.Error as exc:
        raise ValueError('Use comma-separated numeric values in one row.') from exc
    if len(rows) != 1 or not rows[0]:
        raise ValueError('Provide exactly one row of flux-density samples, with no header or time column.')
    cells = rows[0]
    if any(not cell.strip() for cell in cells):
        raise ValueError('Remove empty cells and any trailing comma.')
    try:
        samples = np.asarray([float(cell) for cell in cells], dtype=float)
    except ValueError as exc:
        raise ValueError('Every cell must be a number in tesla (T). Remove headers, units, and text.') from exc
    if not np.isfinite(samples).all():
        raise ValueError('NaN and infinity are not allowed. Every sample must be a finite number.')
    if len(samples) < resolution:
        raise ValueError(f'At least {resolution} samples are required for the selected model; this file contains {len(samples)}.')
    if np.max(np.abs(samples)) > np.finfo(np.float32).max / 1000:
        raise ValueError('The values are too large. Check that flux density is expressed in tesla (T).')
    if np.all(samples == samples[0]):
        raise ValueError('Provide a varying waveform covering one complete period, not a constant value.')
    # Select evenly spaced samples; preserve every sample at exact resolution.
    indices = np.arange(resolution, dtype=np.int64) * len(samples) // resolution
    return samples[indices]
