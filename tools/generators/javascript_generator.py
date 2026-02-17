"""JavaScript generation for interactive reports."""
import json
from typing import Dict, Any


class JavaScriptGenerator:
    """Generates JavaScript code for the report."""
    
    @staticmethod
    def generate_payload_and_texts(payload: Dict[str, Any], texts: Dict[str, dict]) -> str:
        """Generate JavaScript payload and texts."""
        payload_json = json.dumps(payload, default=str)
        texts_json = json.dumps(texts, default=str)
        return f"""    const payload = {payload_json};
    const TEXTS = {texts_json};"""
    
    @staticmethod
    def generate_chart_code() -> str:
        """Generate Plotly chart initialization code."""
        return """
    // Format numbers with 'k' suffix (thousand) to 1 decimal place
    const kFormatter = (v) => {
      if (v >= 1000) {
        return (v / 1000).toFixed(1) + 'k';
      }
      return v.toFixed(1);
    };

    const reqData = [
      { type: 'bar', name: 'XAMPP', x: payload.charts.requests_sec.labels, y: payload.charts.requests_sec.xampp, marker: { color: '#f2b264' } },
      { type: 'bar', name: 'NGINX', x: payload.charts.requests_sec.labels, y: payload.charts.requests_sec.nginx_multi, marker: { color: '#64b5f6' } },
    ];
    Plotly.newPlot('chart-req', reqData, { barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#e7f4f2' }, xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 } }, yaxis: { tickformat: '.1f', ticksuffix: 'k' }, margin: { b: 80 } });

    const latData = [
      { type: 'bar', name: 'XAMPP', x: payload.charts.latency_ms.labels, y: payload.charts.latency_ms.xampp, marker: { color: '#f2b264' } },
      { type: 'bar', name: 'NGINX', x: payload.charts.latency_ms.labels, y: payload.charts.latency_ms.nginx_multi, marker: { color: '#64b5f6' } },
    ];
    Plotly.newPlot('chart-lat', latData, { barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#e7f4f2' }, xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 } }, yaxis: { tickformat: '.1f', ticksuffix: 'k' }, margin: { b: 80 } });

    const xferData = [
      { type: 'bar', name: 'XAMPP', x: payload.charts.transfer_kb_sec.labels, y: payload.charts.transfer_kb_sec.xampp, marker: { color: '#f2b264' } },
      { type: 'bar', name: 'NGINX', x: payload.charts.transfer_kb_sec.labels, y: payload.charts.transfer_kb_sec.nginx_multi, marker: { color: '#64b5f6' } },
    ];
    Plotly.newPlot('chart-xfer', xferData, { barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#e7f4f2' }, xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 } }, yaxis: { tickformat: '.1f', ticksuffix: 'k' }, margin: { b: 80 } });

    const pctlData = [
      { type: 'bar', name: 'XAMPP p50', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p50, marker: { color: 'rgba(242,178,100,0.65)' } },
      { type: 'bar', name: 'XAMPP p90', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p90, marker: { color: 'rgba(242,178,100,0.85)' } },
      { type: 'bar', name: 'XAMPP p99', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.xampp.p99, marker: { color: 'rgba(242,178,100,1.0)' } },
      { type: 'bar', name: 'NGINX p50', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p50, marker: { color: 'rgba(100,181,246,0.65)' } },
      { type: 'bar', name: 'NGINX p90', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p90, marker: { color: 'rgba(100,181,246,0.85)' } },
      { type: 'bar', name: 'NGINX p99', x: payload.charts.latency_pctl.labels, y: payload.charts.latency_pctl.nginx_multi.p99, marker: { color: 'rgba(100,181,246,1.0)' } },
    ];
    if (payload.has_pctl) {
      Plotly.newPlot('chart-pctl', pctlData, { barmode: 'group', paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { color: '#e7f4f2' }, xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 }, standoff: 10 }, yaxis: { tickformat: '.1f', ticksuffix: 'ms' }, margin: { b: 120, l: 60, r: 40, t: 40 } });
    } else {
      const el = document.getElementById('chart-pctl');
      if (el) {
        el.innerHTML = '<div class="desc">No percentile series available.</div>';
      }
    }

    const histData = [
      {
        type: 'violin',
        name: 'XAMPP',
        y: payload.hist_requests.xampp,
        box: { visible: true },
        meanline: { visible: true },
        fillcolor: 'rgba(242, 178, 100, 0.45)',
        line: { color: '#f2b264' },
      },
      {
        type: 'violin',
        name: 'NGINX',
        y: payload.hist_requests.nginx_multi,
        box: { visible: true },
        meanline: { visible: true },
        fillcolor: 'rgba(100, 181, 246, 0.45)',
        line: { color: '#64b5f6' },
      },
    ];
    Plotly.newPlot('chart-hist', histData, {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: { color: '#e7f4f2' },
      xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 } },
      yaxis: { title: 'Req/sec', tickformat: '.1f', ticksuffix: 'k' },
      margin: { b: 80 }
    });

    const deltaData = [
      {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'XAMPP',
        x: payload.charts.requests_sec.labels,
        y: payload.charts.requests_sec.xampp,
        line: { color: '#f2b264', width: 3 },
        marker: { size: 8 }
      },
      {
        type: 'scatter',
        mode: 'lines+markers',
        name: 'NGINX',
        x: payload.charts.requests_sec.labels,
        y: payload.charts.requests_sec.nginx_multi,
        line: { color: '#64b5f6', width: 3 },
        marker: { size: 8 }
      }
    ];
    Plotly.newPlot('chart-delta', deltaData, {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: { color: '#e7f4f2' },
      xaxis: { tickangle: -45, automargin: true, tickfont: { size: 12 } },
      yaxis: { title: 'Requests/sec', tickformat: '.1f', ticksuffix: 'k' },
      margin: { b: 80 },
      hovermode: 'x unified'
    });"""
    
    @staticmethod
    def generate_interaction_code() -> str:
        """Generate theme and language interaction code."""
        return """
    function updateChartsTheme(fontColor) {
      const chartIds = ['chart-req', 'chart-lat', 'chart-xfer', 'chart-pctl', 'chart-hist', 'chart-delta'];
      const layoutUpdate = {
        font: { color: fontColor },
        xaxis: { tickfont: { color: fontColor }, titlefont: { color: fontColor } },
        yaxis: { tickfont: { color: fontColor }, titlefont: { color: fontColor } }
      };
      chartIds.forEach(id => {
        const elem = document.getElementById(id);
        if (elem && elem.data && elem.data.length > 0) {
          Plotly.relayout(id, layoutUpdate);
        }
      });
    }

    function wrapResponsiveTables() {
      document.querySelectorAll('table').forEach((table) => {
        if (table.closest('td, th')) {
          return;
        }

        table.classList.add('table-resizable');
      });
    }

    function setColumnWidth(table, index, widthPx) {
      const cols = table.querySelectorAll('colgroup col');
      if (cols[index]) {
        cols[index].style.width = widthPx + 'px';
      }

      table.querySelectorAll('tr').forEach((row) => {
        if (row.children[index]) {
          row.children[index].style.width = widthPx + 'px';
          row.children[index].style.minWidth = widthPx + 'px';
        }
      });
    }

    function enableTableResize(table) {
      if (table.dataset.resizeReady === '1') {
        return;
      }
      table.dataset.resizeReady = '1';

      const edgeThreshold = 6;
      const minColWidth = 72;
      const minRowHeight = 28;
      let active = null;

      const getCell = (event) => event.target.closest('th,td');

      const detectEdge = (cell, event) => {
        if (!cell) {
          return null;
        }
        const rect = cell.getBoundingClientRect();
        const nearRight = Math.abs(rect.right - event.clientX) <= edgeThreshold;
        const nearBottom = Math.abs(rect.bottom - event.clientY) <= edgeThreshold;
        if (nearRight) {
          return 'col';
        }
        if (nearBottom) {
          return 'row';
        }
        return null;
      };

      table.addEventListener('mousemove', (event) => {
        if (active) {
          return;
        }
        const cell = getCell(event);
        const edge = detectEdge(cell, event);
        if (edge === 'col') {
          table.style.cursor = 'col-resize';
        } else if (edge === 'row') {
          table.style.cursor = 'row-resize';
        } else {
          table.style.cursor = '';
        }
      });

      table.addEventListener('mouseleave', () => {
        if (!active) {
          table.style.cursor = '';
        }
      });

      table.addEventListener('mousedown', (event) => {
        if (event.button !== 0) {
          return;
        }

        const cell = getCell(event);
        if (!cell) {
          return;
        }

        const edge = detectEdge(cell, event);
        if (!edge) {
          return;
        }

        if (edge === 'col') {
          active = {
            mode: 'col',
            table,
            colIndex: cell.cellIndex,
            startX: event.clientX,
            startWidth: cell.getBoundingClientRect().width,
          };
        } else {
          const row = cell.parentElement;
          active = {
            mode: 'row',
            row,
            startY: event.clientY,
            startHeight: row.getBoundingClientRect().height,
          };
        }

        event.preventDefault();
      });

      document.addEventListener('mousemove', (event) => {
        if (!active) {
          return;
        }

        if (active.mode === 'col') {
          const deltaX = event.clientX - active.startX;
          const nextWidth = Math.max(minColWidth, Math.round(active.startWidth + deltaX));
          setColumnWidth(active.table, active.colIndex, nextWidth);
        } else if (active.mode === 'row') {
          const deltaY = event.clientY - active.startY;
          const nextHeight = Math.max(minRowHeight, Math.round(active.startHeight + deltaY));
          active.row.style.height = nextHeight + 'px';
          active.row.querySelectorAll('th,td').forEach((cell) => {
            cell.style.height = nextHeight + 'px';
          });
        }

        event.preventDefault();
      });

      document.addEventListener('mouseup', () => {
        active = null;
        table.style.cursor = '';
      });
    }

    function initializeTables() {
      wrapResponsiveTables();
      document.querySelectorAll('table.table-resizable').forEach((table) => {
        enableTableResize(table);
      });
    }

    function applyTheme(theme) {
      document.body.classList.remove('light-theme', 'dark-theme');
      let fontColor = '#e7f4f2';
      
      if (theme === 'light') {
        document.body.classList.add('light-theme');
        fontColor = '#1a1a1a';
      } else if (theme === 'dark') {
        document.body.classList.add('dark-theme');
        fontColor = '#d0d0d0';
      }
      
      updateChartsTheme(fontColor);
      window.localStorage.setItem('report_theme', theme);
      document.querySelectorAll('.theme-btn').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.theme === theme);
      });
    }

    function applyLang(lang) {
      const t = TEXTS[lang];
      document.documentElement.lang = t.lang;
      document.querySelectorAll('[data-i18n]').forEach((el) => {
        const key = el.dataset.i18n;
        if (t[key]) {
          el.innerHTML = t[key];
        }
      });
      document.getElementById('meta-generated').textContent = payload.meta.generated_at;

      const note = document.getElementById('pctl-note');
      if (payload.has_pctl) {
        note.textContent = '';
        note.style.display = 'none';
      } else {
        note.textContent = t.pctl_missing;
        note.style.display = 'block';
      }

      document.querySelectorAll('.lang-btn').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
      });

      document.querySelectorAll('.lang-zh').forEach((el) => {
        el.style.display = (lang === 'zh') ? '' : 'none';
      });
      document.querySelectorAll('.lang-en').forEach((el) => {
        el.style.display = (lang === 'en') ? '' : 'none';
      });

      if (window.renderMathInElement) {
        renderMathInElement(document.body, {
          delimiters: [
            { left: '$', right: '$', display: false },
            { left: '$$', right: '$$', display: true },
          ],
        });
      }

      initializeTables();
    }

    function applyReportView(view) {
      const nextView = (view === 'sre') ? 'sre' : 'business';
      document.querySelectorAll('.report-view-btn').forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.reportView === nextView);
      });

      document.querySelectorAll('.report-view-content').forEach((el) => {
        const isBusiness = el.classList.contains('report-view-business');
        const isSre = el.classList.contains('report-view-sre');

        if ((nextView === 'business' && isBusiness) || (nextView === 'sre' && isSre)) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });

      window.localStorage.setItem('report_view', nextView);
    }

    window.addEventListener('load', () => {
      const saved = window.localStorage.getItem('report_lang') || 'en';
      applyLang(saved);
      document.querySelectorAll('.lang-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          window.localStorage.setItem('report_lang', btn.dataset.lang);
          applyLang(btn.dataset.lang);
        });
      });
      
      const savedTheme = window.localStorage.getItem('report_theme') || 'default';
      applyTheme(savedTheme);
      document.querySelectorAll('.theme-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          applyTheme(btn.dataset.theme);
        });
      });

      applyReportView('business');
      document.querySelectorAll('.report-view-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          applyReportView(btn.dataset.reportView);
        });
      });
    });"""
