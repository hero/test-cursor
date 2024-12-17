import os
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

console = Console()

def get_proxy_settings():
    """获取代理设置"""
    load_dotenv()

    use_proxy = os.getenv('USE_PROXY', 'false').lower() == 'true'
    if not use_proxy:
        return None

    # 获取.env中的代理设置
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')

    # 如果.env中代理为空，检查系统环境变量
    if use_proxy and not (http_proxy or https_proxy):
        sys_http_proxy = os.environ.get('HTTP_PROXY')
        sys_https_proxy = os.environ.get('HTTPS_PROXY')

        if sys_http_proxy or sys_https_proxy:
            use_sys_proxy = Confirm.ask(
                f"检测到系统代理设置:\nHTTP_PROXY={sys_http_proxy}\nHTTPS_PROXY={sys_https_proxy}\n是否使用系统代理?"
            )
            if use_sys_proxy:
                http_proxy = sys_http_proxy
                https_proxy = sys_https_proxy

    return {
        'http': http_proxy,
        'https': https_proxy
    } if (http_proxy or https_proxy) else None

def test_http1(url: str, timeout: int, proxies: Optional[Dict] = None) -> Dict:
    """Test HTTP/1.1 performance"""
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
    """Test HTTP/2 performance"""
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

def run_tests():
    """Run tests and collect results"""
    load_dotenv()

    # Get configuration
    domains = os.getenv('TEST_DOMAINS', '').split(',')
    iterations = int(os.getenv('TEST_ITERATIONS', '5'))
    timeout = int(os.getenv('TEST_TIMEOUT', '10'))
    results_path = Path(os.getenv('RESULTS_PATH', 'results'))
    proxies = get_proxy_settings()

    if not domains or not domains[0]:
        console.print("[red]Error: Test domains not configured[/red]")
        return

    # Ensure results directory exists
    results_path.mkdir(parents=True, exist_ok=True)

    results = []
    total_tests = len(domains) * iterations * 2  # HTTP/1.1 and HTTP/2

    with console.status("[bold green]Network testing in progress...") as status:
        for domain in domains:
            for i in track(range(iterations), description=f"Testing {domain}"):
                # Test HTTP/1.1
                http1_result = test_http1(domain, timeout, proxies)
                results.append({
                    "domain": domain,
                    "iteration": i + 1,
                    "protocol": "HTTP/1.1",
                    **http1_result
                })

                # Test HTTP/2
                http2_result = test_http2(domain, timeout, proxies)
                results.append({
                    "domain": domain,
                    "iteration": i + 1,
                    "protocol": "HTTP/2",
                    **http2_result
                })

    return analyze_results(results, results_path)

def analyze_results(results: List[Dict], results_path: Path):
    """Analyze test results and generate report"""
    df = pd.DataFrame(results)

    # Calculate success rate and average response time
    analysis = df.groupby(['domain', 'protocol']).agg({
        'success': 'mean',
        'time': ['mean', 'std', 'min', 'max'],
        'error': lambda x: ', '.join(filter(None, x))
    }).round(3)

    # Save raw data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(results_path / f'raw_results_{timestamp}.csv', index=False)

    # Save analysis results
    analysis.to_csv(results_path / f'analysis_{timestamp}.csv')

    # Generate report
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
        'recommendation': get_recommendation(df)
    }

    # Save report
    with open(results_path / f'report_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    display_results(df, report)
    return report

def get_recommendation(df: pd.DataFrame) -> str:
    """Generate configuration recommendation based on test results"""
    http1_avg = df[df['protocol'] == 'HTTP/1.1']['time'].mean()
    http2_avg = df[df['protocol'] == 'HTTP/2']['time'].mean()
    http1_success = df[df['protocol'] == 'HTTP/1.1']['success'].mean()
    http2_success = df[df['protocol'] == 'HTTP/2']['success'].mean()

    if http2_success < 0.8:  # If HTTP/2 success rate is below 80%
        return "Recommend disabling HTTP/2 (set cursor.general.disableHttp2=true)"
    elif http1_avg < http2_avg * 0.8:  # If HTTP/1.1 is more than 20% faster than HTTP/2
        return "Recommend disabling HTTP/2 (set cursor.general.disableHttp2=true)"
    else:
        return "Recommend keeping default HTTP/2 (set cursor.general.disableHttp2=false)"

def display_results(df: pd.DataFrame, report: Dict):
    """Display test results using Rich"""
    console.print("\n[bold]Test Results Summary[/bold]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metrics", style="dim")
    table.add_column("HTTP/1.1", justify="right")
    table.add_column("HTTP/2", justify="right")

    table.add_row(
        "Average Response Time",
        f"{report['summary']['http1_avg_time']:.3f}s",
        f"{report['summary']['http2_avg_time']:.3f}s"
    )
    table.add_row(
        "Success Rate",
        f"{report['summary']['http1_success_rate']:.1%}",
        f"{report['summary']['http2_success_rate']:.1%}"
    )

    console.print(table)
    console.print(f"\n[bold green]Recommended Configuration:[/bold green] {report['recommendation']}")

if __name__ == '__main__':
    run_tests()