import xml.etree.ElementTree as ET
import csv
import re


def clean_xml(xml_str: str) -> str:
    """
    Remove invalid XML characters from a given string.

    Parameters:
    - xml_str (str): XML string to clean.

    Returns:
    - str: Cleaned XML string.
    """
    xml_str = (
        xml_str.replace('xmlns=""', 'xmlns="')
        .replace('""http', '"http')
        .replace('StoreSurvey"">', 'StoreSurvey">')
    )
    return re.sub(r"[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD]", "", xml_str)


def parse_xml_to_dict(xml_str: str) -> dict:
    """
    Parse an XML string to a dictionary.

    Parameters:
    - xml_str (str): XML string to parse.

    Returns:
    - dict: Dictionary with XML tags as keys and text as values.
    """
    xml_str = clean_xml(xml_str)
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}


def main():
    """
    Main function to read a TSV file, parse XML strings and write the new rows into a new TSV file.
    """
    with (
        open("data/processed/Store.csv", "r") as infile,
        open("data/processed_xml/Store.csv", "w", newline="") as outfile,
    ):
        csvreader = csv.reader(infile, delimiter="\t")
        csvwriter = csv.writer(outfile, delimiter="\t")

        for row in csvreader:
            xml_str = row.pop(3)
            xml_dict = parse_xml_to_dict(xml_str)
            row.extend(xml_dict.values())
            csvwriter.writerow(row)
        print(
            [
                col.replace(
                    "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}",
                    "",
                )
                for col in list(xml_dict.keys())
            ]
        )


if __name__ == "__main__":
    example_xml = '<StoreSurvey xmlns=""http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey""><AnnualSales>3000000</AnnualSales><AnnualRevenue>300000</AnnualRevenue><BankName>Primary Bank &amp; Reserve</BankName><BusinessType>OS</BusinessType><YearOpened>1974</YearOpened><Specialty>Mountain</Specialty><SquareFeet>75000</SquareFeet><Brands>2</Brands><Internet>T1</Internet><NumberEmployees>93</NumberEmployees></StoreSurvey>'
    main()
