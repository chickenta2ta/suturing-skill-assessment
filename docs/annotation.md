# アノテーション設計メモ

## データセット

JIGSAWS の Suturing（https://cirl.lcsr.jhu.edu/research/hmm/datasets/jigsaws_release/）

## 評価対象の Sub-Skill

EASE（Haque et al., Urol Pract 2023）のうち、以下を評価する。

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

## 観測区間

1針は needle_withdrawal_end で終わる。その直前の needle_entry を、その針の刺入とする。

途中で引き戻した場合の例（`*` がその針の刺入）:

```
reposition_start → reposition_end → entry → retraction_end
→ reposition_start → reposition_end → entry* → withdrawal_end
```

| Sub-Skill | 観測区間 |
|---|---|
| Needle Hold Ratio / Needle Hold Angle / Depth of Needle Hold | 直前の needle_reposition_end 〜 needle_entry |
| Wrist Rotation | needle_entry 〜 needle_withdrawal_end |

- Needle Hold 系は reposition 後に値が確定するため、区間内のどのフレームで計測してもよい
