from xml.etree import ElementTree as ET

tree = ET.parse("test.xml")
root = tree.getroot()

drug_root = root.find("drug")
# classification_root = drug_root.find("classification")
# classification_description = classification_root.find("description").text
# classification_directParent = classification_root.find("direct-parent").text
# classification_kingdom = classification_root.find("kingdom").text
# classification_superclass = classification_root.find("superclass").text
# classification_class = classification_root.find("class").text
# classification_subclass = classification_root.find("subclass").text
#
# print(type(classification_description))
# print(type(classification_directParent))
# print(type(classification_kingdom))
# print(type(classification_superclass))
# print(type(classification_class))
# print(type(classification_subclass))

synonyms = drug_root.find("synonyms")
for synonym in synonyms.findall("synonym"):
    language = synonym.attrib["language"]
    coder = synonym.attrib["coder"]
    synonym_content = synonym.text
    print(synonym_content)
