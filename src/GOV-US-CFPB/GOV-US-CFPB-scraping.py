import requests
from bs4 import BeautifulSoup
import csv
import re
import os
from pathlib import Path

data_path = Path(__file__).parents[2] / "data" / "GOV-US-CFPB"
out_data_path = data_path / "raw"

with (data_path / "GOV-US-CFPB-links.txt").open("r") as file:
    links = file.readlines()

# a function to find the tags we want:
def tag_constraint(tag):
    if tag.has_attr("class") & tag.has_attr("href"):
        if "icon-link__download" in tag.get("class"):
            return True
    else:
        return False

for link in links:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html5lib")

    all_csv_links = [tag["href"] for tag in soup.find_all(tag_constraint)]
    unique_csv_links = list(set(all_csv_links))

    for csv_link in unique_csv_links:

        csv_request = requests.get(csv_link)
        csv_decoded_content = csv_request.content.decode("utf-8")
        csv_reader = csv.reader(csv_decoded_content.splitlines())

        csv_name = re.sub("^.*/(.*\\.csv)$", "\\1",csv_link)
        csv_lines = list(csv_reader)

        with (out_data_path / csv_name).open("w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(csv_lines)
