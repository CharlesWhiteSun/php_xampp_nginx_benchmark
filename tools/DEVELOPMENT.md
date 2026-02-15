# Development Guide

## Quick Start

### Running Reports
```bash
cd tools
python generate_report_new.py  # Generate report from latest CSV
```

Output: `reports/report.html`

### Local Testing
```bash
python -m http.server 8000 -d reports
# Then open http://localhost:8000/report.html in browser
```

## Module Deep Dives

### Settings Configuration

**File**: `config/settings.py`

Used by: All modules that need configuration

```python
from config.settings import CHART_COLORS, RESULTS_DIR

color_xampp = CHART_COLORS["xampp"]  # "#f2b264"
results_path = RESULTS_DIR  # Path("results")
```

**What to modify**:
- Add new color schemes
- Change default directories
- Adjust default theme/language
- Update unit conversion factors

### Internationalization

**File**: `i18n/texts.py`

Used by: `JavaScriptGenerator`, all HTML sections, `InterpretationBuilder`

```python
from i18n.texts import get_text

texts_en = get_text("en")
title = texts_en["title"]  # "PHP Benchmark Report"
```

**How to add new language**:
1. Add language code to `TEXTS` dict
2. Add all keys for the new language
3. Update `JavaScriptGenerator.generate_interaction_code()` if needed

**How to add new text key**:
1. Add to both "en" and "zh" in TEXTS
2. Use in HTML: `<h1 data-i18n="new_key"></h1>`
3. JavaScript handles the translation

### Data Models

**File**: `models/benchmark.py`

Used by: All processors, loaders, generators

```python
from models.benchmark import BenchmarkRow, ChartData

# BenchmarkRow represents one benchmark measurement
# ChartData represents aggregated data for rendering
```

**Adding new data model**:
1. Create dataclass in `benchmark.py`
2. Update processors to populate it
3. Update generators to render it
4. Update templates to display it

### Parsing and Loading

**Files**: `parsers/data_parsers.py`, `loaders/csv_loader.py`

Used by: `ReportGenerator`, data processors

```python
from parsers.data_parsers import LatencyParser, TransferParser
from loaders.csv_loader import CSVLoader, CSVFinder

# Parse individual values
lat_ms = LatencyParser.parse("100us")  # 0.1

# Load all data
loader = CSVLoader()
rows = loader.load_and_normalize(csv_path)
```

**Adding new unit parser**:
1. Create class in `parsers/data_parsers.py`
2. Implement `parse(value: str) -> float`
3. Use in `CSVLoader._normalize_row()`

### Data Processing

**File**: `processors/data_processor.py`

Used by: `ReportGenerator`

```python
from processors.data_processor import ChartDataProcessor, InsightBuilder

processor = ChartDataProcessor()
charts, endpoints = processor.process(rows)

insights = InsightBuilder.build(rows, endpoints)
# insights[0].endpoint == "cpu.php"
# insights[0].req_winner == "XAMPP"  or "NGINX (Multi-core)"
# insights[0].req_delta == 15.5  # percentage
```

**Modifying analysis logic**:
1. Edit `ChartDataProcessor.process()` for chart data
2. Edit `InsightBuilder.build()` for performance comparison
3. Edit `InterpretationBuilder.build()` for user-friendly text

### HTML and CSS Generation

**Files**: `generators/html_builder.py`, `generators/html_sections.py`

Used by: `ReportGenerator`

```python
from generators.html_builder import CSSGenerator, HTMLStructureBuilder
from generators.html_sections import EndpointsSection, FormulasSection

css = CSSGenerator.generate()  # Returns CSS string
header = HTMLStructureBuilder.build_header()  # Returns HTML
endpoints_html = EndpointsSection.build()  # Returns HTML
```

**Modifying CSS**:
1. Edit `CSSGenerator.generate()` in `html_builder.py`
2. Use CSS variables for theming (--bg, --text, --accent, etc.)
3. Test with all three themes: light, dark, default

**Modifying HTML structure**:
1. Edit corresponding section in `html_sections.py`
2. Use `data-i18n="key"` for translatable text
3. Use `id="chart-xxx"` for Plotly chart containers
4. Use `id="interpretation-list"` for dynamic interpretation list

### JavaScript Generation

**File**: `generators/javascript_generator.py`

Used by: `ReportGenerator`

```python
from generators.javascript_generator import JavaScriptGenerator

# Payload and translations
code1 = JavaScriptGenerator.generate_payload_and_texts(payload, texts)

# Charts (Plotly)
code2 = JavaScriptGenerator.generate_chart_code()

# Interactions (theme, language)
code3 = JavaScriptGenerator.generate_interaction_code()
```

**Chart customization**:
1. Edit `generate_chart_code()` method
2. Modify Plotly configuration (colors, fonts, layouts)
3. Add new chart types by creating new Plotly code blocks
4. Ensure chart container IDs match HTML (`id="chart-xxx"`)

**Theme flexibility**:
- CSS Custom Properties in CSS are mapped to theme values
- `applyTheme()` function updates chart fonts and colors
- Add new properties to CSS and update `applyTheme()` accordingly

## Common Tasks

### Change Chart Colors

**Option 1**: Modify CSS variables
```css
:root {
  --accent: #f2b264;  /* Change XAMPP color */
  --accent2: #6dd3b6; /* Change NGINX color */
}
```

**Option 2**: Modify chart-specific colors
```python
# In generators/javascript_generator.py
bar_color = {
    'type': 'bar',
    'marker': {'color': '#new_color'},
}
```

### Add New Metric

1. **Data Model** (`models/benchmark.py`):
   ```python
   @dataclass
   class BenchmarkRow:
       new_metric: float
   ```

2. **Parser** (`parsers/data_parsers.py`):
   ```python
   class NewMetricParser:
       @staticmethod
       def parse(value: str) -> float:
           return float(value) * conversion_factor
   ```

3. **Loader** (`loaders/csv_loader.py`):
   ```python
   result.new_metric = NewMetricParser.parse(row['new_metric_col'])
   ```

4. **Processor** (`processors/data_processor.py`):
   ```python
   def _build_new_metric_data(self, rows) -> dict:
       # Build chart data for new metric
   ```

5. **Generator** (`generators/javascript_generator.py`):
   ```python
   # Add chart code for new metric
   ```

6. **HTML** (`generators/html_sections.py`):
   ```python
   # Add section to display new metric
   ```

### Add Collapsible Sections

Already implemented! Each major section (endpoints, formulas, charts, insights, interpretations, raw data) has built-in collapse/expand toggle:

```html
<button class="collapse-btn" onclick="...toggleDisplay...">▼</button>
```

To add to new sections, follow the same pattern in `html_sections.py`.

### Change Themes

Update `config/settings.py`:
```python
FONT_COLORS = {
    "light": {
        "text": "#1a1a1a",
        "muted": "#666666",
    },
    "dark": {
        "text": "#d0d0d0",
        "muted": "#888888",
    },
}
```

Then update CSS in `CSSGenerator.generate()` to use matching colors.

### Change Translations

Edit `i18n/texts.py`:
```python
TEXTS = {
    "en": {
        "title": "New Title",
        "description": "New Description",
        # ... add more keys
    },
    "zh": {
        "title": "新標題",
        "description": "新描述",
        # ... add more keys
    },
}
```

## Testing

### Unit Test Example

```python
# test_parsers.py
from parsers.data_parsers import LatencyParser

def test_latency_parser_microseconds():
    assert LatencyParser.parse("1000us") == 1.0
    
def test_latency_parser_milliseconds():
    assert LatencyParser.parse("1ms") == 1.0
    
def test_latency_parser_seconds():
    assert LatencyParser.parse("0.001s") == 1.0
```

### Integration Test Example

```python
# test_integration.py
from generators.report_generator import ReportGenerator
from pathlib import Path
import tempfile

def test_complete_report_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = ReportGenerator(Path("results"), Path(tmpdir))
        output = gen.generate()
        assert output.exists()
        assert output.stat().st_size > 10000  # Check file size
        content = output.read_text()
        assert "<html" in content
        assert "benchmark" in content.lower()
```

## Troubleshooting

### Report not generating
1. Check if `results/` directory exists with CSV files
2. Ensure CSV has required columns (see `CSVLoader.load_raw()`)
3. Check Python console for error messages

### Charts not rendering
1. Verify Plotly CDN is accessible (check network tab)
2. Check browser console for JavaScript errors
3. Verify chart container IDs match HTML (`id="chart-xxx"`)

### Theme not applying
1. Browser may be caching old CSS
2. Clear browser cache or open in incognito mode
3. Check `localStorage` for saved theme preference
4. Verify CSS variables are defined in `:root`

### Translations not showing
1. Ensure HTML elements have `data-i18n="key"` attribute
2. Verify text key exists in both "en" and "zh" dicts in `texts.py`
3. Check browser console for JavaScript errors
4. Verify `applyLang()` function is being called on page load

## Performance Optimization

### Large Datasets
If benchmarks have many endpoints:
1. Reduce chart height temporarily
2. Consider pagination for raw data table
3. Profile with browser DevTools (F12 → Performance)

### Slow Generation
1. Check if CSV file is very large (>100MB)
2. Profile Python code with `cProfile`
3. Consider caching processed data between runs

## Git Workflow

When making changes:
```bash
# Before editing
git checkout -b feature/description

# After editing
git add tools/
git commit -m "Refactor: description of changes"
git push origin feature/description

# Create PR for code review
```

## Best Practices

1. **Keep modules focused** - Each module should have one clear purpose
2. **Use type hints** - Makes code more readable and enables IDE support
3. **Document assumptions** - Especially for data formats and transformations
4. **Add tests for new features** - Even simple unit tests improve maintainability
5. **Update this guide** - When adding new modules or significant changes

## Common Patterns

### Adding a processing step
```python
# 1. Add to ReportGenerator.generate()
new_data = NewProcessor.process(rows)

# 2. Add to ReportPayload dict
payload["new_data"] = new_data

# 3. Pass to JavaScript
# Goes via generate_payload_and_texts()

# 4. Use in JavaScript chart code
```

### Adding a display section
```python
# 1. Create section builder class
class NewSection:
    @staticmethod
    def build(data: dict) -> str:
        return html_string

# 2. Call in ReportGenerator._build_main_content()
new_section = NewSection.build(data)

# 3. Include in template string
```

## Support

For questions or issues:
1. Check this guide first
2. Review comment documentation in source code
3. Examine similar existing modules for patterns
4. Refer to README.md for architecture overview
