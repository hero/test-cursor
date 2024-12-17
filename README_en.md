# test-cursor

[中文](./README.md) | English

A tool for testing HTTP/1.1 and HTTP/2 performance differences locally, helping you decide whether to disable HTTP/2 in [Cursor](https://www.cursor.com/).

This project is also a practical experience of using [Cursor](https://www.cursor.com/), documenting the interaction with [Cursor](https://www.cursor.com/). See [AI Interaction Records](docs/Interacting_with_cursor_records_en.md) for details.

## Features

- Multi-domain concurrent testing
- Simultaneous HTTP/1.1 and HTTP/2 performance testing
- Smart proxy settings (supports .env configuration and system proxy)
- Detailed test reports and performance analysis
- Project structures are often messed up, just look at my current directory structure which works fine 😹
- Cursor configuration recommendations based on test results
- There are problems with the processing of long documents or source files, and Agent local writing will basically mess up. See the last round interaction with cursor in [AI Interaction Records](docs/Interacting_with_cursor_records.md) for details. 

## Installation

This project uses [Rye](https://rye-up.com/) for dependency management. Make sure you have Rye installed, then run:

```bash
# Clone the repository
git clone https://github.com/hero/test-cursor.git
cd test-cursor

# Install dependencies
rye sync
```

## Configuration

Create a `.env` file in the project root directory (you can copy from `.env.example`), and configure the following options:

```ini
# Test domain list (comma-separated)
TEST_DOMAINS=github.com,microsoft.com,vscode.dev,cursor.sh

# Number of tests per domain
TEST_ITERATIONS=5

# Test timeout in seconds
TEST_TIMEOUT=10

# Whether to use proxy
USE_PROXY=True

# Proxy addresses (if proxy is enabled)
HTTP_PROXY=
HTTPS_PROXY=

# Results output path
RESULTS_PATH=src/test_cursor/network/results
```

## Usage

```bash
# Run the test
rye run test-network
```

During the test, it will:

1. Check and load configuration
2. Check system proxy if proxy is enabled but not configured
3. Perform specified number of HTTP/1.1 and HTTP/2 tests for each domain
4. Generate test reports and performance analysis

## Test Results

After testing, the following files will be generated in the configured `RESULTS_PATH` directory:

- `raw_results_{timestamp}.csv`: Raw test data
- `analysis_{timestamp}.csv`: Performance analysis data
- `report_{timestamp}.json`: Test report and configuration recommendations

The console will also display a test summary, including:

- Average response time comparison
- Success rate comparison
- Cursor configuration recommendations

## Cursor Configuration Recommendations

Based on the test results, the tool will provide recommendations on whether to disable HTTP/2. If disabling is recommended, you can add the following to your Cursor settings:

```json
{
  "cursor.general.disableHttp2": true
}
```

## Notes

1. Test results may be affected by network conditions; it's recommended to run multiple tests in your actual usage environment
2. If using a proxy, ensure your proxy server supports HTTP/2
3. Some websites may not support HTTP/2, in which case it will automatically fall back to HTTP/1.1

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License

## Original Cursor Configuration Guide

[View Cursor Configuration Guide](docs/Cursor_config_en.md)
