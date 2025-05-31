# beatHost

**beatHost** is a fast and asynchronous HTTP status checker for domains and subdomains. It helps identify which targets are alive by evaluating their HTTP response codes. Designed for use in reconnaissance phases during penetration testing and bug bounty assessments.

## Features

- Supports both `http` and `https` schemes
- Asynchronous execution for high performance (uses `httpx`)
- Custom filtering by HTTP status codes (e.g., 200, 403, 301)
- Color-coded terminal output for clarity
- Displays only reachable hosts (unless filters are disabled)

## Installation

Requires Python 3.7 or higher.

```bash
git clone https://github.com/yourusername/beathost.git
cd beathost
pip install -r requirements.txt
````

## Usage

```bash
python3 beathost.py -i input.txt
```

### Options

| Argument         | Description                                                                  |
| ---------------- | ---------------------------------------------------------------------------- |
| `-i`, `--input`  | Input file containing domains/subdomains                                     |
| `-f`, `--filter` | (Optional) Comma-separated list of HTTP codes to filter (e.g. `200,403,301`) |

### Example

```bash
# Check for all reachable hosts
python3 beathost.py -i domains.txt

# Check only for HTTP 200 and 403 responses
python3 beathost.py -i domains.txt -f 200,403
```

## Input Format

Plain text file with one domain or subdomain per line:

```
example.com
admin.example.com
portal.site.net
```

## Output

Each result shows:

* HTTP response code (color-coded)
* Full URL (`http://` or `https://`)
* Summary of live hosts at the end

![](https://i.postimg.cc/Kj4ZLZzL/imagen.png)

## Typical Use Case

BeatHost is typically used during perimeter assessments or reconnaissance to quickly verify which hosts are responsive and prioritize them for further analysis.
