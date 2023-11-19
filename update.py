import requests

# File path for master list
master_file = "nrd.txt"

# Function to update the master list with new domains
def update_master_list():
    global master_file  # Accessing the global variable

    # URL to fetch the list of newly registered domains
    url = "https://dl.nrd-list.com/1/nrd-list-32-days.txt"

    # Download the list of newly registered domains
    response = requests.get(url)
    new_domains = response.text.splitlines()

    # Filter new domains to those starting with '||'
    new_domains = [domain for domain in new_domains if domain.startswith("||")]

    # Read the contents of the master file
    try:
        with open(master_file, 'r') as file:
            master_domains = file.readlines()
    except FileNotFoundError:
        master_domains = []

    # Combine new and master domains, remove duplicates, and sort them alphabetically
    combined_domains = list(set(new_domains + master_domains))
    combined_domains = [line.strip() for line in combined_domains if line.startswith("||")]
    combined_domains.sort()

    # Save the sorted unique domains to the master file
    with open(master_file, 'w') as file:
        file.write("\n".join(combined_domains))

    print("Master list updated successfully!")

if __name__ == "__main__":
    update_master_list()
