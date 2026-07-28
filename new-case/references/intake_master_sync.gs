/**
 * Intake → Master one-way sync — GENERALIZED TEMPLATE for new-case.
 * Container-bound to a case's native-Google-Sheet intake (Step 9 `gsheet_id`).
 *
 * Per-case the ONLY line to change is MASTER_TAB (set it to the case's team tab:
 *   Jerry → 'Piteam@', Ryan → 'Picase@', Amos → 'Claims@').
 * Master columns are resolved by HEADER NAME at run time (row 1 of MASTER_TAB), so this
 * survives column re-ordering and works across tabs whose layouts differ.
 *
 * Rules: one-way intake→master; full-content sync; a manually-edited master cell LOCKS
 * (lazy-detected via a stored shadow value) and intake never overwrites it again.
 * Initial Full Sync overwrites everything and re-seeds the shadow + clears locks.
 */

/***************** CONFIG *****************/
const MASTER_ID  = '1bugLaZ7TDbTdKHz_jecymoRoy7mMflCwVdhEUbidUyM';
const MASTER_TAB = 'Picase@';   // ← new-case: set to the assigned CM's tab
const MASTER_NAME_COL = 2;      // col B = Client Name on every team tab

// Intake layout: label/value column pairs (1-indexed). Driver in B/C, passengers across.
const PAIRS = [[2,3],[5,6],[8,9],[11,12],[14,15]];

// canonical field -> [intake-label startsWith, master-header startsWith] (both normalized).
// Order matters (more specific first). 'medi-cal' before 'medicare' is safe (no prefix clash).
const FIELDS = [
  ['Health Insurance', 'health insurance', 'health insurance'],
  ['Primary Doctor',   'primary doctor',   'primary doctor'],
  ['Urgent Care',      'urgentcare',       'urgent care'],
  ['Medi-Cal',         'medi-cal',         'medi-cal'],
  ['Medicare',         'medicare',         'medicare'],
  ['Ambulance',        'ambulance',        'ambulance'],
  ['Emergency',        'emergency',        'emergency']
];

// intake-name (normalized) -> master-name (normalized), for known spelling drift in THIS case.
const NAME_ALIASES = {};

const SHADOW_KEY = 'SYNC_SHADOW_V2';
const LOCK_KEY   = 'SYNC_LOCK_V2';

/***************** HELPERS *****************/
function norm_(s){ return s == null ? '' : String(s).replace(/\s+/g,' ').trim().toLowerCase(); }
function isNameLabel_(l){ const n = norm_(l); return n.slice(-4) === 'name' && (n.indexOf('driver')===0 || n.indexOf('pass')===0); }
function matchIntakeField_(label){
  const n = norm_(label);
  for (const [canon, intakePat] of FIELDS){ if (n.indexOf(intakePat) === 0) return canon; }
  return null;
}
function getProps_(key){ const raw = PropertiesService.getDocumentProperties().getProperty(key); return raw ? JSON.parse(raw) : {}; }
function setProps_(key, obj){ PropertiesService.getDocumentProperties().setProperty(key, JSON.stringify(obj)); }

/** Parse intake into [{client, field, value}] via label-driven scan. */
function parseIntake_(){
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sh.getDataRange().getValues();
  const out = [];
  for (const [lc, vc] of PAIRS){
    let current = null;
    for (let r = 0; r < data.length; r++){
      const label = data[r][lc-1];
      if (label === '' || label == null) continue;
      if (isNameLabel_(label)){
        const nm = data[r][vc-1];
        if (nm != null && String(nm).trim() !== '') current = String(nm).trim();
        continue;
      }
      const field = matchIntakeField_(label);
      if (field && current){
        const v = data[r][vc-1];
        out.push({ client: current, field: field, value: (v == null ? '' : String(v).trim()) });
      }
    }
  }
  return out;
}

/** normalized client name -> master row number */
function getMasterRowMap_(msTab){
  const last = msTab.getLastRow();
  const names = msTab.getRange(1, MASTER_NAME_COL, last, 1).getValues();
  const map = {};
  for (let i = 0; i < names.length; i++){ const nm = norm_(names[i][0]); if (nm) map[nm] = i + 1; }
  return map;
}

/** canonical field -> master column number, resolved from the live header row (row 1). */
function getMasterColMap_(msTab){
  const lastCol = msTab.getLastColumn();
  const hdr = msTab.getRange(1, 1, 1, lastCol).getValues()[0];
  const colMap = {};
  for (const [canon, , masterPat] of FIELDS){
    for (let c = 0; c < hdr.length; c++){
      if (norm_(hdr[c]).indexOf(masterPat) === 0){ colMap[canon] = c + 1; break; }
    }
  }
  return colMap; // fields whose header isn't found are simply absent (skipped)
}

/***************** CORE *****************/
function syncCore_(force){
  const records = parseIntake_();
  const ms = SpreadsheetApp.openById(MASTER_ID);
  const msTab = ms.getSheetByName(MASTER_TAB);
  if (!msTab) throw new Error('Master tab not found: ' + MASTER_TAB);
  const rowMap = getMasterRowMap_(msTab);
  const colMap = getMasterColMap_(msTab);
  const shadow = force ? {} : getProps_(SHADOW_KEY);
  const locks  = force ? {} : getProps_(LOCK_KEY);

  let written = 0, locked = 0, skipped = 0, unmatched = [], nocol = [];

  for (const rec of records){
    const col = colMap[rec.field];
    if (!col){ if (nocol.indexOf(rec.field) < 0) nocol.push(rec.field); continue; }
    let nn = norm_(rec.client); nn = NAME_ALIASES[nn] || nn;
    const row = rowMap[nn];
    if (!row){ if (unmatched.indexOf(rec.client) < 0) unmatched.push(rec.client); continue; }
    const key = rec.client + '||' + rec.field;
    const cell = msTab.getRange(row, col);
    const masterCur = cell.getValue() == null ? '' : String(cell.getValue());

    if (force){
      if (masterCur !== rec.value){ cell.setValue(rec.value); written++; }
      shadow[key] = rec.value; continue;
    }
    if (locks[key]){ skipped++; continue; }
    const shadowVal = shadow[key];
    if (shadowVal === undefined){
      if (masterCur === ''){ if (rec.value !== ''){ cell.setValue(rec.value); written++; } shadow[key] = rec.value; }
      else { locks[key] = true; locked++; }
      continue;
    }
    if (masterCur !== shadowVal){ locks[key] = true; locked++; continue; }
    if (rec.value !== shadowVal){ cell.setValue(rec.value); shadow[key] = rec.value; written++; }
  }
  setProps_(SHADOW_KEY, shadow);
  setProps_(LOCK_KEY, locks);
  return { written, locked, skipped, unmatched, nocol, total: records.length };
}

/***************** ENTRY POINTS *****************/
function onEditInstalled(e){
  try{
    if (!e || !e.range) return;
    if (e.range.getSheet().getIndex() !== 1) return;          // intake tab only
    if (PAIRS.map(p => p[1]).indexOf(e.range.getColumn()) < 0) return; // value cols only
    const s = syncCore_(false);
    SpreadsheetApp.getActiveSpreadsheet().toast('Synced. wrote ' + s.written + ', locked ' + s.locked, 'Intake→Master', 4);
  } catch(err){
    SpreadsheetApp.getActiveSpreadsheet().toast('Sync error: ' + err, 'Intake→Master', 6);
  }
}

function initialFullSync(){
  const s = syncCore_(true);
  SpreadsheetApp.getUi().alert('Initial Full Sync done.\nTab: ' + MASTER_TAB +
    '\nWrote ' + s.written + ' / ' + s.total + ' cells.' +
    '\nUnmatched clients: ' + (s.unmatched.join(', ') || 'none') +
    '\nFields with no master column: ' + (s.nocol.join(', ') || 'none'));
}

function installTrigger(){
  ScriptApp.getProjectTriggers().forEach(t => { if (t.getHandlerFunction() === 'onEditInstalled') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('onEditInstalled').forSpreadsheet(SpreadsheetApp.getActive()).onEdit().create();
  SpreadsheetApp.getUi().alert('Live trigger installed (tab: ' + MASTER_TAB + ').');
}

function showLocks(){
  const keys = Object.keys(getProps_(LOCK_KEY));
  SpreadsheetApp.getUi().alert('Locked cells (' + keys.length + '):\n' + (keys.join('\n') || 'none'));
}

function dryRun(){
  const records = parseIntake_();
  const ms = SpreadsheetApp.openById(MASTER_ID);
  const msTab = ms.getSheetByName(MASTER_TAB);
  const rowMap = getMasterRowMap_(msTab), colMap = getMasterColMap_(msTab);
  const lines = [];
  for (const rec of records){
    const col = colMap[rec.field]; if (!col){ continue; }
    let nn = norm_(rec.client); nn = NAME_ALIASES[nn] || nn;
    const row = rowMap[nn];
    if (!row){ lines.push('NO MATCH: ' + rec.client); continue; }
    const cur = String(msTab.getRange(row, col).getValue());
    if (cur !== rec.value) lines.push(rec.client + ' / ' + rec.field + ': "' + cur + '" -> "' + rec.value + '"');
  }
  Logger.log(lines.join('\n'));
}

function onOpen(){
  SpreadsheetApp.getUi().createMenu('🔁 Intake→Master')
    .addItem('1. Install Live Trigger', 'installTrigger')
    .addItem('2. Initial Full Sync (overwrite all)', 'initialFullSync')
    .addSeparator()
    .addItem('Dry-Run (to log)', 'dryRun')
    .addItem('Show Locked Cells', 'showLocks')
    .addToUi();
}
