import xml.etree.ElementTree as ET

def parse_bioc_xml(xml_text):
    """
    Parse BioC XML and return metadata and sections.
    """
    try:
        root = ET.fromstring(xml_text)
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

    pmc_id = root.find(".//id").text if root.find(".//id") is not None else ""
    doi = ""
    title = ""
    authors = []
    date = ""
    license_use = ""

    #  To extract DOI, license, year
    for infon in root.iter("infon"):
        key = infon.attrib.get("key", "")
        text = infon.text or ""
        if key == "article-id_doi":
            doi = text
        elif key.startswith("name_"):
            authors.append(text)
        elif key == "year":
            date = text
        elif key == "license":
            license_use = text

    # Sections
    sections = {"Abstract": "", "Introduction": "", "Methods": "", "Results": "", "Conclusion": "", "References": ""}
    for passage in root.findall(".//passage"):
        section_type_elem = passage.find(".//infon[@key='section_type']")
        text_elem = passage.find(".//text")
        if section_type_elem is not None and text_elem is not None:
            section_key = section_type_elem.text.upper()
            if "ABSTRACT" in section_key:
                sections["Abstract"] += text_elem.text.strip() + " "
            elif "INTRO" in section_key:
                sections["Introduction"] += text_elem.text.strip() + " "
            elif "METHOD" in section_key:
                sections["Methods"] += text_elem.text.strip() + " "
            elif "RESULT" in section_key:
                sections["Results"] += text_elem.text.strip() + " "
            elif "CONCL" in section_key:
                sections["Conclusion"] += text_elem.text.strip() + " "
            elif "REF" in section_key:
                sections["References"] += text_elem.text.strip() + " "

    return {
        "PMC_ID": pmc_id,
        "DOI": doi,
        "Title": title,
        "Authors": "; ".join(authors),
        "Publication Date": date,
        "License": license_use,
        **sections
    }