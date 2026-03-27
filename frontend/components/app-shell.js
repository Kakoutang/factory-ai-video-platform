"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "总览面板", icon: "dashboard" },
  { href: "/leads", label: "资料素材库", icon: "inventory_2" },
  { href: "/content", label: "视频工厂", icon: "precision_manufacturing" },
  { href: "/publish", label: "成片中心", icon: "movie" },
  { href: "/system", label: "任务中心", icon: "assignment" },
];

export function AppShell({
  topbarTitle,
  topbarBadge,
  searchPlaceholder = "搜索资源或任务...",
  primaryAction,
  pageClassName = "",
  children,
}) {
  const pathname = usePathname();

  return (
    <div className="shell-root">
      <aside className="shell-sidebar">
        <div className="shell-brand-block">
          <h1 className="shell-brand">工厂 AI 视频工厂</h1>
          <p className="shell-brand-subtitle">工业级 AI 视频生产平台</p>
        </div>

        <nav className="shell-nav">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`shell-nav-item${pathname === item.href ? " active" : ""}`}
            >
              <span className="material-symbols-outlined shell-nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="shell-sidebar-cta-wrap">
          <button className="shell-sidebar-cta" type="button">
            <span className="material-symbols-outlined">add</span>
            <span>新建任务</span>
          </button>
        </div>

        <div className="shell-sidebar-footer">
          <button className="shell-sidebar-link" type="button">
            <span className="material-symbols-outlined">settings</span>
            <span>设置</span>
          </button>
          <button className="shell-sidebar-link" type="button">
            <span className="material-symbols-outlined">help</span>
            <span>帮助</span>
          </button>
        </div>
      </aside>

      <main className="shell-main">
        <header className="shell-topbar">
          <div className="shell-topbar-left">
            <span className="shell-topbar-title">{topbarTitle}</span>
            {topbarBadge ? <span className="shell-topbar-badge">{topbarBadge}</span> : null}
          </div>

          <div className="shell-topbar-right">
            <label className="shell-search">
              <span className="material-symbols-outlined shell-search-icon">search</span>
              <input placeholder={searchPlaceholder} type="text" />
            </label>

            <div className="shell-toolbar">
              <button className="shell-icon-button" type="button" aria-label="通知">
                <span className="material-symbols-outlined">notifications</span>
              </button>
              <button className="shell-icon-button" type="button" aria-label="历史">
                <span className="material-symbols-outlined">history</span>
              </button>
              {primaryAction}
              <div className="shell-avatar" aria-hidden="true">
                J
              </div>
            </div>
          </div>
        </header>

        <div className={`shell-page ${pageClassName}`.trim()}>{children}</div>
      </main>
    </div>
  );
}
