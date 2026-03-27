"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "../../components/app-shell";
import { apiGet, apiPost, resolveAssetUrl } from "../../lib/api";

function statusMeta(project) {
  if (project.package_status === "ready" || project.status === "package_ready" || project.status === "approved") {
    return { label: "已完成", tone: "completed" };
  }
  if (project.status === "script_ready") {
    return { label: "生成中", tone: "processing" };
  }
  return { label: "草稿箱", tone: "pending" };
}

function ScriptSidebar({ project, assetChoices }) {
  const script = project?.script_json;

  if (!script?.topic) {
    return (
      <div className="script-sidebar">
        <div className="script-sidebar-head">脚本预览与输出</div>
        <div className="script-sidebar-body">
          <div className="empty-panel">选择左侧任务并生成脚本后，这里会显示定位、钩子、标题候选、镜头结构和检查清单。</div>
        </div>
      </div>
    );
  }

  return (
    <div className="script-sidebar">
      <div className="script-sidebar-head">脚本预览与输出</div>
      <div className="script-sidebar-body">
        <div>
          <div className="script-block-title">定位</div>
          <div className="script-note">{script.positioning}</div>
        </div>

        <div>
          <div className="script-block-title">钩子 (Hook)</div>
          <div className="hook-box">{(script.hook_options || [])[0]}</div>
        </div>

        <div>
          <div className="script-block-title">标题候选</div>
          <div className="mini-list">
            {(script.title_options || []).map((item) => (
              <div className="mini-item" key={item}>
                {item}
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="script-block-title">封面方向</div>
          <div className="cover-grid">
            {(script.cover_options || []).slice(0, 2).map((item, index) => {
              const asset = assetChoices[index];
              return (
                <div className="cover-option" key={item}>
                  {asset ? (
                    asset.asset_type === "image" ? (
                      <img src={resolveAssetUrl(asset.public_url)} alt={asset.title} />
                    ) : (
                      <video src={resolveAssetUrl(asset.public_url)} />
                    )
                  ) : null}
                  <div className="cover-chip">{item}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div>
          <div className="script-block-title">镜头结构</div>
          <div className="scene-list">
            {(script.scenes || []).map((scene) => (
              <div className="scene-item" key={`${scene.scene}-${scene.duration}`}>
                <span className="scene-index">{String(scene.scene).padStart(2, "0")}</span>
                <div className="scene-text">{scene.shot}</div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="script-block-title">检查清单 (Checklist)</div>
          <div className="check-list">
            {[(script.publishing_checklist || [])[0], ...(script.compliance_checklist || []).slice(0, 2)]
              .filter(Boolean)
              .map((item) => (
                <div className="check-item" key={item}>
                  <span className="check-box">
                    <span className="material-symbols-outlined" style={{ fontSize: 14 }}>
                      check
                    </span>
                  </span>
                  <span>{item}</span>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ContentPage() {
  const [projects, setProjects] = useState([]);
  const [assets, setAssets] = useState([]);
  const [summary, setSummary] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({
    product_name: "奶白轻奢全铝餐边柜",
    title: "全铝家居产品展示视频",
    target_audience: "经销商、工程客户、定制家居客户",
    topic_direction: "突出工厂实力、材质工艺和定制能力",
    material_constraints: "优先使用全铝家居真实产品图、工厂图和案例视频",
  });

  async function load() {
    const [projectData, assetData, summaryData] = await Promise.all([
      apiGet("/api/content/projects"),
      apiGet("/api/assets"),
      apiGet("/api/system/summary"),
    ]);
    setProjects(projectData);
    setAssets(assetData.filter((item) => item.asset_type === "image" || item.asset_type === "video"));
    setSummary(summaryData);
    if (!selectedId && projectData[0]) {
      setSelectedId(projectData[0].id);
    }
  }

  useEffect(() => {
    load().catch(console.error);
  }, []);

  async function createProject(event) {
    event.preventDefault();
    const created = await apiPost("/api/content/projects", {
      product_id: 1,
      title: form.title,
      target_audience: form.target_audience,
      topic_direction: form.topic_direction,
      material_constraints: `产品名称：${form.product_name}\n${form.material_constraints}`,
    });
    setMessage("已保存并初始化任务。");
    await load();
    setSelectedId(created.id);
  }

  async function generateScript(id) {
    await apiPost(`/api/content/projects/${id}/generate-script`, {});
    setMessage(`任务 #${id} 已生成脚本。`);
    await load();
    setSelectedId(id);
  }

  async function generateVideo(id) {
    await apiPost(`/api/content/projects/${id}/generate-package`, {});
    setMessage(`任务 #${id} 已生成视频。`);
    await load();
    setSelectedId(id);
  }

  const selectedProject = useMemo(() => projects.find((item) => item.id === selectedId) || projects[0], [projects, selectedId]);
  const previewAssets = useMemo(() => assets.slice(0, 4), [assets]);

  return (
    <AppShell
      topbarTitle="视频工厂"
      searchPlaceholder="搜索任务或视频..."
      primaryAction={<button className="button primary">导出成片</button>}
    >
      {message ? <div className="notice" style={{ marginBottom: 16 }}>{message}</div> : null}

      <section className="factory-top-grid">
        <div className="form-card">
          <h2 className="form-title">
            <span className="material-symbols-outlined" style={{ color: "var(--primary)" }}>
              add_circle
            </span>
            <span>新建视频任务</span>
          </h2>
          <form className="form-stack" onSubmit={createProject}>
            <label className="field">
              <span className="field-label">产品名称</span>
              <input value={form.product_name} onChange={(event) => setForm({ ...form, product_name: event.target.value })} />
            </label>
            <label className="field">
              <span className="field-label">视频标题</span>
              <input value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
            </label>
            <div className="field-grid">
              <label className="field">
                <span className="field-label">目标受众</span>
                <input
                  value={form.target_audience}
                  onChange={(event) => setForm({ ...form, target_audience: event.target.value })}
                />
              </label>
              <label className="field">
                <span className="field-label">视频焦点</span>
                <input
                  value={form.topic_direction}
                  onChange={(event) => setForm({ ...form, topic_direction: event.target.value })}
                />
              </label>
            </div>
            <label className="field">
              <span className="field-label">素材限制</span>
              <textarea
                rows={3}
                value={form.material_constraints}
                onChange={(event) => setForm({ ...form, material_constraints: event.target.value })}
              />
            </label>
            <button className="button primary" type="submit" style={{ width: "100%" }}>
              保存并初始化任务
            </button>
          </form>
        </div>

        <div className="factory-stats">
          <div className="factory-stat active">
            <div className="factory-stat-label">正在处理</div>
            <div className="factory-stat-value">{projects.length}</div>
            <div className="factory-stat-note">Average Render Time: 4.2m</div>
          </div>
          <div className="factory-stat">
            <div className="factory-stat-label">今日已生成</div>
            <div className="factory-stat-value">{summary ? summary.publish_packages : 0}</div>
            <div className="progress-track" style={{ marginTop: 28 }}>
              <div className="progress-bar" style={{ width: "78%" }} />
            </div>
          </div>
          <div className="factory-stat">
            <div className="factory-stat-label" style={{ color: "var(--error)" }}>
              存储空间
            </div>
            <div className="factory-stat-value">{assets.length}</div>
            <div className="factory-stat-note">Factory Node: SHA-12</div>
          </div>
          <div className="highlight-card">
            <div className="highlight-left">
              <div className="highlight-icon">
                <span className="material-symbols-outlined" style={{ color: "white" }}>
                  auto_awesome
                </span>
              </div>
              <div>
                <h3 className="highlight-title">AI 视频优化建议</h3>
                <p className="highlight-text">检测到当前任务更适合使用产品细节镜头开场，先展示材质和工艺，再进入工厂实力和案例展示。</p>
              </div>
            </div>
            <button className="button" type="button" style={{ background: "rgba(255,255,255,0.1)", color: "white" }}>
              查看优化方案
            </button>
          </div>
        </div>
      </section>

      <section className="factory-main-grid">
        <div className="panel">
          <div className="panel-header">
            <div className="panel-title-row">
              <span>当前任务队列</span>
            </div>
            <div className="page-actions">
              <button className="icon-action" type="button">
                <span className="material-symbols-outlined">filter_list</span>
              </button>
              <button className="icon-action" type="button">
                <span className="material-symbols-outlined">refresh</span>
              </button>
            </div>
          </div>
          <div className="panel-body">
            <table className="data-table">
              <thead>
                <tr>
                  <th>任务状态</th>
                  <th>产品名称</th>
                  <th>视频标题</th>
                  <th>核心操作</th>
                  <th>管理</th>
                </tr>
              </thead>
              <tbody>
                {projects.map((project) => {
                  const status = statusMeta(project);
                  return (
                    <tr
                      key={project.id}
                      style={{ background: project.id === selectedId ? "rgba(216,226,255,0.08)" : "transparent", cursor: "pointer" }}
                      onClick={() => setSelectedId(project.id)}
                    >
                      <td>
                        <span className={`status-chip ${status.tone}`}>{status.label}</span>
                      </td>
                      <td>{project.script_json?.product_name || "工厂产品"}</td>
                      <td>{project.title}</td>
                      <td>
                        <div className="page-actions">
                          <button
                            className="button primary"
                            type="button"
                            style={{ padding: "8px 12px", fontSize: 12 }}
                            onClick={(event) => {
                              event.stopPropagation();
                              generateScript(project.id);
                            }}
                          >
                            生成脚本
                          </button>
                          <button
                            className="button dark"
                            type="button"
                            style={{ padding: "8px 12px", fontSize: 12 }}
                            onClick={(event) => {
                              event.stopPropagation();
                              generateVideo(project.id);
                            }}
                          >
                            生成视频
                          </button>
                        </div>
                      </td>
                      <td>
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

        <ScriptSidebar project={selectedProject} assetChoices={previewAssets} />
      </section>

      <button className="fab" type="button" aria-label="新建视频任务">
        <span className="material-symbols-outlined" style={{ fontSize: 28 }}>
          add
        </span>
      </button>
    </AppShell>
  );
}
