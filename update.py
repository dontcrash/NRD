import requests
import os

# URLs to fetch lists of newly registered domains
URLS = [
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd7.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd14-8.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd21-15.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd28-22.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd35-29.txt"
]

directory = "lists"

# Extract TLD from a domain form like: ||example.com^
def get_tld(domain):
    components = domain.split('^')
    if len(components) >= 1:
        tld_component = components[0].strip("|").strip(".")
        if '.' in tld_component:
            return tld_component.split('.')[-1]
    return None

def update_domain_files():
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)

    all_domains = set()

    # Download and combine domains from all URLs
    for url in URLS:
        print(f"Downloading: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            all_domains.update(lines)
        else:
            print(f"Failed to download {url} (HTTP {response.status_code})")

    print(f"Total domains collected: {len(all_domains)}")

    # Process domains by TLD
    tld_domains = {}
    for domain in all_domains:
        if domain.startswith("||"):
            tld = get_tld(domain)
            if tld:
                tld_domains.setdefault(tld, []).append(domain)

    # Write to TLD-specific files
    for tld, domains in tld_domains.items():
        filename = os.path.join(directory, f"{tld}.txt")
        with open(filename, "w") as tld_file:
            tld_file.write("\n".join(sorted(domains)) + "\n")
        print(f"Written {len(domains)} domains to {filename}")

    print("Domain files updated successfully!")

if __name__ == "__main__":
    update_domain_files()
