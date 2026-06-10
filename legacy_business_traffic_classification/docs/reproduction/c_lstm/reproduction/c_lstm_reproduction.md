# C-LSTM Reproduction Notes

## Scope

This repo now includes a paper-style reproduction path for:

- Yan et al., "Deep Learning-Based Efficient Analysis for Encrypted Traffic", *Applied Sciences*, published on 2023-10-27.
- Paper page: https://www.mdpi.com/2076-3417/13/21/11776
- Review report page used to resolve implementation details: https://www.mdpi.com/2076-3417/13/21/11776/review_report

## Paper Details Used Here

The implementation follows the reproducible details exposed on the paper page and review report:

- Task: packet-level encrypted traffic classification.
- Input representation: each packet is converted to a fixed-length `1480` byte vector.
- Preprocessing:
  - remove the data-link header and the network-layer header;
  - retain the transport header and upper-layer payload;
  - zero-pad UDP packets so that the UDP header is extended from `8` bytes to `20` bytes to align with TCP.
- Data split:
  - `80%` train and `20%` test;
  - `10`-fold cross-validation is performed on the training split in the paper.
- Training settings reported by the authors:
  - `batch_size = 32`
  - `epochs = 3`
  - dropout `0.05`

## Architecture Implemented

The C-LSTM model in `src/reproduction/c_lstm/reproduction/train_c_lstm.py` follows the structure disclosed in the review report:

- `Conv1d(1, 50, kernel_size=5, stride=3)`
- `Conv1d(50, 50, kernel_size=4, stride=3)`
- `MaxPool1d(kernel_size=3, stride=2)`
- `LSTM(input_size=81, hidden_size=50)`
- `Linear(2500, 500)`
- `Linear(500, 50)`
- `Linear(50, num_classes)`

One point in the review report is internally inconsistent: the table text states a pooling step size of `3`, but its published output shape is `50 x 81`. That output shape only matches `stride=2`, so the code uses `stride=2` to reproduce the reported tensor dimensions.

## Local Data Reality

The paper evaluates `12` classes:

- `Chat`, `Email`, `File Transfer`, `P2P`, `Streaming`, `VoIP`
- `VPN-Chat`, `VPN-Email`, `VPN-File Transfer`, `VPN-P2P`, `VPN-Streaming`, `VPN-VoIP`

Your current local workspace does not contain every paper class. At the time this note was written, the local files cover:

- non-VPN: `Chat`, `Email`, `File Transfer`, `Streaming`, `VoIP`
- VPN: `VPN-Chat`, `VPN-File Transfer`, `VPN-Streaming`, `VPN-VoIP`

Missing from the local data currently visible in this repo:

- `P2P`
- `VPN-P2P`
- `VPN-Email`

That means the code can reproduce the paper pipeline exactly, but the dataset available in this workspace only supports a partial-class reproduction unless the missing captures are added later.

## Commands

Prepare a packet dataset from the local captures:

```powershell
& 'D:\ProgramData\anaconda3\envs\ai\python.exe' `
  src\reproduction\c_lstm\reproduction\prepare_dataset.py `
  --sources data\NonVPN-PCAPs-01 data\NonVPN-PCAPs-03.zip data\VPN-PCAPs-02.zip `
  --output outputs\c_lstm\reproduction\local_partial\packets_1480.npz `
  --packet-size 1480 `
  --max-packets-per-file 5000
```

Train the paper-style C-LSTM model:

```powershell
& 'D:\ProgramData\anaconda3\envs\ai\python.exe' `
  src\reproduction\c_lstm\reproduction\train_c_lstm.py `
  --data outputs\c_lstm\reproduction\local_partial\packets_1480.npz `
  --output-dir outputs\c_lstm\reproduction\local_partial\run_e3 `
  --batch-size 32 `
  --epochs 3 `
  --cv-folds 10
```

Run a smaller smoke test:

```powershell
& 'D:\ProgramData\anaconda3\envs\ai\python.exe' `
  src\reproduction\c_lstm\reproduction\prepare_dataset.py `
  --sources data\NonVPN-PCAPs-01 data\VPN-PCAPs-02.zip `
  --output outputs\c_lstm\reproduction\smoke\smoke_packets.npz `
  --max-packets-per-file 64

& 'D:\ProgramData\anaconda3\envs\ai\python.exe' `
  src\reproduction\c_lstm\reproduction\train_c_lstm.py `
  --data outputs\c_lstm\reproduction\smoke\smoke_packets.npz `
  --output-dir outputs\c_lstm\reproduction\smoke\run `
  --epochs 1 `
  --cv-folds 0
```

## Outputs

The training script writes:

- `metrics.json`
- `classification_report.txt`
- `classification_report.json`
- `confusion_matrix.png`
- `splits.npz`
- `model.pt`
