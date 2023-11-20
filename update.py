import requests
import os

# URL to fetch the list of newly registered domains
url = "https://dl.nrd-list.com/1/nrd-list-32-days.txt"
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

    # Download the list of newly registered domains
    response = requests.get(url)
    new_domains = response.text.splitlines()

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
