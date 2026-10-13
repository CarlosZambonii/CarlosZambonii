import sys, re
from html import escape
R,P,G,D,Wt='#ff0033','#ff4d4d','#8b949e','#6e7681','#e6e6e6'
def prompt(path): return ('prompt',[('┌──(',R),('carlos@redteam',P),(')-[',R),(path,Wt),(']',R)])
def term(out, path, cmd, body, T=12.0, W=900):
    LH,X,Y0=22,24,62
    lines=[prompt(path),('cmd',[('└─$ ',R),(cmd,Wt)]),('out',[])]+[('out',b) for b in body]+[('out',[]),prompt(path),('last',[('└─$ ',R)])]
    H=Y0+LH*len(lines)+4; css=[]; els=[]; cur=''; t=0.4; pct=lambda s:f'{100*s/T:.2f}%'
    for i,(kind,spans) in enumerate(lines):
        y=Y0+i*LH; ts=''.join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s,c in spans)
        css.append(f'@keyframes k{i}{{0%,{pct(t)}{{opacity:0}}{pct(t+.01)},100%{{opacity:1}}}}')
        if kind=='cmd':
            pre=4*8.4; n=len(cmd); dur=1.4
            css.append(f'@keyframes w{i}{{0%,{pct(t)}{{width:{pre}px}}{pct(t+dur)},100%{{width:{pre+n*8.4}px}}}}')
            els.append(f'<clipPath id="c{i}"><rect x="{X}" y="{y-16}" height="{LH}" style="animation:w{i} {T}s steps({n}) infinite"/></clipPath>')
            els.append(f'<text x="{X}" y="{y}" clip-path="url(#c{i})" style="animation:k{i} {T}s infinite">{ts}</text>'); t+=dur+0.5
        else:
            els.append(f'<text x="{X}" y="{y}" style="animation:k{i} {T}s infinite">{ts}</text>')
            if kind=='last': cur=f'<g class="bl"><rect fill="{R}" x="{X+4*8.4}" y="{y-14}" width="9" height="18" style="opacity:0;animation:k{i} {T}s infinite"/></g>'
            t+=0.25 if kind=='out' else 0.15
    nl='\n'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font: 14px 'JetBrains Mono','Fira Code',Consolas,'DejaVu Sans Mono','Courier New',monospace; white-space: pre; opacity: 0; }}
    .bl {{ animation: bl 1s infinite steps(1); }}
    @keyframes bl {{ 50% {{ opacity: 0; }} }}
    {nl.join(css)}
  </style>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="#0d1117" stroke="#ff0033" stroke-opacity=".5"/>
  <path d="M1 11a10 10 0 0 1 10-10h{W-22}a10 10 0 0 1 10 10v23H1z" fill="#161b22"/>
  <circle cx="22" cy="17" r="6" fill="#ff5f56"/><circle cx="42" cy="17" r="6" fill="#ffbd2e"/><circle cx="62" cy="17" r="6" fill="#27c93f"/>
  <text x="{W/2}" y="22" text-anchor="middle" style="opacity:1;fill:{G};font-size:13px">carlos@redteam: {escape(path)}</text>
  {nl.join(els)}
  {cur}
</svg>'''
    open(out,'w').write(svg)
    import xml.dom.minidom as m; m.parse(out)

