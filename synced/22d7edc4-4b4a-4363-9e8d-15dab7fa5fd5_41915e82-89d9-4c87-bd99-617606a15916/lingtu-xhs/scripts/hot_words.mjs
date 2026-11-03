#!/usr/bin/env node

/**
 * 凌图小红书关键词候选
 * 按业务给出"人群 / 场景 / 问题"组合，帮你想标题和标签。
 * 不联网，没有热度数据。要看真实热度和同类笔记，用 agent-reach 搜小红书。
 */

const topic = process.argv.slice(2).join(' ').trim();

if (!topic) {
  console.log('用法：node hot_words.mjs "<主题>"');
  console.log('示例：node hot_words.mjs "H-1B 换雇主"');
  process.exit(1);
}

const areas = {
  immigration: {
    match: /移民|签证|绿卡|H-?1B|H-?4|L-?1|O-?1|EB-?1|EB-?2|EB-?3|EB-?5|NIW|I-?\d{3}|F-?1|OPT|RFE|NOID|面谈|排期|入籍|公民|婚绿|亲属/i,
    account: '@凌图蔡神奇移民咨询',
    people: ['留学生', 'H-1B 打工人', '在美华人', '博士 / 博后', '刚结婚的夫妻', '父母在国内的'],
    scenes: ['换工作', '被裁员', '收到 RFE', '面谈前', '排期倒退', '身份快到期', '回国探亲'],
    asks: ['要准备什么', '多久能下来', '会不会影响身份', '自己办还是找律师', '常见被拒原因'],
    tags: ['#美国移民', '#美国签证', '#绿卡', '#H1B', '#NIW', '#EB1A', '#婚姻绿卡', '#留学生'],
  },
  pi: {
    match: /车祸|人伤|受伤|狗咬|摔倒|工伤|理赔|保险公司|赔偿|事故/,
    account: '@Lingtu咨询',
    people: ['开车通勤的', 'Uber / 外卖司机', '刚拿驾照的', '带孩子出门的', '老人'],
    scenes: ['刚出车祸', '对方没保险', '保险公司打电话来', '去医院之后', '车被拖走', '停车场被撞'],
    asks: ['第一步做什么', '要不要报警', '能不能录音', '医药费谁出', '多久能结案'],
    tags: ['#车祸', '#车祸理赔', '#美国车祸', '#人身伤害', '#美国保险', '#洛杉矶生活'],
  },
  litigation: {
    match: /诉讼|起诉|官司|合同|纠纷|劳资|欠款|房东|租客|商业|仲裁|小额法庭/,
    account: '@Lingtu咨询',
    people: ['小老板', '餐馆老板', '房东', '租客', '员工'],
    scenes: ['对方不付款', '收到律师信', '被员工告', '合伙闹翻', '押金不退'],
    asks: ['值不值得打', '要花多少时间', '证据怎么留', '小额法庭能不能解决', '先谈还是先告'],
    tags: ['#美国打官司', '#合同纠纷', '#劳资纠纷', '#商业纠纷', '#美国生意'],
  },
  trust: {
    match: /信托|遗嘱|遗产|继承|认证|probate|授权书|POA/i,
    account: '@Lingtu咨询',
    people: ['有房的父母', '新手爸妈', '再婚家庭', '父母在国内的', '退休人士'],
    scenes: ['刚买房', '孩子出生', '父母年纪大了', '家人突然过世', '海外有资产'],
    asks: ['和遗嘱有什么区别', '多少钱', '要不要每年更新', '不做会怎样', '遗产认证要多久'],
    tags: ['#生前信托', '#遗产规划', '#美国遗嘱', '#信托', '#美国买房'],
  },
};

const hit = Object.entries(areas).filter(([, a]) => a.match.test(topic));
const list = hit.length ? hit : Object.entries(areas);

console.log('━━━ 凌图小红书关键词候选 ━━━\n');
console.log(`主题：${topic}`);
if (!hit.length) console.log('（没认出业务类别，四类都列出来）');
console.log('⚠️ 以下只是组合思路，没有热度数据。真实热度请用 agent-reach 搜小红书。\n');

for (const [key, a] of list) {
  console.log(`【${{ immigration: '移民', pi: '人伤', litigation: '诉讼', trust: '信托遗嘱' }[key]}】账号 ${a.account}\n`);
  console.log('人群 + 主题：' + a.people.map((p) => `${p}${topic}`).join(' / '));
  console.log('场景 + 主题：' + a.scenes.map((s) => `${s}，${topic}`).join(' / '));
  console.log('读者会问：' + a.asks.map((q) => `${topic}${q}？`).join(' / '));
  console.log('可选标签：' + a.tags.join(' '));
  console.log();
}

console.log('━━━ 完成 ━━━');
