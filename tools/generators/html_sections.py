"""HTML content builders for different report sections."""
from typing import List, Dict, Any

from models.benchmark import BenchmarkRow, Insight
from processors.data_processor import format_endpoint_label


class SummarySection:
    """Builds the benchmark configuration summary section."""
    
    @staticmethod
    def build(config: Dict[str, Any]) -> str:
        """Build summary section HTML."""
        duration = config.get("duration", "N/A")
        connections = config.get("connections", "N/A")
        endpoint_params = config.get("endpoint_params", {})
        
        cpu_iter = endpoint_params.get("cpu", {}).get("iterations", "N/A")
        json_items = endpoint_params.get("json", {}).get("items", "N/A")
        io_size = endpoint_params.get("io", {}).get("size", "N/A")
        io_iter = endpoint_params.get("io", {}).get("iterations", "N/A")
        io_mode = endpoint_params.get("io", {}).get("mode", "N/A")
        
        return f"""    <div class="card" style="margin-bottom: 16px; background: rgba(109, 211, 182, 0.1); border-color: rgba(109, 211, 182, 0.3);">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="summary_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <p class="desc" data-i18n="summary_intro"></p>
        <div style="margin-top: 16px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 16px;">
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_duration"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{duration}</strong></div>
            <div style="font-size: 11px; color: var(--muted); margin-top: 3px;" data-i18n="summary_duration_unit"></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_connections"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{connections}</strong></div>
            <div style="font-size: 11px; color: var(--muted); margin-top: 3px;" data-i18n="summary_connections_unit"></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_cpu_iter"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{cpu_iter}</strong></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_json_items"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{json_items}</strong></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_io_size"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{io_size}</strong></div>
            <div style="font-size: 11px; color: var(--muted); margin-top: 3px;" data-i18n="summary_io_size_unit"></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_io_iter"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{io_iter}</strong></div>
          </div>
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_io_mode"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{io_mode}</strong></div>
          </div>
        </div>
      </div>
    </div>"""


class EndpointsSection:
    """Builds the endpoints explanation section."""
    
    @staticmethod
    def build() -> str:
        """Build endpoints section HTML."""
        return """    <div class="card" style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="endpoints_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <p class="desc" data-i18n="endpoints_intro"></p>
        <div style="margin-top: 16px; display: grid; gap: 12px;">
          <div style="border-left: 4px solid #f2b264; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;">
            <h3 style="margin: 0 0 6px 0; font-size: 14px; color: #f2b264;" data-i18n="endpoint_cpu_title"></h3>
            <p style="margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;" data-i18n="endpoint_cpu_desc"></p>
          </div>
          <div style="border-left: 4px solid #6dd3b6; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;">
            <h3 style="margin: 0 0 6px 0; font-size: 14px; color: #6dd3b6;" data-i18n="endpoint_io_title"></h3>
            <p style="margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;" data-i18n="endpoint_io_desc"></p>
          </div>
          <div style="border-left: 4px solid #a7c8c2; padding-left: 12px; padding-top: 8px; padding-bottom: 8px;">
            <h3 style="margin: 0 0 6px 0; font-size: 14px; color: #a7c8c2;" data-i18n="endpoint_json_title"></h3>
            <p style="margin: 0; font-size: 13px; color: var(--muted); line-height: 1.6;" data-i18n="endpoint_json_desc"></p>
          </div>
        </div>
      </div>
    </div>"""


class FormulasSection:
    """Builds the formulas section."""
    
    @staticmethod
    def build() -> str:
        """Build formulas section HTML."""
        return """    <div class="card" style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="formulas_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <ul class="formula">
          <li data-i18n="formula_throughput"></li>
          <li data-i18n="formula_percentile"></li>
          <li data-i18n="formula_delta"></li>
        </ul>
      </div>
    </div>"""


class ChartsGridSection:
    """Builds the charts grid section."""
    
    @staticmethod
    def build() -> str:
        """Build charts grid HTML."""
        return """    <div class="grid">
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_requests" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_requests" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-req" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_latency" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_latency" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-lat" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_transfer" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_transfer" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-xfer" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_pctl" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_pctl" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-pctl" class="plot"></div>
          <p class="desc" id="pctl-note" style="margin-top: 8px; margin-bottom: 0;"></p>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_dist" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_dist" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-hist" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <h2 data-i18n="chart_delta" style="margin: 0;"></h2>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_delta" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-delta" class="plot"></div>
        </div>
      </div>
    </div>"""


class InsightsTable:
    """Builds the insights table."""
    
    @staticmethod
    def build(insights: List[Dict[str, Any]]) -> str:
        """Build insights table HTML."""
        rows = "".join([
            f'<tr><td>{format_endpoint_label(i["endpoint"])}</td><td>{i["req_winner"]}</td><td>{i["req_delta"]:.1f}</td><td>{i["lat_winner"]}</td><td>{i["lat_delta"]:.1f}</td></tr>'
            for i in insights
        ])
        
        return f"""    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="insights_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <table>
          <thead>
            <tr>
              <th data-i18n="th_endpoint"></th>
              <th data-i18n="th_winner_throughput"></th>
              <th data-i18n="th_delta"></th>
              <th data-i18n="th_winner_latency"></th>
              <th data-i18n="th_latency_delta"></th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </div>"""


class InterpretationSection:
    """Builds the interpretation section."""
    
    @staticmethod
    def build() -> str:
        """Build interpretation section HTML."""
        return """    <div class="card" style="margin-top: 16px; background: rgba(242, 178, 100, 0.15); border-color: rgba(242, 178, 100, 0.3);">
      <p style="color: var(--accent); margin: 0; line-height: 1.6;"><strong data-i18n="interp_intro"></strong></p>
    </div>

    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="interpretation_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <ul class="interpretation" id="interpretation-list"></ul>
      </div>
    </div>"""


class RawResultsSection:
    """Builds the raw results section."""
    
    @staticmethod
    def build(rows: List[BenchmarkRow]) -> str:
        """Build raw results section HTML."""
        xampp_rows = "".join([
            f'<tr><td>{format_endpoint_label(r.endpoint)}</td><td>{r.requests_sec:.2f}</td><td>{r.latency_avg}</td><td>{r.latency_p50}</td><td>{r.latency_p90}</td><td>{r.latency_p99}</td><td>{r.transfer_sec}</td></tr>'
            for r in rows if r.server == 'xampp'
        ])
        
        nginx_multi_rows = "".join([
            f'<tr><td>{format_endpoint_label(r.endpoint)}</td><td>{r.requests_sec:.2f}</td><td>{r.latency_avg}</td><td>{r.latency_p50}</td><td>{r.latency_p90}</td><td>{r.latency_p99}</td><td>{r.transfer_sec}</td></tr>'
            for r in rows if r.server == 'nginx_multi'
        ])
        
        return f"""    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="raw_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      
      <div class="card-content">
        <div style="margin-bottom: 24px;">
          <h3 style="margin: 0 0 12px 0; font-size: 16px; color: #f2b264;">XAMPP</h3>
          <table>
            <thead>
              <tr>
                <th data-i18n="th_endpoint"></th>
                <th data-i18n="th_req"></th>
                <th data-i18n="th_latency"></th>
                <th data-i18n="th_p50"></th>
                <th data-i18n="th_p90"></th>
                <th data-i18n="th_p99"></th>
                <th data-i18n="th_transfer"></th>
              </tr>
            </thead>
            <tbody>
              {xampp_rows}
            </tbody>
          </table>
        </div>

        <div style="margin-top: 24px;">
          <h3 style="margin: 0 0 12px 0; font-size: 16px; color: #64b5f6;">NGINX (Multi-core)</h3>
          <table>
            <thead>
              <tr>
                <th data-i18n="th_endpoint"></th>
                <th data-i18n="th_req"></th>
                <th data-i18n="th_latency"></th>
                <th data-i18n="th_p50"></th>
                <th data-i18n="th_p90"></th>
                <th data-i18n="th_p99"></th>
                <th data-i18n="th_transfer"></th>
              </tr>
            </thead>
            <tbody>
              {nginx_multi_rows}
            </tbody>
          </table>
        </div>
      </div>
    </div>"""
