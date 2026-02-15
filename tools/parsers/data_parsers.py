"""Parsers for various data formats."""


class LatencyParser:
    """Parses latency values in different units (us, ms, s)."""
    
    @staticmethod
    def parse(value: str) -> float:
        """Parse latency string to milliseconds."""
        if value.endswith("us"):
            return float(value[:-2]) / 1000.0
        if value.endswith("ms"):
            return float(value[:-2])
        if value.endswith("s"):
            return float(value[:-1]) * 1000.0
        return float(value)


class TransferParser:
    """Parses transfer rate values in different units (B, KB, MB)."""
    
    @staticmethod
    def parse(value: str) -> float:
        """Parse transfer rate string to KB/sec."""
        if value.endswith("MB"):
            return float(value[:-2]) * 1024.0
        if value.endswith("KB"):
            return float(value[:-2])
        if value.endswith("B"):
            return float(value[:-1]) / 1024.0
        return float(value)
