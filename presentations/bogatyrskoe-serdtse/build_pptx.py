#!/usr/bin/env python3
"""Build ready-to-send 16:9 agitation deck for SVO veterans."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "Bogatyrskoe-serdtse-nabor.pptx"

BG = RGBColor(0x0A, 0x0A, 0x0A)
SURFACE = RGBColor(0x15, 0x15, 0x15)
GREEN = RGBColor(0xC8, 0xFF, 0x00)
YELLOW = RGBColor(0xF5, 0xC5, 0x18)
WHITE = RGBColor(0xF5, 0xF5, 0xF5)
MUTED = RGBColor(0x9A, 0x9A, 0x9A)
DARK = RGBColor(0x2A, 0x2A, 0x2A)
BLACK = RGBColor(0x00, 0x00, 0x00)

W = Inches(13.333)
H = Inches(7.5)


def set_run(run, size=18, bold=False, color=WHITE):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Arial"


def add_bg(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = BG
    shape.line.fill.background()
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def add_rect(slide, left, top, width, height, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1.5)
    return shape


def add_text(slide, left, top, width, height, text, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color)
    return box


def footer(slide, right=""):
    add_text(slide, Inches(0.5), Inches(7.05), Inches(7), Inches(0.3), "ФФС Смоленской области", size=11, color=MUTED)
    if right:
        add_text(slide, Inches(7.2), Inches(7.05), Inches(5.6), Inches(0.3), right, size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def brand(slide, num):
    add_text(slide, Inches(0.5), Inches(0.28), Inches(8), Inches(0.3), "ФФС · СМОЛЕНСКАЯ ОБЛАСТЬ", size=12, bold=True, color=GREEN)
    add_text(slide, Inches(11.7), Inches(0.28), Inches(1.1), Inches(0.3), f"{num:02d}", size=14, bold=True, color=MUTED, align=PP_ALIGN.RIGHT)


def pic(slide, name, left, top, width, height):
    path = ASSETS / name
    if path.exists():
        return slide.shapes.add_picture(str(path), left, top, width=width, height=height)
    add_rect(slide, left, top, width, height, SURFACE)
    return None


def card(slide, left, top, width, height, title, body, accent=GREEN):
    add_rect(slide, left, top, width, height, SURFACE)
    add_rect(slide, left, top, Inches(0.1), height, accent)
    add_text(slide, left + Inches(0.28), top + Inches(0.2), width - Inches(0.4), Inches(0.4), title, size=16, bold=True, color=WHITE if accent == GREEN else YELLOW)
    add_text(slide, left + Inches(0.28), top + Inches(0.65), width - Inches(0.4), height - Inches(0.8), body, size=13, color=MUTED)


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # 01
    s = prs.slides.add_slide(blank)
    add_bg(s)
    pic(s, "orig_p10_0.png", Inches(6.9), 0, Inches(6.5), H)
    add_rect(s, Inches(6.4), 0, Inches(1.0), H, BG)
    brand(s, 1)
    add_rect(s, Inches(0.5), Inches(1.15), Inches(2.4), Inches(0.4), GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(2.4), Inches(0.3), "ДЛЯ ВЕТЕРАНОВ СВО", size=12, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    add_text(s, Inches(0.5), Inches(1.75), Inches(6.2), Inches(2.3), "Собираем\nсборную\nСмоленщины", size=44, bold=True, color=WHITE)
    # tint "сборную" approximation via second line color not easy; keep white
    add_text(
        s,
        Inches(0.5),
        Inches(4.3),
        Inches(6.0),
        Inches(1.2),
        "Бесплатная секция адаптивного фиджитал-спорта для бойцов, демобилизованных по ранению. Команда своих. Всероссийские старты «Богатырское сердце».",
        size=15,
        color=WHITE,
    )
    add_rect(s, Inches(0.5), Inches(5.75), Inches(1.7), Inches(0.42), GREEN)
    add_text(s, Inches(0.5), Inches(5.8), Inches(1.7), Inches(0.3), "Бесплатно", size=12, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    add_rect(s, Inches(2.35), Inches(5.75), Inches(1.9), Inches(0.42), BG, line=GREEN)
    add_text(s, Inches(2.35), Inches(5.8), Inches(1.9), Inches(0.3), "2× в неделю", size=12, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_rect(s, Inches(4.4), Inches(5.75), Inches(2.1), Inches(0.42), BG, line=YELLOW)
    add_text(s, Inches(4.4), Inches(5.8), Inches(2.1), Inches(0.3), "ДС «Юбилейный»", size=12, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
    footer(s, "Запись: +7 (4812) 374-000, доб. 292")

    # 02
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand(s, 2)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.3), "ЗАЧЕМ ЭТО ВАМ", size=13, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.9), "Не «занятие для галочки».\nСнова команда и цель.", size=32, bold=True, color=WHITE)
    items = [
        (GREEN, "Свои рядом", "Тренируетесь с ребятами, которые прошли СВО. Общая задача, общий результат."),
        (YELLOW, "Нагрузка под вас", "Протез, ограничения — не стоп. Тренер подбирает темп под каждого."),
        (GREEN, "Голова в тонусе", "Реакция, концентрация, быстрые решения — в цифре и в зале."),
        (YELLOW, "Азарт старта", "Снова выйти на соревнования и проверить себя в новом формате."),
        (GREEN, "Сборная области", "Лучшие представляют Смоленщину на «Богатырском сердце»."),
        (YELLOW, "Всё за наш счёт", "ПК, лазертаг и зал — за счёт центра. Вам — справка и желание."),
    ]
    for i, (accent, title, body) in enumerate(items):
        col, row = i % 3, i // 3
        card(s, Inches(0.5 + col * 4.2), Inches(2.4 + row * 2.1), Inches(4.0), Inches(1.9), title, body, accent)
    footer(s, "Опыт в CS2 не нужен — научим с нуля")

    # 03
    s = prs.slides.add_slide(blank)
    add_bg(s)
    pic(s, "lasertag_action.png", Inches(7.6), 0, Inches(5.8), H)
    add_rect(s, Inches(7.1), 0, Inches(1.0), H, BG)
    brand(s, 3)
    add_text(s, Inches(0.5), Inches(0.85), Inches(7), Inches(0.3), "ДИСЦИПЛИНА", size=13, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(7), Inches(1.2), "CS2 + лазертаг\n= общий результат", size=34, bold=True, color=WHITE)
    add_text(
        s,
        Inches(0.5),
        Inches(2.55),
        Inches(6.8),
        Inches(0.7),
        "Фиджитал — одна дисциплина из цифровой и физической частей. Команда выступает в обеих.",
        size=15,
        color=MUTED,
    )
    add_rect(s, Inches(0.5), Inches(3.4), Inches(6.6), Inches(1.45), SURFACE)
    add_rect(s, Inches(0.5), Inches(3.4), Inches(6.6), Inches(0.4), GREEN)
    add_text(s, Inches(0.7), Inches(3.45), Inches(6), Inches(0.3), "ЧАСТЬ 1 · ЦИФРА — Counter-Strike 2", size=13, bold=True, color=BLACK)
    add_text(s, Inches(0.7), Inches(4.0), Inches(6.1), Inches(0.6), "Тактический шутер: точность, связь, игра в связке.", size=15, color=MUTED)
    add_rect(s, Inches(0.5), Inches(5.05), Inches(6.6), Inches(1.45), SURFACE)
    add_rect(s, Inches(0.5), Inches(5.05), Inches(6.6), Inches(0.4), YELLOW)
    add_text(s, Inches(0.7), Inches(5.1), Inches(6), Inches(0.3), "ЧАСТЬ 2 · ЗАЛ — Тактический лазертаг", size=13, bold=True, color=BLACK)
    add_text(s, Inches(0.7), Inches(5.65), Inches(6.1), Inches(0.6), "Реальный бой без боли: укрытия, датчики, работа группой.", size=15, color=MUTED)
    footer(s, "Двоеборье «тактическая стрельба»")

    # 04
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand(s, 4)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.3), "ТРЕНИРОВКА", size=13, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(1.0), "1,5 часа. Два раза в неделю.\nВсё снаряжение на месте.", size=32, bold=True, color=WHITE)
    add_text(s, Inches(0.5), Inches(2.3), Inches(12), Inches(0.4), "Фиджитал-центр ДС «Юбилейный» · ул. Черняховского, 29, Смоленск", size=15, color=MUTED)
    steps = [
        ("10′", DARK, WHITE, "Разминка", "Суставы, координация, разогрев под ваши возможности."),
        ("35′", GREEN, BLACK, "CS2", "Стрельба, реакция, тактика, тренировочные игры."),
        ("35′", YELLOW, BLACK, "Лазертаг", "Укрытия, штурм и оборона, командные схемы."),
        ("10′", DARK, WHITE, "Разбор", "Что сработало, что правим, задачи на следующую."),
    ]
    for i, (t, fill, tc, title, body) in enumerate(steps):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(2.95), Inches(3.0), Inches(3.4), SURFACE)
        add_rect(s, left, Inches(2.95), Inches(3.0), Inches(0.85), fill)
        add_text(s, left, Inches(3.1), Inches(3.0), Inches(0.55), t, size=26, bold=True, color=tc, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(4.1), Inches(2.6), Inches(0.45), title, size=17, bold=True, color=WHITE)
        add_text(s, left + Inches(0.2), Inches(4.65), Inches(2.6), Inches(1.3), body, size=13, color=MUTED)
    footer(s, "Дни и время согласуем с набранной группой")

    # 05
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand(s, 5)
    pic(s, "orig_p9_0.png", Inches(0.45), Inches(1.05), Inches(5.9), Inches(3.2))
    add_text(s, Inches(6.7), Inches(1.05), Inches(6), Inches(0.3), "КУДА ВЕДЁМ КОМАНДУ", size=13, bold=True, color=GREEN)
    add_text(s, Inches(6.7), Inches(1.4), Inches(6), Inches(1.1), "«Богатырское\nсердце»", size=34, bold=True, color=WHITE)
    add_text(
        s,
        Inches(6.7),
        Inches(2.7),
        Inches(6),
        Inches(1.4),
        "Всероссийский проект адаптивного фиджитал-спорта среди ветеранов СВО. Фиджитал рассматривают как инструмент реабилитации через спорт.",
        size=14,
        color=MUTED,
    )
    facts = [
        ("56", GREEN, "ветеранов СВО — Сосновый Бор, март 2026"),
        ("~80", YELLOW, "участников — Раменское, сентябрь 2026"),
        ("10+", GREEN, "регионов — план турниров на 2027"),
        ("CS2", YELLOW, "+ лазертаг — дисциплина секции"),
    ]
    for i, (n, c, label) in enumerate(facts):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(4.55), Inches(3.0), Inches(1.85), SURFACE)
        add_text(s, left + Inches(0.2), Inches(4.7), Inches(2.6), Inches(0.55), n, size=30, bold=True, color=c)
        add_text(s, left + Inches(0.2), Inches(5.4), Inches(2.6), Inches(0.8), label, size=12, color=MUTED)
    footer(s, "sport.lenobl.ru · Ассоциация ветеранов СВО · IVBG")

    # 06
    s = prs.slides.add_slide(blank)
    add_bg(s)
    pic(s, "laser_wide.png", 0, 0, W, H)
    add_rect(s, 0, 0, W, H, RGBColor(0x0A, 0x0A, 0x0A))  # will be opaque - need semi. Skip photo overlay complexity: solid dark + quote
    # Re-cover with dark for readability (pptx has no easy opacity). Use left solid panel.
    add_rect(s, 0, 0, Inches(8.2), H, BG)
    brand(s, 6)
    add_text(s, Inches(0.5), Inches(0.85), Inches(7), Inches(0.3), "ПРИНЦИП ПРОЕКТА", size=13, bold=True, color=GREEN)
    add_text(
        s,
        Inches(0.5),
        Inches(1.8),
        Inches(7.2),
        Inches(2.4),
        "«Главное — не то, какие физические возможности есть у человека сегодня. Главное — что он способен сделать дальше.»",
        size=26,
        bold=True,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.5),
        Inches(4.5),
        Inches(7.2),
        Inches(0.8),
        "Спортсмены с протезами и без выступают в одних командах и борются за общий результат.",
        size=16,
        color=WHITE,
    )
    add_text(
        s,
        Inches(0.5),
        Inches(5.5),
        Inches(7.2),
        Inches(0.9),
        "«Богатырское сердце» — возможность показать себя в соревновательной форме. Фиджитал уже рассматривают как реабилитацию.",
        size=14,
        color=YELLOW,
    )
    # right photo peek
    pic(s, "orig_p10_0.png", Inches(8.3), Inches(1.2), Inches(4.6), Inches(5.2))
    footer(s, "Александр Малов, Ассоциация ветеранов СВО Ленобласти")

    # 07
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand(s, 7)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.3), "ПУТЬ В СБОРНУЮ", size=13, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(1.0), "Четыре шага.\nОт сообщения — до старта.", size=32, bold=True, color=WHITE)
    path = [
        ("1", GREEN, "Пишете нам", "VK, почта или звонок. Имя, телефон, удобные дни. Приносите справку о допуске."),
        ("2", GREEN, "Тренируетесь", "Осваиваете CS2 и лазертаг. Срабатываетесь с командой. Темп — под вас."),
        ("3", GREEN, "Входите в сборную", "Из занимающихся формируем команду Смоленской области."),
        ("★", YELLOW, "Представляете регион", "Всероссийские соревнования «Богатырское сердце»."),
    ]
    for i, (n, accent, title, body) in enumerate(path):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(2.55), Inches(3.0), Inches(3.7), SURFACE)
        oval = s.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(1.05), Inches(2.85), Inches(0.9), Inches(0.9))
        oval.fill.solid()
        oval.fill.fore_color.rgb = accent
        oval.line.fill.background()
        add_text(s, left + Inches(1.05), Inches(3.0), Inches(0.9), Inches(0.55), n, size=20, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(4.05), Inches(2.6), Inches(0.5), title, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(4.65), Inches(2.6), Inches(1.3), body, size=13, color=MUTED, align=PP_ALIGN.CENTER)
    footer(s, "Смоленщина на всероссийских стартах")

    # 08
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand(s, 8)
    add_text(s, Inches(0.5), Inches(0.85), Inches(7), Inches(0.3), "ЗАПИСЬ ОТКРЫТА", size=13, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(7), Inches(1.0), "Готовы встать\nв команду?", size=34, bold=True, color=WHITE)
    add_rect(s, Inches(0.5), Inches(2.4), Inches(6.7), Inches(2.15), GREEN)
    add_text(s, Inches(0.75), Inches(2.55), Inches(6.2), Inches(0.35), "Напишите одним сообщением:", size=15, bold=True, color=BLACK)
    add_text(
        s,
        Inches(0.75),
        Inches(3.0),
        Inches(6.2),
        Inches(1.3),
        "1. Имя и телефон\n2. Ограничения по движению — если есть, коротко\n3. Удобнее: будни вечером или выходные",
        size=15,
        bold=True,
        color=BLACK,
    )
    card(s, Inches(0.5), Inches(4.75), Inches(3.25), Inches(1.7), "Связь", "VK: vk.com/phygital67\nEmail: ffssmol@yandex.ru\n+7 (4812) 374-000, доб. 292", YELLOW)
    card(s, Inches(3.95), Inches(4.75), Inches(3.25), Inches(1.7), "Адрес", "Фиджитал-центр\nДС «Юбилейный»\nул. Черняховского, 29", GREEN)

    add_text(s, Inches(7.6), Inches(1.2), Inches(5.2), Inches(0.4), "Сразу по делу", size=20, bold=True, color=WHITE)
    faqs = [
        ("Сколько стоит?", "Бесплатно. ПК, лазертаг и зал — за счёт центра."),
        ("Не играл в игры?", "Опыт не нужен. Научим с нуля."),
        ("Протез / ограничения?", "Не помеха. Нагрузку подберём."),
        ("Что взять?", "Справку о допуске, форму, сменную обувь."),
        ("Когда?", "2×1,5 ч. Расписание — после набора группы."),
    ]
    for i, (q, a) in enumerate(faqs):
        top = Inches(1.75 + i * 0.75)
        add_text(s, Inches(7.6), top, Inches(5.2), Inches(0.28), q, size=13, bold=True, color=GREEN)
        add_text(s, Inches(7.6), top + Inches(0.28), Inches(5.2), Inches(0.35), a, size=12, color=MUTED)
    add_text(
        s,
        Inches(7.6),
        Inches(5.7),
        Inches(5.2),
        Inches(0.8),
        "Знаете ветерана СВО, которому это нужно? Перешлите ему эту презентацию.",
        size=13,
        bold=True,
        color=YELLOW,
    )
    footer(s, "Спорт. Команда. Сила духа.")

    prs.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
