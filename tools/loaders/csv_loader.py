"""CSV loading and file discovery utilities."""
import csv
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone, timedelta

from models.benchmark import BenchmarkRow
from parsers.data_parsers import LatencyParser, TransferParser


class CSVLoader:
    """Loads and parses CSV files."""
    
    def __init__(self, latency_parser: LatencyParser = None, transfer_parser: TransferParser = None):
        self.latency_parser = latency_parser or LatencyParser()
        self.transfer_parser = transfer_parser or TransferParser()
    
    @staticmethod
    def load_raw(csv_path: Path) -> List[dict]:
        """Load raw CSV data."""
        rows = []
        # Try common encodings in order
        encodings = ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1"]
        
        for enc in encodings:
            try:
                with csv_path.open(newline="", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        rows.append(row)
                return rows
            except (UnicodeDecodeError, LookupError, UnicodeError):
                continue
        
        # If all fail, raise error
        raise ValueError(f"Unable to decode CSV file at {csv_path} with any known encoding")
    
    def load_and_normalize(self, csv_path: Path) -> List[BenchmarkRow]:
        """Load CSV and normalize data."""
        raw_rows = self.load_raw(csv_path)
        return [self._normalize_row(row) for row in raw_rows]
    
    def _normalize_row(self, row: dict) -> BenchmarkRow:
        """Normalize a single row from CSV."""
        p50 = row.get("latency_p50", "")
        p75 = row.get("latency_p75", "")
        p90 = row.get("latency_p90", "")
        p99 = row.get("latency_p99", "")
        
        # Convert timestamp to UTC+8 format
        timestamp_str = row["timestamp"]
        try:
            if timestamp_str.endswith("Z"):
                dt_utc = datetime.fromisoformat(timestamp_str[:-1] + "+00:00")
            else:
                dt_utc = datetime.fromisoformat(timestamp_str)
            utc_plus_8 = timezone(timedelta(hours=8))
            dt_plus8 = dt_utc.astimezone(utc_plus_8)
            timestamp_display = dt_plus8.strftime("%Y-%m-%d %H:%M:%S")
        except:
            timestamp_display = timestamp_str
        
        return BenchmarkRow(
            timestamp=timestamp_display,
            server=row["server"],
            endpoint=row["endpoint"],
            requests_sec=float(row["requests_sec"]),
            latency_ms=self.latency_parser.parse(row["latency_avg"]),
            latency_p50_ms=self.latency_parser.parse(p50) if p50 else None,
            latency_p75_ms=self.latency_parser.parse(p75) if p75 else None,
            latency_p90_ms=self.latency_parser.parse(p90) if p90 else None,
            latency_p99_ms=self.latency_parser.parse(p99) if p99 else None,
            transfer_kb_sec=self.transfer_parser.parse(row.get("transfer_sec", "0")),
            latency_avg=row["latency_avg"],
            latency_p50=p50,
            latency_p75=p75,
            latency_p90=p90,
            latency_p99=p99,
            transfer_sec=row.get("transfer_sec", "0"),
        )


class CSVFinder:
    """Finds the latest CSV file with benchmark results."""
    
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir
    
    def find_latest(self) -> Optional[Path]:
        """Find and return the latest results.csv file."""
        if not self.results_dir.exists():
            return None
        
        candidates = sorted(
            (p for p in self.results_dir.glob("*/results.csv") if p.is_file()),
            reverse=True
        )
        if not candidates:
            return None
        
        with_percentiles = [p for p in candidates if self._has_percentiles(p)]
        return with_percentiles[0] if with_percentiles else candidates[0]
    
    @staticmethod
    def _has_percentiles(csv_path: Path) -> bool:
        """Check if CSV has percentile columns."""
        try:
            # Try common encodings in order
            encodings = ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1"]
            
            for enc in encodings:
                try:
                    with csv_path.open(newline="", encoding=enc) as f:
                        reader = csv.reader(f)
                        header = next(reader, [])
                    return "latency_p50" in header and "latency_p99" in header
                except (UnicodeDecodeError, LookupError, UnicodeError):
                    continue
            
            return False
        except OSError:
            return False
