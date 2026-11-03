#!/usr/bin/env node

/**
 * 凌图小红书合规检查
 * 关键词扫描：结果承诺、资质用语、绝对化、站外引流、客户隐私、平台敏感词
 * 红色 = 必须改；黄色 = 看上下文判断
 */

const text = process.argv.slice(2).join(' ');

if (!text) {
  console.log('用法：node check_violation.mjs "<标题 + 正文>"');
  console.log('示例：node check_violation.mjs "全网第一的移民律师，保证获批，加我微信"');
  process.exit(1);
}

// 先把合法用法挖掉，避免误报（如"投资移民""第一步""不一定"）
const allow = [
  /投资移民/g, /投资签证/g, /E-?2\s*投资/g, /EB-?5/gi, /代理律师/g, /代理案件/g, /代理人/g,
  /第一[步次条点个天年周批份种类]/g, /第一时间/g, /第一优先/g, /第一类/g,
  /不一定/g, /也不一定/g, /最近/g, /最新/g, /最后/g, /最终/g, /最早/g, /最晚/g, /最少/g, /最多/g, /至少/g,
  /治疗费/g, /医疗费/g, /就医/g,
  /打电话/g, /接电话/g, /来电话/g, /电话里/g,
];
let scan = text;
for (const re of allow) scan = scan.replace(re, (m) => '□'.repeat(m.length));

const R = 'red';
const Y = 'yellow';

const rules = [
  // 结果承诺（加州 Rule 7.1）
  { cat: 'promise', lv: R, re: /保证|包过|稳过|必过|必批|必胜|稳赢|零拒签|100\s*%|百分百|一定(能|会|可以|批|过|赢)|肯定(能|会|批|过|赢)|无效退款|不批退款|全额退款/g,
    why: '结果承诺：律所广告不得承诺或暗示案件结果', fix: '删掉；改成讲流程、讲要准备什么' },
  { cat: 'promise', lv: R, re: /(获批|通过|胜诉|成功)率\s*\d+(\.\d+)?\s*%?|\d+\s*%\s*(获批|通过|胜诉|成功)/g,
    why: '成功率数字：容易让人对结果产生不合理期待', fix: '删掉数字，改写成具体案例并加"过往结果不代表未来"' },
  { cat: 'promise', lv: Y, re: /不赢不收费|不成功不收费|no win,? no fee/gi,
    why: '风险代理表述：需同时说明律师费以外的诉讼成本由谁承担', fix: '补一句费用说明，或删掉' },

  // 资质
  { cat: 'credential', lv: R, re: /(移民|签证|绿卡|车祸|人伤|诉讼|信托|遗产|法律)?专家|专精|specialist|权威律师|金牌律师|王牌律师/gi,
    why: '资质用语：加州只有 State Bar 认证的律师才能自称 specialist', fix: '「律师」「执业律师」「专注 XX 业务」' },

  // 绝对化
  { cat: 'absolute', lv: R, re: /最(好|强|专业|权威|靠谱|快|便宜|低价|高|牛|全|厉害|有经验)|全网(第一|首发|最)|第一名|排名第一|No\.?\s*1|顶级|顶尖|唯一|首选|天花板|国家级|独家/gi,
    why: '绝对化用语（广告规范 + 平台限流）', fix: '「常见」「我们的做法是」「实际经验」' },

  // 站外引流
  { cat: 'redirect', lv: R, re: /微信|VX|V信|wx号|威信|二维码|公众号|电话|手机号|(?<![A-Za-z\d])\(?\d{3}\)?[-\s.·]?\d{3}[-\s.·]?\d{4}(?!\d)|https?:\/\/|www\.|\.com\b|lingtulaw|加我|扫码/gi,
    why: '站外引流：平台会限流或封号', fix: '「私信」「看主页」「评论区留言」' },
  { cat: 'redirect', lv: Y, re: /私信我|私我|滴滴我|扣\s*1|扣【|评论区扣|自动发你/g,
    why: '诱导私信 / 诱导互动：平台可能限流', fix: '「评论区说说你的情况」' },

  // 客户隐私
  { cat: 'privacy', lv: R, re: /\b(IOE|WAC|EAC|LIN|SRC|MSC|NBC|YSC)\s*\d{10}\b/gi,
    why: '出现 receipt number', fix: '删掉' },
  { cat: 'privacy', lv: R, re: /\bA[-\s]?\d{8,9}\b|A\s*号\s*\d+/g,
    why: '出现 A-number', fix: '删掉' },
  { cat: 'privacy', lv: Y, re: /\b20\d{2}[-/.年]\s*\d{1,2}[-/.月]\s*\d{1,2}日?/g,
    why: '具体日期：案例里会让客户被认出来；政策生效日可以保留', fix: '案例里改成"今年春天""上个月"' },
  { cat: 'privacy', lv: Y, re: /案号|case\s*(no|number|#)/gi,
    why: '提到案号：确认没有写出具体号码', fix: '删掉号码' },

  // 平台敏感（金融 / 收益）
  { cat: 'platform', lv: Y, re: /赚钱|搞钱|变现|副业|躺赚|暴富|财富自由|月入|年入|理财|股票|基金|币圈|加密货币|返利|佣金|返现/g,
    why: '收益 / 金融类词：小红书重点限流', fix: '换个说法，或确认和业务直接相关' },
  { cat: 'platform', lv: Y, re: /根治|疗效|立刻见效|医院同款|医生推荐/g,
    why: '医疗效果宣称：人伤笔记不要替医疗结果背书', fix: '「先去看医生」「按医生建议治疗」' },
  { cat: 'platform', lv: Y, re: /炸裂|封神|绝绝子|一整个|咱就是说|宝子|姐妹们冲|大数据拯救|\d+\s*人验证|亲测\s*\d/g,
    why: '网络梗 / 虚构背书：不符合凌图口吻', fix: '改成平实的说法；"X 人验证"这类数字没有来源就删' },

  // 用词
  { cat: 'wording', lv: R, re: /活人信托/g,
    why: '凌图统一写"生前信托"', fix: '「生前信托」' },
];

const names = {
  promise: '⚖️ 结果承诺',
  credential: '🎓 资质用语',
  absolute: '📌 绝对化用语',
  redirect: '🔗 站外引流',
  privacy: '🔒 客户隐私',
  platform: '📉 平台敏感 / 口吻',
  wording: '✏️ 凌图用词',
};

const hits = [];
for (const r of rules) {
  const found = new Set();
  for (const m of scan.matchAll(r.re)) {
    // 用原文同位置的文字显示（scan 只是把白名单词挖成了□）
    found.add(text.slice(m.index, m.index + m[0].length));
  }
  if (found.size) hits.push({ ...r, words: [...found] });
}

console.log('━━━ 凌图小红书合规检查 ━━━\n');

if (!hits.length) {
  console.log('✅ 关键词扫描没有发现问题。发布前再对照 SKILL.md 的红线自己读一遍。\n');
  process.exit(0);
}

for (const cat of Object.keys(names)) {
  const items = hits.filter((h) => h.cat === cat);
  if (!items.length) continue;
  console.log(names[cat]);
  for (const h of items) {
    console.log(`  ${h.lv === R ? '🔴' : '🟡'} 「${h.words.join('」「')}」`);
    console.log(`     ${h.why}`);
    console.log(`     建议：${h.fix}`);
  }
  console.log();
}

const red = hits.filter((h) => h.lv === R).length;
const yellow = hits.length - red;
console.log('━━━━━━━━━━━━━━━━');
console.log(`🔴 必须改 ${red} 项　🟡 需判断 ${yellow} 项`);
console.log(red ? '结论：有红色项，改完再发。' : '结论：没有红色项，黄色项按上下文判断。');
process.exitCode = red ? 2 : 0;
