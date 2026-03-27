from __future__ import annotations

import argparse
import json
import re
from datetime import datetime

import httpx
from playwright.sync_api import sync_playwright


COMMENT_NODE_SELECTORS = [
    "[data-e2e='comment-item']",
    "[class*='comment-item']",
    "[class*='CommentItem']",
    "[data-e2e='comment-list'] > div",
    "[class*='comment-list'] > div",
]


def extract_payload(page):
    script = """
() => {
  function textOf(node) {
    return (node?.textContent || '').replace(/\\s+/g, ' ').trim();
  }

  function numberFromText(text) {
    const normalized = (text || '').replace(/[^\\d.kKwW万]/g, '');
    if (!normalized) return 0;
    if (normalized.includes('万') || normalized.toLowerCase().includes('w')) {
      const numeric = parseFloat(normalized.replace('万', '').replace(/[wW]/g, ''));
      return Number.isFinite(numeric) ? Math.round(numeric * 10000) : 0;
    }
    if (normalized.toLowerCase().includes('k')) {
      const numeric = parseFloat(normalized.replace(/[kK]/g, ''));
      return Number.isFinite(numeric) ? Math.round(numeric * 1000) : 0;
    }
    const numeric = parseInt(normalized, 10);
    return Number.isFinite(numeric) ? numeric : 0;
  }

  function pickFirst(root, selectors) {
    for (const selector of selectors) {
      const node = root.querySelector(selector);
      if (node) return node;
    }
    return null;
  }

  function pickAll(selectors) {
    for (const selector of selectors) {
      const nodes = Array.from(document.querySelectorAll(selector));
      if (nodes.length) return nodes;
    }
    return [];
  }

  const title = textOf(
    pickFirst(document, [
      'h1',
      "[data-e2e='video-desc']",
      "[data-e2e='feed-active-video-desc']",
      '.video-info-detail .title',
    ])
  ) || document.title;

  const commentNodes = pickAll(%s);
  const comments = commentNodes.map((node) => {
    const nickname = textOf(
      pickFirst(node, [
        "[data-e2e='comment-user-name']",
        "[class*='user-name']",
        "[class*='nickname']",
        'a',
        'strong',
      ])
    );
    const comment = textOf(
      pickFirst(node, [
        "[data-e2e='comment-item-content']",
        "[class*='comment-content']",
        "[class*='content']",
        'p',
        'span',
      ])
    );
    const timeText = textOf(
      pickFirst(node, [
        "[data-e2e='comment-time']",
        "[class*='comment-time']",
        "[class*='time']",
        'time',
      ])
    );
    const likeText = textOf(
      pickFirst(node, [
        "[data-e2e='comment-like-count']",
        "[class*='like-count']",
        "[class*='digg-count']",
      ])
    );
    const replyText = textOf(
      pickFirst(node, [
        "[data-e2e='comment-reply-count']",
        "[class*='reply-count']",
      ])
    );
    const metaText = textOf(node);
    const uidMatch = metaText.match(/UID[:：\\s]*([A-Za-z0-9_-]+)/i);
    const dyMatch = metaText.match(/抖音号[:：\\s]*([A-Za-z0-9._-]+)/i);
    const gender = metaText.includes('女') ? '女' : metaText.includes('男') ? '男' : '未知';
    const regionMatch = metaText.match(/(北京|上海|天津|重庆|河北|山西|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川|贵州|云南|陕西|甘肃|青海|台湾|内蒙古|广西|西藏|宁夏|新疆|香港|澳门)/);
    return {
      nickname,
      comment,
      time: timeText || new Date().toISOString().slice(0, 16).replace('T', ' '),
      uid: uidMatch?.[1] || '',
      douyinId: dyMatch?.[1] || '',
      gender,
      region: regionMatch?.[1] || '未知',
      likeCount: numberFromText(likeText),
      replyCount: numberFromText(replyText),
    };
  }).filter((item) => item.nickname || item.comment);

  return {
    source: 'playwright-worker',
    collectedAt: new Date().toISOString(),
    page: {
      url: location.href,
      title,
    },
    comments,
  };
}
""" % json.dumps(COMMENT_NODE_SELECTORS)
    return page.evaluate(script)


def normalize_url(url: str) -> str:
    if not re.match(r"^https?://", url):
        raise ValueError("url must start with http or https")
    return url


def run(url: str, scroll_rounds: int = 8):
    url = normalize_url(url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 1100})
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(3000)
        for _ in range(scroll_rounds):
            page.mouse.wheel(0, 2200)
            page.wait_for_timeout(1500)
        payload = extract_payload(page)
        browser.close()
        return payload


def main():
    parser = argparse.ArgumentParser(description="Douyin comment capture worker")
    parser.add_argument("--url", required=True)
    parser.add_argument("--api-base")
    args = parser.parse_args()

    payload = run(args.url)
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    print(output)

    if args.api_base:
        response = httpx.post(
            f"{args.api_base.rstrip('/')}/api/capture/imports/manual-json",
            json=payload,
            timeout=60.0,
        )
        response.raise_for_status()
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
