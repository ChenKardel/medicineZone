from xml.etree import ElementTree as ET

tree = ET.parse("test.xml")
root = tree.getroot()

drug_root = root.find("drug")
print(drug_root.find("description") is None)