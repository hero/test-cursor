import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

import httpx
import requests
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.prompt import Confirm
from dotenv import load_dotenv

from .i18n import I18n

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent.parent
console = Console()

def get_proxy_settings(i18n: I18n):
    """获取代理设置"""
    try:
        # 加载项目根目录下的 .env 文件
        dotenv_values = load_dotenv(ROOT_DIR / '.env')
        
        # 从 .env 文件中读取配置
        use_proxy = os.getenv('USE_PROXY', 'false').lower() == 'true'
        if not use_proxy:
            console.print(i18n.get('proxy_disabled'))
            return None
            
        # 获取.env中的代理设置
        env_file = ROOT_DIR / '.env'
        with open(env_file, encoding='utf-8') as f:
            env_content = f.read()
        
        # 解析 .env 文件内容
        env_dict = {}
        for line in env_content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_dict[key.strip()] = value.strip()
        
        # 从 .env 文件中获取代理设置
        http_proxy = env_dict.get('HTTP_PROXY', '').strip()
        https_proxy = env_dict.get('HTTPS_PROXY', '').strip()
        
        console.print(i18n.get('env_proxy_settings'))
        console.print(f"HTTP_PROXY={http_proxy}")
        console.print(f"HTTPS_PROXY={https_proxy}")
        
        # 如果.env中代理为空，检查系统环境变量
        if not (http_proxy or https_proxy):
            sys_http_proxy = os.environ.get('HTTP_PROXY', '').strip()
            sys_https_proxy = os.environ.get('HTTPS_PROXY', '').strip()
            
            if sys_http_proxy or sys_https_proxy:
                console.print(i18n.get('system_proxy_detected'))
                console.print(f"HTTP_PROXY={sys_http_proxy}")
                console.print(f"HTTPS_PROXY={sys_https_proxy}")
                try:
                    use_sys_proxy = Confirm.ask(
                        i18n.get('use_system_proxy'),
                        default=True
                    )
                    if use_sys_proxy:
                        http_proxy = sys_http_proxy
                        https_proxy = sys_https_proxy
                        console.print(i18n.get('system_proxy_enabled'))
                    else:
                        console.print(i18n.get('system_proxy_skipped'))
                except KeyboardInterrupt:
                    console.print(i18n.get('interrupted'))
                    sys.exit(0)
        
        proxies = {
            'http': http_proxy,
            'https': https_proxy
        } if (http_proxy or https_proxy) else None
        
        if proxies:
            console.print(i18n.get('final_proxy_settings', proxies=proxies))
        else:
            console.print(i18n.get('no_proxy_used'))
            
        return proxies
    except KeyboardInterrupt:
        console.print(i18n.get('interrupted'))
        sys.exit(0)
    except Exception as e:
        console.print(i18n.get('error_occurred', error=str(e)))
        sys.exit(1)

def test_http1(url: str, timeout: int, proxies: Optional[Dict] = None) -> Dict:
    """测试 HTTP/1.1 性能"""
    start_time = time.time()
    try:
        response = requests.get(f"https://{url}", timeout=timeout, proxies=proxies)
        end_time = time.time()
        return {
            "success": True,
            "status_code": response.status_code,
            "time": end_time - start_time,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "time": time.time() - start_time,
            "error": str(e)
        }

def test_http2(url: str, timeout: int, proxies: Optional[Dict] = None) -> Dict:
    """测试 HTTP/2 性能"""
    start_time = time.time()
    try:
        with httpx.Client(http2=True, timeout=timeout, proxies=proxies) as client:
            response = client.get(f"https://{url}")
            end_time = time.time()
            return {
                "success": True,
                "status_code": response.status_code,
                "time": end_time - start_time,
                "error": None
            }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "time": time.time() - start_time,
            "error": str(e)
        }

def run_tests(force_english: bool = False):
    """运行测试并收集结果"""
    i18n = I18n(force_english)
    
    # 获取代理设置
    proxies = get_proxy_settings(i18n)
    
    # 获取配置
    domains = os.getenv('TEST_DOMAINS', '').split(',')
    iterations = int(os.getenv('TEST_ITERATIONS', '5'))
    timeout = int(os.getenv('TEST_TIMEOUT', '10'))
    results_path = Path(os.getenv('RESULTS_PATH', 'results'))

    if not domains or not domains[0]:
        console.print(i18n.get('domains_not_configured'))
        return

    # 确保结果目录存在
    results_path.mkdir(parents=True, exist_ok=True)

    results = []
    total_tests = len(domains) * iterations * 2  # HTTP/1.1 和 HTTP/2

    with console.status(i18n.get('testing_in_progress')) as status:
        for domain in domains:
            for i in track(range(iterations), description=i18n.get('testing_domain', domain=domain)):
                # 测试 HTTP/1.1
                http1_result = test_http1(domain, timeout, proxies)
                results.append({
                    "domain": domain,
                    "iteration": i + 1,
                    "protocol": "HTTP/1.1",
                    **http1_result
                })

                # 测试 HTTP/2
                http2_result = test_http2(domain, timeout, proxies)
                results.append({
                    "domain": domain,
                    "iteration": i + 1,
                    "protocol": "HTTP/2",
                    **http2_result
                })

    return analyze_results(results, results_path, i18n)

def analyze_results(results: List[Dict], results_path: Path, i18n: I18n):
    """分析测试结果并生成报告"""
    df = pd.DataFrame(results)

    # 计算成功率和平均响应时间
    analysis = df.groupby(['domain', 'protocol']).agg({
        'success': 'mean',
        'time': ['mean', 'std', 'min', 'max'],
        'error': lambda x: ', '.join(filter(None, x))
    }).round(3)

    # 保存原始数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(results_path / f'raw_results_{timestamp}.csv', index=False)

    # 保存分析结果
    analysis.to_csv(results_path / f'analysis_{timestamp}.csv')

    # 生成报告
    report = {
        'timestamp': timestamp,
        'summary': {
            'total_tests': len(results),
            'domains_tested': len(df['domain'].unique()),
            'http1_avg_time': df[df['protocol'] == 'HTTP/1.1']['time'].mean(),
            'http2_avg_time': df[df['protocol'] == 'HTTP/2']['time'].mean(),
            'http1_success_rate': df[df['protocol'] == 'HTTP/1.1']['success'].mean(),
            'http2_success_rate': df[df['protocol'] == 'HTTP/2']['success'].mean(),
        },
        'recommendation': get_recommendation(df, i18n)
    }

    # 保存报告
    with open(results_path / f'report_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    display_results(df, report, i18n)
    return report

def get_recommendation(df: pd.DataFrame, i18n: I18n) -> str:
    """基于测试结果生成配置建议"""
    http1_avg = df[df['protocol'] == 'HTTP/1.1']['time'].mean()
    http2_avg = df[df['protocol'] == 'HTTP/2']['time'].mean()
    http1_success = df[df['protocol'] == 'HTTP/1.1']['success'].mean()
    http2_success = df[df['protocol'] == 'HTTP/2']['success'].mean()

    if http2_success < 0.8:  # 如果 HTTP/2 成功率低于 80%
        return i18n.get('disable_http2')
    elif http1_avg < http2_avg * 0.8:  # 如果 HTTP/1.1 比 HTTP/2 快 20% 以上
        return i18n.get('disable_http2')
    else:
        return i18n.get('keep_http2')

def display_results(df: pd.DataFrame, report: Dict, i18n: I18n):
    """使用 Rich 显示测试结果"""
    console.print(i18n.get('test_results_summary'))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(i18n.get('metrics'), style="dim")
    table.add_column("HTTP/1.1", justify="right")
    table.add_column("HTTP/2", justify="right")

    table.add_row(
        i18n.get('avg_response_time'),
        f"{report['summary']['http1_avg_time']:.3f}s",
        f"{report['summary']['http2_avg_time']:.3f}s"
    )
    table.add_row(
        i18n.get('success_rate'),
        f"{report['summary']['http1_success_rate']:.1%}",
        f"{report['summary']['http2_success_rate']:.1%}"
    )

    console.print(table)
    console.print(i18n.get('recommendation', rec=report['recommendation']))

def show_help_message(i18n: I18n):
    """显示帮助信息"""
    help_text = f"""
{i18n.get('help_title')}

{i18n.get('help_usage')}
    rye run test-network [--english]
    rye run help [--chinese]

{i18n.get('help_commands')}
    test-network     {i18n.get('help_cmd_test')}
    help            {i18n.get('help_cmd_help')}

{i18n.get('help_options')}
    --english       {i18n.get('help_opt_english')}
    --chinese       {i18n.get('help_opt_chinese')}

{i18n.get('help_examples')}
    rye run test-network              # {i18n.get('help_example_1')}
    rye run test-network --english    # {i18n.get('help_example_2')}
    rye run help                      # {i18n.get('help_example_3')}
    rye run help --chinese            # {i18n.get('help_example_4')}

{i18n.get('help_more_info')} https://github.com/hero/test-cursor
"""
    console.print(help_text)

def show_help():
    """显示帮助信息的入口点函数"""
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Show help message')
        parser.add_argument('--chinese', action='store_true', help='Show help message in Chinese')
        args = parser.parse_args()
        show_help_message(I18n(not args.chinese))
    except KeyboardInterrupt:
        console.print("\n[yellow]Help display interrupted by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

def main():
    """主函数，处理命令行参数"""
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Test HTTP/1.1 vs HTTP/2 performance')
        parser.add_argument('--english', action='store_true', help='Force English output')
        args = parser.parse_args()
        run_tests(args.english)
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()