# 📂 data – Hinweise zur Datenablage

Dieser Ordner enthält **keine** Datendateien im Repository. Alle `*.csv`-Dateien
werden über die `.gitignore` bewusst ausgeschlossen, damit keine (teils großen bzw.
sensiblen) Datensätze eingecheckt werden.

Die Ordnerstruktur bleibt über leere `.gitkeep`-Dateien erhalten. Die CSV-Dateien
müssen **manuell** in die jeweils passenden Pfade gelegt werden, **bevor** die
Notebooks ausgeführt werden.

## Erwartete Verzeichnisstruktur

```text
data/
├── raw/            # Rohdaten, gefiltert aus der Neon-PostgreSQL-DB (Notebook 01)
│   ├── users.csv
│   ├── sessions.csv
│   ├── flights.csv
│   └── hotels.csv
├── preprocessed/   # Bereinigte Tabellen + Feature-Master (Notebook 02–04)
│   ├── users_cleaned.csv
│   ├── sessions_cleaned.csv
│   ├── flights_cleaned.csv
│   ├── hotels_cleaned.csv
│   ├── master_features.csv
│   ├── master_group.csv
│   └── user_scaled.csv
├── scaled/         # Standardisierte Features für das Clustering (Notebook 05)
│   └── user_features_scaled.csv
└── cluster/        # Clustering-Ergebnisse & Profile (Notebook 05)
    ├── cluster_profile.csv
    └── standard_customers_with_subclusters.csv
```

## Vorgehen

1. **Notebook 01** (`01_traveltide_data_filtering.ipynb`) erzeugt die Dateien in
   `data/raw/` direkt aus der Datenbank – sofern ein gültiger DB-Zugang vorhanden ist.
2. Alternativ können die bereits vorhandenen CSV-Dateien **manuell** in die oben
   genannten Ordner kopiert werden.
3. Erst danach die Notebooks **02 → 05** ausführen, da jedes Notebook auf den
   Ergebnissen des vorherigen aufbaut.

> ℹ️ **Hinweis:** Ohne die CSV-Dateien in `data/raw/` bzw. `data/preprocessed/`
> können die nachfolgenden Notebooks nicht ausgeführt werden.
