# TCPNet-Framework

A minimal unified pipeline for tropical cyclone **rainfall** and **track** prediction.

This repository provides a single entry script (`main.py`) to run:

* Rainfall prediction using **TCP-Diffusion**
* Track prediction using **TropiCycloneNet (TCNM)**
* Simple case-level visualization

---

## Requirements

* Python ≥ 3.8
* PyTorch ≥ 1.10 (GPU recommended)
* NumPy

> It is recommended to use the original environments of TCP-Diffusion and TropiCycloneNet.

---

## 📦 Download Model and Dataset Subset

Download the 2020 subset of the dataset via the following **link**:

**[Dataset](https://drive.google.com/file/d/1C-qlBwNENmMvojrfaZWjyfGz6L8LVwWZ/view?usp=drive_link)**


**Note:**
- Only data from the year **2020** is included for review.

---

## Directory Layout

The project root should be organized as:

```
[ROOT]
├── TCPN-F/
│   ├── main.py
│   ├── visualize.py
│   └── problem_identity_cases/
├── TCP-Diffusion/
└── TropiCycloneNet-Model/
```

---

## Preparation

### 1. TCP-Diffusion

* Follow the original **TCP-Diffusion** README
* Download the pre-trained model via the following **link**:
**[Model](https://drive.google.com/file/d/1woEQWk_x_fJDpTJPXVlCXzwzh4loLtMl/view?usp=drive_link)**
* Make sure the pretrained model and dataset paths are correctly set
* Place the pre-trained model `model-55.pt` into the following directory: `TCP-Diffusion/results/TCP_ICML_Test/`
* 📁 Dataset Preparation
  1. Extract the downloaded dataset `TCPN_D_subset2020` to a path of your choice, e.g., `your_data_path`.
  2. Edit **line 17** of the file: `video_diffusion_pytorch/rainfall_dataset_ICML.py`
  3. Replace the default path with your actual dataset location.* 
* Confirm that `run_rainfall()` works independently

### 2. TropiCycloneNet

* Follow the original **TropiCycloneNet** README
* download all the data we used in TropiCycloneNet.
* $TCN_{M}$'s [checkpoint](https://drive.google.com/file/d/1j5r2L5Y5W81pn7nBfrZCT1BA1_qfnaay/view?usp=sharing)
* $TCN_{D}$'s [subset](https://drive.google.com/file/d/1YJg_gjF-zqvRdNpmAWFG4bG0Akwv_r2p/view?usp=sharing)
* Place the pretrained checkpoint in:

```
TropiCycloneNet-Model/scripts/model_save/best/
```

* modify the path of dataset for the track in line 40:

```
TCPN-Framework\TropiCycloneNet-main\scripts\TCPN_F_Track.py
```

* Confirm that `run_track()` works independently

---

## Run

Edit the project root in `main.py`:

```python
ROOT = Path("/home/hc/code")
```

Then run:

```bash
python main.py \
  --tc_name ZETA \
  --tc_date 2020102700\
  --rainfall_impl TCP-Diffusion \
  --track_impl TCNM
```

---

## Outputs

After running, the following files will be generated:

```
rainfall.npy     # Rainfall prediction
track.npy    # Raw track output (0.1-degree)
```

Visualization results are saved to:

```
TCPN-F/problem_identity_cases/
```

---

## Notes

* Track outputs from TropiCycloneNet are encoded in **0.1-degree units**
* Longitude is automatically wrapped to `[-180, 180]`
* Latitude is constrained to `[-90, 90]`

---

## Acknowledgement

This framework relies on:

* TCP-Diffusion
* TropiCycloneNet

Please cite the original works if you use these models.

```
@article{Huang2025,
  author    = {Huang, Cheng and Mu, Pan and Zhang, Jinglin and Chan, Sixian and Zhang, Shiqi and Yan, Hanting and Chen, Shengyong and Bai, Cong},
  title     = {Benchmark dataset and deep learning method for global tropical cyclone forecasting},
  journal   = {Nature Communications},
  volume    = {16},
  number    = {1},
  pages     = {5923},
  year      = {2025},
  publisher = {Nature Publishing Group},
  doi       = {10.1038/s41467-025-61087-4},
  url       = {https://doi.org/10.1038/s41467-025-61087-4},
  issn      = {2041-1723}
}
```
```
@InProceedings{pmlr-v267-huang25y,
  title = 	 {{TCP}-Diffusion: A Multi-modal Diffusion Model for Global Tropical Cyclone Precipitation Forecasting with Change Awareness},
  author =       {Huang, Cheng and Mu, Pan and Bai, Cong and Watson, Peter Ag},
  booktitle = 	 {Proceedings of the 42nd International Conference on Machine Learning},
  pages = 	 {25634--25653},
  year = 	 {2025},
  editor = 	 {Singh, Aarti and Fazel, Maryam and Hsu, Daniel and Lacoste-Julien, Simon and Berkenkamp, Felix and Maharaj, Tegan and Wagstaff, Kiri and Zhu, Jerry},
  volume = 	 {267},
  series = 	 {Proceedings of Machine Learning Research},
  month = 	 {13--19 Jul},
  publisher =    {PMLR},
  pdf = 	 {https://raw.githubusercontent.com/mlresearch/v267/main/assets/huang25y/huang25y.pdf},
  url = 	 {https://proceedings.mlr.press/v267/huang25y.html},
}
```
