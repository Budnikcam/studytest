#!/usr/bin/env python3
"""Build horizontal 16:9 recruitment deck for Богатырское сердце."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "Bogatyrskoe-serdtse-nabor.pptx"

# Brand
BG = RGBColor(0x0A, 0x0A, 0x0A)
SURFACE = RGBColor(0x16, 0x16, 0x16)
GREEN = RGBColor(0xC8, 0xFF, 0x00)
YELLOW = RGBColor(0xF5, 0xC5, 0x18)
WHITE = RGBColor(0xF4, 0xF4, 0xF4)
MUTED = RGBColor(0x9A, 0x9A, 0x9A)
BLACK = RGBColor(0x00, 0x00, 0x00)

W = Inches(13.333)
H = Inches(7.5)


def set_run(run, size=18, bold=False, color=WHITE, name="Arial"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name


def add_bg(slide, color=BG):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)
    return shape


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


def add_text(slide, left, top, width, height, text, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color)
    return box


def add_para(tf, text, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, space_before=0, space_after=6):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color)
    return p


def footer(slide, left_text="ФФС Смоленской области", right_text=""):
    add_text(slide, Inches(0.5), Inches(7.05), Inches(6), Inches(0.3), left_text, size=11, color=MUTED)
    if right_text:
        add_text(slide, Inches(7), Inches(7.05), Inches(5.8), Inches(0.3), right_text, size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def brand_bar(slide, page_num):
    add_text(slide, Inches(0.5), Inches(0.28), Inches(8), Inches(0.35), "ФФС · СМОЛЕНСКАЯ ОБЛАСТЬ", size=12, bold=True, color=GREEN)
    add_text(slide, Inches(11.6), Inches(0.28), Inches(1.2), Inches(0.35), f"{page_num:02d}", size=14, bold=True, color=MUTED, align=PP_ALIGN.RIGHT)


def picture_cover(slide, path, left, top, width, height):
    if not Path(path).exists():
        add_rect(slide, left, top, width, height, SURFACE)
        return None
    return slide.shapes.add_picture(str(path), left, top, width=width, height=height)


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # ---------- 01 TITLE ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    picture_cover(s, ASSETS / "orig_p10_0.png", Inches(7.2), 0, Inches(6.2), H)
    add_rect(s, Inches(6.7), 0, Inches(0.9), H, BG)  # soft edge feel via overlap
    brand_bar(s, 1)
    add_text(s, Inches(0.5), Inches(1.3), Inches(6.5), Inches(0.35), "НАБОР В СЕКЦИЮ · СМОЛЕНСК", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.8), Inches(6.8), Inches(2.2), "СОБИРАЕМ\nСБОРНУЮ\nОБЛАСТИ", size=48, bold=True, color=WHITE)
    add_text(
        s,
        Inches(0.5),
        Inches(4.3),
        Inches(6.5),
        Inches(1.1),
        "Адаптивный фиджитал-спорт для ветеранов СВО,\nдемобилизованных по ранению.\nДисциплина — двоеборье «тактическая стрельба».",
        size=16,
        color=WHITE,
    )
    # pills
    for i, (label, fill, border) in enumerate(
        [
            ("Бесплатно", GREEN, None),
            ("2 раза в неделю", None, GREEN),
            ("ДС «Юбилейный»", None, YELLOW),
        ]
    ):
        left = Inches(0.5 + i * 2.05)
        if fill:
            shape = add_rect(s, left, Inches(5.7), Inches(1.9), Inches(0.45), fill)
            add_text(s, left, Inches(5.75), Inches(1.9), Inches(0.35), label, size=12, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        else:
            shape = add_rect(s, left, Inches(5.7), Inches(1.9), Inches(0.45), BG, line=border)
            add_text(s, left, Inches(5.75), Inches(1.9), Inches(0.35), label, size=12, bold=True, color=border, align=PP_ALIGN.CENTER)
    footer(s, right_text="+7 (4812) 374-000, доб. 292")

    # ---------- 02 WHAT / OFFER ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 2)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.35), "ЧТО МЫ ПРЕДЛАГАЕМ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.7), "Команда. Тренировки. Всероссийские старты.", size=32, bold=True, color=WHITE)

    cards = [
        (GREEN, "Регулярные тренировки", "2 раза в неделю по 1,5 часа в Фиджитал-центре Дворца спорта «Юбилейный»."),
        (YELLOW, "Новый вид спорта", "Компьютерный тактический шутер CS2 + тактический лазертаг в зале."),
        (GREEN, "Своя команда", "Тренируетесь вместе с ребятами, которые прошли СВО."),
        (YELLOW, "Выезды на старты", "Лучшие войдут в сборную Смоленской области на «Богатырское сердце»."),
    ]
    for i, (accent, title, body) in enumerate(cards):
        col = i % 2
        row = i // 2
        left = Inches(0.5 + col * 6.3)
        top = Inches(2.2 + row * 2.1)
        add_rect(s, left, top, Inches(6.0), Inches(1.85), SURFACE)
        add_rect(s, left, top, Inches(0.12), Inches(1.85), accent)
        add_text(s, left + Inches(0.35), top + Inches(0.3), Inches(5.4), Inches(0.45), title, size=20, bold=True, color=WHITE if accent == GREEN else YELLOW)
        add_text(s, left + Inches(0.35), top + Inches(0.85), Inches(5.4), Inches(0.8), body, size=15, color=MUTED)
    footer(s, right_text="Бесплатно · снаряжение выдаём")

    # ---------- 03 DISCIPLINE ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 3)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.35), "ДИСЦИПЛИНА", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.7), "Двоеборье «тактическая стрельба»", size=32, bold=True, color=WHITE)
    add_text(
        s,
        Inches(0.5),
        Inches(1.9),
        Inches(12),
        Inches(0.5),
        "Фиджитал — одна дисциплина из цифровой и физической частей. Команда выступает в обеих, считается общий результат.",
        size=16,
        color=MUTED,
    )

    # two panels
    add_rect(s, Inches(0.5), Inches(2.6), Inches(5.9), Inches(3.5), SURFACE)
    add_rect(s, Inches(0.5), Inches(2.6), Inches(5.9), Inches(0.55), GREEN)
    add_text(s, Inches(0.7), Inches(2.7), Inches(5.5), Inches(0.4), "ЧАСТЬ 1 · ЦИФРОВАЯ", size=14, bold=True, color=BLACK)
    add_text(s, Inches(0.7), Inches(3.4), Inches(5.5), Inches(0.45), "CS2", size=28, bold=True, color=WHITE)
    add_text(
        s,
        Inches(0.7),
        Inches(4.0),
        Inches(5.5),
        Inches(1.8),
        "Командный тактический шутер на компьютере.\nТочность, реакция, знание карт, чёткие команды\nпо связи и игра в связке с напарниками.",
        size=15,
        color=MUTED,
    )

    add_rect(s, Inches(6.9), Inches(2.6), Inches(5.9), Inches(3.5), SURFACE)
    add_rect(s, Inches(6.9), Inches(2.6), Inches(5.9), Inches(0.55), YELLOW)
    add_text(s, Inches(7.1), Inches(2.7), Inches(5.5), Inches(0.4), "ЧАСТЬ 2 · ФИЗИЧЕСКАЯ", size=14, bold=True, color=BLACK)
    add_text(s, Inches(7.1), Inches(3.4), Inches(5.5), Inches(0.45), "Тактический лазертаг", size=24, bold=True, color=YELLOW)
    add_text(
        s,
        Inches(7.1),
        Inches(4.0),
        Inches(5.5),
        Inches(1.8),
        "Бой в зале с укрытиями и лазерными автоматами.\nБез пуль и боли — попадание фиксирует датчик.\nДвижение, укрытия, работа группой.",
        size=15,
        color=MUTED,
    )
    footer(s, right_text="CS2 + лазертаг = общий результат")

    # ---------- 04 WHO ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 4)
    picture_cover(s, ASSETS / "orig_p10_0.png", Inches(7.4), Inches(1.1), Inches(5.4), Inches(5.5))
    add_text(s, Inches(0.5), Inches(0.85), Inches(6.5), Inches(0.35), "КОГО ИЩЕМ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.25), Inches(6.8), Inches(1.0), "Эта секция — для вас", size=32, bold=True, color=WHITE)

    who = [
        ("Ветеран СВО, демобилизованный по ранению", "Секция создаётся именно для вас."),
        ("Протез или ограничения — не помеха", "На всероссийских стартах значительная часть спортсменов выступает с протезами — в одних командах с остальными."),
        ("Никогда не играли в CS2? Не страшно", "Опыт не нужен. Научим с нуля: управление, стрельба, тактика, связь."),
        ("Нужна справка от врача и желание", "Допуск к занятиям. Остальное — за нами: ПК, снаряжение, зал."),
    ]
    for i, (t, b) in enumerate(who):
        top = Inches(2.4 + i * 1.05)
        add_rect(s, Inches(0.5), top, Inches(6.6), Inches(0.95), SURFACE)
        accent = GREEN if i % 2 == 0 else YELLOW
        add_rect(s, Inches(0.5), top, Inches(0.1), Inches(0.95), accent)
        add_text(s, Inches(0.8), top + Inches(0.12), Inches(6.1), Inches(0.35), t, size=14, bold=True, color=WHITE if i % 2 == 0 else YELLOW)
        add_text(s, Inches(0.8), top + Inches(0.48), Inches(6.1), Inches(0.4), b, size=12, color=MUTED)
    footer(s, right_text="Фото с соревнований проекта")

    # ---------- 05 TRAINING ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 5)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.35), "ТРЕНИРОВКА", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.6), "Как проходит занятие", size=32, bold=True, color=WHITE)
    add_text(s, Inches(0.5), Inches(1.85), Inches(12), Inches(0.4), "2 раза в неделю по 1,5 часа. Темп тренер подбирает индивидуально.", size=16, color=MUTED)

    steps = [
        ("10′", SURFACE, WHITE, "Разминка", "Суставы, координация, разогрев под ваши возможности."),
        ("35′", GREEN, BLACK, "Цифра · CS2", "Стрельба, реакция, тактика, тренировочные игры."),
        ("35′", YELLOW, BLACK, "Зал · лазертаг", "Укрытия, штурм и оборона, командные схемы."),
        ("10′", SURFACE, WHITE, "Разбор", "Что получилось, что правим, задачи на следующую."),
    ]
    for i, (time, fill, tcolor, title, body) in enumerate(steps):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(2.5), Inches(3.0), Inches(3.5), SURFACE)
        add_rect(s, left, Inches(2.5), Inches(3.0), Inches(0.9), fill)
        add_text(s, left, Inches(2.65), Inches(3.0), Inches(0.6), time, size=28, bold=True, color=tcolor, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(3.7), Inches(2.6), Inches(0.5), title, size=16, bold=True, color=WHITE)
        add_text(s, left + Inches(0.2), Inches(4.3), Inches(2.6), Inches(1.4), body, size=13, color=MUTED)
    footer(s, right_text="ул. Черняховского, 29 · ДС «Юбилейный»")

    # ---------- 06 PROJECT FACTS ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 6)
    picture_cover(s, ASSETS / "orig_p9_0.png", Inches(0.4), Inches(1.1), Inches(5.6), Inches(3.5))
    add_text(s, Inches(6.3), Inches(1.1), Inches(6.5), Inches(0.35), "КУДА ГОТОВИМ КОМАНДУ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(6.3), Inches(1.5), Inches(6.5), Inches(0.8), "«Богатырское сердце»", size=30, bold=True, color=WHITE)
    add_text(
        s,
        Inches(6.3),
        Inches(2.4),
        Inches(6.5),
        Inches(1.8),
        "Всероссийский проект адаптивного фиджитал-спорта среди ветеранов СВО.\n\nСоздан федерациями фиджитал-спорта Ленинградской и Московской областей. В 2027 году турниры планируют провести более чем в 10 регионах.",
        size=14,
        color=MUTED,
    )

    facts = [
        ("56", "ветеранов на этапе\nв Сосновом Бору, март 2026"),
        ("~80", "участников на этапе\nв Раменском, сентябрь 2026"),
        ("5", "дисциплин формата:\nдвоеборье и VR-виды"),
        ("10+", "регионов — план\nрасширения на 2027"),
    ]
    for i, (num, label) in enumerate(facts):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(4.85), Inches(3.0), Inches(1.7), SURFACE)
        color = GREEN if i % 2 == 0 else YELLOW
        add_text(s, left + Inches(0.2), Inches(5.0), Inches(2.6), Inches(0.55), num, size=28, bold=True, color=color)
        add_text(s, left + Inches(0.2), Inches(5.55), Inches(2.6), Inches(0.85), label, size=12, color=MUTED)
    footer(s, right_text="Источники: sport.lenobl.ru, Ассоциация ветеранов СВО, IVBG")

    # ---------- 07 PATH ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 7)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.35), "ПУТЬ В СБОРНУЮ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.7), "От первой тренировки — до всероссийских стартов", size=28, bold=True, color=WHITE)

    path_steps = [
        ("1", GREEN, "Записываетесь", "Пишете в VK / на почту / звоните.\nПриносите справку о допуске."),
        ("2", GREEN, "Тренируетесь", "Осваиваете CS2 и лазертаг,\nсрабатываетесь с командой."),
        ("3", GREEN, "Входите в сборную", "Из занимающихся формируем\nкоманду Смоленской области."),
        ("★", YELLOW, "Представляете регион", "На всероссийских соревнованиях\n«Богатырское сердце»."),
    ]
    for i, (n, accent, title, body) in enumerate(path_steps):
        left = Inches(0.5 + i * 3.15)
        add_rect(s, left, Inches(2.4), Inches(3.0), Inches(3.7), SURFACE)
        circle = s.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(1.05), Inches(2.7), Inches(0.9), Inches(0.9))
        circle.fill.solid()
        circle.fill.fore_color.rgb = accent
        circle.line.fill.background()
        add_text(s, left + Inches(1.05), Inches(2.85), Inches(0.9), Inches(0.6), n, size=22, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(3.9), Inches(2.6), Inches(0.5), title, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, left + Inches(0.2), Inches(4.5), Inches(2.6), Inches(1.2), body, size=13, color=MUTED, align=PP_ALIGN.CENTER)
    footer(s, right_text="Смоленщина на всероссийских стартах")

    # ---------- 08 FAQ + CTA ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 8)
    add_text(s, Inches(0.5), Inches(0.85), Inches(6), Inches(0.35), "ЗАПИСЬ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.2), Inches(6.5), Inches(0.6), "Хотите в команду?", size=30, bold=True, color=WHITE)

    add_rect(s, Inches(0.5), Inches(2.0), Inches(6.5), Inches(2.5), GREEN)
    add_text(s, Inches(0.75), Inches(2.2), Inches(6.0), Inches(0.4), "Напишите одним сообщением:", size=16, bold=True, color=BLACK)
    add_text(
        s,
        Inches(0.75),
        Inches(2.7),
        Inches(6.0),
        Inches(1.5),
        "1. Имя и телефон\n2. Ограничения по движению — если есть, коротко\n3. Удобнее: будни вечером или выходные",
        size=15,
        bold=True,
        color=BLACK,
    )

    add_rect(s, Inches(0.5), Inches(4.7), Inches(3.1), Inches(1.7), SURFACE)
    add_text(s, Inches(0.7), Inches(4.85), Inches(2.7), Inches(0.3), "КОНТАКТЫ", size=12, bold=True, color=YELLOW)
    add_text(
        s,
        Inches(0.7),
        Inches(5.2),
        Inches(2.7),
        Inches(1.1),
        "VK: vk.com/phygital67\nEmail: ffssmol@yandex.ru\n+7 (4812) 374-000, доб. 292",
        size=12,
        color=WHITE,
    )

    add_rect(s, Inches(3.8), Inches(4.7), Inches(3.2), Inches(1.7), SURFACE)
    add_text(s, Inches(4.0), Inches(4.85), Inches(2.8), Inches(0.3), "ГДЕ", size=12, bold=True, color=YELLOW)
    add_text(
        s,
        Inches(4.0),
        Inches(5.2),
        Inches(2.8),
        Inches(1.1),
        "Фиджитал-центр\nДС «Юбилейный»\nул. Черняховского, 29",
        size=12,
        color=WHITE,
    )

    # FAQ column
    add_text(s, Inches(7.4), Inches(1.2), Inches(5.4), Inches(0.4), "Частые вопросы", size=18, bold=True, color=WHITE)
    faqs = [
        ("Сколько стоит?", "Бесплатно. ПК, лазертаг и зал — за счёт центра."),
        ("Нет опыта в играх?", "Не нужен. Научим с нуля."),
        ("Протез / ограничения?", "Не помеха. Нагрузку подберём."),
        ("Что взять?", "Справку о допуске, форму, сменную обувь."),
        ("Когда?", "2×1,5 ч. Дни согласуем с группой."),
    ]
    for i, (q, a) in enumerate(faqs):
        top = Inches(1.75 + i * 0.9)
        add_text(s, Inches(7.4), top, Inches(5.4), Inches(0.3), q, size=13, bold=True, color=GREEN)
        add_text(s, Inches(7.4), top + Inches(0.3), Inches(5.4), Inches(0.4), a, size=12, color=MUTED)

    footer(s, right_text="Знаете ветерана? Перешлите эту презентацию.")

    # ---------- 09 SOURCES ----------
    s = prs.slides.add_slide(blank)
    add_bg(s)
    brand_bar(s, 9)
    add_text(s, Inches(0.5), Inches(0.85), Inches(12), Inches(0.35), "ИСТОЧНИКИ И РЕКВИЗИТЫ", size=14, bold=True, color=GREEN)
    add_text(s, Inches(0.5), Inches(1.25), Inches(12), Inches(0.6), "На чём основан материал", size=28, bold=True, color=WHITE)

    sources = [
        "Комитет по спорту Ленинградской области / sport.lenobl.ru — расширение «Богатырского сердца» на 10+ регионов в 2027 году",
        "Ассоциация ветеранов СВО — этапы в Сосновом Бору (март 2026, 56 участников, 8 команд) и Санкт-Петербурге (ноябрь 2026)",
        "Правительство Ленобласти / IVBG — этап в Раменском (сентябрь 2026, ~80 участников, 10 команд); CS2 + лазертаг",
        "РИА Новости (27.02.2026) — открытие фиджитал-центра в ДС «Юбилейный» (Смоленск)",
        "ВФФС / phygitalsport.ru — президент ФФС Смоленской области Шакуро М. А., ffssmol@yandex.ru",
        "Фиджитал-центр Смоленск — ул. Черняховского, 29; +7 (4812) 374-000, доб. 292; VK: phygital67",
    ]
    for i, line in enumerate(sources):
        top = Inches(2.1 + i * 0.7)
        add_rect(s, Inches(0.5), top, Inches(12.3), Inches(0.6), SURFACE)
        add_rect(s, Inches(0.5), top, Inches(0.1), Inches(0.6), GREEN if i % 2 == 0 else YELLOW)
        add_text(s, Inches(0.85), top + Inches(0.12), Inches(11.7), Inches(0.4), line, size=13, color=WHITE)

    footer(s, right_text="Спорт. Команда. Сила духа.")

    prs.save(OUT)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build()
