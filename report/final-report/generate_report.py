# -*- coding: utf-8 -*-
"""
generate_report.py
==================
Erzeugt den kompakten Abschlussbericht "TravelTide_Final_Report.pdf"
(max. 3 Seiten) fuer das TravelTide Customer-Analytics-Projekt.

Bibliothek: ReportLab (platypus)
Aufruf:     python generate_report.py
"""

import os

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)
from reportlab.pdfgen import canvas as rl_canvas

# ----------------------------------------------------------------------
# Pfade & Grunddaten
# ----------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(HERE, "TravelTide_Final_Report.pdf")

DARK = HexColor("#1b2a4a")    # Titelblau
ACCENT = HexColor("#2e6f95")  # Akzentblau
GREY = HexColor("#555555")
LIGHT = HexColor("#eef3f8")


# ----------------------------------------------------------------------
# Dokument-Klasse & Footer mit Seitenzahl "Seite X von 3"
# ----------------------------------------------------------------------
class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates([PageTemplate(id="all", frames=[frame])])


class NumberedCanvas(rl_canvas.Canvas):
    """Canvas, der die Gesamtseitenzahl kennt und den Footer korrekt zeichnet."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_pages = []

    def showPage(self):
        self._saved_pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_pages)
        print("Seitenanzahl im PDF:", total)
        for idx, state in enumerate(self._saved_pages, start=1):
            self.__dict__.update(state)
            self._draw_footer(idx, total)
            super().showPage()
        super().save()

    def _draw_footer(self, page_num, total):
        self.saveState()
        self.setStrokeColor(LIGHT)
        self.setLineWidth(0.8)
        self.line(1.8 * cm, 1.4 * cm, A4[0] - 1.8 * cm, 1.4 * cm)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(GREY)
        self.drawString(1.8 * cm, 1.0 * cm, "TravelTide - Final Report")
        self.drawRightString(
            A4[0] - 1.8 * cm,
            1.0 * cm,
            "Seite %d von %d" % (page_num, total),
        )
        self.restoreState()


# ----------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------
styles = getSampleStyleSheet()

S_TITLE = ParagraphStyle(
    "Title", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=21, leading=24, textColor=DARK, spaceAfter=2,
)
S_SUB = ParagraphStyle(
    "Sub", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=11, leading=13, textColor=ACCENT, spaceAfter=10,
)
S_H1 = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=13, leading=15, textColor=DARK, spaceBefore=6, spaceAfter=4,
)
S_H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=10.5, leading=12.5, textColor=ACCENT, spaceBefore=5, spaceAfter=2,
)
S_BODY = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.3, leading=12.2, textColor=HexColor("#222222"),
    alignment=TA_JUSTIFY, spaceAfter=3,
)
S_BULLET = ParagraphStyle(
    "Bullet", parent=S_BODY, leftIndent=11, bulletIndent=2,
    spaceAfter=2, alignment=TA_LEFT,
)
S_NOTE = ParagraphStyle(
    "Note", parent=S_BODY, fontSize=8.4, leading=10.6, textColor=GREY,
)


def bullets(items, style=S_BULLET):
    return [Paragraph(it, style, bulletText="\u2022") for it in items]


def flow():
    f = []

    # ==================================================================
    # SEITE 1
    # ==================================================================
    f.append(Paragraph("TravelTide &ndash; Final Report", S_TITLE))
    f.append(Paragraph("Customer Analytics &amp; Kundensegmentierung", S_SUB))

    f.append(Paragraph("Projekt&uuml;bersicht", S_H1))
    f.append(Paragraph(
        "TravelTide ist eine Online-Plattform f&uuml;r die Buchung von Fl&uuml;gen und Hotels. "
        "Ziel des Projekts war es, aus der transaktionalen Kundendatenbank verwertbare "
        "Erkenntnisse zu gewinnen und die aktive Kundschaft in aussagekr&auml;ftige Segmente "
        "zu unterteilen. Dazu wurden die Daten aus f&uuml;nf relationalen Quellen extrahiert, "
        "bereinigt, zu benutzerbezogenen Kennzahlen aggregiert und anschlie&szlig;end explorativ "
        "sowie mittels Clustering analysiert. Das Ergebnis ist ein Master-Datensatz auf "
        "<b>user_id</b>-Ebene, eine regelbasierte Segmentierung (8 Gruppen) und ein "
        "K-Means-Clustering der gr&ouml;&szlig;ten Kundengruppe (3 Sub-Cluster).",
        S_BODY,
    ))

    f.append(Paragraph("Zielsetzung des Projekts", S_H1))
    f.extend(bullets([
        "Aktive Nutzer:innen identifizieren und die relevanten Rohdaten "
        "(<i>users, sessions, flights, hotels</i>) bereitstellen.",
        "Datenqualit&auml;t sicherstellen (Cleaning, fehlende Werte, Datentypen, Storno-/Rabattlogik).",
        "Verhaltens- und Umsatzkennzahlen je Kunde aufbauen (Feature Engineering).",
        "Kunden in homogene, marketingrelevante Segmente einteilen.",
        "Konkrete Handlungsempfehlungen f&uuml;r Marketing und Produktstrategie ableiten.",
    ]))

    f.append(Paragraph("Datenfluss durch die Notebooks 01&ndash;05", S_H1))
    f.extend(bullets([
        "<b>01 &ndash; Data Filtering:</b> Extraktion der aktiven User aus der Neon-PostgreSQL-Datenbank.",
        "<b>02 &ndash; EDA:</b> Explorative Analyse der Rohdaten (users, sessions, flights, hotels).",
        "<b>03 &ndash; Features:</b> Cleaning &amp; Feature Engineering &rarr; Master-Dataframe (user_id-Ebene).",
        "<b>04 &ndash; Group Build:</b> Regelbasierte Gruppenbildung / Kundensegmentierung.",
        "<b>05 &ndash; Clustering:</b> K-Means-Clustering der Gruppe &bdquo;Standard Kunde&ldquo; &rarr; Sub-Cluster.",
    ]))
    f.append(Spacer(1, 6))
    f.append(Paragraph(
        "Grafik: <i>report/cluster_dashboard.png</i> fasst die wichtigsten Segment-Kennzahlen zusammen.",
        S_NOTE,
    ))

    f.append(PageBreak())

    # ==================================================================
    # SEITE 2
    # ==================================================================
    f.append(Paragraph("Die Notebooks im &Uuml;berblick", S_H1))

    f.append(Paragraph("01 &ndash; Datenfilterung (<i>01_traveltide_data_filtering</i>)", S_H2))
    f.append(Paragraph(
        "Verbindung zur Neon-PostgreSQL-Datenbank. Definition &bdquo;aktiver User&ldquo;: "
        "<b>session_start &ge; 05.01.2023</b> und <b>&gt; 7 Sessions</b>. Die vier Tabellen "
        "(users, sessions, flights, hotels) werden auf diesen Kundenkreis gefiltert und als CSV "
        "gespeichert. Ergebnis: die Analysebasis der aktiven Kundschaft.", S_BODY,
    ))

    f.append(Paragraph("02 &ndash; Explorative Datenanalyse (<i>02_EDA</i>)", S_H2))
    f.append(Paragraph(
        "Kennzahlen- und Visualisierungs-Dashboards zu allen vier Tabellen: Nutzer (Altersverteilung "
        "mit Schwerpunkt ca. 40&ndash;50 Jahre), Sessions (Buchungs-/Storno-Verhalten, Rabatte, "
        "Session-Dauer), Fl&uuml;ge (Preis pro Sitzplatz, Airlines, Saisonalit&auml;t) und Hotels "
        "(Ketten, St&auml;dte, Preisniveau). Liefert die inhaltliche Grundlage f&uuml;r die weitere "
        "Analyse.", S_BODY,
    ))

    f.append(Paragraph("03 &ndash; Feature Engineering (<i>03_features</i>)", S_H2))
    f.append(Paragraph(
        "Bereinigung und Zusammenf&uuml;hrung der Tabellen (Left Joins &uuml;ber <i>trip_id</i>), "
        "Kostenberechnung f&uuml;r Fl&uuml;ge/Hotels unter Ber&uuml;cksichtigung von Rabatten und "
        "Stornierungen sowie Aggregation auf <i>user_id</i>-Ebene (Sessions, Trips, Ausgaben, "
        "Rabattnutzung, Stornoquote, Gep&auml;ck, Hoteln&auml;chte, Demografie). Ergebnis: "
        "<b>master_features.csv</b> mit <b>5.782 Kunden</b>. Auff&auml;llige Korrelationen: "
        "Hoteln&auml;chte&harr;Hotelkosten 0,53; Gep&auml;ck&harr;Flugkosten 0,33; "
        "Stornorate&harr;Flugkosten 0,27.", S_BODY,
    ))

    f.append(Paragraph("04 &ndash; Gruppenbildung (<i>04_group_build</i>)", S_H2))
    f.append(Paragraph(
        "Regelbasierte Segmentierung &uuml;ber Schwellenwerte (Top-10&thinsp;%-Spender, "
        "&uuml;berdurchschnittliche Hotel-/Flugkosten, Top-25&thinsp;% Trips bzw. Buchungsratio, "
        "Alter &lt; 20 / &gt; 60). Ergebnis: <b>8 Segmente</b>; gr&ouml;&szlig;te Gruppe "
        "&bdquo;<b>Standard Kunde</b>&ldquo; mit <b>2.070 Kunden (35,8&thinsp;%)</b>.", S_BODY,
    ))

    f.append(Paragraph("05 &ndash; Clustering (<i>05_clustering</i>)", S_H2))
    f.append(Paragraph(
        "Filterung der Gruppe &bdquo;Standard Kunde&ldquo;, Standardisierung der Features "
        "(StandardScaler) und K-Means-Clustering. Die optimale Clusterzahl wird &uuml;ber "
        "Elbow-Methode und Silhouette-Score bestimmt: <b>k = 3</b>. Ergebnis: drei neue, "
        "klar getrennte Sub-Cluster.", S_BODY,
    ))

    f.append(Paragraph("Verwendete Methoden", S_H1))
    f.extend(bullets([
        "<b>Data Cleaning:</b> Typkonvertierung, Umgang mit fehlenden Werten, Bereinigung der "
        "Storno-/Rabattlogik und Boolean-Felder.",
        "<b>EDA:</b> Deskriptive Statistik, Histogramme, Boxplots, Balken- und Streudiagramme, "
        "Korrelations-Heatmaps.",
        "<b>Feature Engineering:</b> Zusammenf&uuml;hrung &uuml;ber <i>trip_id</i>, Kosten- und "
        "Kennzahlen-Aggregation auf <i>user_id</i>-Ebene.",
        "<b>Clustering:</b> StandardScaler + K-Means, Bestimmung von <i>k</i> via Elbow-Methode "
        "und Silhouette-Score (k = 3).",
    ]))

    f.append(PageBreak())

    # ==================================================================
    # SEITE 3
    # ==================================================================
    f.append(Paragraph("Hauptergebnisse &amp; Erkenntnisse aus dem Clustering", S_H1))
    f.append(Paragraph(
        "K-Means (k = 3) auf der Gruppe &bdquo;Standard Kunde&ldquo; (2.070 Kunden) "
        "identifiziert drei unterscheidbare Verhaltensmuster:", S_BODY,
    ))
    f.extend(bullets([
        "<b>Cluster 0 &ndash; Treue Wertk&auml;ufer:</b> &Oslash; 43,7 Jahre, h&ouml;chste Ausgaben "
        "($1.545,21) und Conversion (41&thinsp;%), 3,39 Reisen, <b>0&thinsp;% Storno</b>, wenig Rabatte "
        "&ndash; stabilstes und profitabelstes Segment.",
        "<b>Cluster 1 &ndash; Low-Engagement Surfer:</b> &Oslash; 35,6 Jahre, geringster Umsatz "
        "($471,62), nur 1,69 Reisen und 21&thinsp;% Conversion &ndash; viel Browsing, hohe "
        "Kaufh&uuml;rde.",
        "<b>Cluster 2 &ndash; Deal-Seeker &amp; Storno-Risiko:</b> &Oslash; 37,8 Jahre, hoher Umsatz "
        "($1.438,21), 3,10 Reisen, intensive Rabattnutzung (2,36/2,00) und <b>12&thinsp;% Stornorate</b> "
        "&ndash; das einzige Cluster mit nennenswerten Stornierungen.",
    ]))
    f.append(Paragraph(
        "<b>Kernaussage:</b> Auch innerhalb der homogen wirkenden Gruppe existieren klar trennbare "
        "Muster &ndash; von loyalen Wertkunden &uuml;ber preisgetriebene Schn&auml;ppchenj&auml;ger bis "
        "zu stornoaffinen, rabattfokussierten Kunden. Das erm&ouml;glicht eine zielgenaue Ansprache.",
        S_BODY,
    ))

    f.append(Paragraph("Wichtigste Visualisierungen (Ordner <i>report</i>)", S_H1))
    f.append(Paragraph(
        "<b>EDA &amp; Feature-Analyse:</b> Altersverteilung_der_Kunden.png, Korrelations_Heatmap.png, "
        "Verteilung_der_Flugkosten.png, Verteilung_der_Hotelausgaben.png, "
        "Flugkosten_vs_Hotelkosten.png", S_NOTE,
    ))
    f.append(Paragraph(
        "<b>Segmentierung:</b> Verteilung_der_Kundensegmente.png, "
        "Venn-Diagramm_&uuml;berdurchschnittliche_Spender.png, "
        "Kunden-Segmentierung_nach_&uuml;berdurchschnittlichen_Ausgaben.png", S_NOTE,
    ))
    f.append(Paragraph(
        "<b>Clustering:</b> elbow_silhouette_plot.png (k-Wahl), cluster_dashboard.png, "
        "cluster_metrics_heatmap.png, cluster_radar_chart.png, Sub-Cluster_Vergleich_dashboard.png",
        S_NOTE,
    ))
    f.append(Paragraph(
        "<b>Dashboards:</b> users_dashboard.png, sessions_dashboard.png, Flights_Daschboard_1&ndash;3.png, "
        "Hotels_Analysis_Dashboard.png, Hotels_Cleaning_Dashboard.png", S_NOTE,
    ))

    f.append(Paragraph("Fazit &amp; m&ouml;gliche n&auml;chste Schritte", S_H1))
    f.append(Paragraph(
        "<b>Fazit:</b> Die Kombination aus regelbasierter Segmentierung und un&uuml;berwachtem "
        "K-Means-Clustering liefert ein belastbares, unmittelbar nutzbares Kundenbild: eine kleine, "
        "hochwertige Wertkundschaft, eine gro&szlig;e, preissensible Mittelschicht und eine "
        "rabatt-/stornokritische Gruppe. Damit lassen sich Marketingbudget und Retention-Ma&szlig;nahmen "
        "gezielt steuern.", S_BODY,
    ))
    f.extend(bullets([
        "Segmentierte Kampagnen umsetzen (VIP-Loyalty f&uuml;r Cluster 0, Aktivierung f&uuml;r "
        "Cluster 1, Non-Refundable-/Rabatt-Steuerung f&uuml;r Cluster 2).",
        "Cross-Selling ausbauen (Hotel zu Flug bzw. Flug zu Hotel) und Ancillaries wie Gep&auml;ck "
        "und N&auml;chte-Upselling f&ouml;rdern.",
        "KPIs der Segmente laufend monitoren (Conversion, Stornorate, CLV) und Segmente an neuen "
        "Daten validieren (z.&nbsp;B. per A/B-Test).",
        "Technisch: die DB-Verbindung aus Umgebungsvariablen laden statt im Notebook zu hinterlegen.",
    ]))

    return f


# ----------------------------------------------------------------------
# PDF erzeugen
# ----------------------------------------------------------------------
def build():
    doc = ReportDoc(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.8 * cm,
        title="TravelTide - Final Report",
        author="TravelTide Analytics",
    )
    doc.build(flow(), canvasmaker=NumberedCanvas)
    print("PDF erstellt:", OUTPUT_PDF)
    return OUTPUT_PDF


if __name__ == "__main__":
    build()

