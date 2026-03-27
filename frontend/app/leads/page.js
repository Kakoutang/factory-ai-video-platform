"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "../../components/app-shell";
import { apiGet, apiPost, resolveAssetUrl } from "../../lib/api";

const filters = [
  ["all", "全部素材", "grid_view"],
  ["产品图", "产品实拍", "inventory"],
  ["工厂图", "工厂环境", "factory"],
  ["数字人", "数字人资产", "face_6"],
  ["AI视频", "视频样例", "video_library"],
  ["资料文档", "文档资料", "description"],
];

function assetPreview(asset) {
  if (asset.asset_type === "image") {
    return <img className="asset-thumb" src={resolveAssetUrl(asset.public_url)} alt={asset.title} />;
  }

  if (asset.asset_type === "video") {
    return (
      <>
        <video className="asset-thumb" src={resolveAssetUrl(asset.public_url)} />
        <div className="asset-duration">视频</div>
      </>
    );
  }

  return <div className="asset-thumb" />;
}

function assetActionLabel(asset) {
  if (asset.asset_type === "video") return "预览";
  if (asset.asset_type === "image") return "预览";
  return "打开";
}

export default function AssetLibraryPage() {
  const [assets, setAssets] = useState([]);
  const [activeFilter, setActiveFilter] = useState("all");
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function load() {
      setAssets(await apiGet("/api/assets"));
    }

    load().catch(console.error);
  }, []);

  async function syncAssets() {
    const result = await apiPost("/api/assets/sync-local", {});
    setMessage(`已同步 ${result.assets} 个素材文件。`);
    setAssets(await apiGet("/api/assets"));
  }

  const filteredAssets = useMemo(() => {
    if (activeFilter === "all") return assets;
    return assets.filter((asset) => asset.category === activeFilter);
  }, [activeFilter, assets]);

  const categoryCount = (category) => {
    if (category === "all") return assets.length;
    return assets.filter((asset) => asset.category === category).length;
  };

  return (
    <AppShell
      topbarTitle="当前位置: 资料素材库"
      searchPlaceholder="搜索素材名称或路径..."
      primaryAction={<button className="button secondary">导出成片</button>}
    >
      {message ? <div className="notice" style={{ marginBottom: 16 }}>{message}</div> : null}

      <section className="page-header">
        <div>
          <h2 className="page-title-xl">资料素材库</h2>
          <p className="page-subtitle">管理、预览和同步用于 AI 视频生成的工业级素材资源</p>
        </div>
        <div className="page-actions">
          <button className="button primary" type="button" onClick={syncAssets}>
            <span className="material-symbols-outlined">sync</span>
            <span>同步素材库</span>
          </button>
        </div>
      </section>

      <section className="asset-toolbar">
        <div className="asset-filter-row">
          {filters.map(([value, label, icon]) => (
            <button
              key={value}
              className={`asset-filter-chip${activeFilter === value ? " active" : ""}`}
              type="button"
              onClick={() => setActiveFilter(value)}
            >
              <span className="material-symbols-outlined" style={activeFilter === value ? { fontVariationSettings: '"FILL" 1' } : {}}>
                {icon}
              </span>
              <span>
                {label} ({categoryCount(value)})
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="asset-grid">
        {filteredAssets.slice(0, 8).map((asset) => (
          <article className="asset-card" key={asset.id}>
            <div className="asset-thumb-wrap">{assetPreview(asset)}</div>
            <div className="asset-body">
              <h3 className="asset-title">{asset.title}</h3>
              <p className="asset-path">{asset.relative_path}</p>
              <div className="asset-bottom">
                <span className="asset-meta">
                  {asset.asset_type === "image" ? "图片" : asset.asset_type === "video" ? "视频" : "文档"} · {asset.category}
                </span>
                <button className="asset-action" type="button">
                  <span className="material-symbols-outlined" style={{ fontSize: 16 }}>
                    {asset.asset_type === "document" || asset.asset_type === "spreadsheet" ? "open_in_new" : "visibility"}
                  </span>
                  <span>{assetActionLabel(asset)}</span>
                </button>
              </div>
            </div>
          </article>
        ))}
      </section>

      <footer className="asset-footer">
        <div className="asset-footer-stats">
          <div>
            <div className="asset-footer-stat-label">Total Storage</div>
            <div className="asset-footer-stat-value">本地素材库</div>
          </div>
          <div>
            <div className="asset-footer-stat-label">Asset Count</div>
            <div className="asset-footer-stat-value">{assets.length} Files</div>
          </div>
          <div>
            <div className="asset-footer-stat-label">Sync Status</div>
            <div className="asset-footer-stat-value asset-footer-status">实时同步中</div>
          </div>
        </div>
        <div className="nowrap">Displaying 1-{Math.min(filteredAssets.length, 8)} of {filteredAssets.length} items</div>
      </footer>
    </AppShell>
  );
}
