# «Куда текут деньги» as a page of its own (owner, 23.10.2026: «это корневой элемент.. можешь его сделать
# отдельной страницей»). Built from the published ai_capital/index.html: the same styles, data and scripts;
# the flow scheme on top, every other section kept in the markup but hidden, so the page scripts that fill
# them still find their containers. Output: ai_flows/index.html.
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
s = (HERE / "ai_capital" / "index.html").read_text(encoding="utf-8")


def cut(marker):
    i = s.find(marker)
    if i < 0 or s.count(marker) != 1:
        raise SystemExit(f"marker not unique: {marker!r}")
    return i


body = cut("<body>")
wrap = cut('<div class="wrap">\n') + len('<div class="wrap">\n')
flow_a = cut("<h2>Куда текут деньги</h2>")
flow_b = cut("<h2>Что из этого следует</h2>")
foot = cut('<p class="foot">')

head = re.sub(r"<title>.*?</title>", "<title>Куда текут деньги ИИ</title>", s[:body], count=1, flags=re.S)
flow = s[flow_a + len("<h2>Куда текут деньги</h2>"):flow_b]
old_note = "оценка DCF — в подсказке при наведении, на графике «Что об этом думают наши модели» и в таблице внизу"
if flow.count(old_note) != 1:
    raise SystemExit("flow note changed")
flow = flow.replace(old_note, "оценка DCF — в подсказке при наведении")
top = ('<h1>Куда текут деньги ИИ</h1>\n'
       '<p class="lead">Кто даёт деньги эпохи ИИ, кто их получает и на что они уходят — до наших публичных компаний. '
       'Схема из страницы <a href="../ai_capital/">«Деньги ИИ и наши компании»</a>, там же разбор, графики и оценки DCF.</p>\n')
page = (head + "<body>\n<div class=\"wrap\">\n" + top + flow
        + '<div hidden aria-hidden="true">\n' + s[wrap:flow_a] + s[flow_b:foot] + "</div>\n"
        + s[foot:])
out = HERE / "ai_flows" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print("written", out, len(page))
