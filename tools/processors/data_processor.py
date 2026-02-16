"""Data processors for benchmark analysis."""
from collections import defaultdict
from typing import List, Dict, Any, Tuple

from models.benchmark import BenchmarkRow, ChartData, PercentileData, Insight, Interpretation
from i18n.texts import get_text


def format_endpoint_label(endpoint: str) -> str:
    """Convert endpoint to display label (e.g., 'cpu.php' -> 'CPU')."""
    name = endpoint.replace(".php", "").lower()
    if name == "cpu":
        return "CPU"
    elif name == "io":
        return "I/O"
    elif name == "json":
        return "JSON"
    else:
        return name.upper()


class ChartDataProcessor:
    """Processes benchmark data into chart-ready format."""
    
    def process(self, rows: List[BenchmarkRow]) -> Tuple[Dict[str, Any], List[str]]:
        """
        Process rows into chart data.
        
        Returns:
            Tuple of (charts dict, endpoints list)
        """
        by_endpoint = defaultdict(list)
        for row in rows:
            by_endpoint[row.endpoint].append(row)
        
        endpoints = sorted(by_endpoint.keys())
        labels = [format_endpoint_label(e) for e in endpoints]
        
        charts = {
            "requests_sec": self._build_chart_data(by_endpoint, endpoints, lambda r: r.requests_sec),
            "latency_ms": self._build_chart_data(by_endpoint, endpoints, lambda r: r.latency_ms),
            "transfer_kb_sec": self._build_chart_data(by_endpoint, endpoints, lambda r: r.transfer_kb_sec),
            "latency_pctl": self._build_percentile_data(by_endpoint, endpoints),
            "throughput_delta_pct": self._build_delta_data(by_endpoint, endpoints),
        }
        
        return charts, endpoints
    
    @staticmethod
    def _build_chart_data(by_endpoint, endpoints, accessor) -> ChartData:
        """Build a single chart dataset."""
        chart = ChartData()
        for endpoint in endpoints:
            label = format_endpoint_label(endpoint)
            chart.labels.append(label)
            
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            chart.xampp.append(accessor(x) if x else None)
            chart.nginx_multi.append(accessor(nm) if nm else None)
        
        return {
            "labels": chart.labels,
            "xampp": chart.xampp,
            "nginx_multi": chart.nginx_multi,
        }
    
    @staticmethod
    def _build_percentile_data(by_endpoint, endpoints) -> Dict[str, Any]:
        """Build percentile data."""
        pctl = PercentileData()
        for endpoint in endpoints:
            label = format_endpoint_label(endpoint)
            pctl.labels.append(label)
            
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            if x:
                pctl.xampp["p50"].append(x.latency_p50_ms)
                pctl.xampp["p75"].append(x.latency_p75_ms)
                pctl.xampp["p90"].append(x.latency_p90_ms)
                pctl.xampp["p99"].append(x.latency_p99_ms)
            if nm:
                pctl.nginx_multi["p50"].append(nm.latency_p50_ms)
                pctl.nginx_multi["p75"].append(nm.latency_p75_ms)
                pctl.nginx_multi["p90"].append(nm.latency_p90_ms)
                pctl.nginx_multi["p99"].append(nm.latency_p99_ms)
        
        return {
            "labels": pctl.labels,
            "xampp": pctl.xampp,
            "nginx_multi": pctl.nginx_multi,
        }
    
    @staticmethod
    def _build_delta_data(by_endpoint, endpoints) -> Dict[str, Any]:
        """Build throughput delta data."""
        labels = []
        values = []
        for endpoint in endpoints:
            labels.append(format_endpoint_label(endpoint))
            
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            delta = None
            if nm and nm.requests_sec > 0:
                delta = (x.requests_sec - nm.requests_sec) / nm.requests_sec * 100.0 if x else None
            values.append(delta)
        
        return {"labels": labels, "values": values}


class HistogramDataProcessor:
    """Processes data into histogram format."""
    
    @staticmethod
    def process(rows: List[BenchmarkRow], metric: str = "requests_sec") -> Dict[str, List[float]]:
        """Generate histogram data."""
        accessor = getattr(BenchmarkRow, metric) if hasattr(BenchmarkRow, metric) else None
        
        return {
            "xampp": [getattr(r, metric) for r in rows if r.server == "xampp"],
            "nginx_multi": [getattr(r, metric) for r in rows if r.server == "nginx_multi"],
        }


class InsightBuilder:
    """Builds performance insights."""
    
    @staticmethod
    def build(rows: List[BenchmarkRow], endpoints: List[str]) -> List[Insight]:
        """Build insights for each endpoint."""
        by_endpoint = defaultdict(list)
        for row in rows:
            by_endpoint[row.endpoint].append(row)
        
        insights = []
        for endpoint in endpoints:
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            # Find winners
            req_values = {}
            if x: req_values["xampp"] = x.requests_sec
            if nm: req_values["nginx_multi"] = nm.requests_sec
            req_winner = max(req_values, key=req_values.get) if req_values else "N/A"
            
            lat_values = {}
            if x: lat_values["xampp"] = x.latency_ms
            if nm: lat_values["nginx_multi"] = nm.latency_ms
            lat_winner = min(lat_values, key=lat_values.get) if lat_values else "N/A"
            
            # Calculate deltas
            req_delta = 0.0
            if nm and nm.requests_sec > 0 and x:
                req_delta = (x.requests_sec - nm.requests_sec) / nm.requests_sec * 100.0
            
            lat_delta = 0.0
            if nm and nm.latency_ms > 0 and x:
                lat_delta = (x.latency_ms - nm.latency_ms) / nm.latency_ms * 100.0
            
            insights.append(Insight(
                endpoint=endpoint,
                req_winner=req_winner,
                req_delta=req_delta,
                lat_winner=lat_winner,
                lat_delta=lat_delta,
            ))
        
        return insights


class InterpretationBuilder:
    """Builds user-friendly interpretations."""
    
    @staticmethod
    def build(rows: List[BenchmarkRow], endpoints: List[str], lang: str = "zh") -> List[Interpretation]:
        """Build interpretations for each endpoint."""
        texts = get_text(lang)
        by_endpoint = defaultdict(list)
        for row in rows:
            by_endpoint[row.endpoint].append(row)
        
        notes = []
        for endpoint in endpoints:
            label = endpoint.replace(".php", "")
            display_label = format_endpoint_label(endpoint)
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            # Find winners with display names
            req_values = {}
            if x: req_values["XAMPP"] = x.requests_sec
            if nm: req_values["NGINX"] = nm.requests_sec
            req_winner = max(req_values, key=req_values.get) if req_values else "N/A"
            
            lat_values = {}
            if x: lat_values["XAMPP"] = x.latency_ms
            if nm: lat_values["NGINX"] = nm.latency_ms
            lat_winner = min(lat_values, key=lat_values.get) if lat_values else "N/A"
            
            # Calculate performance deltas for additional context
            req_delta = None
            lat_delta = None
            if x and nm and x.requests_sec > 0 and nm.requests_sec > 0:
                req_delta = ((nm.requests_sec - x.requests_sec) / x.requests_sec * 100)
                lat_delta = ((nm.latency_ms - x.latency_ms) / x.latency_ms * 100) if x.latency_ms > 0 else None
            
            # Build interpretation text with endpoint-specific insights
            parts = []
            
            # 1. Main comparison
            parts.append(texts["interp_compare"].format(req_winner=req_winner, lat_winner=lat_winner))
            
            # 2. Endpoint-specific introduction and context
            endpoint_type = label.lower()
            if endpoint_type == "cpu":
                parts.append(texts["interp_cpu_winner"].format(winner=req_winner))
                if req_winner == lat_winner:
                    parts.append(texts["interp_cpu_consistent"].format(winner=req_winner))
                else:
                    if "NGINX" in req_winner:
                        parts.append(texts["interp_cpu_nginx_wins"])
                    else:
                        parts.append(texts["interp_cpu_xampp_wins"])
                    parts.append(texts["interp_cpu_tradeoff"].format(req_winner=req_winner, lat_winner=lat_winner))
                    
            elif endpoint_type == "io":
                parts.append(texts["interp_io_winner"].format(winner=req_winner))
                if req_winner == lat_winner:
                    parts.append(texts["interp_io_consistent"].format(winner=req_winner))
                else:
                    if "XAMPP" in req_winner:
                        parts.append(texts["interp_io_xampp_wins"])
                    else:
                        parts.append(texts["interp_io_nginx_wins"])
                    parts.append(texts["interp_io_tradeoff"].format(req_winner=req_winner, lat_winner=lat_winner))
                parts.append(texts["interp_io_context"])
                
            elif endpoint_type == "json":
                parts.append(texts["interp_json_winner"].format(winner=req_winner))
                if req_winner == lat_winner:
                    parts.append(texts["interp_json_consistent"].format(winner=req_winner))
                else:
                    if "NGINX" in req_winner:
                        parts.append(texts["interp_json_nginx_wins"])
                    else:
                        parts.append(texts["interp_json_xampp_wins"])
                    parts.append(texts["interp_json_tradeoff"].format(req_winner=req_winner, lat_winner=lat_winner))
                parts.append(texts["interp_json_context"])
            
            # 3. Performance delta context (optional)
            if req_delta is not None:
                if req_delta > 10:
                    direction = "significantly faster"
                elif req_delta > 0:
                    direction = "moderately faster"
                elif req_delta > -10:
                    direction = "slightly slower"
                else:
                    direction = "significantly slower"
                # Only add if notable difference
                if abs(req_delta) > 5:
                    parts.append(f"({req_winner} is {direction})")
            
            # 4. Check P99 tail latency
            p99_values = []
            if x and x.latency_p99_ms is not None: p99_values.append(x.latency_p99_ms)
            if nm and nm.latency_p99_ms is not None: p99_values.append(nm.latency_p99_ms)
            
            if p99_values and max(p99_values) >= 1000.0:
                parts.append(texts["interp_tail"])
            elif not p99_values:
                parts.append(texts["interp_p99_missing"])
            
            # Build the finding summary (in appropriate language)
            if lang == "zh":
                if req_winner == lat_winner:
                    finding = f"吞吐與延遲均：{req_winner}"
                else:
                    finding = f"吞吐：{req_winner} | 延遲：{lat_winner}"
            else:
                if req_winner == lat_winner:
                    finding = f"Both metrics favor {req_winner}"
                else:
                    finding = f"Throughput: {req_winner} | Latency: {lat_winner}"
            
            notes.append(Interpretation(endpoint=display_label, text=" ".join(parts), finding=finding, endpoint_type=label))
        
        return notes

