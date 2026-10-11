# Needle Hold の 3 項目の測り方（keypoint）

Needle Hold Angle・Needle Hold Ratio・Depth of Needle Hold を、keypoint（annotation.md の Keypoint）と event から測る。

## 区間

観測区間: その針の刺入（needle_entry）の直前の needle_reposition_end から刺入まで。
なければ前の needle_withdrawal_end（1 針目は動画の最初）から。

## フレームごとの値

持つ器具は、needle_grasp が付いているフレームで、2 つの顎の先端の中点が needle_grasp に近い方の器具とする。
項目ごとに、必要な点がすべて付いているフレームだけで測る。

| 項目 | 必要な点 | 値 |
|---|---|---|
| Needle Hold Angle | needle_grasp, needle_tip, head, shaft | needle_grasp → needle_tip の向きと、head → shaft の向き（器具の根元向き）のなす角（0〜180 度） |
| Needle Hold Ratio | needle_tip, needle_grasp, needle_tail | 3 点を通る円の上で、needle_tip → needle_grasp の弧の長さ / needle_tip → needle_tail の弧の長さ |
| Depth of Needle Hold | left_clasper, right_clasper, needle_grasp, head | 2 つの顎の先端の中点 c から needle_grasp へのベクトルを、c → head の向きに射影した長さ / c と head の距離 |

- Ratio は 0 で針先、1 でお尻を持つ。3 点がほぼ一直線のときは直線上の長さの比になる
- Depth は 0 で顎の先端、1 で顎の付け根を持つ

## 良いフレーム

項目ごとに、見え方の長さが長いフレームを選ぶ。長さはその動画の 95 パーセンタイルで割る（動画ごとにカメラとの距離が違うため）。

| 項目 | 長さ |
|---|---|
| Needle Hold Angle | needle_grasp と needle_tip の距離 × head と shaft の距離 |
| Needle Hold Ratio | needle_tip と needle_tail の距離 |
| Depth of Needle Hold | c と head の距離 |

1 針の値は、観測区間で長さが上位 10 フレームの値の中央値とする。
必要な点がすべて付いているフレームが 1 枚もない針は、その項目を測れないとする。
