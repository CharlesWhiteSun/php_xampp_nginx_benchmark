"""Data processors for benchmark analysis."""
from collections import defaultdict
from typing import List, Dict, Any, Tuple

from models.benchmark import BenchmarkRow, ChartData, PercentileData, Insight, Interpretation
from i18n.texts import get_text


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
        labels = [e.replace(".php", "") for e in endpoints]
        
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
            label = endpoint.replace(".php", "")
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
            label = endpoint.replace(".php", "")
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
            labels.append(endpoint.replace(".php", ""))
            
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
            x = next((r for r in by_endpoint[endpoint] if r.server == "xampp"), None)
            nm = next((r for r in by_endpoint[endpoint] if r.server == "nginx_multi"), None)
            
            # Find winners with display names
            req_values = {}
            if x: req_values["XAMPP"] = x.requests_sec
            if nm: req_values["NGINX (Multi-core)"] = nm.requests_sec
            req_winner = max(req_values, key=req_values.get) if req_values else "N/A"
            
            lat_values = {}
            if x: lat_values["XAMPP"] = x.latency_ms
            if nm: lat_values["NGINX (Multi-core)"] = nm.latency_ms
            lat_winner = min(lat_values, key=lat_values.get) if lat_values else "N/A"
            
            # Build interpretation text
            parts = []
            parts.append(texts["interp_compare"].format(req_winner=req_winner, lat_winner=lat_winner))
            
            if req_winner != lat_winner:
                parts.append(texts["interp_tradeoff"])
            else:
                parts.append(texts["interp_consistent"].format(winner=req_winner))
            
            # Check P99
            p99_values = []
            if x and x.latency_p99_ms is not None: p99_values.append(x.latency_p99_ms)
            if nm and nm.latency_p99_ms is not None: p99_values.append(nm.latency_p99_ms)
            
            if p99_values and max(p99_values) >= 1000.0:
                parts.append(texts["interp_tail"])
            elif not p99_values:
                parts.append(texts["interp_p99_missing"])
            
            notes.append(Interpretation(endpoint=label, text=" ".join(parts)))
        
        return notes
