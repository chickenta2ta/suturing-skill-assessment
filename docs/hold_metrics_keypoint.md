# Needle Hold の 3 項目の測り方（keypoint）

Needle Hold Angle・Needle Hold Ratio・Depth of Needle Hold を、keypoint（annotation.md の Keypoint）と event から測る。

## 区間

観測区間: その針の刺入（needle_entry）の直前の needle_reposition_end から刺入まで。
なければ前の needle_withdrawal_end（1 針目は動画の最初）から。

## フレームごとの値

持つ器具は、grasp が付いている器具とする。2 本とも grasp が付いているフレーム（持ち直しの最中）は使わない。
c は 2 つの顎の先端（clasper_1, clasper_2）の中点。
項目ごとに、必要な点がすべて付いているフレームだけで測る。

| 項目 | 必要な点 | 値 |
|---|---|---|
| Needle Hold Angle | grasp, needle_tip, clasper_1, clasper_2, head | grasp → needle_tip の向きと、c → head の向き（顎に沿って根元へ向かう向き）のなす角（0〜180 度） |
| Needle Hold Ratio | needle_tip, grasp, needle_tail | 3 点を通る円の上で、needle_tip → grasp の弧の長さ / needle_tip → needle_tail の弧の長さ |
| Depth of Needle Hold | clasper_1, clasper_2, grasp, head | c から grasp へのベクトルを、c → head の向きに射影した長さ / c と head の距離 |

- Ratio は 0 で針先、1 でお尻を持つ。3 点がほぼ一直線のときは直線上の長さの比になる
- Depth は 0 で顎の先端、1 で顎の付け根を持つ

## 良いフレーム

項目ごとに、見え方の長さが長いフレームを選ぶ。長さはその動画の 95 パーセンタイルで割る（動画ごとにカメラとの距離が違うため）。

| 項目 | 長さ |
|---|---|
| Needle Hold Angle | grasp と needle_tip の距離 × c と head の距離 |
| Needle Hold Ratio | needle_tip と needle_tail の距離 |
| Depth of Needle Hold | c と head の距離 |

1 針の値は、観測区間で長さが上位 10 フレームの値の中央値とする。
必要な点がすべて付いているフレームが 1 枚もない針は、その項目を測れないとする。
