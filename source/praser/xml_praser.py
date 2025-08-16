import xml.etree.ElementTree as ET

def prase_xml(xml_txt):
    try:
        root = ET.fromstring(xml_txt)
    except Exception as e:
        print(f"XML Prasing error: {e}")
        return None
    
    title = ""
    authors = []
    date = ""
    license_use = ""
    can_use = "No"

    sections = {
        "Abstract" : "",
        "Introduction": "",
        "Methods" : "",
        "Results" : "",
        "Conclusion" : "",
        "References" : ""
    }
    
    try:
        for passage in root.findall(".//passage"):
            section_type_elem = passage.find(".//infon[@key='section_type']")
            text_elem = passage.find(".//text")
            section_type = section_type_elem.text.strip() if section_type_elem is not None else None
            text = text_elem.text.strip() if text_elem is not None else ""

            #for title
            if section_type == "Title" and not title:
                title = text

            # Append text to section if exists
            if section_type in sections and text:
                if sections[section_type]:
                    sections[section_type] += "/n" + text
                else:
                    sections[section_type] = text
    except Exception as e:
        print(f"Error extracting sections: {e}")

    # For extracting author, year liscense 
    try:
        for infon in root.iter("infon"):
            key = infon.attrib.get("key", "")
            if key.startswith("name_"):
                authors.append(infon.text.strip() if infon.text else "")
            elif key == "year":
                date = infon.text.strip() if infon.text else ""
            elif key == "license":
                license_use = infon.text or ""
            if any(keyword in license_use.lower() for keyword in ["cc-by","cc0", "public domain", "cc by", "cc-by-4.0"]):
                can_use = "Yes"

    except Exception as e:
        print(f"Error extracting metadata: {e}")

    # combine all of the results
    result = {
        "Title": title,
        "Authors" :";" .join(authors),
        "Publication Date" : date,
        "License" : license_use,
        "Can use" : can_use
    }

    result.update(sections)
    return result