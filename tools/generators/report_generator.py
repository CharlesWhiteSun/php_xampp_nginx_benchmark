"""Main report generator - orchestrates all components."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List
import json

from models.benchmark import BenchmarkRow, Insight, Interpretation, ReportPayload
from loaders.csv_loader import CSVLoader, CSVFinder
from processors.data_processor import ChartDataProcessor, HistogramDataProcessor, InsightBuilder, InterpretationBuilder
from generators.html_builder import CSSGenerator, HTMLStructureBuilder
from generators.javascript_generator import JavaScriptGenerator
from generators.html_sections import EndpointsSection, FormulasSection, ChartsGridSection, InsightsTable, InterpretationSection, EndpointAnalysisSection, RawResultsSection, SummarySection
from i18n.texts import get_text


class ReportGenerator:
    """Main orchestrator for report generation."""
    
    def __init__(self, results_dir: Path, reports_dir: Path):
        self.results_dir = results_dir
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.csv_loader = CSVLoader()
        self.csv_finder = CSVFinder(results_dir)
        self.chart_processor = ChartDataProcessor()
    
    def generate(self) -> Path:
        """Generate the complete report."""
        # Find and load CSV
        csv_path = self.csv_finder.find_latest()
        if csv_path is None:
            raise FileNotFoundError("No results.csv found under results/")
        
        # Load and normalize data
        rows = self.csv_loader.load_and_normalize(csv_path)
        
        # Load benchmark configuration
        config = self._load_config(csv_path.parent)
        
        # Process data
        charts, endpoints = self.chart_processor.process(rows)
        hist_requests = HistogramDataProcessor.process(rows, "requests_sec")
        insights = InsightBuilder.build(rows, endpoints)
        interpretations = {
            "en": InterpretationBuilder.build(rows, endpoints, "en"),
            "zh": InterpretationBuilder.build(rows, endpoints, "zh"),
        }
        
        # Build payload
        utc_plus_8 = timezone(timedelta(hours=8))
        generated_at_local = datetime.now(timezone.utc).astimezone(utc_plus_8)
        generated_at_str = generated_at_local.strftime("%Y-%m-%d %H:%M:%S")
        source_name = f"results/{csv_path.parent.name}/results.csv"
        
        payload = {
            "meta": {
                "generated_at": generated_at_str,
                "source": source_name,
            },
            "endpoints": endpoints,
            "charts": charts,
            "hist_requests": hist_requests,
            "insights": [self._insight_to_dict(i) for i in insights],
            "interpretations": {
                "en": [self._interpretation_to_dict(i) for i in interpretations["en"]],
                "zh": [self._interpretation_to_dict(i) for i in interpretations["zh"]],
            },
            "has_pctl": self._has_percentiles(rows),
            "rows": [self._row_to_dict(r) for r in rows],
        }
        
        # Generate HTML
        html_content = self._build_html(payload, rows, insights, config)
        output_path = self.reports_dir / "report.html"
        output_path.write_text(html_content, encoding="utf-8")
        
        return output_path
    
    def _build_html(self, payload: dict, rows: List[BenchmarkRow], insights: List[Insight], config: dict) -> str:
        """Build complete HTML document."""
        texts = {
            "en": get_text("en"),
            "zh": get_text("zh"),
        }
        
        css = CSSGenerator.generate()
        header = HTMLStructureBuilder.build_header()
        footer = HTMLStructureBuilder.build_footer()
        head = HTMLStructureBuilder.build_head(css)
        payload_and_texts = JavaScriptGenerator.generate_payload_and_texts(payload, texts)
        chart_code = JavaScriptGenerator.generate_chart_code()
        interaction_code = JavaScriptGenerator.generate_interaction_code()
        
        # Build main content sections
        main_content = self._build_main_content(rows, insights, config)
        
        # Load the main HTML structure template
        html_template = self._get_html_template()
        
        # Insert generated content
        html = html_template.format(
            html_head=head,
            header=header,
            main_content=main_content,
            footer=footer,
            payload_and_texts=payload_and_texts,
            chart_code=chart_code,
            interaction_code=interaction_code,
        )
        
        return html
    
    def _build_main_content(self, rows: List[BenchmarkRow], insights: List[Insight], config: dict) -> str:
        """Build all main content sections."""
        summary_html = SummarySection.build(config)
        endpoints_html = EndpointsSection.build()
        raw_results_html = RawResultsSection.build(rows)
        formulas_html = FormulasSection.build()
        charts_html = ChartsGridSection.build()
        insights_html = InsightsTable.build([self._insight_to_dict(i) for i in insights])
        interpretation_html = InterpretationSection.build()
        endpoint_analysis_html = EndpointAnalysisSection.build()
        
        return f"""{summary_html}

{endpoints_html}

{raw_results_html}

{formulas_html}

{interpretation_html}

{charts_html}

{insights_html}

{endpoint_analysis_html}"""
    
    def _get_html_template(self) -> str:
        """Get HTML template with placeholders."""
        return """<!DOCTYPE html>
<html lang="zh-Hant">
{html_head}
<body>
  {header}
  <div class="container">
    {main_content}
  </div>
  {footer}
  <script>
    {payload_and_texts}

    {chart_code}

    {interaction_code}
  </script>
</body>
</html>"""
    
    # Helper methods
    @staticmethod
    def _insight_to_dict(insight: Insight) -> dict:
        """Convert Insight to dictionary."""
        return {
            "endpoint": insight.endpoint,
            "req_winner": insight.req_winner,
            "req_delta": insight.req_delta,
            "lat_winner": insight.lat_winner,
            "lat_delta": insight.lat_delta,
        }
    
    @staticmethod
    def _interpretation_to_dict(interp: Interpretation) -> dict:
        """Convert Interpretation to dictionary."""
        return {
            "endpoint": interp.endpoint,
            "text": interp.text,
            "finding": interp.finding,
            "endpoint_type": interp.endpoint_type,
        }
    
    @staticmethod
    def _row_to_dict(row: BenchmarkRow) -> dict:
        """Convert BenchmarkRow to dictionary."""
        return {
            "timestamp": row.timestamp,
            "server": row.server,
            "endpoint": row.endpoint,
            "requests_sec": row.requests_sec,
            "latency_ms": row.latency_ms,
            "latency_p50_ms": row.latency_p50_ms,
            "latency_p75_ms": row.latency_p75_ms,
            "latency_p90_ms": row.latency_p90_ms,
            "latency_p99_ms": row.latency_p99_ms,
            "transfer_kb_sec": row.transfer_kb_sec,
            "latency_avg": row.latency_avg,
            "latency_p50": row.latency_p50,
            "latency_p75": row.latency_p75,
            "latency_p90": row.latency_p90,
            "latency_p99": row.latency_p99,
            "transfer_sec": row.transfer_sec,
        }
    
    @staticmethod
    def _has_percentiles(rows: List[BenchmarkRow]) -> bool:
        """Check if rows have percentile data."""
        for row in rows:
            if row.latency_p50_ms is not None or row.latency_p99_ms is not None:
                return True
        return False    
    @staticmethod
    def _load_config(results_dir: Path) -> dict:
        """Load benchmark configuration from config.json."""
        config_path = results_dir / "config.json"
        
        # Default configuration
        default_config = {
            "duration": 10,
            "connections": 50,
            "endpoints": ["cpu.php", "json.php", "io.php"],
            "endpoint_params": {
                "cpu": {"iterations": 10000},
                "json": {"items": 2000},
                "io": {"size": 8192, "iterations": 20, "mode": "memory"}
            },
            "test_time": "N/A"
        }
        
        # Try to load configuration from file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    return {**default_config, **loaded_config}
            except (json.JSONDecodeError, IOError):
                pass
        
        return default_config