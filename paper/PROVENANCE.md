# 論文の数値・事実の出どころ

論文に書いた数値と事実ごとに、何から求めたか（スクリプト・入力・出力、または文献）を記録する。
数値を本文に入れたら、同じ変更でここにも追記する。`data/` は git 対象外（古いリポのローカル）。

## データ（3.1 Data and annotations）

| 本文の記述 | 出どころ |
|---|---|
| JIGSAWS は da Vinci、ベンチトップモデル、術者 8 人、Suturing 39 試行 | PMC7671974（JIGSAWS を解析した論文。JIGSAWS 公式ページと Gao 2014 の PDF は 403 で未取得） |
| 自己申告の技能（初心者 B, G, H, I／中級 C, F／熟練 D, E）、各組が熟練 1・中級 1・初心者 2 | PMC7671974、公開リポ `docs/dataset.md` |
| 1 試行 4 針 | `annotations/events_and_ease.json`（公開リポ）: 使った 35 試行で needle_withdrawal_end が各 4（計 140） |
| 開発用 B, E, F, I（16 試行、64 針）、テスト用 C, D, G, H（19 試行、76 針） | 公開リポ `configs/split.yaml`、`docs/dataset.md`、`annotations/events_and_ease.json` |
| few-shot の 2 試行（B001, E003）は他に使わない | 公開リポ `docs/dataset.md` |

## EASE の基準（2.1、2.3–2.5）

| 本文の記述 | 出どころ |
|---|---|
| Repositions ≤2 / 3 / ≥4、Ratio 1:1〜3/4:1/4、Angle 90–135° / 135–150°、Depth 1/4 / 1/2 | Haque 2022 Figure 2（`data/references/haque2022_ease_nihms-1871225.pdf` p.10、画像 `haque2022_p-10.png`） |
| AutoEASE は全 sub-skill を 2 値で採点、ideal frame を YOLOv12 で選ぶ（536 枚） | Deo 2026（`data/references/deo2026.txt`） |

## 実装（3.2 Implementation）

| 本文の記述 | 出どころ |
|---|---|
| GPT-6 Astra（gpt-6-astra）、reasoning medium | 公開リポ `suturing_assessment/astra_events.py`、`astra_keypoints_and_masks.py`（MODEL、REASONING_EFFORT） |
| System Card（2026-09-03） | `data/references/openai_gpt6_astra_system_card.pdf` |
| イベント: 5 fps、1 リクエスト 20 s、前後 10 s の文脈、それまでのイベントを渡す | `astra_events.py`（EVENT_STEP=6, TARGET_SECONDS=20, CONTEXT_SECONDS=10） |
| keypoint とマスク: 10 fps、20 フレーム／リクエスト、例は 20 フレーム | `astra_keypoints_and_masks.py`（FRAME_STEP=3, WINDOW=20）、`annotations/keypoint_fewshot_E003.json` |
| （本文には書かない）実装は needle_retraction_end も検出し、few-shot 例にも 1 クリップある。検出した値は次のリクエストに渡す針の状態（組織内か）の判定にだけ使い、針の区切り・区間には使わない | `astra_events.py` の window_text、`needle_hold.py` の stitches |

## 比較手法と指標（3.3 Baselines and metrics）

| 本文の記述 | 出どころ |
|---|---|
| 直接採点: 評価対象区間を 5 fps、前後 10 s、EASE 基準と補足、開発用 3 針の点数付き例、点数・確率・値を返す | 公開リポ `docs/astra_ease.md`、`results/test/astra_ease/` |
| 予測区間の対応: 人手の針の区間（前の引き抜き終了の後〜その針の引き抜き終了）に検出の刺入がある針と1対1で対応、複数なら刺入が最も近いもの | `data/paper_analysis/final/analysis_final.py` の match_pred（TOL=−1） |
| イベント検出の F1、許容 1 s、4 イベントで集計 | `data/paper_analysis/final/event_f1.py` → `event_f1_{dev,test}.txt`（5 種での集計は旧 `paper/event_detection.txt` と一致） |
| AUC: 陽性 = EASE 3（Ratio は 2–3）、順位は EASE 基準への符号付きマージン、直接採点は陽性クラスの確率 | `data/paper_analysis/final/README.md`、`analysis_final.py` |
| 測れなかった針は両指標で誤り（AUC は最悪順位）。該当は全条件で 0 針 | `final/analysis_{dev,test}.txt` の missing 行 |
| 動画単位ブートストラップ（本文に回数は書かない。実際は 2000 回）、差は対応あり | `analysis_final.py`（B = 2000） |

## 結果の数値（未記入）

- 主結果・完全自動・Astra との差: `data/paper_analysis/final/analysis_{dev,test}.txt`（`final/run_final.sh` で再実行、定義は `final/README.md`）
- 構成要素の比較: `data/paper_analysis/final/ablation_*.txt`、`pf_analysis_*.txt`
- イベント検出: `data/paper_analysis/paper/event_detection.txt`
- keypoint とマスクの精度（H004）: `data/paper_analysis/paper/perception_H004.txt`
- 5 fps での感度分析: `data/paper_analysis/final/analysis_{dev,test}_fps5.txt`、`paired_fps_{dev,test}.txt`

## 要旨

| 本文の記述 | 出どころ |
|---|---|
| 完全自動で AUC 0.89–0.97 | `final/analysis_test.txt` の ours_pred（Repositions 0.974, Ratio 0.921, Angle 0.966, Depth 0.890）＝ Table 3 |

## 結果（4 Results）

| 本文の記述 | 出どころ |
|---|---|
| Table 1（tab:main、人手の評価対象区間、直接採点 vs 我々、AUC・BA と 95% 区間、差 = 我々 − 直接採点） | `data/paper_analysis/final/analysis_test.txt` の main metrics（ours, astra）と paired differences（astra − ours の符号を反転）。差の CI は 3 桁（2026-10-23 に `analysis_final.py` の表示を 3 桁にして `analysis_*.txt` を再生成） |
| Table 2（tab:e2e、完全自動、4 項目の AUC・BA と 95% 区間） | `data/paper_analysis/final/analysis_test.txt` の main metrics（ours_pred） |
| Angle の差 AUC +0.119（95% CI 0.047–0.226）、EASE 1 の再現率 0.58（直接採点）vs 0.83（我々） | `final/analysis_test.txt` の paired differences（astra Angle AUC −0.119 [−0.226, −0.047]）と main metrics の recall |
| 5 fps のフレームだけで計測しても test の AUC の変化は 0.04 未満（Ratio +0.032, Angle −0.007, Depth +0.015） | `final/paired_fps_test.txt` |
| イベント検出 F1 0.89（test、許容 1 s、本文の 4 イベントで集計: TP 376／pred 421／gt 425 → 0.889。retraction end 込みの 5 種でも 0.888） | `data/paper_analysis/final/event_f1_test.txt`（`event_f1.py`） |
| 76/76 針が対応、余分な検出 1、刺入誤差の中央値 0.28 s | `final/analysis_test.txt` の冒頭（predicted stitches 77, matched 76/76） |
| 人手区間との AUC の差は最大 0.012（Ratio +0.011, Angle +0.002, Depth −0.012） | `final/analysis_test.txt` の paired differences（ours_pred） |
| 5 Discussion: 誤りのうちしきい値の近く Ratio 15/17（0.05 以内）、Angle 9/10（10° 以内）、Depth は遠い誤り 8/17（0.05 以内は 9/17） | `data/paper_analysis/fig2/fig2_drafts.py`（公開リポを入力、標準出力の "ours wrong … within … of a threshold"）。誤り = 我々の点数（Ratio は good/poor）≠ 正解、距離 = 計測値から最も近い EASE のしきい値まで |
| 5 Discussion: 顎は画像で数十画素 | `~/Downloads/parts_H004_2409.png` の jaw length（30〜55 px）。H004 の 1 針の例 |
| 5 Discussion: EASE の評価者間信頼性は中程度以上 | Haque 2022 の Abstract・Results（ICC 中央値 0.69、範囲 0.51–0.97、PABAK 0.77）、`data/references/haque2022.txt` |
| Fig. 2（`figures/values_vs_ground_truth.pdf`）: test 76 針の計測値と EASE の正解、正誤 | 公開リポ `results/test/{needle_hold_ratio,needle_hold_angle,depth_of_needle_hold}.json` と `annotations/events_and_ease.json`。生成は `data/paper_figures/fig2_values.py REPO --publish`（語彙は同じフォルダの `figstyle.py`） |
| Fig. 1（`figures/overview.pdf`。`overview_perception.pdf` (a) と `overview_measurement.pdf` (b) を `figures/overview.tex` と `make_overview.sh` で合体）: 術者 H の試行 4 の 3 針目（Suturing_H004、entry 2409、hold window 2272–2409、t = 0 は reposition end）。(a) のイベントは `annotations/events_and_ease.json`、キーポイントとマスクは `results/test/astra_keypoints_and_masks/Suturing_H004.json`（公開リポ）。(b) の採用値 Ratio 0.586、Angle 124.3°、Depth 0.079 は `results/test/{needle_hold_ratio,needle_hold_angle,depth_of_needle_hold}.json`、正解 good / 3 / 3 は annotations。針の円弧の当てはめ（半径 90.5 px、中心角 130°）は `data/paper_figures/fit_arc.py`、各コマの推定値（Angle・Depth は手法どおり、Ratio は各コマ単独の当てはめ）は `fit_perframe.py`、出力は `data/paper_figures/fit/`。生成は `fig1a_perception.py` と `fig1b_series.py` の `--publish paper`（語彙は `figstyle.py`） |
