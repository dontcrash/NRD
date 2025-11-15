## NRD Blocklist Splitter
This script automates the update process for a blocklist of newly registered domains from [https://github.com/hagezi/dns-blocklists?tab=readme-ov-file#nrd](https://github.com/hagezi/dns-blocklists?tab=readme-ov-file#nrd)


The original list contains every single TLD in one file, which leads to long update times, by breaking the list apart, it allows the end user to select what newly registered domains they want to block based on TLD.

A GitHub action runs daily, updating each TLD file in the lists directory and the badge below indicates if the script executed successfully.

[![Update NRD list](https://github.com/dontcrash/homelab/actions/workflows/main.yml/badge.svg)](https://github.com/dontcrash/homelab/actions/workflows/main.yml)
