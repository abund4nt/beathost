#!/usr/bin/env python3
import httpx
import argparse
import asyncio
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

BANNER = r"""
   __            __  __            __ 
  / /  ___ ___ _/ /_/ /  ___  ___ / /_
 / _ \/ -_) _ `/ __/ _ \/ _ \(_-</ __/
/_.__/\__/\_,_/\__/_//_/\___/___/\__/ 
                    @abund4nt
"""

print(BANNER)

alive_hosts = []

def get_color_by_status(status_code: int) -> str:
    if status_code == 200:
        return Fore.GREEN
    elif 300 <= status_code < 400:
        return Fore.CYAN
    elif 400 <= status_code < 500:
        return Fore.YELLOW
    elif 500 <= status_code < 600:
        return Fore.RED
    else:
        return Style.RESET_ALL

async def check_domain(client, domain, filters):
    domain = domain.strip()
    if not domain:
        return

    for scheme in ["http://", "https://"]:
        url = f"{scheme}{domain}"
        try:
            response = await client.get(url, timeout=5, follow_redirects=True)
            status = response.status_code
            if not filters or status in filters:
                color = get_color_by_status(status)
                if status == 200:
                    status_text = f"{color}200 OK{Style.RESET_ALL}"
                else:
                    status_text = f"{color}{status}{Style.RESET_ALL}"
                print(f"[{status_text}] {url}")
                alive_hosts.append(url)
            return
        except httpx.RequestError:
            if not filters:
                print(f"[{Fore.RED}FAILED{Style.RESET_ALL}] {url}")
            return

async def main(file_path, filters):
    if not os.path.isfile(file_path):
        print(f"[!] File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        domains = f.readlines()

    async with httpx.AsyncClient() as client:
        tasks = [check_domain(client, domain, filters) for domain in domains]
        await asyncio.gather(*tasks)

    print(f"\n[+] Total live hosts: {Fore.GREEN}{len(alive_hosts)}{Style.RESET_ALL}")
    for host in alive_hosts:
        print(f" - {host}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeatHost - Fast HTTP status checker for domains and subdomains.")
    parser.add_argument("-i", "--input", required=True, help="File containing domains and/or subdomains")
    parser.add_argument("-f", "--filter", required=False, help="Comma-separated HTTP status codes to filter (e.g. 200,301,404)")
    args = parser.parse_args()

    if args.filter:
        try:
            filters = set(int(code.strip()) for code in args.filter.split(",") if code.strip())
        except ValueError:
            print("[-] Error: Filter must contain only numbers separated by commas.")
            exit(1)
    else:
        filters = set()

    asyncio.run(main(args.input, filters))
