# -*- coding: utf-8 -*-
"""Generate dashboard/index.html — an interactive compliance dashboard.

    python build/build_dashboard.py

Self-contained single HTML page (no external data; the assessment JSON is inlined).
Reproducible from the same source of truth as every other artifact.
"""
import os
import json

import compute_stats as S
from controls_data import CONTROLS, SYSTEM, FRAMEWORK, ASSESSMENT_DATE, THEME_ORDER
from risk_data import RISKS, band

OUT = os.path.join(os.path.dirname(__file__), "..", "dashboard", "index.html")

GAP_ST = ("Partially Implemented", "Not Implemented")


def build_payload():
    score, napp = S.compliance_score()
    counts = S.overall_counts()
    return {
        "system": {k: SYSTEM[k] for k in ("company", "product", "tagline",
                                          "environment", "certification_goal")},
        "framework": FRAMEWORK,
        "assessment_date": ASSESSMENT_DATE.strftime("%d %b %Y"),
        "totals": {
            "controls": len(CONTROLS), "applicable": napp,
            "implemented": counts.get("Implemented", 0),
            "partial": counts.get("Partially Implemented", 0),
            "not_implemented": counts.get("Not Implemented", 0),
            "not_applicable": counts.get("Not Applicable", 0),
            "weighted": round(score, 1),
            "impl_rate": round(S.implemented_rate(), 1),
            "gaps": len(S.gaps()),
        },
        "gaps_by_sev": dict(S.gaps_by_severity()),
        "by_theme": {t: {"score": round(d["score_pct"], 1),
                         "applicable": d["applicable"],
                         "impl": d["Implemented"], "part": d["Partially Implemented"],
                         "noim": d["Not Implemented"], "na": d["Not Applicable"]}
                     for t, d in S.by_theme().items()},
        "theme_order": THEME_ORDER,
        "controls": [
            {"id": c["id"], "title": c["title"], "theme": c["theme"],
             "status": c["status"], "owner": c["owner"], "risk": c["risk"],
             "gap": c["gap"] if c["status"] in GAP_ST else "",
             "remediation": c["remediation"] if c["status"] in GAP_ST else "",
             "target": c["target"] if c["status"] in GAP_ST else "",
             "nist": c["nist"]}
            for c in CONTROLS
        ],
        "risks": [
            {"id": r["id"], "title": r["title"], "owner": r["owner"],
             "li": r["l_inh"], "ii": r["i_inh"],
             "lr": r["l_res"], "ir": r["i_res"],
             "inherent": r["l_inh"] * r["i_inh"], "residual": r["l_res"] * r["i_res"],
             "inh_band": band(r["l_inh"] * r["i_inh"]),
             "res_band": band(r["l_res"] * r["i_res"]),
             "treatment": r["treatment"], "controls": r["controls"]}
            for r in RISKS
        ],
    }


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sightline ISMS Readiness</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet"/>
<style>
  /* Layout: scannable compliance dashboard — summary tiles, charts, filterable control register.
     Palette: slate-navy accent with semantic good/warn/bad/critical, neutrals biased to navy. */
  :root{
    --bg:#eef1f5; --surface:#ffffff; --surface-2:#f6f8fb; --ink:#1b2430;
    --muted:#5c6773; --line:#d9e0e9; --accent:#1f5c8b; --accent-2:#163f5f;
    --accent-ink:#ffffff;
    --good:#2e8b7a; --good-bg:#d7ece6; --good-ink:#1c6253;
    --warn:#c98a00; --warn-bg:#faeccc; --warn-ink:#7a5400;
    --bad:#c0392b; --bad-bg:#f6d6d2; --bad-ink:#8c2618;
    --crit:#7b1e1e; --crit-bg:#ecd3d0; --crit-ink:#5a1414;
    --na:#8a93a0; --na-bg:#e6e9ee;
    --shadow:0 1px 2px rgba(20,35,55,.06),0 6px 20px rgba(20,35,55,.06);
    --radius:14px;
  }
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0f141b; --surface:#171e27; --surface-2:#1e2732; --ink:#e7edf4;
    --muted:#9aa6b4; --line:#2a333f; --accent:#5aa0d2; --accent-2:#8cc2e8;
    --accent-ink:#0c1016;
    --good:#49b89f; --good-bg:#15332d; --good-ink:#8fe0cd;
    --warn:#e0a63a; --warn-bg:#3a2d12; --warn-ink:#f0cf8f;
    --bad:#e2695b; --bad-bg:#3a1e1a; --bad-ink:#f2b3aa;
    --crit:#e08b8b; --crit-bg:#331717; --crit-ink:#f0bcbc;
    --na:#7e8794; --na-bg:#232c37;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }}
  :root[data-theme="dark"]{
    color-scheme:dark;
    --bg:#0f141b; --surface:#171e27; --surface-2:#1e2732; --ink:#e7edf4;
    --muted:#9aa6b4; --line:#2a333f; --accent:#5aa0d2; --accent-2:#8cc2e8;
    --accent-ink:#0c1016;
    --good:#49b89f; --good-bg:#15332d; --good-ink:#8fe0cd;
    --warn:#e0a63a; --warn-bg:#3a2d12; --warn-ink:#f0cf8f;
    --bad:#e2695b; --bad-bg:#3a1e1a; --bad-ink:#f2b3aa;
    --crit:#e08b8b; --crit-bg:#331717; --crit-ink:#f0bcbc;
    --na:#7e8794; --na-bg:#232c37;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{background:var(--bg);color:var(--ink);
    font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1180px;margin:0 auto;padding:24px 16px 56px}
  .num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
  a{color:var(--accent)}
  h1,h2,h3{text-wrap:balance;margin:0}
  /* header */
  header.top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:6px}
  .brand h1{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:clamp(1.5rem,2.4vw,2.1rem);letter-spacing:-.01em}
  .brand .sub{color:var(--muted);font-size:.95rem;margin-top:4px;max-width:62ch}
  .meta{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
  .pill{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;
    font-size:.74rem;font-weight:600;border:1px solid var(--line);background:var(--surface-2);color:var(--muted)}
  .toggle{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;
    padding:8px 14px;font:inherit;font-size:.82rem;font-weight:600;cursor:pointer;box-shadow:var(--shadow)}
  .toggle:hover{border-color:var(--accent)}
  .note{font-size:.78rem;color:var(--muted);background:var(--surface-2);border:1px dashed var(--line);
    border-radius:10px;padding:8px 12px;margin:14px 0 20px}
  /* tiles */
  .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}
  .tile{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:16px 18px;box-shadow:var(--shadow);position:relative;overflow:hidden}
  .tile .k{font-size:.76rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
  .tile .v{font-size:2.05rem;font-weight:600;margin-top:6px;letter-spacing:-.02em}
  .tile .foot{font-size:.8rem;color:var(--muted);margin-top:4px}
  .stripe{position:absolute;left:0;top:0;bottom:0;width:5px}
  .s-good{background:var(--good)} .s-warn{background:var(--warn)} .s-bad{background:var(--bad)} .s-accent{background:var(--accent)}
  .bar{height:7px;border-radius:999px;background:var(--surface-2);margin-top:12px;overflow:hidden}
  .bar>i{display:block;height:100%;border-radius:999px}
  /* panels */
  .grid2{display:grid;grid-template-columns:1.15fr .85fr;gap:16px;margin-bottom:16px}
  .panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:18px;box-shadow:var(--shadow)}
  .panel h2{font-size:1rem;font-weight:700;margin-bottom:2px}
  .panel .cap{color:var(--muted);font-size:.82rem;margin-bottom:14px}
  /* family bars */
  .fam{display:flex;align-items:center;gap:12px;margin:11px 0}
  .fam .name{width:120px;font-size:.86rem;font-weight:600;flex:none}
  .fam .track{flex:1;height:22px;background:var(--surface-2);border-radius:7px;overflow:hidden;position:relative}
  .fam .fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent-2));border-radius:7px}
  .fam .val{width:48px;text-align:right;font-weight:600;font-size:.86rem;flex:none}
  .fam .cnt{width:118px;font-size:.72rem;color:var(--muted);flex:none}
  /* status segmented */
  .seg{display:flex;height:30px;border-radius:8px;overflow:hidden;border:1px solid var(--line)}
  .seg>span{display:flex;align-items:center;justify-content:center;color:#fff;font-size:.78rem;font-weight:600}
  .legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;font-size:.8rem;color:var(--muted)}
  .legend b{color:var(--ink)}
  .dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:middle}
  /* chips */
  .sev-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
  .sev{flex:1;min-width:86px;border-radius:10px;padding:12px;text-align:center;border:1px solid var(--line)}
  .sev .n{font-size:1.5rem;font-weight:600}
  .sev .l{font-size:.74rem;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
  .sev.crit{background:var(--crit-bg);color:var(--crit-ink)}
  .sev.high{background:var(--bad-bg);color:var(--bad-ink)}
  .sev.med{background:var(--warn-bg);color:var(--warn-ink)}
  .sev.low{background:var(--good-bg);color:var(--good-ink)}
  /* controls table */
  .toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
  .toolbar input,.toolbar select{font:inherit;font-size:.85rem;padding:8px 10px;border-radius:9px;
    border:1px solid var(--line);background:var(--surface);color:var(--ink)}
  .toolbar input{flex:1;min-width:160px}
  .toolbar input:focus,.toolbar select:focus{outline:2px solid var(--accent);outline-offset:1px}
  .count{font-size:.8rem;color:var(--muted);margin-left:auto}
  .tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
  table{border-collapse:collapse;width:100%;font-size:.86rem;min-width:720px}
  thead th{position:sticky;top:0;background:var(--surface-2);text-align:left;padding:10px 12px;
    font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);border-bottom:1px solid var(--line);cursor:pointer;white-space:nowrap}
  thead th:hover{color:var(--ink)}
  tbody td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
  tbody tr:hover{background:var(--surface-2)}
  tbody tr.gap{cursor:pointer}
  td.cid{font-family:"IBM Plex Mono",monospace;font-weight:600;color:var(--accent);white-space:nowrap}
  .tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.73rem;font-weight:600;white-space:nowrap}
  .st-impl{background:var(--good-bg);color:var(--good-ink)}
  .st-part{background:var(--warn-bg);color:var(--warn-ink)}
  .st-noim{background:var(--bad-bg);color:var(--bad-ink)}
  .st-na{background:var(--na-bg);color:var(--muted)}
  .rk-Critical{background:var(--crit-bg);color:var(--crit-ink)}
  .rk-High{background:var(--bad-bg);color:var(--bad-ink)}
  .rk-Medium{background:var(--warn-bg);color:var(--warn-ink)}
  .rk-Low{background:var(--good-bg);color:var(--good-ink)}
  .rk-None,.rk-NA{color:var(--muted)}
  .detail td{background:var(--surface-2);font-size:.84rem;color:var(--muted)}
  .detail b{color:var(--ink)}
  .hidden{display:none}
  /* risk section */
  .risk-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  .matrix{display:grid;grid-template-columns:auto repeat(5,1fr);gap:3px;font-size:.72rem}
  .matrix .cell{aspect-ratio:1;border-radius:6px;display:flex;align-items:center;justify-content:center;
    flex-wrap:wrap;gap:2px;color:#fff;font-weight:600;font-family:"IBM Plex Mono",monospace;position:relative}
  .matrix .axis{display:flex;align-items:center;justify-content:center;color:var(--muted);font-weight:600}
  .matrix .rid{background:rgba(0,0,0,.28);border-radius:4px;padding:0 3px;font-size:.66rem}
  .mx-Low{background:var(--good)} .mx-Medium{background:var(--warn)} .mx-High{background:var(--bad)} .mx-Critical{background:var(--crit)}
  .toprisk{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:.85rem}
  .toprisk:last-child{border-bottom:none}
  .toprisk .rid{font-family:"IBM Plex Mono",monospace;font-weight:600;color:var(--accent);flex:none;width:40px}
  .toprisk .arrow{color:var(--muted);font-family:"IBM Plex Mono",monospace;flex:none}
  footer{margin-top:28px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.8rem;
    display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
  @media (max-width:860px){.tiles{grid-template-columns:repeat(2,1fr)}.grid2{grid-template-columns:1fr}.risk-grid{grid-template-columns:1fr}}
  @media (max-width:430px){.tiles{grid-template-columns:1fr}.fam .cnt{display:none}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1 id="h-title"></h1>
      <div class="sub" id="h-sub"></div>
      <div class="meta" id="h-meta"></div>
    </div>
    <button class="toggle" id="themeBtn" aria-label="Toggle colour theme">◑ Theme</button>
  </header>
  <div class="note" id="h-note"></div>

  <section class="tiles" id="tiles"></section>

  <div class="grid2">
    <div class="panel">
      <h2>Compliance by control theme</h2>
      <div class="cap">Weighted implementation score (Implemented = 1, Partial = 0.5) over applicable controls</div>
      <div id="fam"></div>
    </div>
    <div class="panel">
      <h2>Implementation status</h2>
      <div class="cap">All <span id="st-total"></span> Annex A controls</div>
      <div class="seg" id="seg"></div>
      <div class="legend" id="seg-legend"></div>
      <h2 style="margin-top:20px">Open gaps by severity</h2>
      <div class="cap"><span id="g-total"></span> gaps across partial &amp; not-implemented controls</div>
      <div class="sev-row" id="sev"></div>
    </div>
  </div>

  <div class="panel" style="margin-bottom:16px">
    <h2>Control register</h2>
    <div class="cap">Filter and sort all 93 controls. Click a row with an open gap to see the finding and remediation.</div>
    <div class="toolbar">
      <input id="q" type="search" placeholder="Search control id, title, owner…" aria-label="Search controls"/>
      <select id="f-theme" aria-label="Filter by theme"><option value="">All themes</option></select>
      <select id="f-status" aria-label="Filter by status"><option value="">All statuses</option></select>
      <select id="f-risk" aria-label="Filter by risk"><option value="">All risk ratings</option></select>
      <span class="count" id="rowcount"></span>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr>
          <th data-sort="id">Control</th>
          <th data-sort="title">Title</th>
          <th data-sort="theme">Theme</th>
          <th data-sort="status">Status</th>
          <th data-sort="owner">Owner</th>
          <th data-sort="risk">Risk</th>
        </tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </div>

  <div class="panel">
    <h2>Risk register</h2>
    <div class="cap">Inherent risk matrix (5×5) and the largest residual risks after current controls</div>
    <div class="risk-grid">
      <div>
        <div class="matrix" id="matrix"></div>
        <div class="legend" style="margin-top:10px">
          <span><span class="dot" style="background:var(--good)"></span>Low</span>
          <span><span class="dot" style="background:var(--warn)"></span>Medium</span>
          <span><span class="dot" style="background:var(--bad)"></span>High</span>
          <span><span class="dot" style="background:var(--crit)"></span>Critical</span>
          <span style="color:var(--muted)">numbers = Risk IDs · axis: impact → / likelihood ↑</span>
        </div>
      </div>
      <div id="toprisks"></div>
    </div>
  </div>

  <footer>
    <span id="f-left"></span>
    <span>Synthetic data · framework references are real · <a href="https://github.com/Krishita17/ComplyForge">github.com/Krishita17/ComplyForge</a></span>
  </footer>
</div>

<script type="application/json" id="data">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById("data").textContent);
const $ = s => document.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;};
const STATUS_CLASS={"Implemented":"st-impl","Partially Implemented":"st-part","Not Implemented":"st-noim","Not Applicable":"st-na"};
const STATUS_SHORT={"Implemented":"Implemented","Partially Implemented":"Partial","Not Implemented":"Not impl.","Not Applicable":"N/A"};
const SEGC={"Implemented":"var(--good)","Partially Implemented":"var(--warn)","Not Implemented":"var(--bad)","Not Applicable":"var(--na)"};

/* header */
$("#h-title").textContent = D.system.product + " — ISMS Readiness";
$("#h-sub").textContent = D.system.tagline + ". " + D.system.company + ".";
$("#h-meta").innerHTML = [
  D.framework, "NIST 800-53 crosswalk", D.system.environment.split(";")[0].trim(),
  "Assessed " + D.assessment_date
].map(x=>`<span class="pill">${x}</span>`).join("");
$("#h-note").innerHTML = "<b>Portfolio artifact.</b> "+D.system.company+" and "+D.system.product+
  " are fictional. Control IDs/titles are the real ISO/IEC 27001:2022 Annex A set; statuses, evidence and gaps are synthetic. Goal: "+D.system.certification_goal+".";
$("#f-left").textContent = D.totals.controls+" controls · "+D.totals.applicable+" applicable · "+D.risks.length+" risks";

/* tiles */
const T=D.totals, G=D.gaps_by_sev;
const tiles=[
  {k:"Weighted compliance",v:T.weighted+"%",foot:T.impl_rate+"% fully implemented",stripe: T.weighted>=75?"s-good":"s-warn",bar:T.weighted,barc:T.weighted>=75?"var(--good)":"var(--warn)"},
  {k:"Controls implemented",v:T.implemented+"/"+T.applicable,foot:T.partial+" partial · "+T.not_implemented+" not implemented",stripe:"s-accent",bar:100*T.implemented/T.applicable,barc:"var(--accent)"},
  {k:"Open gaps",v:T.gaps,foot:(G.Critical||0)+" critical · "+(G.High||0)+" high",stripe:(G.Critical||G.High)?"s-bad":"s-warn"},
  {k:"Not applicable",v:T.not_applicable,foot:"scoped out with justification",stripe:"s-accent"},
];
const tilesBox=$("#tiles");
tiles.forEach(t=>{
  const d=el("div","tile");
  d.appendChild(el("div","stripe "+t.stripe));
  d.appendChild(el("div","k",t.k));
  d.appendChild(el("div","v num",t.v));
  d.appendChild(el("div","foot",t.foot));
  if(t.bar!=null){const b=el("div","bar");const i=el("i");i.style.width=Math.min(100,t.bar)+"%";i.style.background=t.barc;b.appendChild(i);d.appendChild(b);}
  tilesBox.appendChild(d);
});

/* family bars */
const famBox=$("#fam");
D.theme_order.forEach(t=>{
  const d=D.by_theme[t];
  const row=el("div","fam");
  row.appendChild(el("div","name",t));
  const track=el("div","track");const fill=el("div","fill");fill.style.width=d.score+"%";track.appendChild(fill);
  row.appendChild(track);
  row.appendChild(el("div","val num",d.score+"%"));
  row.appendChild(el("div","cnt","I"+d.impl+" · P"+d.part+" · N"+d.noim+(d.na?" · NA"+d.na:"")));
  famBox.appendChild(row);
});

/* status segmented */
const order=["Implemented","Partially Implemented","Not Implemented","Not Applicable"];
const stCounts={Implemented:T.implemented,"Partially Implemented":T.partial,"Not Implemented":T.not_implemented,"Not Applicable":T.not_applicable};
$("#st-total").textContent=T.controls;
const seg=$("#seg");
order.forEach(s=>{const n=stCounts[s];if(!n)return;const span=el("span","",n);span.style.flex=n;span.style.background=SEGC[s];if(n<4)span.textContent="";seg.appendChild(span);});
$("#seg-legend").innerHTML=order.map(s=>`<span><span class="dot" style="background:${SEGC[s]}"></span>${STATUS_SHORT[s]} <b>${stCounts[s]}</b></span>`).join("");

/* severity chips */
$("#g-total").textContent=T.gaps;
const sevs=[["Critical","crit"],["High","high"],["Medium","med"],["Low","low"]];
$("#sev").innerHTML=sevs.map(([name,c])=>`<div class="sev ${c}"><div class="n num">${G[name]||0}</div><div class="l">${name}</div></div>`).join("");

/* control table */
const themes=[...new Set(D.controls.map(c=>c.theme))];
themes.forEach(t=>$("#f-theme").appendChild(el("option",null,t))&&($("#f-theme").lastChild.value=t));
order.forEach(s=>{const o=el("option",null,s);o.value=s;$("#f-status").appendChild(o);});
["Critical","High","Medium","Low"].forEach(r=>{const o=el("option",null,r);o.value=r;$("#f-risk").appendChild(o);});

let sortKey="id",sortDir=1;
function render(){
  const q=$("#q").value.toLowerCase().trim();
  const ft=$("#f-theme").value,fs=$("#f-status").value,fr=$("#f-risk").value;
  let rows=D.controls.filter(c=>{
    if(ft&&c.theme!==ft)return false;
    if(fs&&c.status!==fs)return false;
    if(fr&&c.risk!==fr)return false;
    if(q&&!(c.id+" "+c.title+" "+c.owner).toLowerCase().includes(q))return false;
    return true;
  });
  rows.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];return (x>y?1:x<y?-1:0)*sortDir;});
  const tb=$("#tbody");tb.innerHTML="";
  rows.forEach(c=>{
    const tr=el("tr",c.gap?"gap":"");
    tr.innerHTML=`<td class="cid">${c.id}</td><td>${c.title}</td><td>${c.theme}</td>`+
      `<td><span class="tag ${STATUS_CLASS[c.status]}">${STATUS_SHORT[c.status]}</span></td>`+
      `<td>${c.owner}</td>`+
      `<td><span class="tag rk-${c.risk.replace('/','')}">${c.risk==="None"?"—":c.risk}</span></td>`;
    tb.appendChild(tr);
    if(c.gap){
      const dr=el("tr","detail hidden");
      dr.innerHTML=`<td colspan="6"><b>Gap:</b> ${c.gap}<br><b>Remediation:</b> ${c.remediation} <b>· Target:</b> ${c.target} <b>· NIST:</b> ${c.nist}</td>`;
      tb.appendChild(dr);
      tr.addEventListener("click",()=>dr.classList.toggle("hidden"));
    }
  });
  $("#rowcount").textContent=rows.length+" of "+D.controls.length+" controls";
}
["#q","#f-theme","#f-status","#f-risk"].forEach(s=>$(s).addEventListener("input",render));
document.querySelectorAll("th[data-sort]").forEach(th=>th.addEventListener("click",()=>{
  const k=th.dataset.sort;sortDir=(sortKey===k)?-sortDir:1;sortKey=k;render();
}));
render();

/* risk matrix */
const mx=$("#matrix");
const byCell={};D.risks.forEach(r=>{(byCell[r.li+"-"+r.ii]=byCell[r.li+"-"+r.ii]||[]).push(r.id.replace("R-",""));});
function cellBand(s){return s>=15?"Critical":s>=10?"High":s>=5?"Medium":"Low";}
for(let L=5;L>=1;L--){
  mx.appendChild(el("div","axis",L));
  for(let I=1;I<=5;I++){
    const s=L*I;const c=el("div","cell mx-"+cellBand(s));
    const ids=byCell[L+"-"+I]||[];
    c.innerHTML=ids.map(x=>`<span class="rid">${x}</span>`).join("");
    c.title="Likelihood "+L+" × Impact "+I+" = "+s;
    mx.appendChild(c);
  }
}
mx.appendChild(el("div","axis",""));
["1","2","3","4","5"].forEach(i=>mx.appendChild(el("div","axis",i)));

/* top residual risks */
const topRisks=[...D.risks].sort((a,b)=>b.residual-a.residual).slice(0,6);
$("#toprisks").innerHTML=topRisks.map(r=>
  `<div class="toprisk"><span class="rid">${r.id}</span>`+
  `<span style="flex:1">${r.title}</span>`+
  `<span class="tag rk-${r.inh_band}">${r.inherent}</span>`+
  `<span class="arrow">→</span>`+
  `<span class="tag rk-${r.res_band}">${r.residual}</span></div>`
).join("");

/* theme toggle */
const btn=$("#themeBtn");
function sysDark(){return window.matchMedia&&window.matchMedia("(prefers-color-scheme:dark)").matches;}
let mode=null;try{mode=localStorage.getItem("cf-theme");}catch(e){}
function apply(){if(mode)document.documentElement.setAttribute("data-theme",mode);else document.documentElement.removeAttribute("data-theme");}
apply();
btn.addEventListener("click",()=>{
  const dark=mode?mode==="dark":sysDark();
  mode=dark?"light":"dark";
  try{localStorage.setItem("cf-theme",mode);}catch(e){}
  apply();
});
</script>
</body>
</html>
"""


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = json.dumps(build_payload(), ensure_ascii=False)
    html = HTML.replace("__DATA__", payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.relpath(OUT), f"({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
