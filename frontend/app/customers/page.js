"use client";

import { AppShell } from "../../components/app-shell";

export default function ExtensionPage() {
  return (
    <AppShell
      topbarTitle="二期扩展"
      searchPlaceholder="搜索..."
      primaryAction={<button className="button secondary">返回主流程</button>}
    >
      <section className="page-header">
        <div>
          <h2 className="page-title-xl">二期扩展</h2>
          <p className="page-subtitle">当前交付重点仍然是视频生产主流程，这里保留后续扩展入口。</p>
        </div>
      </section>

      <div className="empty-panel">这里先不作为主产品入口展示，后续如需接评论承接或客户跟进，再单独扩展。</div>
    </AppShell>
  );
}
