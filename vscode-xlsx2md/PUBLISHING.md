# VS Code Marketplace 发布指南

本文档记录将 **xlsx2md** 扩展发布到 [VS Code Marketplace](https://marketplace.visualstudio.com/) 的完整步骤。

---

## 目录

1. [一次性准备工作](#一次性准备工作)
   - [Step 1 — 注册/登录 Microsoft 账号](#step-1--注册登录-microsoft-账号)
   - [Step 2 — 创建 Publisher](#step-2--创建-publisher)
   - [Step 3 — 生成 Personal Access Token (PAT)](#step-3--生成-personal-access-token-pat)
   - [Step 4 — 将 PAT 添加为 GitHub Secret](#step-4--将-pat-添加为-github-secret)
2. [每次发布操作](#每次发布操作)
   - [Step 5 — 更新版本号](#step-5--更新版本号)
   - [Step 6 — 推送版本 Tag](#step-6--推送版本-tag)
   - [Step 7 — 验证发布结果](#step-7--验证发布结果)
3. [本地手动发布（备用）](#本地手动发布备用)
4. [更新已发布版本](#更新已发布版本)
5. [常见问题](#常见问题)

---

## 一次性准备工作

以下步骤**只需做一次**。

---

### Step 1 — 注册/登录 Microsoft 账号

VS Code Marketplace 使用 Microsoft 账号（或 Azure Active Directory 账号）进行身份验证。

- 若已有 Microsoft 账号，直接跳到 Step 2。
- 否则访问 <https://account.microsoft.com> 免费注册。

---

### Step 2 — 创建 Publisher

> Publisher ID 必须与 `package.json` 中的 `"publisher"` 字段完全一致：**`easetools`**。

1. 访问 <https://marketplace.visualstudio.com/manage>，用 Microsoft 账号登录。

2. 点击页面右上角的 **"Create publisher"**（若已有同名 publisher 可跳过此步）。

3. 填写信息：

   | 字段 | 值 |
   |------|-----|
   | **Publisher ID** | `easetools`（必须与 package.json 一致） |
   | **Name** | `EaseTools`（显示名称，可自定义） |
   | **Description** | 可选 |

4. 点击 **"Create"**。

5. 回到 Manage 页面，确认新 Publisher 出现在列表中。

> ⚠️ **注意**：Publisher ID 一旦创建**不可修改**，且全局唯一。`easetools` 若已被他人注册，需在 `package.json` 中将 `publisher` 改为其他可用 ID，并同步修改 CI workflow。

---

### Step 3 — 生成 Personal Access Token (PAT)

PAT 是 CI 流程（`vsce publish`）用来代替密码认证的令牌。

1. 访问 <https://dev.azure.com>，用 **同一个** Microsoft 账号登录。

2. 点击右上角头像 → **"Personal access tokens"**（或导航至 `https://dev.azure.com/<你的组织>/_usersSettings/tokens`）。

   > 如果没有 Azure DevOps 组织，系统会引导你创建一个，填写任意名称即可。

3. 点击 **"New Token"**，填写如下：

   | 字段 | 推荐值 |
   |------|--------|
   | **Name** | `vsce-publish-easetools` |
   | **Organization** | All accessible organizations |
   | **Expiration** | 自定义，建议 **1 年** |
   | **Scopes** | 选择 **Custom defined** → 勾选 **Marketplace → Manage** |

4. 点击 **"Create"**，然后**立即复制**显示的 Token（只显示一次）。

---

### Step 4 — 将 PAT 添加为 GitHub Secret

CI 流程通过 `${{ secrets.VSCE_PAT }}` 读取 PAT，必须在仓库 Secrets 中配置。

1. 打开 GitHub 仓库页面：<https://github.com/eternityman/EaseTools>。

2. 进入 **Settings → Secrets and variables → Actions**。

3. 点击 **"New repository secret"**：

   | 字段 | 值 |
   |------|-----|
   | **Name** | `VSCE_PAT` |
   | **Secret** | 粘贴 Step 3 中复制的 Token |

4. 点击 **"Add secret"**。

---

## 每次发布操作

准备工作完成后，每次发布只需以下三步。

---

### Step 5 — 更新版本号

遵循 [语义化版本](https://semver.org/) (`MAJOR.MINOR.PATCH`)：

```bash
cd vscode-xlsx2md
# 手动编辑 package.json，将 "version" 改为新版本号，例如：
# "version": "0.1.0" → "version": "0.1.1"

# 同时更新 CHANGELOG.md，记录本次变更内容
```

> 也可以使用 npm 自动递增版本：
> ```bash
> npm version patch   # 0.1.0 → 0.1.1  (bug fix)
> npm version minor   # 0.1.0 → 0.2.0  (new feature)
> npm version major   # 0.1.0 → 1.0.0  (breaking change)
> ```

提交版本变更：

```bash
git add vscode-xlsx2md/package.json vscode-xlsx2md/CHANGELOG.md
git commit -m "chore: bump extension version to 0.1.1"
git push
```

---

### Step 6 — 推送版本 Tag

打 Tag 会触发 CI 自动发布：

```bash
# Tag 名称必须以 "v" 开头，后接版本号
git tag v0.1.1
git push origin v0.1.1
```

CI 流程（`.github/workflows/package-vsix.yml`）会自动执行：

```
1. 将 xlsx2md/xlsx2md.py 复制到 vscode-xlsx2md/scripts/
2. 运行 vsce package → 生成 xlsx2md-0.1.1.vsix
3. 将 VSIX 上传为 GitHub Actions artifact（保留 90 天）
4. 运行 vsce publish → 发布到 VS Code Marketplace  ← 仅 tag 触发
```

可在 GitHub Actions 页面监控进度：<https://github.com/eternityman/EaseTools/actions>。

---

### Step 7 — 验证发布结果

发布成功后（通常需要 5–15 分钟审核）：

1. 访问 <https://marketplace.visualstudio.com/items?itemName=easetools.xlsx2md> 确认页面更新。
2. 打开 VS Code → 扩展面板搜索 `xlsx2md`，确认版本号已更新。
3. 在 Manage 页面 <https://marketplace.visualstudio.com/manage/publishers/easetools> 查看统计数据。

---

## 本地手动发布（备用）

如果 CI 不可用，也可以在本地手动发布：

```bash
# 安装 vsce
npm install -g @vscode/vsce

# 进入扩展目录
cd vscode-xlsx2md

# 确保脚本已同步（模拟 CI 的 bundle 步骤）
cp ../xlsx2md/xlsx2md.py scripts/xlsx2md.py

# 打包
vsce package

# 发布（会提示输入 PAT）
vsce publish

# 或者直接指定 PAT
vsce publish --pat <YOUR_VSCE_PAT>
```

---

## 更新已发布版本

```bash
# 修复 bug / 小改动
npm version patch          # e.g. 0.1.0 → 0.1.1

# 新增功能（向下兼容）
npm version minor          # e.g. 0.1.1 → 0.2.0

# 重大不兼容变更
npm version major          # e.g. 0.2.0 → 1.0.0

git push && git push --tags
```

---

## 常见问题

**Q: CI 报错 `Error: Missing publisher name`**  
A: 检查 `package.json` 中的 `"publisher"` 字段是否为 `"easetools"`，且该 Publisher 已在 Marketplace 创建。

**Q: CI 报错 `Error: 401 Unauthorized`**  
A: PAT 过期或权限不足。重新生成 PAT（Step 3），并更新 GitHub Secret（Step 4）。

**Q: CI 报错 `Error: A publisher 'easetools' was not found`**  
A: Publisher 尚未创建，执行 Step 2。

**Q: 发布后在 Marketplace 搜索不到**  
A: 新扩展上架后有 5–30 分钟的索引延迟，稍后再搜索。也可以直接访问 
`https://marketplace.visualstudio.com/items?itemName=easetools.xlsx2md` 验证是否已上架。

**Q: 如何取消发布 / 下架扩展**  
A: 访问 <https://marketplace.visualstudio.com/manage/publishers/easetools>，找到扩展，点击 **"..."** → **"Unpublish"**。

**Q: 如何更换 Publisher ID**  
A: Publisher ID 创建后不可更改。需要修改 `package.json` 中的 `"publisher"` 字段为新 ID，重新发布（会产生一个不同 `itemName` 的新扩展条目）。

---

*生成日期：2024-03-23*
