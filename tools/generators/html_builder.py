"""HTML and CSS generation for reports."""
from pathlib import Path
from typing import Dict, Any


class CSSGenerator:
    """Generates CSS styles for the report."""
    
    @staticmethod
    def generate() -> str:
        """Generate CSS styles."""
        return """
    :root {
      --bg: #0f1b1e;
      --panel: #13262a;
      --text: #e7f4f2;
      --muted: #a7c8c2;
      --accent: #f2b264;
      --accent2: #6dd3b6;
    }
    body {
      margin: 0;
      font-family: "Noto Serif TC", "Source Han Serif TC", "PMingLiU", serif;
      background: radial-gradient(1200px 800px at 20% -10%, #1f3c3f, transparent), var(--bg);
      color: var(--text);
    }
    body.light-theme {
      --bg: #f5f5f5;
      --panel: #ffffff;
      --text: #1a1a1a;
      --muted: #666666;
      --accent: #f2b264;
      --accent2: #6dd3b6;
      background: radial-gradient(1200px 800px at 20% -10%, #e8f0ef, transparent), var(--bg);
    }
    body.dark-theme {
      --bg: #000000;
      --panel: #0a0a0a;
      --text: #d0d0d0;
      --muted: #888888;
      --accent: #f2b264;
      --accent2: #6dd3b6;
      background: var(--bg);
    }
    header {
      padding: 32px 24px;
      border-bottom: 1px solid rgba(31, 60, 63, 0.5);
      background: var(--panel);
    }
    body.light-theme header {
      background: linear-gradient(120deg, rgba(232, 240, 239, 0.8), var(--bg));
      border-bottom: 1px solid #d0d0d0;
    }
    body.dark-theme header {
      background: var(--bg);
      border-bottom: 1px solid #1a1a1a;
    }
    .header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    h1 {
      margin: 0 0 8px 0;
      font-size: 28px;
      letter-spacing: 0.5px;
      color: var(--text);
    }
    .lang-switch {
      display: flex;
      gap: 8px;
      justify-content: center;
    }
    .header-controls {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }
    .lang-btn {
      border: 1px solid rgba(31, 60, 63, 0.3);
      background: transparent;
      color: var(--muted);
      padding: 6px 10px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 12px;
    }
    body.light-theme .lang-btn {
      border-color: #d0d0d0;
    }
    body.dark-theme .lang-btn {
      border-color: #333333;
    }
    .lang-btn.active {
      border-color: var(--accent);
      color: var(--accent);
    }
    footer {
      background: transparent;
      border-top: 1px solid rgba(31, 60, 63, 0.35);
      padding: 20px 24px 28px 24px;
      margin-top: 40px;
      text-align: center;
    }
    .theme-switch {
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
    }
    .header-theme-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .theme-note {
      text-align: center;
      color: var(--text);
      font-size: 14px;
      font-weight: 500;
      line-height: 1.6;
    }
    .theme-note > div {
      margin: 2px 0;
    }
    .theme-label {
      color: var(--muted);
      font-size: 13px;
      margin-right: 8px;
    }
    .theme-btn {
      border: 2px solid #1f3c3f;
      background: transparent;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
      transition: all 0.3s ease;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0;
    }
    .theme-btn::after {
      content: '●';
      font-size: 9px;
      color: var(--muted);
      opacity: 0;
      transition: all 0.3s ease;
    }
    .theme-btn:hover {
      border-color: var(--muted);
    }
    .theme-btn.active {
      border-color: var(--accent);
    }
    .theme-btn.active::after {
      opacity: 1;
      color: var(--accent);
    }
    .meta {
      color: var(--muted);
      font-size: 14px;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      padding: 24px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--panel);
      border: 1px solid #1f3c3f;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .card h2 {
      margin: 0 0 8px 0;
      font-size: 18px;
      color: var(--accent);
    }
    .metric-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 2px 10px;
      font-size: 11px;
      font-weight: 600;
      line-height: 1.4;
      border: 1px solid transparent;
      letter-spacing: 0.2px;
      white-space: nowrap;
    }
    .metric-high {
      color: #6dd3b6;
      border-color: rgba(109, 211, 182, 0.45);
      background: rgba(109, 211, 182, 0.12);
    }
    .metric-low {
      color: #64b5f6;
      border-color: rgba(100, 181, 246, 0.45);
      background: rgba(100, 181, 246, 0.12);
    }
    .metric-compare {
      color: #f2b264;
      border-color: rgba(242, 178, 100, 0.45);
      background: rgba(242, 178, 100, 0.12);
    }
    .report-view-btn {
      border: 1px solid #1f3c3f;
      background: rgba(109, 211, 182, 0.08);
      color: var(--muted);
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      cursor: pointer;
    }
    .report-view-btn.active {
      color: var(--accent);
      border-color: rgba(109, 211, 182, 0.45);
      background: rgba(109, 211, 182, 0.15);
    }
    .plot {
      height: 320px;
    }
    .desc {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      margin: 8px 0 0 0;
    }
    .formula {
      display: grid;
      gap: 6px;
      margin: 0;
      padding-left: 18px;
    }
    .formula li {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }
    .interpretation {
      display: grid;
      gap: 8px;
      margin: 0;
      padding-left: 18px;
    }
    .interpretation li {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }
    th, td {
      border-bottom: 1px solid #1f3c3f;
      padding: 8px;
      text-align: left;
      position: relative;
    }
    th {
      color: var(--muted);
      font-weight: 600;
    }
    table.table-resizable th,
    table.table-resizable td {
      user-select: none;
    }
    @media (max-width: 900px) {
      table {
        font-size: 13px;
      }
      th, td {
        padding: 6px;
      }
    }
    /* Charts section styling for theme differentiation */
    #charts-section {
      background: linear-gradient(135deg, rgba(31, 60, 63, 0.2), rgba(109, 211, 182, 0.05)) !important;
    }
    body.light-theme #charts-section {
      background: linear-gradient(135deg, rgba(109, 211, 182, 0.1), rgba(109, 211, 182, 0.04)) !important;
    }
    body.dark-theme #charts-section {
      background: linear-gradient(135deg, rgba(31, 60, 63, 0.3), rgba(109, 211, 182, 0.12)) !important;
    }
"""


class HTMLStructureBuilder:
    """Builds HTML structure."""
    
    @staticmethod
    def build_header() -> str:
        """Build header section."""
        return """  <header>
    <div class="header-row">
      <div>
        <h1 data-i18n="title"></h1>
        <div class="meta"><span data-i18n="meta_generated"></span>: <span id="meta-generated"></span></div>
      </div>
      <div class="header-controls">
        <div class="lang-switch">
          <button class="lang-btn" data-lang="zh">中文</button>
          <button class="lang-btn" data-lang="en">EN</button>
        </div>
        <div class="header-theme-wrap">
          <div class="theme-switch">
            <button class="theme-btn" data-theme="light" title="Light Theme"></button>
            <button class="theme-btn" data-theme="default" title="Default/Dark Theme"></button>
            <button class="theme-btn" data-theme="dark" title="Pure Dark Theme"></button>
          </div>
        </div>
      </div>
    </div>
  </header>"""
    
    @staticmethod
    def build_footer() -> str:
        """Build footer section."""
        return """  <footer>
    <div class="theme-note">
      <div data-i18n="provider_name"></div>
      <div data-i18n="provider_contact"></div>
    </div>
  </footer>"""
    
    @staticmethod
    def build_head(css: str = "") -> str:
        """Build HTML head section."""
        head_start = """<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PHP Benchmark Report</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
  <style>
{css}
  </style>
</head>"""
        return head_start.format(css=css)
