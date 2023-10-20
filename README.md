# iresoft-files-task

# Instalace na lokálním prostředí

## Požadavky
Předtím než začnete s instalací, ujistěte se, že na vašem počítači jsou nainstalovány následující komponenty:
- [Python](https://www.python.org/): Django je framework napsaný v Pythonu.
- [PIP](https://pip.pypa.io/en/stable/): Správce balíčků pro Python.
- [Virtualenv](https://virtualenv.pypa.io/en/latest/): Nástroj pro izolaci Python projektů.

## Krok 1: Stáhněte Aplikaci
Stáhněte zdrojový kód aplikace z repozitáře nebo zkopírujte jej na váš lokální počítač.

```bash
git clone https://github.com/jmeno/aplikace.git
```

## Krok 2: Vytvořte virtuální prostředí
Pro izolaci závislostí a balíčků aplikace doporučujeme vytvoření virtuálního prostředí. Přejděte do složky aplikace a vytvořte virtuální prostředí.
```bash
cd aplikace/
python -m venv venv
```

## Krok 3: Aktivujte virtuální prostředí
Aktivujte virtuální prostředí, abyste mohli instalovat balíčky specifické pro aplikaci.

Na Windows
```bash
venv\Scripts\activate
```
Na macOS a Linux
```bash
source venv/bin/activate
```

## Krok 4: Instalace závislostí
Nainstalujte všechny balíčky a závislosti potřebné pro aplikaci pomocí PIPu.

```bash
pip install -r requirements.txt
```

## Krok 5: Připravte databázi
Defaultně nastavena databáze typu sqlite3. Je však potřeba provést vytvoření tabulek pomocí příkazů makemigrations a migrate.

```bash
python manage.py makemigrations
python manage.py migrate
```
## Krok 6: Spusťte lokální server
Spusťte lokální vývojový server, který umožňuje testovat vaši aplikaci na vašem počítači.

```bash
python manage.py runserver
```
Aplikace by nyní měla být přístupná na http://127.0.0.1:8000/ ve vašem webovém prohlížeči.
Zobrazí se openapi schema s dostupnými endpointy.

## Krok 7: Spuštění testů (volitelný)
Spusťte automatické testy aplikace.

```bash
python manage.py test
```

# Endpointy:
1. **GET /list/**: Získání seznamu souborů.
   - **Response:** Seznam souborů s následujícími atributy:
     - `id` (int): Unikátní identifikátor souboru.
     - `file_name` (str): Název souboru.
     - `file_type` (str): Typ souboru.
     - `file_size` (int): Velikost souboru v bajtech.
     - `added_at` (datetime.datetime): Datum a čas přidání souboru.
     - filtrování je možné dle atributů `file_name`, `file_type`, `file_size` a `added_at`

2. **GET /download/{file_id}**: Stáhnutí konkrétního souboru podle jeho ID.
   - **Response:** Stáhne vybraný soubor.

3. **POST /upload**: Nahrání nového souboru.
   - **Request:** Očekává nahraný soubor v těle požadavku.
   - **Response:** Potvrzení nahrání souboru s názvem nově nahraného souboru.

4. **DELETE /delete/{file_id}**: Smazání konkrétního souboru podle jeho ID.
   - **Response:** Potvrzení smazání souboru s názvem smazaného souboru.

5. **GET /stats/**: Získání statistik o uložených souborech.
   - **Response:** Statistiky obsahují:
     - `files_count` (int): Celkový počet souborů.
     - `total_size` (str): Celková velikost všech souborů v čitelném formátu.
     - `average_size` (str): Průměrná velikost souborů v čitelném formátu.
     - `median_size` (str): Medián velikosti souborů v čitelném formátu.
     - `biggest_file` (str): Velikost největšího souboru v čitelném formátu.
     - `smallest_file` (str): Velikost nejmenšího souboru v čitelném formátu.

