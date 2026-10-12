"""Build public/work.html and public/zennith.html.

The home page (public/index.html) is the source of truth for the <head>,
the site header and the footer; this script copies them into the sub-pages
and adds each page's own content. Run it after editing index.html:

    python scripts/build_subpages.py
"""
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
home = (PUBLIC / "index.html").read_text(encoding="utf8")

head = home[:home.index("<body")]
wrap = re.search(r'<body id="top">\n(<div style="background[^>]*>)', home).group(1)
header = re.search(r"<header.*?</header>", home, re.S).group(0)
footer = re.search(r"<footer.*?</footer>", home, re.S).group(0)


def to_subpage(s):
    for a in ("about", "expertise", "process", "contact"):
        s = s.replace(f'href="#{a}"', f'href="index.html#{a}"')
    return s.replace('href="#top"', 'href="index.html"')


header, footer = to_subpage(header), to_subpage(footer)
EMAIL = "mailto:cmutizwa@gmail.com"


def page(filename, title, description, main, current):
    hd = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head)
    hd = re.sub(r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{description}">', hd)
    hdr = header.replace('<a href="work.html" style="text-decoration: none">',
                         f'<a href="work.html" aria-current="{current}" style="text-decoration: none">')
    html = (f'{hd}<body id="top">\n{wrap}\n{hdr}\n\n<main id="main">\n{main}\n</main>\n\n'
            f'{footer}\n</div>\n</body>\n</html>\n')
    (PUBLIC / filename).write_text(html, encoding="utf8", newline="\n")


G = "#A8834F"
SEC = "max-width: 1240px; margin: 0 auto; padding: {}px 32px 0"
SERIF = "'Cormorant Garamond', serif"
ARROW = ('<svg width="22" height="12" viewBox="0 0 22 12" fill="none" stroke="currentColor" '
         'stroke-width="1.3" aria-hidden="true"><path d="M0 6h20M15 1l5 5-5 5"></path></svg>')


def eyebrow(t):
    return (f'<div style="font-size: 12px; letter-spacing: 3px; text-transform: uppercase; '
            f'color: #7E6033; font-weight: 400">{t}</div>')


def h1(t):
    return (f'<h1 style="margin: 8px 0 0; font-family: {SERIF}; font-weight: 500; '
            f'font-size: clamp(48px, 7vw, 92px); line-height: 0.95; letter-spacing: 1px; '
            f'text-transform: uppercase; color: #333A2B">{t}</h1>')


def h2(t):
    return (f'<h2 class="h2-xl" style="margin: 0 0 20px; font-family: {SERIF}; font-weight: 500; '
            f'font-size: 40px; line-height: 1.05; text-transform: uppercase; letter-spacing: 1px">{t}</h2>')


def p(t, mw=640):
    return f'<p style="margin: 0 0 16px; max-width: {mw}px; font-size: 17px; line-height: 1.7">{t}</p>'


def tags(ts, col=G):
    return ('<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:20px">' + "".join(
        f'<span style="padding:8px 14px;border:1px solid {col};font-size:11px;letter-spacing:2px;'
        f'text-transform:uppercase;font-weight:400">{t}</span>' for t in ts) + "</div>")


def btn(href, t):
    return (f'<a href="{href}" style="display: inline-flex; align-items: center; gap: 18px; '
            f'padding: 15px 26px; background: #3B4232; color: #F4EEE6; text-decoration: none; '
            f'font-size: 13px; letter-spacing: 2.5px; text-transform: uppercase; font-weight: 400">'
            f'{t} {ARROW}</a>')


def cta_row(question):
    return (f'<section style="{SEC.format(80)}"><div style="display:flex;flex-wrap:wrap;gap:20px;'
            f'align-items:center;justify-content:space-between;border-top:1px solid #C9B89A;padding-top:36px">'
            f'<p style="margin:0;font-family:{SERIF};font-size:30px;line-height:1.25">{question}</p>'
            f'{btn(EMAIL, "Email me")}</div></section>\n<div style="height:110px"></div>')


# ---------------------------------------------------------------- work.html
def case(id, bg, fg, name, sub, body, tg, link=""):
    cta = f'<div style="margin-top:28px">{link}</div>' if link else ""
    return (f'<section id="{id}" style="{SEC.format(72)}"><div style="background:{bg};color:{fg};'
            f'padding:48px 44px;display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start">'
            f'<div style="flex:1 1 280px;min-width:0"><h2 class="h2-xl" style="margin:0;font-family:{SERIF};'
            f'font-size:44px;font-weight:500;line-height:1;text-transform:uppercase">{name}</h2>'
            f'<div style="margin-top:14px;font-size:12px;letter-spacing:2px;text-transform:uppercase;'
            f'line-height:1.7;font-weight:400">{sub}</div></div>'
            f'<div style="flex:2 1 400px;min-width:0">{body}{tg}{cta}</div></div></section>')


case_link = (f'<a href="zennith.html" style="display:inline-flex;align-items:center;gap:14px;color:inherit;'
             f'font-size:13px;letter-spacing:2.5px;text-transform:uppercase;text-decoration:none;'
             f'border-bottom:1px solid #F7F2EA;padding-bottom:6px;font-weight:400">Read the Zennith case study {ARROW}</a>')

work = f'''<section style="{SEC.format(24)}">{eyebrow('Selected')}{h1('Work')}<p style="margin:24px 0 0;max-width:560px;font-size:17px;line-height:1.65">Software built where law, health and everyday commerce meet, each project shaped by the regulation around it.</p></section>
{case('zennith', '#646B55', '#F7F2EA', 'Zennith', 'Clinic management<br>system',
      p('A clinic management system piloting at Hillbrow Community Health Centre, with role-based tools for doctors, nurses, pharmacists, receptionists and patients. I lead the team and build the backend.', 560),
      tags(['React', 'TypeScript', 'Firebase', 'SMS'], '#F7F2EA'), case_link)}
{case('legalizeit', '#333A2B', '#F7F2EA', 'LegalizeIT', 'Legal-tech progressive<br>web app',
      p('A legal-tech progressive web app that gives informal traders timestamped records of their trade.', 560),
      tags(['PWA', 'Legal tech', 'Records'], '#F7F2EA'))}
{case('ehs', '#DCD3C3', '#333A2B', 'EHS Legal<br>Analyst', 'AI skill for compliance<br>registers',
      p('An AI skill that reads environmental, health and safety legislation and drafts compliance register entries, tagging each provision by domain so compliance teams do not start from a blank page.', 560),
      tags(['AI', 'Compliance', 'Legislation'], '#333A2B'))}
{cta_row('Have a project in mind?')}'''

page("work.html", "Work — Chiedza Mutizwa",
     "Selected projects by Chiedza Mutizwa: Zennith, LegalizeIT and EHS Legal Analyst.",
     work, current="page")


# ------------------------------------------------------------- zennith.html
def facts(items):
    cells = ""
    for i, (a, b) in enumerate(items):
        bd = "border-right:1px solid rgba(244,238,230,0.25)" if i < len(items) - 1 else ""
        cells += (f'<div style="padding:8px 28px;{bd}"><div style="font-size:11px;letter-spacing:2px;'
                  f'text-transform:uppercase;font-weight:400">{a}</div><div style="margin-top:8px;'
                  f'font-family:{SERIF};font-size:24px;font-weight:500;line-height:1.15">{b}</div></div>')
    return (f'<div style="background:#636B53;color:#F4EEE6;display:grid;'
            f'grid-template-columns:repeat(auto-fit,minmax(200px,1fr));padding:26px 12px">{cells}</div>')


def block(title, body):
    return f'<div style="flex:1 1 320px;min-width:0">{h2(title)}{body}</div>'


def li(items):
    return ('<ul role="list" style="margin:0;padding:0;list-style:none;display:grid;gap:14px">' + "".join(
        f'<li style="display:flex;gap:14px;font-size:16px;line-height:1.6">'
        f'<span aria-hidden="true" style="color:{G};flex:none">✦</span><span>{t}</span></li>'
        for t in items) + "</ul>")


back = ('<a href="work.html" style="font-size:12px;letter-spacing:3px;text-transform:uppercase;'
        'text-decoration:none;color:#7E6033;font-weight:400"><span aria-hidden="true">←</span> All work</a>')

zen = f'''<section style="{SEC.format(24)}">{back}<div style="margin-top:28px">{eyebrow('Case study')}{h1('Zennith')}<div style="margin-top:22px;font-size:15px;letter-spacing:5px;text-transform:uppercase;color:#7E6033;font-weight:400">Clinic management system</div></div></section>
<section style="{SEC.format(48)}">{facts([('Role', 'Group leader &amp; backend developer'), ('Pilot site', 'Hillbrow Community Health Centre'), ('Stack', 'React · TypeScript · Firebase'), ('Compliance', 'POPIA')])}</section>
<section style="{SEC.format(72)}"><div style="display:flex;flex-wrap:wrap;gap:56px">
{block('The challenge', p('Public clinics struggle with three linked problems: medication stock-outs, long queues and paper records.') + p('Zennith tackles all three with role-based tools for doctors, nurses, pharmacists, receptionists and patients. It is built on React, TypeScript and Firebase, and is piloting at Hillbrow Community Health Centre.'))}
{block('My role', p('As group leader and backend developer, I designed the database and moved the app from mock data to live Firebase. I also built the nurse OCR (optical character recognition) feature and set up two-way SMS appointment reminders that patients can reply to.') + p('Behind the scenes, I plan our sprints, keep the project logs and open every pitch.'))}
</div></section>
<section style="{SEC.format(72)}"><div style="border-left:1px solid #C9B89A;padding-left:40px">{h2('Highlights')}{li([
    'A database schema with practitioner registration numbers and separate storage for login credentials',
    'Secure sign-in with two-factor authentication and role-based access',
    'SMS reminders where patients reply 1 or 2 to confirm, and reception is told straight away',
    'Sprint planning that covers POPIA (Protection of Personal Information Act) compliance and Zero Trust security',
])}{tags(['React', 'TypeScript', 'Firebase', 'OCR', 'SMS'])}</div></section>
{cta_row('Want to hear more about Zennith?')}'''

page("zennith.html", "Zennith — Chiedza Mutizwa",
     "Case study: Zennith, a clinic management system piloting at Hillbrow Community Health Centre. Chiedza Mutizwa leads the team and builds the backend.",
     zen, current="true")
print("built work.html and zennith.html")
