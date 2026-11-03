import re, os
def sort_key(name):
    """Order files inside an exhibit folder: numeric prefix, then sub-letter group,
    then original before its English translation."""
    b=os.path.basename(name)
    m=re.match(r'^(\d+(?:-\d+)*)([A-Za-z0-9\-]*)', b)
    nums, suf = ((), "")
    if m:
        nums=tuple(int(x) for x in m.group(1).split("-"))
        suf=m.group(2) or ""
    grp = suf[0].lower() if suf else ""
    is_tr = 1 if re.search(r'English Translation|Certified Translation', b) else 0
    # within one numbered item: every English rendering first, then the originals
    return (nums, 0 if is_tr else 1, grp, b)

CJK=re.compile(r'[㐀-鿿豈-﫿]')
TRMARK=re.compile(r'English Translation|Certified Translation|English translation', re.I)
def is_translation(rel, siblings):
    """A file is the English rendering of a Chinese original if it is marked as such, or
    if it is a .docx with a purely Latin name sitting next to CJK-named sources."""
    b=os.path.basename(rel)
    if TRMARK.search(b): return True
    if b.lower().endswith(".docx") and not CJK.search(b):
        if any(CJK.search(os.path.basename(s)) for s in siblings if s!=rel): return True
    return False

def translations_first(items):
    """Single pass: wherever an original is immediately followed by its translation, swap."""
    rels=[(it[0] if isinstance(it,tuple) else it) for it in items]
    out=list(items); i=0
    while i < len(out)-1:
        a=out[i][0] if isinstance(out[i],tuple) else out[i]
        b=out[i+1][0] if isinstance(out[i+1],tuple) else out[i+1]
        if (not is_translation(a, rels)) and is_translation(b, rels):
            out[i], out[i+1] = out[i+1], out[i]
            i += 2
        else:
            i += 1
    return out

def _stem(name):
    """(numeric parts, suffix) from a leading token like 5-4-5ca -> ((5,4,5),'ca')"""
    b=os.path.basename(name)
    m=re.match(r'^(\d+(?:-\d+)*)([A-Za-z][A-Za-z0-9]*)?', b)
    if not m: return ((), "")
    return (tuple(int(x) for x in m.group(1).split("-")), (m.group(2) or ""))

def _words(name):
    b=os.path.basename(name)
    b=re.sub(r'^\S+\s*', '', b)                       # drop the number token
    b=re.sub(r'English Translation|\(original[^)]*\)|\.docx|\.pdf|\.png|\.jpe?g', ' ', b, flags=re.I)
    return {w for w in re.findall(r'[a-z0-9]+', b.lower()) if len(w)>2}

def pair_order(files):
    """One-to-one: each English rendering immediately followed by the original it renders.
    Pairing is by suffix (b->ba, c->ca, d->da, falling back to 'a' then the bare number);
    a leftover original attaches to the translation whose title it matches best."""
    groups={}
    for f in files:
        nums,suf=_stem(f)
        groups.setdefault(nums, []).append((suf, f))
    out=[]
    for nums in sorted(groups):
        items=groups[nums]
        trans=[(s,f) for s,f in items if TRMARK.search(os.path.basename(f))]
        origs=[(s,f) for s,f in items if not TRMARK.search(os.path.basename(f))]
        trans.sort(key=lambda x: x[0]); origs.sort(key=lambda x: x[0])
        used=set(); seq=[]
        for s,f in trans:
            mate=None
            for cand in (s[0]+"a" if s else None, "a", ""):
                if cand is None: continue
                for s2,f2 in origs:
                    if f2 in used: continue
                    if s2==cand: mate=(s2,f2); break
                if mate: break
            seq.append((f, mate[1] if mate else None))
            if mate: used.add(mate[1])
        leftover=[(s,f) for s,f in origs if f not in used]
        # attach each leftover to the closest-matching translation, else keep at the end
        tail=[]
        for s,f in leftover:
            best=None; score=0
            for i,(tf,_m) in enumerate(seq):
                sc=len(_words(f) & _words(tf))
                if sc>score: score, best = sc, i
            if best is not None and score>=2: seq[best]=seq[best]+(f,)
            else: tail.append(f)
        for entry in seq:
            for f in entry:
                if f: out.append(f)
        out.extend(tail)
    return out
