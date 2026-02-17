"""HTML content builders for different report sections."""
from typing import List, Dict, Any

from models.benchmark import BenchmarkRow, Insight
from processors.data_processor import format_endpoint_label
from utils.duration_formatter import format_duration_display


class ParametersSection:
    """Builds benchmark parameters section with configured values."""
    
    @staticmethod
    def build(config: Dict[str, Any]) -> str:
        """Build parameters section HTML."""
        duration = format_duration_display(config.get("duration", 0))
        connections = config.get("connections", "N/A")
        endpoint_params = config.get("endpoint_params", {})
        
        cpu_iter = endpoint_params.get("cpu", {}).get("iterations", "N/A")
        json_items = endpoint_params.get("json", {}).get("items", "N/A")
        io_size = endpoint_params.get("io", {}).get("size", "N/A")
        io_iter = endpoint_params.get("io", {}).get("iterations", "N/A")
        io_mode = endpoint_params.get("io", {}).get("mode", "N/A")
        
        return f"""    <div class="card" style="margin-bottom: 16px; background: rgba(109, 211, 182, 0.1); border-color: rgba(109, 211, 182, 0.3);">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="params_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <div style="margin-top: 16px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 16px;">
          <div style="text-align: center;">
            <div style="font-weight: 500; color: var(--muted); font-size: 12px; margin-bottom: 6px;" data-i18n="summary_duration"></div>
            <div style="font-size: 18px; font-weight: bold; color: var(--text);"><strong>{duration}</strong></div>
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
        <table style="margin-top: 12px; width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
              <th style="padding: 10px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 16%;" data-i18n="summary_rationale_param"></th>
              <th style="padding: 10px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 28%;" data-i18n="summary_rationale_why"></th>
              <th style="padding: 10px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 36%;" data-i18n="summary_rationale_meaning"></th>
              <th style="padding: 10px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1); width: 20%;" data-i18n="summary_rationale_goal"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 10px; color: var(--text); font-weight: 600;" data-i18n="summary_duration"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_duration_why"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_duration_meaning"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_duration_goal"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 10px; color: var(--text); font-weight: 600;" data-i18n="summary_connections"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_connections_why"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_connections_meaning"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_connections_goal"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 10px; color: var(--text); font-weight: 600;" data-i18n="summary_endpoints"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_endpoint_why"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_endpoint_meaning"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_endpoint_goal"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 10px; color: var(--text); font-weight: 600;" data-i18n="summary_payload_group"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_payload_why"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_payload_meaning"></td>
              <td style="padding: 10px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="summary_rationale_payload_goal"></td>
            </tr>
          </tbody>
        </table>
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
        <table style="margin-top: 16px; width: 100%; border-collapse: collapse; table-layout: fixed;">
          <colgroup>
            <col style="width: 10%;">
            <col style="width: 15%;">
            <col style="width: 15%;">
            <col style="width: 20%;">
            <col style="width: 40%;">
          </colgroup>
          <thead>
            <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="endpoint_name"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="endpoint_workload"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="endpoint_use_case"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="endpoint_method"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="endpoint_description"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #f2b264; font-weight: 600;" data-i18n="endpoint_cpu_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_cpu_workload"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_cpu_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_cpu_method"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_cpu_desc"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #6dd3b6; font-weight: 600;" data-i18n="endpoint_json_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_json_workload"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_json_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_json_method"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_json_desc"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: #a7c8c2; font-weight: 600;" data-i18n="endpoint_io_title"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px;" data-i18n="endpoint_io_workload"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_io_usecase"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_io_method"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5; overflow-wrap: anywhere; word-break: break-word;" data-i18n="endpoint_io_desc"></td>
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
      <div class="charts-grid-content">
        <div class="grid">
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_requests" style="margin: 0;"></h2>
            <span class="metric-chip metric-high" data-i18n="metric_high"></span>
          </div>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_requests" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-req" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_latency" style="margin: 0;"></h2>
            <span class="metric-chip metric-low" data-i18n="metric_low"></span>
          </div>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_latency" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-lat" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_transfer" style="margin: 0;"></h2>
            <span class="metric-chip metric-high" data-i18n="metric_high"></span>
          </div>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_transfer" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-xfer" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_pctl" style="margin: 0;"></h2>
            <span class="metric-chip metric-low" data-i18n="metric_low"></span>
          </div>
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
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_dist" style="margin: 0;"></h2>
            <span class="metric-chip metric-compare" data-i18n="metric_compare"></span>
          </div>
          <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
        </div>
        <p class="desc" data-i18n="desc_dist" style="margin-bottom: 12px; margin-top: 0;"></p>
        <div class="card-content">
          <div id="chart-hist" class="plot"></div>
        </div>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <h2 data-i18n="chart_delta" style="margin: 0;"></h2>
            <span class="metric-chip metric-compare" data-i18n="metric_compare"></span>
          </div>
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


class BenchmarkReportSection:
    """Builds consolidated benchmark report section from insights and endpoint analysis."""

    @staticmethod
    def build(insights: List[Dict[str, Any]]) -> str:
        """Build consolidated benchmark report section HTML."""

        def format_server_name(name: str) -> str:
            if "xampp" in name.lower():
                return "XAMPP"
            if "nginx" in name.lower():
                return "NGINX"
            return name.upper()

        def bilingual_inline(zh_text: str, en_text: str) -> str:
          return (
            f'<span class="lang-zh">{zh_text}</span>'
            f'<span class="lang-en" style="display:none;">{en_text}</span>'
          )

        throughput_xampp = 0
        throughput_nginx = 0
        latency_xampp = 0
        latency_nginx = 0
        req_deltas = []
        lat_deltas = []

        scenario_map_zh = {
          "CPU": "Laravel Queue / 批次工作（排程、匯整、背景任務）",
          "JSON": "Laravel API / 控制器回應（即時 API 與前後端互動）",
          "I/O": "Laravel DB + Storage（查詢、檔案存取、快取互動）",
        }
        scenario_map_en = {
          "CPU": "Laravel Queue / Batch Jobs (scheduler, aggregation, background tasks)",
          "JSON": "Laravel API / Controller Responses (real-time API and frontend interaction)",
          "I/O": "Laravel DB + Storage (queries, file access, cache interactions)",
        }

        endpoint_profiles_zh = {
          "CPU": {
            "business": {
              "same_diff": "{winner} 在 CPU 端點同時取得吞吐 {req_chip} 與延遲 {lat_chip} 優勢，代表在計算型工作負載具一致效益。",
              "split_diff": "CPU 端點有明顯取捨：{req_winner} 吞吐較高 {req_chip}、{lat_winner} 延遲較低 {lat_chip}，需依工作型態分流。",
              "same_deploy": "批次報表、排程匯整、背景運算優先部署於 {winner}，可在單一平台放大 CPU 成本效益。",
              "split_deploy": "長批次與高併發計算流量走 {req_winner}；需要即時回應的同步流程走 {lat_winner}。",
            },
            "sre": {
              "same_diff": "{winner} 在 CPU 端點雙指標同向領先（吞吐 {req_chip} / 延遲 {lat_chip}），顯示 PHP worker 調度、Opcode 命中與執行器排程更穩定。",
              "split_diff": "CPU 路徑分裂：{req_winner} 在 worker 併發吞吐領先 {req_chip}，{lat_winner} 在短請求路徑延遲領先 {lat_chip}，反映執行佇列與排程策略差異。",
              "same_deploy": "Queue/Horizon/排程 Worker 佈署在 {winner}，並優先調整 process manager、worker 數與 max execution time。",
              "split_deploy": "將 batch worker pool 固定於 {req_winner}，interactive sync route 置於 {lat_winner}，分別調整 worker class 與 timeout profile。",
            },
          },
          "JSON": {
            "business": {
              "same_diff": "{winner} 在 JSON 端點同向領先（吞吐 {req_chip}、延遲 {lat_chip}），對 API 服務可同時提升容量與體感速度。",
              "split_diff": "JSON 端點呈雙向優勢：{req_winner} 併發吞吐較強 {req_chip}，{lat_winner} 互動延遲較佳 {lat_chip}。",
              "same_deploy": "API 與前後端資料交換流量優先部署於 {winner}，可同時降低尖峰壓力與等待時間。",
              "split_deploy": "大流量資料輸出、批次 API 走 {req_winner}；登入、交易、互動型 API 走 {lat_winner}。",
            },
            "sre": {
              "same_diff": "{winner} 在 JSON 端點雙指標領先（吞吐 {req_chip} / 延遲 {lat_chip}），顯示序列化鏈路、FastCGI 緩衝與回應 flush path 較佳。",
              "split_diff": "JSON 路徑出現 trade-off：{req_winner} 在 payload throughput 佔優 {req_chip}，{lat_winner} 在 request turnaround 佔優 {lat_chip}。",
              "same_deploy": "將 API gateway/serialization-heavy controller 置於 {winner}，並強化 keep-alive、gzip 與 response buffer 策略。",
              "split_deploy": "bulk payload endpoint 走 {req_winner}，latency-sensitive endpoint 走 {lat_winner}；以 route-based upstream policy 分流。",
            },
          },
          "I/O": {
            "business": {
              "same_diff": "{winner} 在 I/O 端點同時領先（吞吐 {req_chip}、延遲 {lat_chip}），適合資料存取與檔案服務主路徑。",
              "split_diff": "I/O 端點出現取捨：{req_winner} 吞吐較高 {req_chip}、{lat_winner} 延遲較低 {lat_chip}。",
              "same_deploy": "資料查詢、檔案存取、匯入匯出流程優先部署於 {winner}，降低維運複雜度。",
              "split_deploy": "背景同步、批次寫入走 {req_winner}；交易查詢、即時讀取走 {lat_winner}。",
            },
            "sre": {
              "same_diff": "{winner} 在 I/O 端點雙指標同向領先（吞吐 {req_chip} / 延遲 {lat_chip}），顯示 connection reuse、pool 行為與 I/O queue 控管較佳。",
              "split_diff": "I/O 端點分裂：{req_winner} 在 queue depth 吞吐表現領先 {req_chip}，{lat_winner} 在 tail latency 表現領先 {lat_chip}。",
              "same_deploy": "DB/storage-heavy route 佈署於 {winner}，集中調整 connection pool、read/write timeout 與 cache TTL。",
              "split_deploy": "write-heavy 與 background sync upstream 指向 {req_winner}；read-heavy 與 latency-critical upstream 指向 {lat_winner}。",
            },
          },
        }
        endpoint_profiles_en = {
          "CPU": {
            "business": {
              "same_diff": "{winner} leads CPU endpoint in both throughput {req_chip} and latency {lat_chip}, indicating balanced efficiency for compute-heavy workloads.",
              "split_diff": "CPU endpoint shows a trade-off: {req_winner} has higher throughput {req_chip}, while {lat_winner} has lower latency {lat_chip}; route by workload type.",
              "same_deploy": "Deploy batch reports, scheduled aggregation, and background compute flows on {winner} to maximize CPU cost-efficiency.",
              "split_deploy": "Route long-running and high-concurrency compute traffic to {req_winner}; route interactive synchronous paths to {lat_winner}.",
            },
            "sre": {
              "same_diff": "{winner} leads CPU endpoint on both metrics (throughput {req_chip} / latency {lat_chip}), suggesting better worker scheduling and execution-path stability.",
              "split_diff": "CPU path diverges: {req_winner} leads worker throughput {req_chip}, while {lat_winner} leads short-request latency {lat_chip}, reflecting scheduling and queue behavior differences.",
              "same_deploy": "Place Queue/Horizon/scheduled workers on {winner}; tune process manager, worker count, and max execution time there first.",
              "split_deploy": "Pin batch worker pools to {req_winner}; keep interactive sync routes on {lat_winner} with separate timeout/worker profiles.",
            },
          },
          "JSON": {
            "business": {
              "same_diff": "{winner} leads JSON endpoint in both throughput {req_chip} and latency {lat_chip}, improving both API capacity and user responsiveness.",
              "split_diff": "JSON endpoint is split: {req_winner} is stronger on concurrent API throughput {req_chip}, while {lat_winner} is better for interactive latency {lat_chip}.",
              "same_deploy": "Prioritize API and frontend data-exchange traffic on {winner} to reduce peak pressure and response wait time.",
              "split_deploy": "Route bulk output and batch APIs to {req_winner}; route login/checkout/interactive APIs to {lat_winner}.",
            },
            "sre": {
              "same_diff": "{winner} leads JSON endpoint on both dimensions (throughput {req_chip} / latency {lat_chip}), indicating stronger serialization and response flush paths.",
              "split_diff": "JSON path trade-off: {req_winner} wins payload throughput {req_chip}, while {lat_winner} wins request turnaround latency {lat_chip}.",
              "same_deploy": "Place API gateway and serialization-heavy controllers on {winner}; tune keep-alive, gzip, and response buffering accordingly.",
              "split_deploy": "Route bulk-payload endpoints to {req_winner}; latency-sensitive endpoints to {lat_winner} via route-based upstream policy.",
            },
          },
          "I/O": {
            "business": {
              "same_diff": "{winner} leads I/O endpoint in both throughput {req_chip} and latency {lat_chip}, making it suitable for data-access and file-service main paths.",
              "split_diff": "I/O endpoint has a clear trade-off: {req_winner} has higher throughput {req_chip}, while {lat_winner} has lower latency {lat_chip}.",
              "same_deploy": "Prioritize DB query, storage access, and import/export flows on {winner} to reduce operational complexity.",
              "split_deploy": "Route background sync and batch writes to {req_winner}; route transactional queries and real-time reads to {lat_winner}.",
            },
            "sre": {
              "same_diff": "{winner} leads I/O endpoint on both metrics (throughput {req_chip} / latency {lat_chip}), indicating stronger connection reuse and queue handling.",
              "split_diff": "I/O endpoint diverges: {req_winner} leads queue-depth throughput {req_chip}, while {lat_winner} leads latency under contention {lat_chip}.",
              "same_deploy": "Deploy DB/storage-heavy routes on {winner}; centralize connection pool, timeout, and cache TTL tuning.",
              "split_deploy": "Point write-heavy/background-sync upstream to {req_winner}; point read-heavy/latency-critical upstream to {lat_winner}.",
            },
          },
        }
        endpoint_color_map = {
          "CPU": "#f2b264",
          "JSON": "#6dd3b6",
          "I/O": "#a7c8c2",
        }

        def render_percent_chip(percent_value: float, chip_class: str = "metric-high") -> str:
          return f'<span class="metric-chip {chip_class}" style="vertical-align: middle;">{abs(percent_value):.1f}%</span>'

        matrix_rows = ""
        for item in insights:
          endpoint_label = format_endpoint_label(item["endpoint"])
          req_winner = format_server_name(item["req_winner"])
          lat_winner = format_server_name(item["lat_winner"])
          req_delta = item["req_delta"]
          lat_delta = item["lat_delta"]

          req_deltas.append(req_delta)
          lat_deltas.append(lat_delta)

          if req_winner == "XAMPP":
            throughput_xampp += 1
          elif req_winner == "NGINX":
            throughput_nginx += 1

          if lat_winner == "XAMPP":
            latency_xampp += 1
          elif lat_winner == "NGINX":
            latency_nginx += 1

          throughput_compare = bilingual_inline(
              f"{req_winner} 較優 {render_percent_chip(req_delta, 'metric-high')}",
              f"{req_winner} better {render_percent_chip(req_delta, 'metric-high')}"
          )
          latency_compare = bilingual_inline(
              f"{lat_winner} 較優 {render_percent_chip(lat_delta, 'metric-high')}",
              f"{lat_winner} better {render_percent_chip(lat_delta, 'metric-high')}"
          )

          endpoint_profile_zh = endpoint_profiles_zh.get(endpoint_label, endpoint_profiles_zh["JSON"])
          endpoint_profile_en = endpoint_profiles_en.get(endpoint_label, endpoint_profiles_en["JSON"])
          req_chip = render_percent_chip(req_delta, "metric-high")
          lat_chip = render_percent_chip(lat_delta, "metric-high")

          if req_winner == lat_winner:
            business_conclusion_zh = endpoint_profile_zh["business"]["same_diff"].format(
              winner=req_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            business_conclusion_en = endpoint_profile_en["business"]["same_diff"].format(
              winner=req_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            sre_conclusion_zh = endpoint_profile_zh["sre"]["same_diff"].format(
              winner=req_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            sre_conclusion_en = endpoint_profile_en["sre"]["same_diff"].format(
              winner=req_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            business_deploy_zh = endpoint_profile_zh["business"]["same_deploy"].format(winner=req_winner)
            business_deploy_en = endpoint_profile_en["business"]["same_deploy"].format(winner=req_winner)
            sre_deploy_zh = endpoint_profile_zh["sre"]["same_deploy"].format(winner=req_winner)
            sre_deploy_en = endpoint_profile_en["sre"]["same_deploy"].format(winner=req_winner)
          else:
            business_conclusion_zh = endpoint_profile_zh["business"]["split_diff"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            business_conclusion_en = endpoint_profile_en["business"]["split_diff"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            sre_conclusion_zh = endpoint_profile_zh["sre"]["split_diff"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            sre_conclusion_en = endpoint_profile_en["sre"]["split_diff"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
              req_chip=req_chip,
              lat_chip=lat_chip,
            )
            business_deploy_zh = endpoint_profile_zh["business"]["split_deploy"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
            )
            business_deploy_en = endpoint_profile_en["business"]["split_deploy"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
            )
            sre_deploy_zh = endpoint_profile_zh["sre"]["split_deploy"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
            )
            sre_deploy_en = endpoint_profile_en["sre"]["split_deploy"].format(
              req_winner=req_winner,
              lat_winner=lat_winner,
            )

          business_conclusion = bilingual_inline(business_conclusion_zh, business_conclusion_en)
          sre_conclusion = bilingual_inline(sre_conclusion_zh, sre_conclusion_en)
          business_deploy = bilingual_inline(business_deploy_zh, business_deploy_en)
          sre_deploy = bilingual_inline(sre_deploy_zh, sre_deploy_en)

          matrix_rows += (
            f'<tr>'
            f'<td style="padding: 12px; color: {endpoint_color_map.get(endpoint_label, "var(--text)")}; font-weight: 600;">{endpoint_label}</td>'
            f'<td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;">{bilingual_inline(scenario_map_zh.get(endpoint_label, "Laravel 一般工作負載"), scenario_map_en.get(endpoint_label, "General Laravel workload"))}</td>'
            f'<td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;">{throughput_compare}</td>'
            f'<td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;">{latency_compare}</td>'
            f'<td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;">'
            f'<div class="report-view-content report-view-business">{business_conclusion}</div>'
            f'<div class="report-view-content report-view-sre" style="display:none;">{sre_conclusion}</div>'
            f'</td>'
            f'<td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;">'
            f'<div class="report-view-content report-view-business">{business_deploy}</div>'
            f'<div class="report-view-content report-view-sre" style="display:none;">{sre_deploy}</div>'
            f'</td>'
            f'</tr>'
          )

        avg_req_delta = sum(req_deltas) / len(req_deltas) if req_deltas else 0.0
        avg_lat_delta = sum(lat_deltas) / len(lat_deltas) if lat_deltas else 0.0

        if avg_req_delta > 0:
          overall_throughput = bilingual_inline(
            f"XAMPP 平均領先 {render_percent_chip(avg_req_delta, 'metric-high')}",
            f"XAMPP leads on average by {render_percent_chip(avg_req_delta, 'metric-high')}"
          )
        elif avg_req_delta < 0:
          overall_throughput = bilingual_inline(
            f"NGINX 平均領先 {render_percent_chip(avg_req_delta, 'metric-high')}",
            f"NGINX leads on average by {render_percent_chip(avg_req_delta, 'metric-high')}"
          )
        else:
          overall_throughput = bilingual_inline("吞吐表現接近", "Throughput is close")

        if avg_lat_delta > 0:
          overall_latency = bilingual_inline(
            f"NGINX 平均延遲較低 {render_percent_chip(avg_lat_delta, 'metric-high')}",
            f"NGINX has lower average latency by {render_percent_chip(avg_lat_delta, 'metric-high')}"
          )
        elif avg_lat_delta < 0:
          overall_latency = bilingual_inline(
            f"XAMPP 平均延遲較低 {render_percent_chip(avg_lat_delta, 'metric-high')}",
            f"XAMPP has lower average latency by {render_percent_chip(avg_lat_delta, 'metric-high')}"
          )
        else:
          overall_latency = bilingual_inline("延遲表現接近", "Latency is close")

        def render_score_pair(xampp_value: int, nginx_value: int) -> str:
          if xampp_value > nginx_value:
            xampp_chip_class = "metric-chip metric-high"
            nginx_chip_class = "metric-chip metric-low"
          elif xampp_value < nginx_value:
            xampp_chip_class = "metric-chip metric-low"
            nginx_chip_class = "metric-chip metric-high"
          else:
            xampp_chip_class = "metric-chip metric-compare"
            nginx_chip_class = "metric-chip metric-compare"

          return (
            f'XAMPP: <span class="{xampp_chip_class}" style="vertical-align: middle;">{xampp_value}</span> '
            f'/ NGINX: <span class="{nginx_chip_class}" style="vertical-align: middle;">{nginx_value}</span>'
          )

        throughput_score_display = render_score_pair(throughput_xampp, throughput_nginx)
        latency_score_display = render_score_pair(latency_xampp, latency_nginx)

        xampp_score = throughput_xampp + latency_xampp
        nginx_score = throughput_nginx + latency_nginx
        score_gap = abs(nginx_score - xampp_score)
        delta_signal = max(abs(avg_req_delta), abs(avg_lat_delta))

        if score_gap >= 3 or (score_gap >= 2 and delta_signal >= 10):
          confidence_basis_chip_class = "metric-high"
        elif score_gap >= 1 or delta_signal >= 5:
          confidence_basis_chip_class = "metric-compare"
        else:
          confidence_basis_chip_class = "metric-low"

        if xampp_score > nginx_score:
          xampp_score_chip_class = "metric-high"
          nginx_score_chip_class = "metric-low"
        elif xampp_score < nginx_score:
          xampp_score_chip_class = "metric-low"
          nginx_score_chip_class = "metric-high"
        else:
          xampp_score_chip_class = "metric-compare"
          nginx_score_chip_class = "metric-compare"

        xampp_score_display = f'<span class="metric-chip {xampp_score_chip_class}" style="vertical-align: middle;">{xampp_score}</span>'
        nginx_score_display = f'<span class="metric-chip {nginx_score_chip_class}" style="vertical-align: middle;">{nginx_score}</span>'
        score_gap_display = f'<span class="metric-chip {confidence_basis_chip_class}" style="vertical-align: middle;">{score_gap}</span>'
        confidence_signal_display = render_percent_chip(delta_signal, confidence_basis_chip_class)

        if nginx_score > xampp_score:
          final_recommend_business = bilingual_inline(
            "建議優先採用 NGINX 作為 Laravel 生產環境，XAMPP 保留於開發與相容驗證。",
            "Prioritize NGINX for Laravel production; keep XAMPP for development and compatibility checks."
          )
          final_recommend_sre = bilingual_inline(
            f"建議生產流量主路徑使用 NGINX（總分 {nginx_score_display} 對 {xampp_score_display}），XAMPP 保留在開發/回歸驗證節點。",
            f"Use NGINX as the primary production path (total score {nginx_score_display} vs {xampp_score_display}); keep XAMPP for dev/regression nodes."
          )
        elif xampp_score > nginx_score:
          final_recommend_business = bilingual_inline(
            "目前數據偏向 XAMPP，但建議先以 NGINX 進行長時壓測再定案。",
            "Current data favors XAMPP, but run long-duration validation on NGINX before finalizing."
          )
          final_recommend_sre = bilingual_inline(
            f"目前 XAMPP 總分領先（{xampp_score_display} 對 {nginx_score_display}），但建議補做長時與尖峰壓測，確認 NGINX 調校後再決策。",
            f"XAMPP currently leads by total score ({xampp_score_display} vs {nginx_score_display}); add long-run and peak tests before deciding after NGINX tuning."
          )
        else:
          final_recommend_business = bilingual_inline(
            "兩者各有優勢，建議依端點特性分流部署並持續監測。",
            "Both have strengths; route traffic by endpoint characteristics and keep continuous monitoring."
          )
          final_recommend_sre = bilingual_inline(
            f"總分持平（XAMPP {xampp_score_display} / NGINX {nginx_score_display}），建議採 route-based upstream 分流並以 APM 持續觀測 tail latency。",
            f"Total score is tied (XAMPP {xampp_score_display} / NGINX {nginx_score_display}); use route-based upstream split and monitor tail latency with APM."
          )

        return f"""    <div class="card" style="margin-top: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
        <h2 data-i18n="benchmark_report_title" style="margin: 0;"></h2>
        <button class="collapse-btn" onclick="this.parentElement.parentElement.querySelector('.card-content').style.display = this.parentElement.parentElement.querySelector('.card-content').style.display === 'none' ? 'block' : 'none'; this.textContent = this.textContent === '▼' ? '▶' : '▼';" style="background: none; border: none; color: var(--muted); cursor: pointer; font-size: 12px; padding: 4px 8px;">▼</button>
      </div>
      <div class="card-content">
        <p class="desc" data-i18n="benchmark_report_intro" style="margin: 8px 0 20px 0;"></p>

        <h3 style="margin: 6px 0 12px 0; color: var(--accent);" data-i18n="report_overall_title"></h3>
        <table style="margin-top: 12px; margin-bottom: 18px; width: 100%; border-collapse: collapse; table-layout: fixed;">
          <colgroup>
            <col style="width: 25%;">
            <col style="width: 25%;">
            <col style="width: 25%;">
            <col style="width: 25%;">
          </colgroup>
          <thead>
            <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_overall_win_throughput"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_overall_win_latency"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_overall_avg_throughput"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_overall_avg_latency"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{throughput_score_display}</td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{latency_score_display}</td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{overall_throughput}</td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{overall_latency}</td>
            </tr>
          </tbody>
        </table>

        <div style="display: flex; justify-content: flex-end; gap: 8px; margin: 4px 0 10px 0;">
          <button class="report-view-btn active" data-report-view="business" data-i18n="report_view_business"></button>
          <button class="report-view-btn" data-report-view="sre" data-i18n="report_view_sre"></button>
        </div>

        <table style="margin-top: 12px; width: 100%; border-collapse: collapse; table-layout: fixed;">
          <colgroup>
            <col style="width: 8%;">
            <col style="width: 20%;">
            <col style="width: 12%;">
            <col style="width: 12%;">
            <col style="width: 22%;">
            <col style="width: 26%;">
          </colgroup>
          <thead>
            <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="th_endpoint"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_col_scenario"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_analysis"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_compare"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_key_diff"></th>
              <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_deploy"></th>
            </tr>
          </thead>
          <tbody>
            {matrix_rows}
          </tbody>
        </table>

        <div style="margin-top: 16px; padding: 12px 14px; background: rgba(109, 211, 182, 0.1); border: 1px solid rgba(109, 211, 182, 0.3); border-radius: 8px;">
          <p style="color: var(--muted); margin: 0 0 10px 0; line-height: 1.6;"><strong style="color: var(--accent);" data-i18n="report_confidence_basis"></strong></p>
          <table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
            <colgroup>
              <col style="width: 25%;">
              <col style="width: 25%;">
              <col style="width: 25%;">
              <col style="width: 25%;">
            </colgroup>
            <thead>
              <tr style="background-color: rgba(109, 211, 182, 0.1); border-bottom: 2px solid rgba(109, 211, 182, 0.3);">
                <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_compare_gap"></th>
                <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_compare_xampp_score"></th>
                <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_compare_nginx_score"></th>
                <th style="padding: 12px; text-align: left; font-weight: 600; color: rgba(109, 211, 182, 1);" data-i18n="report_compare_signal"></th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid rgba(109, 211, 182, 0.15);">
                <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{score_gap_display}</td>
                <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{xampp_score_display}</td>
                <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{nginx_score_display}</td>
                <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.6; vertical-align: top;">{confidence_signal_display}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div style="margin-top: 12px; padding: 12px 14px; background: rgba(109, 211, 182, 0.1); border: 1px solid rgba(109, 211, 182, 0.3); border-radius: 8px;">
          <p style="color: var(--muted); margin: 0; line-height: 1.6;"><strong style="color: var(--accent);" data-i18n="report_overall_final"></strong>：
            <span class="report-view-content report-view-business">{final_recommend_business}</span>
            <span class="report-view-content report-view-sre" style="display:none;">{final_recommend_sre}</span>
          </p>
        </div>
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
              <td style="padding: 12px; color: #f2b264; font-weight: 600; font-size: 13px; line-height: 1.5;" data-i18n="interp_throughput"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;"><span class="metric-chip metric-high" data-i18n="metric_high"></span><div style="margin-top: 6px;" data-i18n="interp_throughput_eval"></div></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="interp_throughput_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #6dd3b6; font-weight: 600; font-size: 13px; line-height: 1.5;" data-i18n="interp_latency"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;"><span class="metric-chip metric-low" data-i18n="metric_low"></span><div style="margin-top: 6px;" data-i18n="interp_latency_eval"></div></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="interp_latency_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #a7c8c2; font-weight: 600; font-size: 13px; line-height: 1.5;" data-i18n="interp_percentile"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;"><span class="metric-chip metric-low" data-i18n="metric_low"></span><div style="margin-top: 6px;" data-i18n="interp_percentile_eval"></div></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="interp_percentile_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #64b5f6; font-weight: 600; font-size: 13px; line-height: 1.5;" data-i18n="interp_transfer"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;"><span class="metric-chip metric-high" data-i18n="metric_high"></span><div style="margin-top: 6px;" data-i18n="interp_transfer_eval"></div></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="interp_transfer_recommend"></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(242, 178, 100, 0.15);">
              <td style="padding: 12px; color: #d7b366; font-weight: 600; font-size: 13px; line-height: 1.5;" data-i18n="interp_consistency"></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;"><span class="metric-chip metric-compare" data-i18n="metric_stable"></span><div style="margin-top: 6px;" data-i18n="interp_consistency_eval"></div></td>
              <td style="padding: 12px; color: var(--muted); font-size: 13px; line-height: 1.5;" data-i18n="interp_consistency_recommend"></td>
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
          <h3 style="margin: 0 0 12px 0; font-size: 16px; color: #64b5f6;">NGINX</h3>
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
