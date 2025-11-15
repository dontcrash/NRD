import requests
import os

# URLs to fetch the list of newly registered domains
url1 = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd7.txt"
url2 = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd14-8.txt"
url3 = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd21-15.txt"
url4 = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd28-22.txt"
url5 = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd35-29.txt"

# Store in a list so we can loop
URLS = [url1, url2, url3, url4, url5]

directory = "lists"

# Function to extract TLD from a domain line
def get_tld(domain):
    components = domain.split('^')
    if len(components) >= 1:
        tld_component = components[0].strip("|").strip(".")
        if tld_component.count('.') >= 1:
            tld = tld_component.split('.')[-1]
            return tld
    return None

# Function to update the domain files with new domains
def update_domain_files():

    # Create the 'lists' directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # NEW: Combined domains from all URLs
    new_domains = []

    # Download lists one by one
    for url in URLS:
        response = requests.get(url)
        if response.status_code == 200:
            new_domains.extend(response.text.splitlines())
        else:
            print(f"Failed to download {url} (HTTP status {response.status_code})")

    # Filter new domains to those starting with '||' and extract TLDs
    tld_domains = {}
    for domain in new_domains:
        if domain.startswith("||"):
            tld = get_tld(domain)
            if tld:
                tld_domains.setdefault(tld, []).append(domain)

    # Update domains in separate files for each TLD, replacing existing files
    for tld, domains in tld_domains.items():
        filename = os.path.join(directory, f"{tld}.txt")
        with open(filename, 'w') as tld_file:
            tld_file.write('\n'.join(domains) + '\n')
        print(f"Domains for TLD {tld} written to {filename}")

    print("Domain files updated successfully!")

if __name__ == "__main__":
    update_domain_files()
