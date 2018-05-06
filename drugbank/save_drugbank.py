import time
import xml.dom as dom
from _elementtree import Element
from xml.etree import ElementTree as ET


# from drugbank.models import *


def parseXml(xmlFile):
    # drug = Drug()
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    drug_root = root.find("drug")
    drugbankIds = drug_root.findall("drugbank-id")

    # find ids of drugs
    drugbankIdsList = []
    for drugbankId in drugbankIds:
        if "primary" in drugbankId.attrib and drugbankId.attrib["primary"] == 'true':
            drugbankIdsList.insert(0, drugbankId.text)
        else:
            drugbankIdsList.append(drugbankId.text)
    print(drugbankIdsList)

    # find name
    name = drug_root.find("name").text

    # find description
    description = drug_root.find('description').text

    # find cas-number
    casNumber = drug_root.find('cas-number').text

    # find unii
    unii = drug_root.find('unii').text

    # find state
    state = drug_root.find('state').text
    find_all_elements = lambda subtree_root, tag: [sub.text for sub in subtree_root.findall(tag)]

    # find groups
    group_root = drug_root.find('groups')
    groups = find_all_elements(group_root, 'group')
    # groups = [group.text for group in group_root.findall('group')]
    print(groups)

    # find general-references
    general_references = drug_root.find("general-references")
    # find articles
    articles_root = general_references.find("articles")
    articles = articles_root.findall("article")
    drugArticleList = []
    for article in articles:
        pubmed_id = article.find("pubmed-id").text
        citation = article.find("citation").text
        drugArticleList.append({'pubmed_id': pubmed_id, 'citation': citation})
    print(drugArticleList)
    # find textbook
    textbooks_root = general_references.find("textbooks")
    textbooks = textbooks_root.findall("textbook")
    drugTextbookList = []
    for textbook in textbooks:
        isbn = textbook.find("isbn").text
        citation = textbook.find("citation").text
        drugTextbookList.append({'isbn': isbn, 'citation': citation})
    print(drugArticleList)
    # links
    links_root = general_references.find("links")
    links = links_root.findall("link")
    drugLinkList = []
    for link in links:
        title = link.find("title").text
        url = link.find("url").text
        drugLinkList.append({'title': title, 'url': url})
    print(drugArticleList)

    synthesisReference = drug_root.find("synthesis-reference").text
    indication = drug_root.find("indication").text
    pharmacodynamics = drug_root.find("pharmacodynamics").text
    mechanismOfAction = drug_root.find("mechanism-of-action").text
    toxicity = drug_root.find("toxicity").text
    metabolism = drug_root.find("metabolism").text
    absorption = drug_root.find("absorption").text
    halfLife = drug_root.find("half-life").text
    proteinBinding = drug_root.find("protein-binding").text
    routeOfElimination = drug_root.find("route-of-elimination").text
    volumeOfDistribution = drug_root.find("volume-of-distribution").text
    clearance = drug_root.find().text
    classification_root = drug_root.find("classification")
    if classification_root is None:
        classification_description = classification_root.find("description").text
        classification_directParent = classification_root.find("direct-parent").text
        classification_kingdom = classification_root.find("kingdom").text
        classification_superclass = classification_root.find("superclass").text
        classification_class = classification_root.find("class").text
        classification_subclass = classification_root.find("subclass").text
        # todo: save in database
    else:
        # todo: save None in database, classification of this drug there is None
        pass

    synonym_root = drug_root.find("synonyms")
    synonyms = synonym_root.findall("synonym")
    synonymsList = []
    for synonym in synonyms:
        language = synonym.attrib["language"]
        coder = synonym.attrib["coder"]
        synonym_content = synonym.text
        synonymsList.append({"language": language, "coder": coder, "content": synonym_content})
    products_root = drug_root.find('products')
    products = products_root.findall('product')
    productsList = []
    for product in products:
        product_name = product.find("name").text
        product_labeller = product.find("labeller").text
        product_ndcId = product.find("ndc-id").text
        product_ndcProductCode = product.find("ndc-product-code").text
        product_dpdId = product.find("dpd-id").text
        product_emaProductCode = product.find("ema-product-code").text
        product_emaMaNumber = product.find("ema-ma-number").text
        product_startedMarketingOn = product.find("started-marketing-on").text
        product_endedMarketingOn = product.find("ended-marketing-on").text
        product_dosageForm = product.find('dosage-form').text
        product_strength = product.find('strength').text
        product_route = product.find('route').text
        product_fdaApplicationNumber = product.find('fda-application-number').text
        product_generic = product.find("generic").text
        product_overTheCounter = product.find('over-the-counter').text
        product_approved = product.find('approved').text
        product_country = product.find("country").text
        product_source = product.find("source").text
        productsList.append({
            "name": product_name,
            "labeller": product_labeller,
            "ndcId": product_ndcId,
            "ndcProductCode": product_ndcProductCode,
            "dpdId": product_dpdId,
            "emaProductCode": product_emaProductCode,
            "emaMaNumber": product_emaMaNumber,
            "startedMarketingOn": product_startedMarketingOn,
            "endedMarketingOn": product_endedMarketingOn,
            "dosageForm": product_dosageForm,
            "strength": product_strength,
            "route": product_route,
            "fdaApplicationNumber": product_fdaApplicationNumber,
            "generic": product_generic,
            "overTheCounter": product_overTheCounter,
            "approved": product_approved,
            "country": product_country,
            "source": product_source
        })

    internationalBrand_root = drug_root.find("international-brands")
    internationalBrands = internationalBrand_root.findall("international-brand")
    internationalBrandsList = []
    for internationalBrand in internationalBrands:
        internationalBrand_name = internationalBrand.find("name").text
        internationalBrand_company = internationalBrand.find("company").text
        internationalBrandsList.append({"name": internationalBrand_name, "company": internationalBrand_company})

    mixtures_root = drug_root.find('mixtures')
    mixtures = mixtures_root.findall('mixture')
    mixturesList = []
    for mixture in mixtures:
        mixture_name = mixture.find("name").text
        mixture_ingredients = mixture.find("ingredients").text
        mixturesList.append({'name': mixture_name, 'ingredients': mixture_ingredients})

    packagers_root = drug_root.find('packagers')
    packagers = packagers_root.findall('packager')
    packagersList = []
    for packager in packagers:
        packager_name = packager.find("name").text
        packager_url = packager.find("url").text
        packagersList.append({'name': packager_name, 'url': packager_url})

    manufacturers_root = drug_root.find('manugacturers')
    manufacturers = manufacturers_root.findall('manufacturer')
    manufacturersList = []
    for manufacturer in manufacturers:
        manufacturer_generic = manufacturer.attrib["generic"]
        manufacturer_url = manufacturer.attrib["url"]
        manufacturer_content = manufacturer.text
        manufacturersList.append({
            "generic": manufacturer_generic,
            "url": manufacturer_url,
            "content": manufacturer_content
        })


parseXml("partial.xml")
