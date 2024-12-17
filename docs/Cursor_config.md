# Cursor 配置选项

中文 | [English](./Cursor_config_en.md)

> 提示: 在 Cursor 中按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS) 打开命令面板，输入 "首选项: 打开用户设置(JSON)" 来修改配置。

### 1. C++ 相关配置

- `cursor.cpp.disabledLanguages`: 禁用 Cursor Tab 的语言列表
- `cursor.cpp.enablePartialAccepts`: 启用 Cursor Tab 的部分接受功能

### 2. 终端相关配置

- `cursor.chat.terminalShowHoverHint`: 在终端中显示悬停提示
- `cursor.terminal.usePreviewBox`: 在终端中使用预览框显示 cmd-k 的结果

### 3. 命令行(cmd-k)相关配置

- `cursor.cmdk.autoSelect`: 自动选择内联代码编辑区域
- `cursor.cmdk.useThemedDiffBackground`: 在内联差异中使用主题背景色

### 4. 差异对比相关配置

- `cursor.diffs.useCharacterLevelDiffs`: 在内联差异中使用字符级别的差异对比

### 5. AI 功能相关配置

- `cursor.aipreview.enabled`: 启用 AI 预览功能(在任何符号上按住 Shift 触发)

### 6. 通用配置

- `cursor.general.disableHttp2`: 禁用 HTTP/2，改用 HTTP/1.1
- `cursor.general.enableShadowWorkspace`: 启用影子工作区(会增加内存使用)
- `cursor.general.gitGraphIndexing`: Git 历史索引设置
- `cursor.preferNotificationsSameAsChat`: 在与聊天相同位置显示通知提示

### 7. Composer 相关配置

- `cursor.composer.cmdPFilePicker2`: 在 Composer 中启用 Cmd+P/Ctrl+P 快捷键用于文件选择
- `cursor.composer.collapsePaneInputBoxPills`: 在 composer 面板中折叠输入框标签
- `cursor.composer.renderPillsInsteadOfBlocks`: 将 composer 代码块渲染为标签而不是代码块
- `cursor.composer.shouldAutoScrollToBottom`: 新消息生成时自动滚动到 composer 面板底部
- `cursor.composer.showSuggestedFiles`: 在 composer 中显示建议的文件

## 推荐配置示例

分析 `defaultSettings.json` 中与 Cursor 相关的配置选项。以下是所有以 `cursor.` 开头的配置项及其分析：

### 1. C++ 相关配置

```json
// 禁用 Cursor Tab 的语言列表
"cursor.cpp.disabledLanguages": [],

// 启用 Cursor Tab 的部分接受功能
"cursor.cpp.enablePartialAccepts": false,
```

### 2. 终端相关配置

```json
// 在终端中显示悬停提示
"cursor.chat.terminalShowHoverHint": true,

// 在终端中使用预览框显示 cmd-k 的结果
"cursor.terminal.usePreviewBox": false,
```

### 3. 命令行(cmd-k)相关配置

```json
// 自动选择内联代码编辑区域
"cursor.cmdk.autoSelect": true,

// 在内联差异中使用主题背景色
"cursor.cmdk.useThemedDiffBackground": false,
```

### 4. 差异对比相关配置

```json
// 在内联差异中使用字符级���的差异对比
"cursor.diffs.useCharacterLevelDiffs": false,
```

### 5. AI 功能相关配置

```json
// 启用 AI 预览功能(在任何符号上按住 Shift 触发)
"cursor.aipreview.enabled": false,
```

### 6. 通用配置

```json
// 禁用 HTTP/2，改用 HTTP/1.1, 但是禁用了就没法使用Agent模式了
"cursor.general.disableHttp2": false,

// 启用影子工作区(会增加内存使用)
"cursor.general.enableShadowWorkspace": false,

// Git 历史索引设置
"cursor.general.gitGraphIndexing": "default",

// 在与聊天相同位置显示通知提示
"cursor.preferNotificationsSameAsChat": false,
```

### 7. Composer 相关配置

```json
// 在 Composer 中启用 Cmd+P/Ctrl+P 快捷键用于文件选择
"cursor.composer.cmdPFilePicker2": false,

// 在 composer 面板中折叠输入框标签
"cursor.composer.collapsePaneInputBoxPills": false,

// 将 composer 代码块渲染为标签而不是代码块
"cursor.composer.renderPillsInsteadOfBlocks": false,

// 新消息生成时自动滚动到 composer 面板底部
"cursor.composer.shouldAutoScrollToBottom": true,

// 在 composer 中显示建议的文件
"cursor.composer.showSuggestedFiles": true,
```

## 建议配置

根据这些选项，建议以下本地配置：

1. 基础功能配置：

```json
{
  "cursor.chat.terminalShowHoverHint": true,
  "cursor.terminal.usePreviewBox": true,
  "cursor.cmdk.autoSelect": true,
  "cursor.composer.shouldAutoScrollToBottom": true,
  "cursor.composer.showSuggestedFiles": true
}
```

2. 如果你的网络环境不稳定或使用公司代理：

```json
{
  "cursor.general.disableHttp2": true
}
```

3. 如果你需要更好的代码差异对比体验：

```json
{
  "cursor.diffs.useCharacterLevelDiffs": true,
  "cursor.cmdk.useThemedDiffBackground": true
}
```

4. 如果你的机器内存充足且需要更好的 AI 功能：

```json
{
  "cursor.general.enableShadowWorkspace": true,
  "cursor.aipreview.enabled": true
}
```

5. 如果你需要更好的 Git 集成：

```json
{
  "cursor.general.gitGraphIndexing": "default"
}
```

注意事项：

1. `cursor.general.enableShadowWorkspace` 会增加内存使用，请根据机器配置决定是否启用
2. `cursor.general.disableHttp2` 只有在遇到网络问题时才需要启用
3. 大多数默认配置已经能满足日常使用，不需要全部修改

这些配置可以根据个人使用习惯和需求进行调整。建议先使用默认配置，在使用过程中根据实际需求逐步调整。
