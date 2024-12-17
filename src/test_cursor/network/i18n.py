"""国际化支持"""

# 翻译字典
TRANSLATIONS = {
    'zh': {
        'proxy_disabled': "[yellow]代理设置已禁用 (USE_PROXY=false)[/yellow]",
        'env_proxy_settings': "[blue].env 文件中的代理设置:[/blue]",
        'system_proxy_detected': "\n[yellow]检测到系统代理设置:[/yellow]",
        'use_system_proxy': "是否使用系统代理?",
        'system_proxy_enabled': "[green]已启用系统代理[/green]",
        'system_proxy_skipped': "[yellow]已跳过系统代理[/yellow]",
        'final_proxy_settings': "[green]最终使用的代理设置: {proxies}[/green]",
        'no_proxy_used': "[yellow]未使用任何代理[/yellow]",
        'config_file_not_found': "[red]错误: 未找到配置文件 {file}[/red]",
        'domains_not_configured': "[red]错误: 未配置测试域名[/red]",
        'test_config': "[green]测试配置:[/green]",
        'domain_list': "域名列表: {domains}",
        'test_iterations': "测试次数: {iterations}",
        'timeout': "超时时间: {timeout}秒",
        'results_path': "结果路径: {path}",
        'testing_in_progress': "[bold green]正在进行网络测试...[/bold green]",
        'testing_domain': "测试 {domain}",
        'test_results_summary': "\n[bold]测试结果摘要[/bold]",
        'metrics': "指标",
        'avg_response_time': "平均响应时间",
        'success_rate': "成功率",
        'recommendation': "\n[bold green]建议配置:[/bold green] {rec}",
        'disable_http2': "建议禁用 HTTP/2 (设置 cursor.general.disableHttp2=true)",
        'keep_http2': "建议使用默认的 HTTP/2 (设置 cursor.general.disableHttp2=false)",
        # 帮助信息
        'help_title': "HTTP/1.1 与 HTTP/2 性能测试工具",
        'help_usage': "用法：",
        'help_commands': "命令：",
        'help_options': "选项：",
        'help_examples': "示例：",
        'help_more_info': "更多信息，请访问：",
        'help_cmd_test': "运行网络性能测试",
        'help_cmd_help': "显示帮助信息",
        'help_opt_english': "强制使用英文输出测试结果",
        'help_opt_chinese': "以中文显示帮助信息",
        'help_example_1': "运行测试（语言根据系统区域设置）",
        'help_example_2': "使用英文运行测试",
        'help_example_3': "显示英文帮助信息",
        'help_example_4': "显示中文帮助��息",
        'interrupted': "\n[yellow]操作被用户中断[/yellow]",
        'error_occurred': "[red]错误: {error}[/red]"
    },
    'en': {
        'proxy_disabled': "[yellow]Proxy settings disabled (USE_PROXY=false)[/yellow]",
        'env_proxy_settings': "[blue]Proxy settings in .env file:[/blue]",
        'system_proxy_detected': "\n[yellow]System proxy detected:[/yellow]",
        'use_system_proxy': "Use system proxy?",
        'system_proxy_enabled': "[green]System proxy enabled[/green]",
        'system_proxy_skipped': "[yellow]System proxy skipped[/yellow]",
        'final_proxy_settings': "[green]Final proxy settings: {proxies}[/green]",
        'no_proxy_used': "[yellow]No proxy used[/yellow]",
        'config_file_not_found': "[red]Error: Configuration file not found {file}[/red]",
        'domains_not_configured': "[red]Error: Test domains not configured[/red]",
        'test_config': "[green]Test Configuration:[/green]",
        'domain_list': "Domain list: {domains}",
        'test_iterations': "Test iterations: {iterations}",
        'timeout': "Timeout: {timeout} seconds",
        'results_path': "Results path: {path}",
        'testing_in_progress': "[bold green]Network testing in progress...[/bold green]",
        'testing_domain': "Testing {domain}",
        'test_results_summary': "\n[bold]Test Results Summary[/bold]",
        'metrics': "Metrics",
        'avg_response_time': "Average Response Time",
        'success_rate': "Success Rate",
        'recommendation': "\n[bold green]Recommended Configuration:[/bold green] {rec}",
        'disable_http2': "Recommend disabling HTTP/2 (set cursor.general.disableHttp2=true)",
        'keep_http2': "Recommend keeping HTTP/2 (set cursor.general.disableHttp2=false)",
        # Help messages
        'help_title': "HTTP/1.1 vs HTTP/2 Performance Testing Tool",
        'help_usage': "Usage:",
        'help_commands': "Commands:",
        'help_options': "Options:",
        'help_examples': "Examples:",
        'help_more_info': "For more information, visit:",
        'help_cmd_test': "Run network performance tests",
        'help_cmd_help': "Show this help message",
        'help_opt_english': "Force English output for test-network command",
        'help_opt_chinese': "Show help message in Chinese",
        'help_example_1': "Run tests (language based on system locale)",
        'help_example_2': "Run tests with English output",
        'help_example_3': "Show this help in English",
        'help_example_4': "Show help in Chinese",
        'interrupted': "\n[yellow]Operation interrupted by user[/yellow]",
        'error_occurred': "[red]Error: {error}[/red]"
    }
}

class I18n:
    def __init__(self, force_english: bool = False):
        # 如果强制使用英文，直接设置为英文
        if force_english:
            self.lang = 'en'
            from rich.console import Console
            console = Console()
            console.print("[yellow]Force English output (--english flag)[/yellow]")
        else:
            # 获取系统语言
            import locale
            sys_lang = locale.getdefaultlocale()[0]
            from rich.console import Console
            console = Console()
            console.print(f"[blue]System language detected: {sys_lang}[/blue]")
            # 确定使用的语言
            self.lang = 'zh' if sys_lang and sys_lang.startswith('zh') else 'en'
        console.print(f"[blue]Using {'English' if self.lang == 'en' else 'Chinese'} output[/blue]")
    
    def get(self, key: str, **kwargs) -> str:
        """获取指定语言的文本"""
        text = TRANSLATIONS[self.lang].get(key, TRANSLATIONS['en'][key])
        return text.format(**kwargs) if kwargs else text 