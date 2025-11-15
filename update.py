import requests
import os
import traceback

# URLs to fetch the list of newly registered domains
URLS = [
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd7.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd14-8.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd21-15.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd28-22.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd35-29.txt"
]

directory = "lists"

def debug(msg):
    print(f"[DEBUG] {msg}")

# Extract TLD from a raw domain entry like "example.com"
def get_tld(domain):
    try:
        if "." not in domain:
            debug(f"Skipping invalid domain (no dot): {domain}")
            return None
        return domain.strip().lower().split(".")[-1]
    except Exception as e:
        debug(f"Error extracting TLD from domain {domain}: {e}")
        return None

def update_domain_files():
    try:
        # Create lists directory
        if not os.path.exists(directory):
            os.makedirs(directory)
            debug(f"Created directory: {directory}")
        else:
            debug(f"Directory already exists: {directory}")

        new_domains = []

        # Download from each URL
        for url in URLS:
            debug(f"Fetching: {url}")
            try:
                response = requests.get(url)
                debug(f"Status Code: {response.status_code}")

                if response.status_code == 200:
                    # Remove comments and empty lines
                    lines = [
                        line.strip()
                        for line in response.text.splitlines()
                        if line.strip() and not line.startswith("#")
                    ]
                    new_domains.extend(lines)
                    debug(f"Fetched {len(lines)} valid domains from {url}")
                else:
                    print(f"Failed to download {url} (HTTP {response.status_code})")

            except Exception as e:
                debug(f"Error fetching {url}: {e}")
                traceback.print_exc()

        debug(f"Total domains after cleaning: {len(new_domains)}")

        # TLD sorting
        tld_domains = {}

        for domain in new_domains:
            tld = get_tld(domain)
            if tld:
                tld_domains.setdefault(tld, []).append(domain)

        debug(f"TLD buckets created: {len(tld_domains)}")

        for tld, domains in tld_domains.items():
            debug(f"TLD `{tld}` has {len(domains)} domains")

        # Write output files
        for tld, domains in tld_domains.items():
            filename = os.path.join(directory, f"{tld}.txt")
            try:
                with open(filename, "w") as f:
                    f.write("\n".join(domains) + "\n")
                debug(f"Wrote {len(domains)} domains to {filename}")
            except Exception as e:
                debug(f"Error writing file {filename}: {e}")
                traceback.print_exc()

        print("Domain files updated successfully!")

    except Exception:
        debug("FATAL ERROR IN SCRIPT")
        traceback.print_exc()

if __name__ == "__main__":
    update_domain_files()
