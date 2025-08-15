import xml.etree.ElementTree as ET

def prase_xml(xml_txt):
    root = ET.fromstring(xml_txt)

    data = {
        "PMC ID" : "",
        "DOI" : "",
        "Title" : "",
        "Authors" : "",
        "Abstrct" : "",
        "Introduction" : "",
        "Methods" : "",
        "Result" : "",
        "Conclusion" : "",
        "References" : "",
        "License" : ""
    }
    
    author_list = []
    