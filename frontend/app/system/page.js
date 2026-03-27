"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../../components/app-shell";
import { apiGet } from "../../lib/api";

export default function SystemPage() {
  const [summary, setSummary] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [audits, setAudits] = useState([]);

  useEffect(() => {
    async function load() {
      const [summaryData, taskData, auditData] = await Promise.all([
        apiGet("/api/system/summary"),
        apiGet("/api/tasks"),
        apiGet("/api/audit-logs"),
      ]);
      setSummary(summaryData);
      setTasks(taskData);
      setAudits(auditData);
    }

    load().catch(console.error);
  }, []);

  return (
    <AppShell
      topbarTitle="任务中心"
      searchPlaceholder="搜索任务..."
      primaryAction={<button className="button secondary">导出成片</button>}
    >
      <section className="page-header">
        <div>
          <h2 className="page-title-xl">任务中心</h2>
          <p className="page-subtitle">查看视频任务、处理状态和系统操作记录。</p>
        </div>
      </section>

      {summary ? (
        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">视频任务</div>
            <div className="stat-value">
              {summary.content_projects}
              <span className="stat-unit"> 个</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">成片数量</div>
            <div className="stat-value">
              {summary.publish_packages}
              <span className="stat-unit"> 条</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">素材文件</div>
            <div className="stat-value">
              {summary.asset_files}
              <span className="stat-unit"> 项</span>
            </div>
          </div>
        </section>
      ) : null}

      <section className="grid two">
        <div className="panel">
          <div className="panel-header">
            <div>
              <div className="panel-title-row">任务列表</div>
              <p className="panel-subtitle">查看每条任务的类型、对象和处理状态。</p>
            </div>
          </div>
          <div className="panel-body">
            <table className="data-table">
              <thead>
                <tr>
                  <th>类型</th>
                  <th>对象</th>
                  <th>状态</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id}>
                    <td>{task.task_type}</td>
                    <td>
                      {task.entity_type} #{task.entity_id}
                    </td>
                    <td>{task.status}</td>
                    <td>{task.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <div>
              <div className="panel-title-row">操作记录</div>
              <p className="panel-subtitle">查看最近的创建、生成和审核动作。</p>
            </div>
          </div>
          <div className="panel-body">
            <table className="data-table">
              <thead>
                <tr>
                  <th>对象</th>
                  <th>动作</th>
                  <th>详情</th>
                </tr>
              </thead>
              <tbody>
                {audits.map((item) => (
                  <tr key={item.id}>
                    <td>
                      {item.entity_type} #{item.entity_id}
                    </td>
                    <td>{item.action}</td>
                    <td>{item.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </AppShell>
  );
}
