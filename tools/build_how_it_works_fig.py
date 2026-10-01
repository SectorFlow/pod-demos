#!/usr/bin/env python3
"""Generic 'where the code goes' figure for how-a-pod-works.html. Same layout as the kit's
architecture figure, no internal service or file names. Prints the SVG."""

def esc(t): return str(t).replace("&", "&amp;").replace("<", "&lt;")
def box(x,y,w,h,title,subs=(),cls="b",tsize=14):
    n=1+len(subs); top=y+h/2-(n-1)*8.5+5
    o=f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
    o+=f'<text class="t" x="{x+w/2}" y="{top}" text-anchor="middle" font-size="{tsize}">{esc(title)}</text>'
    for k,s in enumerate(subs):
        o+=f'<text class="s" x="{x+w/2}" y="{top+17*(k+1)}" text-anchor="middle">{esc(s)}</text>'
    return o
def arrow(x1,y1,x2,y2,label=None,lx=None,ly=None,anchor="start",cls="ln"):
    o=f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#a)"/>'
    if label: o+=f'<text class="lab" x="{lx}" y="{ly}" text-anchor="{anchor}">{esc(label)}</text>'
    return o
def band(x,y,w,h,label,cls):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/><text class="bl" x="{x+14}" y="{y+22}">{esc(label)}</text>'
DEFS='<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#1A6FC4"/></marker></defs>'

SERVICES=[("Model access",["models, budgets,","data guard"]),("Knowledge",["your documents,","versioned"]),("Connections",["your systems, keys,","approvals"]),("Quality gate",["your test cases,","release gate"]),("Tracing",["one trace","per run"]),("Sign-in",["your accounts,","roles"]),("Versions",["what is live,","rollback"])]

def fig():
    f='<svg viewBox="0 0 1040 760" role="img" aria-label="How a pod is built: your pod on top of a shared platform, connected to your systems">'+DEFS
    f+=box(40,14,260,54,"Your team",["phone, email, Teams or Slack, portal"],"p")
    f+=box(790,14,230,54,"Your managers",["browser"],"p")
    f+=box(40,112,260,64,"How work arrives",["calls, messages, schedules, data feeds"],"b")
    f+=box(790,112,230,64,"Your portal",["branded, your people only"],"b")
    f+=arrow(170,68,170,110,"requests, questions",178,94)
    f+=arrow(905,68,905,110,"sign in",913,94)
    f+=band(20,208,750,230,"YOUR POD · built for you, one per client, from a tested template","custom")
    f+=box(40,244,200,176,"Your agents",["read, decide, draft","and act, inside","the rules you set"],"b")
    chips=[("Settings",["models, limits, hosts"]),("Agent steps",["what each agent does,","in what order"]),("Messages",["what agents say,","in your words"]),("Tools",["which of your systems","each agent may use"]),("Test cases",["real cases from","your history"]),("Metrics",["the number you","judge the pod on"])]
    for k,(t,s) in enumerate(chips):
        f+=box(260+(k%3)*170,244+(k//3)*92,156,78,t,s,"c",13)
    f+=arrow(170,176,170,242,"work and data in",178,198)
    f+=band(20,474,1000,196,"SHARED PLATFORM · one platform under every pod, no interface of its own","head")
    for k,(n,d) in enumerate(SERVICES):
        f+=box(34+k*140,512,128,82,n,d,"h",13.5)
    f+='<text class="s" x="470" y="624">Shared by every pod. Every record carries your tenant id; the database enforces it.</text>'
    f+='<text class="s" x="470" y="644">A pod can only reach the systems named in its settings. Keys never leave the platform.</text>'
    f+=arrow(470,438,470,472,"every call traced, every action logged",480,468,cls="lnb")
    f+=arrow(1005,176,1005,472)
    f+='<text class="lab" x="995" y="196" text-anchor="end">reviews runs, edits</text><text class="lab" x="995" y="212" text-anchor="end">rules, approves</text>'
    f+='<rect class="p" x="790" y="262" width="190" height="84" rx="8"/>'
    f+='<circle cx="818" cy="292" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M804 322 q14 -22 28 0" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    f+='<text class="t" x="842" y="298" font-size="14">Your team</text><text class="t" x="842" y="316" font-size="14">decides</text><text class="s" x="842" y="334">people on the loop</text>'
    f+='<path class="lnb" d="M 120 420 L 120 446 L 860 446 L 860 348" fill="none" marker-end="url(#g)"/>'
    f+='<text class="labb" x="868" y="398">handoff with</text><text class="labb" x="868" y="414">the context</text>'
    f+='<path class="lnd" d="M 930 534 L 930 350" fill="none" marker-end="url(#a)"/>'
    f+='<text class="lab" x="922" y="432" text-anchor="end">flagged</text><text class="lab" x="922" y="448" text-anchor="end">runs to</text><text class="lab" x="922" y="464" text-anchor="end">review</text>'
    f+=box(250,712,540,44,"Your systems: ERP, CRM, WMS, phone, email, ticketing",[],"p",13.5)
    f+=arrow(378,594,378,710,"signed calls, only through Connections",386,700,cls="ln")
    return f+'</svg>'

if __name__=="__main__":
    print(fig())
