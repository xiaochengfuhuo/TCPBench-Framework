#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry for TCPN-F pipeline
- Select Rainfall / Track implementations via CLI
- Run inference
- Visualize one case
"""

import sys
import argparse
from pathlib import Path
import numpy as np

# ============================================================
# Project root
# ============================================================
ROOT = Path("/home/hc/code")

# ============================================================
# Step 1: CLI arguments (select implementation)
# ============================================================
parser = argparse.ArgumentParser(description="TCPN-F unified pipeline")

parser.add_argument(
    "--rainfall_impl",
    type=str,
    default="TCP-Diffusion",
    choices=["TCP-Diffusion"],
    help="Rainfall model implementation"
)

parser.add_argument(
    "--track_impl",
    type=str,
    default="TCNM",
    choices=["TCNM"],
    help="Track model implementation"
)

parser.add_argument(
    "--tc_name",
    type=str,
    default="ZETA",
    help="Tropical cyclone name"
)

parser.add_argument(
    "--tc_date",
    type=str,
    default="2020102700",
    help="Tropical cyclone initial time"
)

args = parser.parse_args()

# ============================================================
# Step 2: sys.path mapping (ONLY place to manage paths)
# ============================================================
RAIN_IMPL_PATHS = {
    "TCP-Diffusion": [
        ROOT / "TCP-Diffusion",
    ],
}

TRACK_IMPL_PATHS = {
    "TCNM": [
        ROOT / "TropiCycloneNet-Model" / "scripts",
        ROOT / "TropiCycloneNet-Model",
    ],
}

# inject rainfall paths
for p in RAIN_IMPL_PATHS[args.rainfall_impl]:
    sys.path.append(str(p))

# inject track paths
for p in TRACK_IMPL_PATHS[args.track_impl]:
    sys.path.append(str(p))

# ============================================================
# Step 3: import AFTER sys.path is ready
# ============================================================
from TCPN_F_Rainfall import run_rainfall
from TCPN_F_Track import run_track
from visualize import show_one_case

# ============================================================
# Step 4: Rainfall inference arguments
# ============================================================
rainfall_args = [
    "ICML",
    "--save", "results/TCP_ICML_Test",
    "--output_frames", "4",
    "--train_batch_size", "16",
    "--test_epoch", "55",
    "--timesteps", "200",
    "--new_split",
    "--multi_modals", "tquvz_t2m_sst_msl_topo_ifs",
    "--input_transform_key", "loge",
    "--loss_type", "l2",
]

# ============================================================
# Step 5: Run Rainfall
# ============================================================
print("[INFO] Running Rainfall model...")
rainfall_data = run_rainfall(rainfall_args)

if rainfall_data is None:
    raise RuntimeError("Rainfall model returned None")

print("[INFO] Rainfall output shape:", rainfall_data.shape)
np.save("rainfall.npy", rainfall_data)

# ============================================================
# Step 6: Run Track
# ============================================================
print("[INFO] Running Track model...")
track = run_track([
    "--TC_name", args.tc_name,
    "--TC_date", args.tc_date,
])

if track is None:
    raise RuntimeError("Track model returned None")

print("[INFO] Track output shape:", track.shape)
np.save("track_raw.npy", track)

# ============================================================
# Step 7: Decode track (unit = 0.1 degree → degree)
# ============================================================
def decode_track_01deg(track_01deg: np.ndarray) -> np.ndarray:
    """
    Convert 0.1-degree encoded lon/lat to real degrees
    """
    track_deg = track_01deg.astype(float) * 0.1

    # wrap longitude to [-180, 180]
    track_deg[:, 0] = (track_deg[:, 0] + 180.0) % 360.0 - 180.0

    # sanity check
    assert np.all(np.abs(track_deg[:, 0]) <= 180)
    assert np.all(np.abs(track_deg[:, 1]) <= 90)

    return track_deg


track_deg = decode_track_01deg(track)
np.save("track_deg.npy", track_deg)

print("[INFO] Decoded track range:")
print("  lon:", track_deg[:, 0].min(), track_deg[:, 0].max())
print("  lat:", track_deg[:, 1].min(), track_deg[:, 1].max())

# ============================================================
# Step 8: Visualization
# ============================================================
print("[INFO] Generating visualization...")
save_root = ROOT / "TCPN-F" / "problem_identity_cases"

show_one_case(
    track=track_deg,
    rainfall_data=rainfall_data,
    file_name=f"{args.tc_name}{args.tc_date}",
    # save_root=str(save_root),
)

print("[INFO] Done. Results saved to:", save_root)
