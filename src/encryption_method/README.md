# Unified Encryption-Method Pipeline

This directory contains the current pipeline for encryption-method identification.
The old application/business traffic classification code has been archived under
`legacy_business_traffic_classification/`.

## Files

- `build_unified_dataset.py`
  - Builds a unified dataset from all cleanly mappable sources under `data/`.
- `train_hybrid_classifier.py`
  - Trains a two-stage deep model: binary pretraining, then multiclass fine-tuning.
- `benchmark_tabular_baselines.py`
  - Trains first-layer full-data tabular baselines under the same split/evaluation protocol.
- `build_paper_benchmark_dataset.py`
  - Builds the second-layer 5-class PCAP benchmark for packet/sequence paper methods.
- `benchmark_paper_methods.py`
  - Runs ET-BERT / TFE-GNN / Deep Packet style comparison methods on the PCAP benchmark.
- `train_enhanced_pcap_fusion.py`
  - Trains the current enhanced PCAP fusion method for the 5-class paper-method benchmark.
- `train_full_enhanced_fusion.py`
  - Trains the latest full 9-class main method on all unified data.
- `packet_encoding_utils.py`
  - Local packet byte extraction and TrafficFormer-style tokenization helpers used by the current PCAP benchmark.
- `unified_benchmark_utils.py`
  - Shared full-data loading, preprocessing, metrics, and result-writing utilities.

## Main Commands

Build the unified full-data dataset:

```powershell
python src\encryption_method\build_unified_dataset.py `
  --output-dir data\unified_encryption_method_v2_all_data
```

Train the latest full 9-class main method:

```powershell
python src\encryption_method\train_full_enhanced_fusion.py `
  --data-dir data\unified_encryption_method_v2_all_data `
  --output-dir outputs\encryption_method\full_enhanced_fusion_v1
```

Build the 5-class PCAP paper-method benchmark:

```powershell
python src\encryption_method\build_paper_benchmark_dataset.py `
  --max-flows-per-label 40 `
  --output-dir data\paper_benchmark\encryption_method_5class_pcap_v1
```

Run paper-method comparisons:

```powershell
python src\encryption_method\benchmark_paper_methods.py `
  --data-dir data\paper_benchmark\encryption_method_5class_pcap_v1 `
  --output-dir outputs\encryption_method\paper_methods_5class_v1
```

## Unified Final Labels

- `NON_ENCRYPTED`
- `TLS_FAMILY`
- `SSH`
- `QUIC`
- `VPN`
- `TOR`
- `I2P`
- `FREENET`
- `ZERONET`

Rare protocol labels are merged conservatively:

- `TLS` + `DTLS` -> `TLS_FAMILY`
- `WIREGUARD` + `OPENVPN` + generic `VPN` -> `VPN`

This mapping keeps the task focused on visible encrypted transport or
anonymity mechanism instead of application semantics.
