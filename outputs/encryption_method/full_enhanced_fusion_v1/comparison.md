# Full-Data Enhanced Fusion Method

- Data dir: `data\unified_encryption_method_v2_all_data`
- Source leakage guard: `source_name` excluded
- Feature fusion: flow statistics + transport + sequence-derived statistics

| model_name                   |   accuracy |   f1_macro |   f1_weighted |   macro_recall |   num_features |
|:-----------------------------|-----------:|-----------:|--------------:|---------------:|---------------:|
| full_enhanced_fusion_xgboost |   0.993978 |   0.892797 |      0.994046 |       0.909893 |             41 |
