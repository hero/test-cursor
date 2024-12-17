# test-cursor

中文 | [English](./README_en.md)

一个用于本地测试 HTTP/1.1 和 HTTP/2 性能差异的工具，帮助你决定是否需要在 [Cursor](https://www.cursor.com/) 中禁用 HTTP/2。

同时，本项目也是一次使用[Cursor](https://www.cursor.com/)的实战体验，与[Cursor](https://www.cursor.com/)交互的记录文档，详见[AI 交互记录](docs/Interacting_with_cursor_records.md)。

三十三个回合的对话，完全搞定了本工程 💯

我只是在中间[Cursor](https://www.cursor.com/)卡壳的时候，写了一条用于 Debug 的 print 语句，其它都是[Cursor](https://www.cursor.com/)自行完成的。在惊叹 AI 技术飞速发展的同时，也体会到了[Cursor](https://www.cursor.com/)目前还存在的缺陷：

- 不能动态跟踪程序运行调用栈数据
- 有时候会反复出现`我明白了`或者`我知道了`，但是却是在一本正经的胡言乱语 😅
- 如果是语法错误，[Cursor](https://www.cursor.com/)很快就能解决，但是如果是程序调用逻辑问题，还是需要人工介入才能尽快解决问题。
- 好的代码，它会经常该乱掉。即使你在注释中加入了`User confirmed`的字样，它还是会改乱掉
- 项目结构经常被搞乱，看看我现在这个虽然能够正常工作的目录结构就知道了😹
- 长文档或源文件的处理有问题，Agent本地写入基本会搞乱。详见[AI 交互记录](docs/Interacting_with_cursor_records.md)我最后一个回合的记录

拥抱 AI，使用[Cursor](https://www.cursor.com/)辅助编程，过程很有趣 😻

## 功能特点

- 支持多域名并发测试
- 同时测试 HTTP/1.1 和 HTTP/2 性能
- 智能代理设置（支持 .env 配置和系统代理）
- 详细的测试报告和性能分析
- 基于测试结果提供 Cursor 配置建议
- 支持中英文界面切换
- 优雅的异常处理和用户中断
- 完整的命令行帮助系统

## 安装

本项目使用 [Rye](https://rye-up.com/) 进行依赖管理。确保你已经安装了 Rye，然后执行：

```bash
# 克隆项目
git clone https://github.com/hero/test-cursor.git
cd test-cursor

# 安装依赖
rye sync
```

## 配置

在项目根目录创建 `.env` 文件（可以复制 `.env.example`），配置以下选项：

```ini
# 测试域名列表(逗号分隔)
TEST_DOMAINS=github.com,microsoft.com,vscode.dev,cursor.sh

# 每个域名测试次数
TEST_ITERATIONS=5

# 测试超时时间(秒)
TEST_TIMEOUT=10

# 是否使用代理
USE_PROXY=True

# 代理地址(如果启用代理)
HTTP_PROXY=
HTTPS_PROXY=

# 结果输出路径
RESULTS_PATH=src/test_cursor/network/results
```

## 使用方法

```bash
# 运行测试
rye run test-network
```

测试过程中会：

1. 检查并加载配置
2. 如果启用了代理且未配置代理地址，会检查系统代理
3. 对每个域名进行指定次数的 HTTP/1.1 和 HTTP/2 测试
4. 生成测试报告和性能分析

## 测试结果

测试完成后，会在配置的 `RESULTS_PATH` 目录下生成以下文件：

- `raw_results_{timestamp}.csv`: 原始测试数据
- `analysis_{timestamp}.csv`: 性能分析数据
- `report_{timestamp}.json`: 测试报告和配置建议

同时会在控制台显示测试摘要，包括：

- 平均响应时间对比
- 成功率对比
- Cursor 配置建议

## Cursor 配置建议

根据测试结果，工具会给出是否需要禁用 HTTP/2 的建议。如果需要禁用，可以在 Cursor 的设置中添加：

```json
{
  "cursor.general.disableHttp2": true
}
```

## 注意事项

1. 测试结果可能受网络环境影响，建议在实际使用环境下进行多次测试
2. 如果使用代理，确保代理服务器支持 HTTP/2
3. 某些网站可能不支持 HTTP/2，这种情况下会自动降级到 HTTP/1.1

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 原 Cursor 配置说明

[查看 Cursor 配置说明](docs/Cursor_config.md)
