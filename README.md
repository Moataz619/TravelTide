# ✈️ TravelTide – Customer Analytics & Segmentation 🧳

> **Von Rohdaten zu handlungsorientierten Kundensegmenten** – eine vollständige
> Data-Analytics-Pipeline zur Aufbereitung, explorativen Analyse, regelbasierten
> Segmentierung und zum Machine-Learning-Clustering der TravelTide-Kundschaft.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white">
</p>

---

## 📖 Kurzbeschreibung

TravelTide ist eine (fiktive) Online-Reiseplattform für Flüge und Hotels. Dieses Projekt
wertet die Buchungsdaten ihrer **aktiven Nutzer:innen** end-to-end aus: von der Filterung
der Rohdaten aus einer PostgreSQL-Datenbank über die explorative Analyse bis hin zu einem
Feature-Master-Dataset. Anschließend wird die Kundschaft **regelbasiert segmentiert** und die
größte, unscharfe Gruppe („Standard Kunde“) mit **K-Means-Clustering** tiefer analysiert.
Das Ergebnis sind datengestützte **Marketing- und Business-Handlungsempfehlungen** pro Segment.

---

## 🗂️ Projektstruktur

```text
TravelTide/
├── data/
│   ├── raw/                    # In NB01 aus der Neon-PostgreSQL-DB gefilterte Rohdaten
│   │   ├── users.csv
│   │   ├── sessions.csv
│   │   ├── flights.csv
│   │   └── hotels.csv
│   ├── preprocessed/           # Bereinigte Daten + Feature-Master (NB02–NB04)
│   │   ├── users_cleaned.csv
│   │   ├── sessions_cleaned.csv
│   │   ├── flights_cleaned.csv
│   │   ├── hotels_cleaned.csv
│   │   ├── master_features.csv     # Feature-Master (eine Zeile pro user_id)
│   │   ├── master_group.csv        # master_features + Spalte „group“
│   │   └── user_scaled.csv
│   ├── scaled/                 # Standardisierte Features für das Clustering (NB05)
│   │   └── user_features_scaled.csv
│   └── cluster/                # Clustering-Ergebnisse & Profile (NB05)
│       ├── cluster_profile.csv
│       └── standard_customers_with_subclusters.csv
├── Notebooks/
│   ├── 01_traveltide_data_filtering.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_features.ipynb
│   ├── 04_group_build.ipynb
│   └── 05_clustering.ipynb
├── report/                     # 21 exportierte Diagramme & Dashboards
|    └── final-report/                   # Finaler PDF-Bericht
|           └── TravelTide_Final_Report.pdf
└── README.md
```

| Ordner | Inhalt | Erzeugt durch |
| :--- | :--- | :--- |
| `data/raw/` | Gefilterte Kern-Tabellen (aktive Nutzer) | Notebook **01** |
| `data/preprocessed/` | Bereinigte Tabellen + Feature-Master | Notebook **02, 03, 04** |
| `data/scaled/` | Standardisierte (z-normierte) Features | Notebook **05** |
| `data/cluster/` | Cluster-Profile & Sub-Cluster-Zuordnung | Notebook **05** |
| `report/` | Alle Visualisierungen als PNG | Notebook **02, 03, 04, 05** |
| `Notebooks/` | Analyse-Pipeline (01 → 05) | – |

---

## 🔄 Datenfluss – Schritt für Schritt

```text
   [Neon PostgreSQL]
   users · sessions · flights · hotels
            │
            ▼
 ┌───────────────────────────┐   „aktive User“:
 │ 01  Datenfilterung        │   session_start ≥ 2023-01-05  UND  > 7 Sessions
 └───────────────────────────┘
            │  data/raw/*.csv
            ▼
 ┌───────────────────────────┐   EDA & Cleaning pro Tabelle
 │ 02  Exploratory Analysis  │   → users / sessions / flights / hotels
 └───────────────────────────┘
            │  data/preprocessed/*_cleaned.csv
            ▼
 ┌───────────────────────────┐   Merge auf trip_id → Kosten → Aggregation je user_id
 │ 03  Feature Engineering   │   → Demografie verknüpfen  ⇒  Feature-Master
 └───────────────────────────┘
            │  data/preprocessed/master_features.csv
            ▼
 ┌───────────────────────────┐   Regelbasierte Segmentierung (np.select)
 │ 04  Gruppenbildung        │   → 7 Gruppen + „Standard Kunde“-Fallback
 └───────────────────────────┘
            │  data/preprocessed/master_group.csv
            ▼
 ┌───────────────────────────┐   Filter „Standard Kunde“ → Skalierung
 │ 05  K-Means Clustering    │   → Elbow/Silhouette → k=3 Sub-Cluster
 └───────────────────────────┘
            │  data/scaled/…  +  data/cluster/…
            ▼
   [report/ – 21 Visualisierungen]
```

---

## 📓 Die 5 Notebooks im Detail

### 1️⃣ `01_traveltide_data_filtering.ipynb` – Datenfilterung
Verbindet sich per **SQLAlchemy** mit der **Neon PostgreSQL**-Datenbank und filtert die
Kern-Tabellen auf **„aktive User“**: `session_start ≥ 2023-01-05` **und** mehr als 7 Sessions
(`HAVING COUNT(session_id) > 7`). Gelegenheitsnutzer:innen werden bewusst ausgeschlossen.
Die vier Tabellen werden als CSV exportiert:

| Tabelle | Zeilen | Spalten |
| :--- | ---: | ---: |
| `users` | 5.782 | 11 |
| `sessions` | 48.683 | 13 |
| `flights` | 13.767 | 13 |
| `hotels` | 14.374 | 7 |

➡️ Ausgabe: `data/raw/{users,sessions,flights,hotels}.csv`

### 2️⃣ `02_EDA.ipynb` – Explorative Datenanalyse & Cleaning
Analysiert und bereinigt jede Tabelle einzeln und visualisiert sie in Dashboards:

- **Users:** Altersverteilung (5-Jahres-Bins), Geschlecht, Familienstatus, Top-10-Städte.
- **Sessions:** Session-Dauern & Seitenklicks – Ø **3,15 Min.** über alle Sessions, Ø **6,44 Min.**
  bei Sessions mit Buchung (Bucher verbringen mehr als doppelt so viel Zeit auf der Plattform).
- **Flights:** Feature-Anreicherung (`departure_month/weekday/hour`, `trip_duration_days`,
  `route`, `price_category`, `onewayflug`, `is_weekend`, `price_per_seat`) + Preis-/Saison-/Airline-Analysen.
- **Hotels:** Bereinigungs-Dashboard (u. a. Entfernung negativer `nights`) + Buchungsanalyse
  (Aufenthaltsdauer, Preisverteilung, Städte, Ketten, Umsatz, Saisonalität).

➡️ Ausgabe: `data/preprocessed/*_cleaned.csv` + `report/*dashboard*.png`

### 3️⃣ `03_features.ipynb` – Feature Engineering & Master-Dataframe
Führt die bereinigten Transaktionsdaten über `trip_id` zusammen und aggregiert alles
**auf `user_id`-Ebene**. Kernschritte:

1. **Merge:** `sessions ← hotels ← flights` (Left Join auf `trip_id`).
2. **Kostenberechnung:** `flight_cost` und `hotel_cost` unter Berücksichtigung von
   **Buchung, Storno und Rabatt** (stornierte/nicht gebuchte Positionen = 0).
3. **Aggregation je Nutzer:** `total_sessions`, `total_trips`, gebuchte Flüge/Hotels (gesamt & valide),
   `total_flights_cost`, `total_hotels_cost`, `avg_checked_bags`, `avg_hotel_nights`,
   `discount_flight_uses`, `discount_hotel_uses`, `total_cancellations`, `cancellation_rate`.
4. **Demografie verknüpfen** & **Alter** aus `birthdate` berechnen → **`df_master`**.
5. **EDA-Visualisierungen** → Altersverteilung, Flug- vs. Hotelkosten (Scatter), Korrelations-Heatmap,
   Kostenverteilungen, Ausgaben nach Familienstand/Kinderstatus, Segmentierung nach überdurchschnittlichen
   Ausgaben + Venn-Diagramm (Spend-Overlap), inkl. strategischer Business-Empfehlungen.

➡️ Ausgabe: `data/preprocessed/master_features.csv` + 8 Report-Grafiken

### 4️⃣ `04_group_build.ipynb` – Regelbasierte Kundensegmentierung
Lädt `master_features.csv`, berechnet `buchung_ratio = total_trips / total_sessions` und
segmentiert die Kunden per **`np.select`** anhand von Schwellenwerten (Top-10 % Ausgaben,
Durchschnittsausgaben für Flug/Hotel, 75 %-Quantile für Trips & Buchungsratio, Altersgrenzen):

| Segment | Kunden | Anteil | Beschreibung |
| :--- | ---: | ---: | :--- |
| **Standard Kunde** | 2.070 | 35,8 % | Unauffälliges Buchungsverhalten – Fallback-Gruppe |
| **Top Spender Hotel** | 1.550 | 26,8 % | Überdurchschnittliche Hotelausgaben |
| **Top Spender Flug** | 1.096 | 19,0 % | Überdurchschnittliche Flugausgaben |
| **Top Spender Allgemein** | 579 | 10,0 % | VIP-Kunden (Top 10 % Gesamtausgaben) |
| **Rentner (>60)** | 251 | 4,3 % | Kunden über 60 Jahre |
| **Oft Bucher** | 200 | 3,5 % | Hohe Trip-Frequenz (Top 25 %) |
| **Young (<20)** | 36 | 0,6 % | Jüngste Kundengruppe |
| **Gesamt** | **5.782** | **100 %** | |

➡️ Ausgabe: `data/preprocessed/master_group.csv` + `report/Verteilung_der_Kundensegmente.png`

### 5️⃣ `05_clustering.ipynb` – K-Means-Clustering der „Standard Kunden“
Da die 2.070 „Standard Kunden“ durch einfache Schwellenwerte nicht differenziert werden,
werden **nur diese** weiter analysiert:

1. **Filter & Encoding:** Kategorie `gender` → numerisch, nicht-numerische Geo-Spalten entfernen.
2. **Skalierung:** `StandardScaler` (z-Normalisierung) der Features.
3. **Optimierung:** *Elbow-Methode* (Inertia/WCSS) **und** *Silhouette-Score* über `k = 2…10`.
4. **Clustering:** `KMeans(n_clusters=3, random_state=42, n_init=10)` → **3 Sub-Cluster**.
5. **Profiling & Visualisierung:** Cluster-Profile, Dashboard, Radar-Chart & Metrik-Heatmap;
   die Sub-Cluster-Labels werden in `master_group` zurückgeschrieben.

| Sub-Cluster | Ø Alter | Ø Gesamtausgaben | Conversion | Storno-Rate | Rabatte (Flug/Hotel) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **0 · Treue Wertkäufer** | 43,7 J. | **1.545,21 $** | **41 %** | 0,0 % | 1,43 / 1,10 |
| **1 · Low-Engagement Surfer** | 35,6 J. | 471,62 $ | 21 % | 0,0 % | wenige |
| **2 · Deal-Seeker & Storno-Risiko** | 37,8 J. | 1.438,21 $ | 37 % | **12,0 %** | **2,36 / 2,00** |

➡️ Ausgabe: `data/scaled/user_features_scaled.csv`, `data/cluster/*.csv` + 5 Report-Grafiken

---

## 📊 Ergebnisse & Visualisierungen (`report/`)

Alle Diagramme werden mit `matplotlib`/`seaborn` erstellt und als PNG exportiert.

| # | Datei | Notebook | Inhalt |
| :-: | :--- | :-: | :--- |
| 1 | `users_dashboard.png` | 02 | Alters-/Geschlechter-/Familienverteilung & Top-Städte |
| 2 | `sessions_dashboard.png` | 02 | Session-Dauer & Nutzungsverhalten |
| 3 | `Flights_Daschboard_1.png` | 02 | Flug-Überblick: Preis/Sitz, Airlines, Häfen, Monate |
| 4 | `Flights_Daschboard_2.png` | 02 | Preis-Analysen: One-Way vs. Round-Trip, Wochentage |
| 5 | `Flights_Daschboard_3.png` | 02 | Routen-/Saison-/Buchungsanalysen |
| 6 | `Hotels_Cleaning_Dashboard.png` | 02 | Datenbereinigung der Hotels (vor/nach) |
| 7 | `Hotels_Analysis_Dashboard.png` | 02 | Nächte, Preise, Städte, Ketten, Umsatz, Saison |
| 8 | `Altersverteilung_der_Kunden.png` | 03 | Altersstruktur der Kundenbasis |
| 9 | `Flugkosten_vs_Hotelkosten.png` | 03 | Scatter Flug- vs. Hotelausgaben |
| 10 | `Korrelations_Heatmap.png` | 03 | Korrelationen der Nutzer-Features |
| 11 | `Verteilung_der_Flugkosten.png` | 03 | Verteilung der Flugausgaben |
| 12 | `Verteilung_der_Hotelausgaben.png` | 03 | Verteilung der Hotelausgaben |
| 13 | `Gesamtausgaben_nach_Familienstand_und_Kinderstatus.png` | 03 | Ausgaben nach Familie/Kindern |
| 14 | `Kunden-Segmentierung_nach_überdurchschnittlichen_Ausgaben.png` | 03 | Segmentierung nach Spend-Schnitt |
| 15 | `Venn-Diagramm_überdurchschnittliche_Spender.png` | 03 | Overlap „Flug über“ ∩ „Hotel über“ |
| 16 | `Verteilung_der_Kundensegmente.png` | 04 | Verteilung der regelbasierten Gruppen |
| 17 | `elbow_silhouette_plot.png` | 05 | Optimale Clusteranzahl (Elbow + Silhouette) |
| 18 | `cluster_dashboard.png` | 05 | Vergleich der 3 Sub-Cluster |
| 19 | `Sub-Cluster_Vergleich_dashboard.png` | 05 | Ausgaben, Conversion, Rabatte je Cluster |
| 20 | `cluster_metrics_heatmap.png` | 05 | Kennzahlen-Heatmap der Cluster |
| 21 | `cluster_radar_chart.png` | 05 | Normalisierter „Profil-Fingerabdruck“ |

> 💡 **Kernaussagen (Auszug):** Nur **38,2 %** der Kunden liegen bei Flugkosten,
> **36,2 %** bei Hotelkosten über dem Durchschnitt → ausgeprägte Rechtsschiefe.
> Die Hotel-/Flug-Buchungen konzentrieren sich stark auf **Nordamerika (v. a. New York)**
> mit einem klaren Saison-Peak im **Q1**.

---

## 🛠️ Verwendete Technologien

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white">
  <img alt="NumPy" src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white">
  <img alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=matplotlib&logoColor=white">
  <img alt="seaborn" src="https://img.shields.io/badge/seaborn-4C72B0?style=flat-square">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white">
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL%20(Neon)-4169E1?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white">
</p>

| Bereich | Bibliotheken / Tools |
| :--- | :--- |
| **Sprache / Umgebung** | Python 3.14, Jupyter Notebook / VS Code |
| **Datenbankanbindung** | SQLAlchemy, PostgreSQL (Neon), psycopg2 |
| **Datenverarbeitung** | pandas, NumPy |
| **Visualisierung** | matplotlib, seaborn, matplotlib-venn |
| **Machine Learning** | scikit-learn (`StandardScaler`, `KMeans`, `silhouette_score`) |

---

## ⚙️ Installation & Voraussetzungen

**Voraussetzungen**

- 🐍 **Python 3.14** (getestet mit `3.14.6`; ab 3.10 kompatibel)
- 🌐 Internetzugang für die **Neon-PostgreSQL**-Verbindung (nur für Notebook 01)
- 📦 Die Notebooks nutzen **relative Pfade** (`../data`, `../report`) und müssen daher
  aus dem Ordner `Notebooks/` heraus ausgeführt werden

**Abhängigkeiten installieren**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn \
            sqlalchemy psycopg2-binary matplotlib-venn jupyter
```

---

## 🚀 Nutzung

Die Notebooks im Ordner `Notebooks/` **in numerischer Reihenfolge** ausführen –
jedes Notebook baut auf den Ergebnissen des vorherigen auf:

```bash
# Optional: virtuelle Umgebung
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Jupyter starten und Ordner Notebooks/ öffnen
jupyter notebook
```

| Schritt | Notebook | Eingabe | Ausgabe |
| :---: | :--- | :--- | :--- |
| 1 | `01_traveltide_data_filtering.ipynb` | Neon-DB | `data/raw/*.csv` |
| 2 | `02_EDA.ipynb` | `data/raw/*.csv` | `data/preprocessed/*_cleaned.csv`, `report/` |
| 3 | `03_features.ipynb` | `*_cleaned.csv` | `master_features.csv`, `report/` |
| 4 | `04_group_build.ipynb` | `master_features.csv` | `master_group.csv`, `report/` |
| 5 | `05_clustering.ipynb` | `master_group.csv` | `data/scaled/*`, `data/cluster/*`, `report/` |

> ⚠️ **Hinweis:** Notebook 01 enthält eine Datenbank-URL mit Zugangsdaten.
> Für einen produktiven Einsatz sollten Zugangsdaten aus der Umgebung (z. B. `.env`) geladen werden.

---

## 🌟 Projekt-Highlights

- 🔗 **End-to-End-Pipeline** – von der Datenbankabfrage bis zum fertigen Kundensegment.
- 🗄️ **Echte DB-Anbindung** – Anbindung an **Neon PostgreSQL** per SQLAlchemy mit sauberer
  CTE-basierter Filterung der „aktiven User“.
- 💰 **Realistisches Kostenmodell** – Flug-/Hotelkosten berücksichtigen **Buchung, Storno und Rabatte**.
- 🧩 **Hybrides Segmentierungs-Konzept** – erst **regelbasiert** (Transparenz), dann
  **K-Means (ML)** für die unscharfe Restgruppe (Treue Wertkäufer · Low-Engagement Surfer · Deal-Seeker).
- 🎯 **Business-orientiert** – jedes Segment wird mit konkreten **Marketing- & Handlungsempfehlungen** hinterlegt.
- 📈 **Aussagekräftige Dashboards** – 21 exportierte, publikationsreife Visualisierungen in `report/`.
- 🧪 **Methodisch saubere ML** – Feature-Skalierung sowie Kombination aus **Elbow-Methode** und **Silhouette-Score**.

---

<p align="center"><i>Erstellt mit ❤️ für datengestützte Reise-Entscheidungen – TravelTide Customer Analytics.</i></p>

