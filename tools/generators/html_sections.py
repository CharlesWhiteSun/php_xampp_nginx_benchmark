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
        """Build endpoints section HTML with table format."""
        return """    <div class="card" style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="endpoints_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <p class="desc" data-i18n="endpoints_intro"></p>
        <table style="margin-top: 16px; width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 15%;" data-i18n="endpoint_name"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 20%;" data-i18n="endpoint_use_case"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 35%;" data-i18n="endpoint_description"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 30%;" data-i18n="endpoint_method"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #f2b264; font-weight: 600;" data-i18n="endpoint_cpu_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_cpu_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_cpu_desc"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_cpu_method"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #6dd3b6; font-weight: 600;" data-i18n="endpoint_json_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_json_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_json_desc"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_json_method"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #a7c8c2; font-weight: 600;" data-i18n="endpoint_io_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_io_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_io_desc"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="endpoint_io_method"></td>
            </tr>
          </tbody>
        </table>
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
        """Build charts grid HTML with professional wrapper."""
        return """    <div id="charts-section" class="card" style="margin-top: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="performance_analysis_section" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.charts-grid-content').style.display = this.parentElement.parentElement.querySelector('.charts-grid-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <p class="desc" data-i18n="desc_performance_analysis" style="margin-bottom: 12px; margin-top: 0;"></p>
      <div class="charts-grid-content">
        <div class="grid">
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
        </div>
      </div>
    </div>"""


class InsightsTable:
    """Builds the insights table."""
    
    @staticmethod
    def build(insights: List[Dict[str, Any]]) -> str:
        """Build insights table HTML."""
        def format_server_name(name: str) -> str:
            """Format server name to uppercase: xampp -> XAMPP, nginx_multi -> NGINX"""
            if "xampp" in name.lower():
                return "XAMPP"
            elif "nginx" in name.lower():
                return "NGINX"
            return name.upper()
        
        rows = "".join([
            f'<tr><td>{format_endpoint_label(i["endpoint"])}</td><td>{format_server_name(i["req_winner"])}</td><td>{i["req_delta"]:.1f}</td><td>{format_server_name(i["lat_winner"])}</td><td>{i["lat_delta"]:.1f}</td></tr>'
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
              <th data-i18n="th_winner_throughput_improved"></th>
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
    """Builds the performance indicators section."""
    
    @staticmethod
    def build() -> str:
        """Build interpretation section HTML with table format."""
        return """    <div class="card" style="margin-top: 16px; background: rgba(242, 178, 100, 0.15); border-color: rgba(242, 178, 100, 0.3);">
      <p style="color: var(--accent); margin: 0; line-height: 1.6;"><strong data-i18n="interp_intro"></strong></p>
    </div>

    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="indicators_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
          <thead>
            <tr style="background-color: rgba(242, 178, 100, 0.1); border-bottom: 2px solid rgba(242, 178, 100, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 25%;" data-i18n="interp_metric"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 25%;" data-i18n="interp_evaluation"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 50%;" data-i18n="interp_recommendations"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #f2b264; font-weight: 600; font-size: 13px;" data-i18n="interp_throughput"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_throughput_eval"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_throughput_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #6dd3b6; font-weight: 600; font-size: 13px;" data-i18n="interp_latency"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_latency_eval"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_latency_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #a7c8c2; font-weight: 600; font-size: 13px;" data-i18n="interp_percentile"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_percentile_eval"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_percentile_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #64b5f6; font-weight: 600; font-size: 13px;" data-i18n="interp_transfer"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_transfer_eval"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_transfer_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #d7b366; font-weight: 600; font-size: 13px;" data-i18n="interp_consistency"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_consistency_eval"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 12px; line-height: 1.5;" data-i18n="interp_consistency_recommend"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>"""


class EndpointAnalysisSection:
    """Builds the endpoint analysis section."""
    
    @staticmethod
    def build() -> str:
        """Build endpoint analysis section HTML."""
        return """    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="endpoint_analysis_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <table id="interpretation-table" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color: rgba(242, 178, 100, 0.1); border-bottom: 2px solid rgba(242, 178, 100, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 15%;" data-i18n="endpoint_name_short"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 30%;" data-i18n="interp_finding"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(242, 178, 100, 1); width: 55%;" data-i18n="interp_detail"></th>
            </tr>
          </thead>
          <tbody id="interpretation-list">
          </tbody>
        </table>
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
        
        return f"""    <div class="card" style="margin-top: 16px; margin-bottom: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="test_values_title" style="margin: 0;"></h2>
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
