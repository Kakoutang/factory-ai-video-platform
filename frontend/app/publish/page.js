"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "../../components/app-shell";
import { apiGet, apiPost, resolveAssetUrl } from "../../lib/api";

function approvalMeta(pkg) {
  return pkg.approval_status === "approved"
    ? { label: "审核通过", tone: "completed" }
    : { label: "待审核", tone: "processing" };
}

export default function PublishPage() {
  const [packages, setPackages] = useState([]);
  const [activeTab, setActiveTab] = useState("全部");
  const [message, setMessage] = useState("");

  async function load() {
    setPackages(await apiGet("/api/publish-packages"));
  }

  useEffect(() => {
    load().catch(console.error);
  }, []);

  async function approvePackage(id) {
    await apiPost(`/api/publish-packages/${id}/approve`, { approved_by: "系统审核" });
    setMessage(`成片 #${id} 已审核通过。`);
    await load();
  }

  const filteredPackages = useMemo(() => {
    if (activeTab === "待审核") {
      return packages.filter((pkg) => pkg.approval_status !== "approved");
    }
    if (activeTab === "已通过") {
      return packages.filter((pkg) => pkg.approval_status === "approved");
    }
    return packages;
  }, [activeTab, packages]);

  return (
    <AppShell
      topbarTitle="成片中心"
      searchPlaceholder="搜索成片..."
      primaryAction={<button className="button primary">导出成片</button>}
    >
      {message ? <div className="notice" style={{ marginBottom: 16 }}>{message}</div> : null}

      <section className="page-header" style={{ alignItems: "center" }}>
        <div className="page-actions" style={{ gap: 14 }}>
          <h2 className="page-title-xl" style={{ fontSize: 40 }}>
            成片中心
          </h2>
          <div style={{ width: 1, height: 16, background: "rgba(168,179,187,0.3)" }} />
          <span className="page-subtitle" style={{ margin: 0 }}>
            库内成片: {packages.length} 条
          </span>
        </div>
      </section>

      <section className="publish-filter-bar">
        <div className="tab-row">
          {["全部", "待审核", "已通过", "草稿箱"].map((tab) => (
            <button
              key={tab}
              className={`tab-button${activeTab === tab ? " active" : ""}`}
              type="button"
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="page-actions" style={{ color: "var(--muted)", fontSize: 12 }}>
          <span>排序:</span>
          <span style={{ fontWeight: 700 }}>最新创建</span>
          <span className="material-symbols-outlined" style={{ fontSize: 18 }}>
            expand_more
          </span>
        </div>
      </section>

      <section className="publish-grid">
        {filteredPackages.map((pkg) => {
          const approval = approvalMeta(pkg);
          return (
            <article className="publish-card" key={pkg.id}>
              <div className="publish-cover">
                {pkg.preview_url ? <video src={resolveAssetUrl(pkg.preview_url)} controls /> : null}
              </div>
              <div className="publish-body">
                <div className="publish-title-row">
                  <h3 className="publish-title">{pkg.title}</h3>
                  <span className={`status-chip ${approval.tone}`}>{approval.label}</span>
                </div>
                <p className="publish-summary">{pkg.description}</p>
                <div className="publish-cover-copy">
                  <span className="publish-cover-copy-label">封面文案:</span> {pkg.cover_text}
                </div>
                <div className="tag-row">
                  {(pkg.hashtags || []).map((tag) => (
                    <span className="tag" key={tag}>
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="publish-actions">
                  <button
                    className={`button ${pkg.approval_status === "approved" ? "secondary" : "primary"}`}
                    type="button"
                    disabled={pkg.approval_status === "approved"}
                    onClick={() => approvePackage(pkg.id)}
                  >
                    {pkg.approval_status === "approved" ? "已在库中" : "审核通过"}
                  </button>
                  <button className="button icon" type="button">
                    <span className="material-symbols-outlined" style={{ fontSize: 18 }}>
                      more_vert
                    </span>
                  </button>
                </div>
              </div>
            </article>
          );
        })}
      </section>

      <button className="fab" type="button" aria-label="新建任务">
        <span className="material-symbols-outlined" style={{ fontSize: 28 }}>
          add
        </span>
      </button>
    </AppShell>
  );
}
