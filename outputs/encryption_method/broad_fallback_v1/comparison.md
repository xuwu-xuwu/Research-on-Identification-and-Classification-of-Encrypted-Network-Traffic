# Broad Fallback Model

- Routing role: used when the 21 numeric flow features are incomplete.
- Training augmentation: full + partial numeric missing + all numeric missing + transport-only.
- Base train samples: `221617`
- Augmented train samples: `886468`

| scenario        |   accuracy |   f1_macro |   f1_weighted |   macro_recall |
|:----------------|-----------:|-----------:|--------------:|---------------:|
| full            |   0.990504 |   0.850941 |      0.990654 |       0.878045 |
| partial_numeric |   0.961342 |   0.705741 |      0.962178 |       0.721044 |
| no_numeric      |   0.526298 |   0.289372 |      0.513755 |       0.316867 |
| transport_only  |   0.420074 |   0.110943 |      0.396931 |       0.159676 |
