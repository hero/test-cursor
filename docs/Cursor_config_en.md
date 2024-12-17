# Cursor Configuration Options

[中文](./Cursor_config.md) | English

> Tip: In Cursor, press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the command palette, then type "Preferences: Open User Settings (JSON)" to modify the configuration.

## 1. C++ Related Configuration

- `cursor.cpp.disabledLanguages`: List of languages to disable in Cursor Tab
- `cursor.cpp.enablePartialAccepts`: Enable partial accepts feature in Cursor Tab

## 2. Terminal Related Configuration

- `cursor.chat.terminalShowHoverHint`: Show hover hints in terminal
- `cursor.terminal.usePreviewBox`: Use preview box to display cmd-k results in terminal

## 3. Command Line (cmd-k) Related Configuration

- `cursor.cmdk.autoSelect`: Auto-select inline code editing area
- `cursor.cmdk.useThemedDiffBackground`: Use themed background color in inline diffs

## 4. Diff Comparison Configuration

- `cursor.diffs.useCharacterLevelDiffs`: Use character-level diff comparison in inline diffs

## 5. AI Feature Configuration

- `cursor.aipreview.enabled`: Enable AI preview feature (triggered by holding Shift on any symbol)

## 6. General Configuration

- `cursor.general.disableHttp2`: Disable HTTP/2 and use HTTP/1.1 instead
- `cursor.general.enableShadowWorkspace`: Enable shadow workspace (increases memory usage)
- `cursor.general.gitGraphIndexing`: Git history indexing settings
- `cursor.preferNotificationsSameAsChat`: Display notifications in the same location as chat

## 7. Composer Configuration

- `cursor.composer.cmdPFilePicker2`: Enable Cmd+P/Ctrl+P shortcut for file selection in Composer
- `cursor.composer.collapsePaneInputBoxPills`: Collapse input box pills in composer panel
- `cursor.composer.renderPillsInsteadOfBlocks`: Render composer code blocks as pills instead of blocks
- `cursor.composer.shouldAutoScrollToBottom`: Auto-scroll to bottom when new messages are generated
- `cursor.composer.showSuggestedFiles`: Show suggested files in composer

## Configuration Examples

Analysis of Cursor-related configuration options in `defaultSettings.json`. Here are all the settings starting with `cursor.`:

### 1. C++ Related Configuration

```json
// List of languages to disable in Cursor Tab
"cursor.cpp.disabledLanguages": [],

// Enable partial accepts feature in Cursor Tab
"cursor.cpp.enablePartialAccepts": false,
```

### 2. Terminal Related Configuration

```json
// Show hover hints in terminal
"cursor.chat.terminalShowHoverHint": true,

// Use preview box to display cmd-k results in terminal
"cursor.terminal.usePreviewBox": false,
```

### 3. Command Line (cmd-k) Related Configuration

```json
// Auto-select inline code editing area
"cursor.cmdk.autoSelect": true,

// Use themed background color in inline diffs
"cursor.cmdk.useThemedDiffBackground": false,
```

### 4. Diff Comparison Configuration

```json
// Use character-level diff comparison in inline diffs
"cursor.diffs.useCharacterLevelDiffs": false,
```

### 5. AI Feature Configuration

```json
// Enable AI preview feature (triggered by holding Shift on any symbol)
"cursor.aipreview.enabled": false,
```

### 6. General Configuration

```json
// Disable HTTP/2 and use HTTP/1.1 instead, but Agent mode won't work if disabled
"cursor.general.disableHttp2": false,

// Enable shadow workspace (increases memory usage)
"cursor.general.enableShadowWorkspace": false,

// Git history indexing settings
"cursor.general.gitGraphIndexing": "default",

// Display notifications in the same location as chat
"cursor.preferNotificationsSameAsChat": false,
```

### 7. Composer Configuration

```json
// Enable Cmd+P/Ctrl+P shortcut for file selection in Composer
"cursor.composer.cmdPFilePicker2": false,

// Collapse input box pills in composer panel
"cursor.composer.collapsePaneInputBoxPills": false,

// Render composer code blocks as pills instead of blocks
"cursor.composer.renderPillsInsteadOfBlocks": false,

// Auto-scroll to bottom when new messages are generated
"cursor.composer.shouldAutoScrollToBottom": true,

// Show suggested files in composer
"cursor.composer.showSuggestedFiles": true,
```

## Recommended Configuration

Based on these options, here are the recommended local configurations:

1. Basic functionality configuration:

```json
{
  "cursor.chat.terminalShowHoverHint": true,
  "cursor.terminal.usePreviewBox": true,
  "cursor.cmdk.autoSelect": true,
  "cursor.composer.shouldAutoScrollToBottom": true,
  "cursor.composer.showSuggestedFiles": true
}
```

2. If your network is unstable or using corporate proxy:

```json
{
  "cursor.general.disableHttp2": true
}
```

3. If you need better code diff comparison experience:

```json
{
  "cursor.diffs.useCharacterLevelDiffs": true,
  "cursor.cmdk.useThemedDiffBackground": true
}
```

4. If you have sufficient memory and need better AI features:

```json
{
  "cursor.general.enableShadowWorkspace": true,
  "cursor.aipreview.enabled": true
}
```

5. If you need better Git integration:

```json
{
  "cursor.general.gitGraphIndexing": "default"
}
```

Notes:

1. `cursor.general.enableShadowWorkspace` increases memory usage, please decide based on your machine's configuration
2. `cursor.general.disableHttp2` should only be enabled when experiencing network issues
3. Most default configurations are sufficient for daily use, no need to modify all of them

These configurations can be adjusted according to personal usage habits and needs. It's recommended to start with default settings and gradually adjust based on actual requirements.
