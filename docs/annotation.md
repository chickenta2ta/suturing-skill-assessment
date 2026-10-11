# アノテーション設計メモ

## データセット

JIGSAWS の Suturing（https://cirl.lcsr.jhu.edu/research/hmm/datasets/jigsaws_release/）

人単位で 4 人ずつに分ける。どちらも熟練度（自己申告）が熟練者 1・中級者 1・初心者 2 で、GRS の分布が近くなるように選んだ。

- 開発用（few-shot の例・ロジック開発・ハイパラ調整）: B, E, F, I
- テスト用: C, D, G, H

## 評価対象の Sub-Skill

EASE（Haque et al., Urol Pract 2023）のうち、以下を評価する。

- Needle Repositions
- Needle Hold Ratio
- Needle Hold Angle
- Depth of Needle Hold
- Wrist Rotation（Needle Driving と Needle Withdrawal を分けずに評価する）

## Event

動画中の瞬間（1フレーム）を event と呼ぶ。1フレームの瞬間を検出するタスクは動画認識で event spotting と呼ばれ（例: Precise Event Spotting, ECCV 2022）、スイングを event で区切る GolfDB（CVPR Workshops 2019）とも構図が同じ。

id は COCO や AVA と同様に、1 始まりの整数 id と名前の文字列で持つ。

| id | name | 定義 |
|---|---|---|
| 1 | needle_reposition_start | 針が組織外にある状態で、両方の器具が針を把持した瞬間 |
| 2 | needle_reposition_end | 片方の器具が針を離した瞬間 |
| 3 | needle_entry | 針先が組織に入った瞬間。刺すたびに付ける |
| 4 | needle_withdrawal_end | 反対側へ通し切り、針全体が組織から出た瞬間 |
| 5 | needle_retraction_end | 刺入側へ引き戻し、針全体が組織から出た瞬間 |

- 針の状態は「組織外」「刺入中」の 2 つ。動画開始時は組織外
- needle_entry で刺入中になり、4 か 5 のどちらかで組織外に戻る
- needle_reposition は組織外でのみ付ける

オクルージョンで瞬間が見えない場合は、見えない間を「刺入中」「両手で把持中」とみなし、以下に付ける。

| event | 付けるフレーム |
|---|---|
| needle_reposition_start | 片手で把持していると確認できた最後のフレーム |
| needle_reposition_end | 片手で把持していると確認できた最初のフレーム |
| needle_entry | 組織外にあると確認できた最後のフレーム |
| needle_withdrawal_end / needle_retraction_end | 組織外にあると確認できた最初のフレーム |

## Keypoint

針に 2 点、器具に 4 点を付ける。器具は見えている 2 本ともに付け、2 本の順番に意味はない。
名前は COCO と同様に小文字と下線で書き、器具の点は Du et al.（IEEE TMI 2018）の名前に、針の点は Chiu et al.（IROS 2022）・PinPoint（2026）の名前に合わせる。

| name | 対象 | 定義 |
|---|---|---|
| needle_tip | 針 | 針先 |
| needle_tail | 針 | 針のお尻（糸の付け根） |
| clasper_1, clasper_2 | 器具 | 2 枚の顎の先端（順番に意味はない）。顎が閉じているときはほぼ同じ位置 |
| head | 器具 | 顎の付け根（2 枚の顎が開閉する関節） |
| grasp | 器具 | 針の中心線と顎の中心線（顎の向きに沿い、顎の幅の真ん中を通る線）の交点。顎が針を挟んでいるときだけ |

- 隠れて見えない点は付けない（位置を推定しない）
- grasp は、顎が針を挟んでいるのが見えれば付ける（挟まれた部分は顎に隠れていてよい）。両方の器具が挟んでいるときは両方に付ける
- 顎の先端が片方しか見えないときは clasper_1 に付ける
- Du et al. の shaft と end は付けない。顎は手首の関節でシャフトから曲がり、EASE の Needle Hold は顎で決まるため（顎の向きは顎の先端と head で決まる）

## 観測区間

1針は needle_withdrawal_end で終わる。その直前の needle_entry を、その針の刺入とする。

途中で引き戻した場合の例（`*` がその針の刺入）:

```
reposition_start → reposition_end → entry → retraction_end
→ reposition_start → reposition_end → entry* → withdrawal_end
```

| Sub-Skill | 観測区間 |
|---|---|
| Needle Repositions | 前の針の needle_withdrawal_end（1針目は動画開始）〜 needle_entry |
| Needle Hold Ratio / Needle Hold Angle / Depth of Needle Hold | 直前の needle_reposition_end 〜 needle_entry |
| Wrist Rotation | needle_entry 〜 needle_withdrawal_end |

- 表中の needle_entry は、その針の刺入（例の `*`）を指す
- Needle Repositions は、区間内の needle_reposition_start の数で評価する
- Needle Hold 系は reposition 後に値が確定するため、区間内のどのフレームで計測してもよい

## フォーマット

COCO と同様に、データセット全体を 1 つの JSON で持つ。

```json
{
  "event_categories": [
    {"id": 1, "name": "needle_reposition_start"}
  ],
  "videos": [
    {"id": 1, "file_name": "Suturing_B001_capture1.avi",
     "width": 640, "height": 480, "fps": 30, "num_frames": 5640}
  ],
  "events": [
    {"id": 1, "video_id": 1, "category_id": 1, "frame_index": 371}
  ],
  "stitches": [
    {"id": 1, "video_id": 1,
     "entry_event_id": 7, "withdrawal_end_event_id": 8,
     "ease_scores": {"needle_repositions": 2, "needle_hold_ratio": 3,
                     "needle_hold_angle": 2, "depth_of_needle_hold": 3,
                     "wrist_rotation": null}}
  ]
}
```

- `id` は整数で、ファイル全体で一意
- `frame_index`: 元の avi を OpenCV（`cv2.VideoCapture`）で先頭から `read()` した順番（0 始まり）。JIGSAWS のジェスチャーラベル・キネマティクスのフレーム番号とは一致しない
- 観測区間はデータに持たず、観測区間の規則から計算する
- `wrist_rotation` は needle_entry 〜 needle_withdrawal_end を見て 1 つ付ける
- 評価できない場合は `null`
