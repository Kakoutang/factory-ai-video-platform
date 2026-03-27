const inlineGlobalStyles = `
:root {
  --surface: #f7f9fc;
  --surface-container-lowest: #ffffff;
  --surface-container-low: #f0f4f8;
  --surface-container-high: #e1e9f0;
  --surface-container-highest: #d9e4ec;
  --surface-container: #e8eff4;
  --text: #29343a;
  --muted: #566168;
  --outline: #717c84;
  --outline-variant: #a8b3bb;
  --primary: #415e94;
  --primary-dim: #345287;
  --primary-container: #d8e2ff;
  --secondary-container: #d1e4ff;
  --tertiary-container: #d9d7f8;
  --inverse-surface: #0b0f11;
  --inverse-on-surface: #f7f9fc;
  --error: #9f403d;
  --shadow: 0 12px 32px rgba(41, 52, 58, 0.06);
}

* {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
  min-height: 100%;
}

body {
  background: var(--surface);
  color: var(--text);
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
select,
textarea {
  font: inherit;
}

.material-symbols-outlined {
  font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24;
  vertical-align: middle;
}

.shell-root {
  min-height: 100vh;
  background: var(--surface);
}

.shell-sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 256px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  background: #f8fafc;
  border-right: 1px solid rgba(217, 226, 234, 0.55);
  z-index: 40;
}

.shell-brand-block {
  margin-bottom: 32px;
  padding: 0 8px;
}

.shell-brand {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #111827;
}

.shell-brand-subtitle {
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--muted);
}

.shell-nav {
  display: grid;
  gap: 6px;
  flex: 1;
}

.shell-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 12px;
  border-radius: 10px;
  color: #67768b;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.shell-nav-item:hover {
  background: #e7edf4;
  color: var(--text);
}

.shell-nav-item.active {
  background: var(--surface-container-lowest);
  color: #2457b2;
  box-shadow: 0 4px 16px rgba(65, 94, 148, 0.08);
}

.shell-nav-icon {
  font-size: 20px;
}

.shell-sidebar-cta-wrap {
  padding: 14px 8px 22px;
}

.shell-sidebar-cta {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 8px;
  padding: 13px 16px;
  background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dim) 100%);
  color: #f7f7ff;
  font-size: 15px;
  font-weight: 700;
  box-shadow: 0 10px 24px rgba(65, 94, 148, 0.18);
  cursor: pointer;
}

.shell-sidebar-footer {
  display: grid;
  gap: 6px;
  padding: 0 8px;
}

.shell-sidebar-link {
  display: flex;
  align-items: center;
  gap: 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #67768b;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
}

.shell-sidebar-link:hover {
  background: #e7edf4;
  color: var(--text);
}

.shell-main {
  margin-left: 256px;
  min-height: 100vh;
}

.shell-topbar {
  position: fixed;
  top: 0;
  right: 0;
  width: calc(100% - 256px);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 32px;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(217, 226, 234, 0.5);
  z-index: 30;
}

.shell-topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.shell-topbar-title {
  font-size: 14px;
  font-weight: 700;
  color: #1f2933;
  white-space: nowrap;
}

.shell-topbar-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 4px;
  background: var(--secondary-container);
  color: #455d79;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.shell-topbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.shell-search {
  position: relative;
  display: flex;
  align-items: center;
}

.shell-search-icon {
  position: absolute;
  left: 12px;
  color: #94a3b8;
  font-size: 18px;
}

.shell-search input {
  width: 260px;
  padding: 9px 14px 9px 38px;
  border: none;
  border-radius: 8px;
  background: var(--surface-container-highest);
  color: var(--text);
  outline: none;
}

.shell-toolbar {
  display: flex;
  align-items: center;
  gap: 14px;
}

.shell-icon-button {
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  padding: 0;
}

.shell-icon-button:hover {
  color: var(--primary);
}

.shell-avatar {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: linear-gradient(180deg, #0f172a, #111827);
  color: white;
  font-size: 12px;
  font-weight: 800;
}

.shell-page {
  padding: 88px 32px 48px;
}

.grid {
  display: grid;
  gap: 24px;
}

.grid.two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.grid.three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 32px;
}

.page-title-xl {
  margin: 0;
  font-size: 48px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
}

.page-subtitle {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.6;
}

.section-card {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  box-shadow: var(--shadow);
  padding: 24px;
}

.stat-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: var(--primary-container);
  color: var(--primary);
}

.stat-trend {
  font-size: 12px;
  font-weight: 800;
  color: var(--primary);
}

.stat-label {
  font-size: 14px;
  color: var(--muted);
}

.stat-value {
  margin-top: 8px;
  font-size: 44px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
}

.stat-unit {
  font-size: 16px;
  font-weight: 500;
  color: #94a3b8;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1fr);
  gap: 32px;
  align-items: start;
}

.panel {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(217, 226, 234, 0.38);
}

.panel-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 800;
  color: #1f2933;
}

.panel-subtitle {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
}

.panel-link {
  border: none;
  background: transparent;
  color: var(--primary);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.panel-body {
  padding: 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: var(--surface-container-low);
}

.data-table th,
.data-table td {
  padding: 14px 18px;
  text-align: left;
  font-size: 13px;
  vertical-align: middle;
}

.data-table th {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.data-table tbody tr {
  border-top: 1px solid rgba(217, 226, 234, 0.36);
}

.task-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.task-thumb {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  object-fit: cover;
  background: var(--surface-container-high);
}

.task-title {
  font-size: 15px;
  font-weight: 700;
}

.task-meta {
  margin-top: 4px;
  font-size: 12px;
  color: var(--muted);
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.status-chip.processing {
  background: var(--tertiary-container);
  color: #54536f;
}

.status-chip.completed {
  background: var(--primary-container);
  color: #345186;
}

.status-chip.pending {
  background: var(--surface-container-highest);
  color: #566168;
}

.progress-wrap {
  width: 110px;
}

.progress-text {
  font-size: 10px;
  font-weight: 800;
  color: var(--muted);
  margin-bottom: 6px;
}

.progress-track {
  height: 4px;
  border-radius: 999px;
  background: #edf1f5;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--primary);
}

.icon-action {
  border: none;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
}

.quick-card {
  background: var(--surface-container-low);
  border-radius: 12px;
  padding: 24px;
}

.quick-title {
  margin: 0 0 18px;
  font-size: 18px;
  font-weight: 800;
}

.quick-actions {
  display: grid;
  gap: 12px;
}

.quick-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 16px;
  border-radius: 10px;
  background: var(--surface-container-lowest);
  color: #1f2933;
  font-weight: 700;
}

.quick-action-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quick-icon {
  color: var(--primary);
}

.telemetry-card {
  margin-top: 24px;
  background: var(--inverse-surface);
  color: var(--inverse-on-surface);
  border-radius: 12px;
  padding: 22px;
}

.telemetry-kicker {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.2em;
  opacity: 0.72;
  text-transform: uppercase;
}

.telemetry-row {
  margin-top: 22px;
  display: grid;
  gap: 18px;
}

.telemetry-value {
  font-size: 38px;
  line-height: 1;
  font-weight: 900;
}

.telemetry-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.telemetry-label {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.72;
}

.telemetry-subvalue {
  margin-top: 6px;
  font-size: 15px;
  font-weight: 700;
}

.page-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.button.primary {
  background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dim) 100%);
  color: #f7f7ff;
}

.button.secondary {
  background: var(--primary-container);
  color: #345186;
}

.button.dark {
  background: var(--inverse-surface);
  color: white;
}

.button.icon {
  width: 40px;
  height: 36px;
  padding: 0;
  background: transparent;
  border: 1px solid rgba(168, 179, 187, 0.24);
  color: var(--muted);
}

.form-card {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  box-shadow: var(--shadow);
  padding: 24px;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px;
  font-size: 18px;
  font-weight: 800;
}

.form-stack {
  display: grid;
  gap: 14px;
}

.field {
  display: grid;
  gap: 6px;
}

.field-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-bottom: 1px solid rgba(168, 179, 187, 0.24);
  border-radius: 6px 6px 0 0;
  background: var(--surface-container-highest);
  color: var(--text);
  outline: none;
  font-size: 14px;
  resize: none;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.factory-top-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.9fr);
  gap: 24px;
  margin-bottom: 32px;
}

.factory-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.factory-stat {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow);
}

.factory-stat.active {
  background: rgba(216, 226, 255, 0.3);
  border-left: 4px solid var(--primary);
}

.factory-stat-label {
  font-size: 14px;
  font-weight: 700;
  color: var(--muted);
}

.factory-stat-value {
  margin-top: 12px;
  font-size: 46px;
  line-height: 1;
  font-weight: 900;
}

.factory-stat-note {
  margin-top: 28px;
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
}

.highlight-card {
  grid-column: 1 / -1;
  background: var(--inverse-surface);
  color: var(--inverse-on-surface);
  border-radius: 12px;
  padding: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.highlight-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.highlight-icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: var(--primary-dim);
}

.highlight-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
}

.highlight-text {
  margin: 8px 0 0;
  font-size: 14px;
  line-height: 1.7;
  opacity: 0.76;
}

.factory-main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(320px, 0.95fr);
  gap: 28px;
  align-items: start;
}

.script-sidebar {
  background: var(--surface-container-lowest);
  border-radius: 12px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.script-sidebar-head {
  background: var(--surface-container-low);
  padding: 16px 20px;
  border-bottom: 1px solid rgba(217, 226, 234, 0.42);
  font-size: 17px;
  font-weight: 800;
}

.script-sidebar-body {
  padding: 20px;
  display: grid;
  gap: 22px;
  max-height: 760px;
  overflow-y: auto;
}

.script-block-title {
  margin: 0 0 10px;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
}

.script-note {
  padding: 14px;
  background: var(--surface-container);
  border-left: 2px solid rgba(65, 94, 148, 0.24);
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.7;
}

.hook-box {
  padding: 14px;
  background: var(--surface-container-low);
  border-radius: 8px;
  color: var(--primary);
  font-size: 14px;
  font-style: italic;
}

.mini-list {
  display: grid;
  gap: 8px;
}

.mini-item {
  padding: 12px;
  border: 1px solid rgba(217, 226, 234, 0.6);
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
}

.cover-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.cover-option {
  position: relative;
  aspect-ratio: 16 / 9;
  border-radius: 10px;
  overflow: hidden;
  background: var(--surface-container-highest);
}

.cover-option img,
.cover-option video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-chip {
  position: absolute;
  right: 8px;
  bottom: 8px;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 10px;
}

.scene-list {
  display: grid;
  gap: 12px;
}

.scene-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.scene-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 20px;
  border-radius: 4px;
  background: var(--primary);
  color: white;
  font-size: 10px;
  font-weight: 800;
}

.scene-text {
  font-size: 13px;
  line-height: 1.7;
}

.check-list {
  display: grid;
  gap: 10px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--muted);
}

.check-box {
  width: 16px;
  height: 16px;
  display: grid;
  place-items: center;
  border-radius: 4px;
  border: 1px solid rgba(168, 179, 187, 0.6);
  color: var(--primary);
}

.asset-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}

.asset-filter-row {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.asset-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  background: var(--surface-container-low);
  color: var(--muted);
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
}

.asset-filter-chip.active {
  background: var(--primary-container);
  color: #345186;
}

.asset-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 24px;
}

.asset-card {
  background: var(--surface-container-lowest);
  border-radius: 8px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.asset-thumb-wrap {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--surface-container-high);
}

.asset-thumb,
.asset-thumb-wrap video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.asset-duration {
  position: absolute;
  right: 8px;
  bottom: 8px;
  padding: 3px 8px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.64);
  color: white;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}

.asset-body {
  padding: 16px;
}

.asset-title {
  margin: 0;
  font-size: 15px;
  font-weight: 800;
  line-height: 1.4;
}

.asset-path {
  margin-top: 6px;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.5;
}

.asset-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(217, 226, 234, 0.36);
}

.asset-meta {
  font-size: 11px;
  color: var(--muted);
  font-weight: 600;
}

.asset-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: none;
  background: transparent;
  color: var(--primary);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}

.asset-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid rgba(217, 226, 234, 0.4);
  color: var(--muted);
  font-size: 12px;
}

.asset-footer-stats {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
}

.asset-footer-stat-label {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.asset-footer-stat-value {
  margin-top: 4px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.asset-footer-status {
  color: var(--green);
}

.publish-filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}

.tab-row {
  display: flex;
  gap: 8px;
}

.tab-button {
  border: none;
  background: transparent;
  padding: 8px 16px;
  border-radius: 8px;
  color: var(--muted);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.tab-button.active {
  background: var(--secondary-container);
  color: #345186;
}

.publish-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 24px;
}

.publish-card {
  background: var(--surface-container-lowest);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.publish-cover {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--surface-container-high);
}

.publish-cover video,
.publish-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.publish-body {
  padding: 14px 14px 16px;
}

.publish-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.publish-title {
  margin: 0;
  font-size: 15px;
  font-weight: 800;
  line-height: 1.45;
}

.publish-summary {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.6;
}

.publish-cover-copy {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 6px;
  background: var(--surface-container);
  font-size: 11px;
  color: var(--text);
}

.publish-cover-copy-label {
  color: var(--muted);
  font-weight: 700;
}

.tag-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 14px;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid rgba(168, 179, 187, 0.28);
  color: var(--muted);
  font-size: 10px;
  font-weight: 700;
}

.publish-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.publish-actions .button {
  flex: 1;
  padding: 11px 12px;
  font-size: 12px;
}

.publish-actions .button.icon {
  flex: 0 0 40px;
}

.fab {
  position: fixed;
  right: 32px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  border: none;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: var(--primary);
  color: white;
  box-shadow: 0 12px 24px rgba(65, 94, 148, 0.24);
  cursor: pointer;
  z-index: 25;
}

.empty-panel {
  padding: 24px;
  background: var(--surface-container-low);
  border-radius: 10px;
  color: var(--muted);
  font-size: 14px;
}

.nowrap {
  white-space: nowrap;
}

@media (max-width: 1380px) {
  .asset-grid,
  .publish-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 1220px) {
  .stats-grid,
  .content-grid,
  .factory-top-grid,
  .factory-main-grid,
  .asset-grid,
  .publish-grid {
    grid-template-columns: 1fr;
  }

  .factory-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 980px) {
  .shell-sidebar {
    position: static;
    width: 100%;
    height: auto;
  }

  .shell-main {
    margin-left: 0;
  }

  .shell-topbar {
    position: static;
    width: 100%;
    height: auto;
    padding: 18px 20px;
    flex-direction: column;
    align-items: stretch;
  }

  .shell-topbar-right {
    flex-direction: column;
    align-items: stretch;
  }

  .shell-search input {
    width: 100%;
  }

  .shell-page {
    padding: 24px 20px 40px;
  }

  .page-header,
  .asset-toolbar,
  .publish-filter-bar,
  .asset-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .field-grid,
  .cover-grid {
    grid-template-columns: 1fr;
  }
}
`;

export const metadata = {
  title: "工厂 AI 视频工厂",
  description: "帮助工厂整理素材、生成脚本、生成视频并输出成片。",
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
        <style dangerouslySetInnerHTML={{ __html: inlineGlobalStyles }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
