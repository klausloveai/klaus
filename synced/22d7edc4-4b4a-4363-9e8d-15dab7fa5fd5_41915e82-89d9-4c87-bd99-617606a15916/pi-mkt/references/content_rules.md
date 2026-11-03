# Content rules — 事故类型 / 受伤详情 / 天数 / 编号

## 事故类型 (pick one; write it exactly as in the "Canva text" column)

Pick what the photos (and anything in the folder, e.g. dashcam file names, police report) suggest. When nothing points anywhere, rotate: don't reuse the type from the last post if another fits just as well.

| Type | Canva text |
|---|---|
| Rear-End Collision 追尾 | 追尾事故(Rear-End Collision) |
| T-Bone / Side Impact 侧面碰撞 | 侧面碰撞(T-Bone / Side Impact) |
| Hit and Run 肇事逃逸 | 肇事逃逸(Hit and Run) |
| Pedestrian Accident 行人事故 | 行人事故(Pedestrian Accident) |
| Bicycle Accident 自行车事故 | 自行车事故(Bicycle Accident) |
| Motorcycle Accident 摩托车事故 | 摩托车事故(Motorcycle Accident) |
| Uber/Lyft/Rideshare Accident 网约车事故 | 网约车事故(Rideshare Accident) |
| Truck / Commercial Vehicle Accident 卡车/商业车辆事故 | 商业车辆事故(Truck Accident) |
| Parking Lot Accident 停车场事故 | 停车场事故(Parking Lot Accident) |
| Uninsured Motorist Accident 对方无保险事故 | 对方无保险事故(Uninsured Motorist) |
| DUI Accident 酒驾/毒驾事故 | 酒驾事故(DUI Accident) |
| Intersection Accident 路口事故 | 路口事故(Intersection Accident) |

The value box is ~515px wide at 30.6pt. The shortened English keeps every option on one line.

Visual cues: rear bumper/trunk damage → 追尾; door/side panel damage → 侧面碰撞; front-corner damage at a crossing → 路口; parked cars / lot lines → 停车场. Don't choose Pedestrian/Bicycle/Motorcycle/Truck/DUI/Hit-and-run unless something in the folder supports it. Those are claims about the case, not just the car.

### Non-vehicle cases (狗咬, 滑倒摔伤 …)
The template is car-themed (its footer reads "车祸别慌 · 理赔有方 · 凌图律所 · 全程担当"). Still build the post, using e.g. `狗咬事故(Dog Bite)` or `滑倒摔伤(Slip and Fall)` as 事故类型 and fitting injuries (咬伤、割伤、流血、肿胀 …). Leave the footer, and flag in the report and tracker 备注 that the footer says 车祸 so Teresa can decide.

## 受伤详情 (compose three short phrases, joined by ，)

Teresa's reference list:
1. 受伤部位：头部，颈部，背部，胸部，腹部，上肢，下肢
2. 受伤疼痛：刺痛，扭伤，勒痕，肿胀，淤青，擦伤，割伤，流血
3. 受伤症状：头疼，头晕，恶心，想吐，发麻，耳鸣，短暂失忆，意识模糊，难以入睡，开车PTSD

Pattern: `<部位+疼痛>，<部位+疼痛>，<症状+症状>`. Keep the whole line ≤ 15 characters so it stays on one line.
Examples: `颈背扭伤，上肢淤青，头晕恶心` · `颈部扭伤，下肢肿胀，头疼耳鸣` · `背部刺痛，胸部淤青，难以入睡` · `颈背疼痛，上肢擦伤，开车PTSD`
Keep it plausible for the accident type (a parking-lot bump shouldn't read 短暂失忆，流血). Vary it between posts.

## 结案天数
Random integer 30–60: `python3 -c "import random; print(random.randint(30,60))"`. Text: `<N>天高效结案`.

## 案件编号
`#LT-<YYYY>-<MMDD>` from the check's **issue date** (the date printed on the check itself, not the loss date).
Example: check dated 09-16-2026 → `#LT-2026-0916`. Zack Feng: 07/16/2026 → `#LT-2026-0716`.

**Numbers must be unique** (Teresa, 2026-09-29). Insurers often cut a batch of checks on the same day, so before using a number, search the PI tab's 备注 column for it. If `#LT-2026-0817` is already taken, use `#LT-2026-0817-2`; if that is taken too, `-3`, and so on. The first post keeps the plain number. When several cases in one run share a date, number them in the order their tracker rows are written. The suffixed number fits on one line in the cover and reveal pills at the template font size.

## Design title
`<Client name as in folder>-<M>:<D>:<YYYY>` using the folder's loss date. Folder `Lianhai Mu-6-26-26` → `Lianhai Mu-6:26:2026`.
