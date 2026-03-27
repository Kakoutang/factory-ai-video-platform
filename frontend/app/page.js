"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { AppShell } from "../components/app-shell";
import { apiGet, resolveAssetUrl } from "../lib/api";

function dashboardMetrics(summary) {
  if (!summary) return [];
  return [
    {
      label: "资料素材库",
      value: summary.asset_files,
      unit: "项",
      icon: "inventory_2",
      trend: `+${summary.local_images || 0}`,
      colorClass: "",
    },
    {
      label: "总视频任务",
      value: summary.content_projects,
      unit: "个",
      icon: "precision_manufacturing",
      trend: "活跃中",
      colorClass: "",
    },
    {
      label: "已成片中心",
      value: summary.publish_packages,
      unit: "部",
      icon: "movie",
      trend: "已归档",
      colorClass: "",
    },
  ];
}

function taskStatus(project) {
  if (project.package_status === "ready" || project.status === "package_ready" || project.status === "approved") {
    return { label: "Completed", tone: "completed", progress: 100 };
  }
  if (project.status === "script_ready") {
    return { label: "Generating", tone: "processing", progress: 78 };
  }
  return { label: "Pending Script", tone: "pending", progress: 0 };
}

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [projects, setProjects] = useState([]);
  const [packages, setPackages] = useState([]);

  useEffect(() => {
    async function load() {
      const [summaryData, projectData, packageData] = await Promise.all([
        apiGet("/api/system/summary"),
        apiGet("/api/content/projects"),
        apiGet("/api/publish-packages"),
      ]);
      setSummary(summaryData);
      setProjects(projectData.slice(0, 3));
      setPackages(packageData.slice(0, 3));
    }

    load().catch(console.error);
  }, []);

  const metrics = useMemo(() => dashboardMetrics(summary), [summary]);

  return (
    <AppShell
      topbarTitle="总览面板"
      topbarBadge="PRO CONSOLE"
      searchPlaceholder="搜索资源项或任务..."
      primaryAction={
        <button className="button secondary" type="button">
          <span className="material-symbols-outlined" style={{ fontSize: 18 }}>
            export_notes
          </span>
          <span>导出成片</span>
        </button>
      }
    >
      <section className="page-header">
        <div>
          <h2 className="page-title-xl">工作台概览</h2>
          <p className="page-subtitle">欢迎回来。当前视频任务、素材和成片都在同一条生产线内流转，可以直接进入下一步处理。</p>
        </div>
      </section>

      <section className="stats-grid">
        {metrics.map((metric) => (
          <article className="stat-card" key={metric.label}>
            <div className="stat-top">
              <div className="stat-icon">
                <span className="material-symbols-outlined">{metric.icon}</span>
              </div>
              <span className="stat-trend">{metric.trend}</span>
            </div>
            <div className="stat-label">{metric.label}</div>
            <div className="stat-value">
              {metric.value}
              <span className="stat-unit"> {metric.unit}</span>
            </div>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <div>
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title-row">
                <span className="material-symbols-outlined" style={{ color: "var(--primary)", fontSize: 20 }}>
                  analytics
                </span>
                <span>最近视频任务</span>
              </div>
              <button className="panel-link" type="button">
                查看全部
              </button>
            </div>
            <div className="panel-body">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>任务名称</th>
                    <th>状态</th>
                    <th>进度</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  {projects.map((project) => {
                    const status = taskStatus(project);
                    const thumb = packages.find((pkg) => pkg.content_project_id === project.id && pkg.preview_url)?.preview_url;
                    return (
                      <tr key={project.id}>
                        <td>
                          <div className="task-name">
                            {thumb ? (
                              <video className="task-thumb" src={resolveAssetUrl(thumb)} />
                            ) : (
                              <div className="task-thumb" />
                            )}
                            <div>
                              <div className="task-title">{project.title}</div>
                              <div className="task-meta">{project.target_audience}</div>
                            </div>
                          </div>
                        </td>
                        <td>
                          <span className={`status-chip ${status.tone}`}>{status.label}</span>
                        </td>
                        <td>
                          <div className="progress-wrap">
                            <div className="progress-text">{status.progress}%</div>
                            <div className="progress-track">
                              <div className="progress-bar" style={{ width: `${status.progress}%` }} />
                            </div>
                          </div>
                        </td>
                        <td style={{ textAlign: "right" }}>
                          <button className="icon-action" type="button">
                            <span className="material-symbols-outlined">more_vert</span>
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <aside>
          <div className="quick-card">
            <h3 className="quick-title">快速操作</h3>
            <div className="quick-actions">
              <Link className="quick-action" href="/leads">
                <span className="quick-action-left">
                  <span className="material-symbols-outlined quick-icon">sync</span>
                  <span>同步素材</span>
                </span>
                <span className="material-symbols-outlined">chevron_right</span>
              </Link>
              <Link className="quick-action" href="/content">
                <span className="quick-action-left">
                  <span className="material-symbols-outlined quick-icon">video_call</span>
                  <span>创建视频任务</span>
                </span>
                <span className="material-symbols-outlined">chevron_right</span>
              </Link>
              <Link className="quick-action" href="/publish">
                <span className="quick-action-left">
                  <span className="material-symbols-outlined quick-icon">cloud_upload</span>
                  <span>查看成片</span>
                </span>
                <span className="material-symbols-outlined">chevron_right</span>
              </Link>
            </div>
          </div>

          <div className="telemetry-card">
            <div className="telemetry-kicker">SYSTEM STATUS</div>
            <div className="telemetry-row">
              <div>
                <div className="telemetry-label">待处理任务</div>
                <div className="telemetry-value">{summary ? summary.content_projects : 0}</div>
              </div>
              <div className="telemetry-meta">
                <div>
                  <div className="telemetry-label">素材库存</div>
                  <div className="telemetry-subvalue">{summary ? summary.asset_files : 0} Files</div>
                </div>
                <div>
                  <div className="telemetry-label">成片数量</div>
                  <div className="telemetry-subvalue">{summary ? summary.publish_packages : 0} Items</div>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </section>

      <button className="fab" type="button" aria-label="新建任务">
        <span className="material-symbols-outlined" style={{ fontSize: 28 }}>
          add
        </span>
      </button>
    </AppShell>
  );
}
