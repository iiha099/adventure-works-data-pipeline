from pipeline.process_store import parse_xml_to_dict
import pathlib

challenge_path = pathlib.Path(__file__).parent.parent.absolute()


def test_parse_xml_to_dict():
    example_xml = '<StoreSurvey xmlns=""http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey""><AnnualSales>3000000</AnnualSales><AnnualRevenue>300000</AnnualRevenue><BankName>Primary Bank &amp; Reserve</BankName><BusinessType>OS</BusinessType><YearOpened>1974</YearOpened><Specialty>Mountain</Specialty><SquareFeet>75000</SquareFeet><Brands>2</Brands><Internet>T1</Internet><NumberEmployees>93</NumberEmployees></StoreSurvey>'
    processed_xml = parse_xml_to_dict(example_xml)
    target_xml = {
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualSales": "3000000",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualRevenue": "300000",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BankName": "Primary Bank & Reserve",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BusinessType": "OS",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}YearOpened": "1974",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Specialty": "Mountain",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}SquareFeet": "75000",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Brands": "2",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Internet": "T1",
        "{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}NumberEmployees": "93",
    }

    assert isinstance(processed_xml, dict), "Function output is not a dictionary"
    assert processed_xml == target_xml


def test_store_csv():
    with open(challenge_path / "data" / "processed_xml" / "Store.csv", "r") as f:
        first_line = f.readline().strip().split("\t")

    expected_first_line = [
        "292",
        "Next-Door Bike Store",
        "279",
        "A22517E3-848D-4EBE-B9D9-7437F3432304",
        "2025-09-11 11:15:07.497",
        "800000",
        "80000",
        "United Security",
        "BM",
        "1996",
        "Mountain",
        "21000",
        "2",
        "ISDN",
        "13",
    ]

    assert len(first_line) == len(expected_first_line), "Incorrect number of columns"
    assert first_line == expected_first_line, "Ensure the column order is correct"
