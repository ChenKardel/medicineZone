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
    name = getContent(drug_root.find("name"))

    # find description
    description = getContent(drug_root.find('description'))

    # find cas-number
    casNumber = getContent(drug_root.find('cas-number'))

    # find unii
    unii = getContent(drug_root.find('unii'))

    # find state
    state = getContent(drug_root.find('state'))
    find_all_elements = lambda subtree_root, tag: [getContent(sub) for sub in subtree_root.findall(tag)]

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
        pubmed_id = getContent(article.find("pubmed-id"))
        citation = getContent(article.find("citation"))
        drugArticleList.append({'pubmed_id': pubmed_id, 'citation': citation})
    print(drugArticleList)
    # find textbook
    textbooks_root = general_references.find("textbooks")
    textbooks = textbooks_root.findall("textbook")
    drugTextbookList = []
    for textbook in textbooks:
        isbn = getContent(textbook.find("isbn"))
        citation = getContent(textbook.find("citation"))
        drugTextbookList.append({'isbn': isbn, 'citation': citation})
    print(drugArticleList)
    # links
    links_root = general_references.find("links")
    links = links_root.findall("link")
    drugLinkList = []
    for link in links:
        title = getContent(link.find("title"))
        url = getContent(link.find("url"))
        drugLinkList.append({'title': title, 'url': url})
    print(drugArticleList)

    synthesisReference = getContent(drug_root.find("synthesis-reference"))
    indication = getContent(drug_root.find("indication"))
    pharmacodynamics = getContent(drug_root.find("pharmacodynamics"))
    mechanismOfAction = getContent(drug_root.find("mechanism-of-action"))
    toxicity = getContent(drug_root.find("toxicity"))
    metabolism = getContent(drug_root.find("metabolism"))
    absorption = getContent(drug_root.find("absorption"))
    halfLife = getContent(drug_root.find("half-life"))
    proteinBinding = getContent(drug_root.find("protein-binding"))
    routeOfElimination = getContent(drug_root.find("route-of-elimination"))
    volumeOfDistribution = getContent(drug_root.find("volume-of-distribution"))
    clearance = getContent(drug_root.find())
    classification_root = drug_root.find("classification")
    if classification_root is None:
        classification_description = getContent(classification_root.find("description"))
        classification_directParent = getContent(classification_root.find("direct-parent"))
        classification_kingdom = getContent(classification_root.find("kingdom"))
        classification_superclass = getContent(classification_root.find("superclass"))
        classification_class = getContent(classification_root.find("class"))
        classification_subclass = getContent(classification_root.find("subclass"))
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
        product_name = getContent(product.find("name"))
        product_labeller = getContent(product.find("labeller"))
        product_ndcId = getContent(product.find("ndc-id"))
        product_ndcProductCode = getContent(product.find("ndc-product-code"))
        product_dpdId = getContent(product.find("dpd-id"))
        product_emaProductCode = getContent(product.find("ema-product-code"))
        product_emaMaNumber = getContent(product.find("ema-ma-number"))
        product_startedMarketingOn = getContent(product.find("started-marketing-on"))
        product_endedMarketingOn = getContent(product.find("ended-marketing-on"))
        product_dosageForm = getContent(product.find('dosage-form'))
        product_strength = getContent(product.find('strength'))
        product_route = getContent(product.find('route'))
        product_fdaApplicationNumber = getContent(product.find('fda-application-number'))
        product_generic = getContent(product.find("generic"))
        product_overTheCounter = getContent(product.find('over-the-counter'))
        product_approved = getContent(product.find('approved'))
        product_country = getContent(product.find("country"))
        product_source = getContent(product.find("source"))
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
        internationalBrand_name = getContent(internationalBrand.find("name"))
        internationalBrand_company = getContent(internationalBrand.find("company"))
        internationalBrandsList.append({"name": internationalBrand_name, "company": internationalBrand_company})

    mixtures_root = drug_root.find('mixtures')
    mixtures = mixtures_root.findall('mixture')
    mixturesList = []
    for mixture in mixtures:
        mixture_name = getContent(mixture.find("name"))
        mixture_ingredients = getContent(mixture.find("ingredients"))
        mixturesList.append({'name': mixture_name, 'ingredients': mixture_ingredients})

    packagers_root = drug_root.find('packagers')
    packagers = packagers_root.findall('packager')
    packagersList = []
    for packager in packagers:
        packager_name = getContent(packager.find("name"))
        packager_url = getContent(packager.find("url"))
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

    prices_root = drug_root.find('prices')
    prices = prices_root.findall('price')
    pricesList = []
    for price in prices:
        price_description = getContent(price.find('description'))
        currency = price.attrib['currency']
        price_cost = currency + ": " + getContent(price.find('cost'))
        price_unit = price.find('unit').text
        pricesList.append({
            'description': price_description,
            'cost': price_cost,
            'unit': price_unit
        })

    categories_root = drug_root.find('categories')
    categories = categories_root.findall('category')
    categoriesList = []
    for category in categories:
        category_category = getContent(category.find('category'))
        category_mesh_id = getContent(category.find('mesh-id'))
        categoriesList.append({
            'category': category_category,
            'mesh-id': category_mesh_id
        })

    affected_organisms_root = drug_root.find("affected_organisms")
    affected_organisms = affected_organisms_root.findall('affected_organism')
    affected_organismsList = [i.text for i in affected_organisms]

    dosages_root = drug_root.find("dosages")
    dosages = dosages_root.findall("dosage")
    dosagesList = []
    for dosage in dosages:
        dosage_form = getContent(dosage.find('form'))
        dosage_route = getContent(dosage.find('route'))
        dosage_strength = getContent(dosage.find('strength'))
        dosagesList.append({
            'form': dosage_form,
            'route': dosage_route,
            'strength': dosage_strength
        })

    atcCodes_root = drug_root.find('atc-codes')
    atcCodes = atcCodes_root.findall('atc-code')
    atcCodesList = []
    for atcCode in atcCodes:
        atcCode_code = atcCode.attrib['code']
        atcCode_levels = atcCode.findall('level')
        atcCode_levelsList = []
        for atcCode_level in atcCode_levels:
            level_code = atcCode_level.attrib['code']
            level_content = getContent(atcCode_level)
            atcCode_levelsList.append({
                'code': level_code,
                'content': level_content
            })
        atcCodesList.append({
            'code': atcCode_code,
            'levels': atcCode_levelsList
        })

    ahfs_codes_root = drug_root.find('ahfs-codes')
    ahfs_codesList = [i.text for i in ahfs_codes_root.findall('ahfs-code')]

    pdb_entries_root = drug_root.find('pdb-entries')
    pdb_entriesList = [i.text for i in pdb_entries_root.findall('pdb-entry')]

    fda_label = getContent(drug_root.find('fda_label'))
    msds = getContent(drug_root.find('msds'))

    patents_root = drug_root.find('patents')
    patents = patents_root.findall('patent')
    patentsList = []
    for patent in patents:
        patent_number = getContent(patent.find('number'))
        patent_country = getContent(patent.find('country'))
        patent_approved = getContent(patent.find('approved'))
        patent_expires = getContent(patent.find('expires'))
        patent_pediatric_extension = getContent(patent.find('pediatric-extension'))
        patentsList.append({
            'number': patent_number,
            'country': patent_country,
            'approved': patent_approved,
            'expires': patent_expires,
            'pediatric-extension': patent_pediatric_extension
        })
    foodInteractions_root = drug_root.find('food-interactions')
    foodInteractionsList = [i.text for i in foodInteractions_root.findall('food-interaction')]

    drugInteractions_root = drug_root.find('drug-interactions')
    drugInteractions = drugInteractions_root.findall('drug-interaction')
    drugInteractionsList = []
    for drugInteraction in drugInteractions:
        drugInteraction_drugbank_id = getContent(drugInteraction.find('drugbank-id'))
        drugInteraction_name = getContent(drugInteraction.find('name'))
        drugInteraction_description = getContent(drugInteraction.find('description'))
        drugInteractionsList.append({
            'drugbank-id': drugInteraction_drugbank_id,
            'name': drugInteraction_name,
            'description': drugInteraction_description
        })

    sequences_root = drug_root.find('sequences')
    sequences = sequences_root.findall('sequence')
    sequencesList = [i.text for i in sequences]

    experimentalProperties_root = drug_root.find('experimental-properties')
    properties = experimentalProperties_root.findall('property')
    propertiesList = []
    for property in properties:
        property_kind = getContent(property.find('kind'))
        property_value = getContent(property.find('value'))
        property_source = getContent(property.find('source'))
        propertiesList.append({
            'kind': property_kind,
            'value': property_value,
            'source': property_source
        })

    externalIdentifiers_root = drug_root.find('external-identifiers')
    externalIdentifiers = externalIdentifiers_root.findall('external-identifier')
    externalIdentifiersList = []
    for externalIdentifier in externalIdentifiers:
        externalIdentifier_resource = getContent(externalIdentifier.find('resource'))
        externalIdentifier_identifier = getContent(externalIdentifier.find('identifier'))
        externalIdentifiersList.append({
            'resource': externalIdentifier_resource,
            'identifier': externalIdentifier_identifier
        })

    externalLinks_root = drug_root.find('external-links')
    externalLinks = externalLinks_root.findall('external-link')
    externalLinksList = []
    for externalLink in externalLinks:
        externalLink_resource = getContent(externalLink.find('resource'))
        externalLink_url = getContent(externalLink.find('url'))
        externalLinksList.append({
            'resource': externalLink_resource,
            'url': externalLink_url
        })

    pathways_root = drug_root.find('pathways')
    pathways = pathways_root.findall('pathway')
    pathwaysList = []
    for pathway in pathways:
        pathway_smpdbId = getContent(pathway.find('smpdb-id'))
        pathway_name = getContent(pathway.find('name'))
        pathway_category = getContent(pathway.find('category'))

        pathway_drugs_root = pathway.find('drugs')
        pathway_drugs = pathway_drugs_root.findall('drug')
        pathway_drugsList = []
        for pathway_drug in pathway_drugs:
            pathway_drug_drugbank_id = getContent(pathway_drug.find('drugbank-id'))
            pathway_drug_name = getContent(pathway_drug.find('name'))
            pathway_drugsList.append({
                'drugbank-id': pathway_drug_drugbank_id,
                'name': pathway_drug_name
            })

        enzymes = [i.text for i in pathway.find('enzymes').findall('uniprot-id')]

    reactions_root = drug_root.find('reactions')
    reactions = reactions_root.findall('reaction')
    reactionsList = []
    for reaction in reactions:
        reaction_sequence = reaction.find('sequence')
        reaction_left_element_root = reaction.find('left-element')
        reaction_left_element_drugbank_id = getContent(reaction_left_element_root.find('drugbank-id'))
        reaction_left_element_name = getContent(reaction_left_element_root.find('name'))

        reaction_right_element_root = reaction.find('right-element')
        reaction_right_element_drugbank_id = getContent(reaction_right_element_root.find('drugbank-id'))
        reaction_right_element_name = getContent(reaction_right_element_root.find('name'))

        reaction_enzymes_root = reaction.find('enzymes')
        reaction_enzymes = reaction_enzymes_root.findall('enzyme')
        reaction_enzymesList = []
        for reaction_enzyme in reaction_enzymes:
            reaction_enzyme_drugbank_id = getContent(reaction_enzyme.find('drugbank-id'))
            reaction_enzyme_name = getContent(reaction_enzyme.find('name'))
            reaction_enzyme_uniprot_id = getContent(reaction_enzyme.find('uniprot-id'))
            reaction_enzymesList.append({
                'drugbank-id': reaction_enzyme_drugbank_id,
                'name': reaction_enzyme_name,
                'uniprot-id': reaction_enzyme_uniprot_id
            })
        reactionsList.append({
            'sequence': reaction_sequence,
            'left-element': {
                'drugbank-id': reaction_left_element_drugbank_id,
                'name': reaction_left_element_name
            },
            'right-element': {
                'drugbank-id': reaction_right_element_drugbank_id,
                'name': reaction_right_element_name
            },
            'enzymes': reaction_enzymesList
        })

    snp_effects_root = drug_root.find('snp-effects')
    snp_effects = snp_effects_root.findall('effect')
    snp_effectsList = []
    for snp_effect in snp_effects:
        snp_effect_protein_name = getContent(snp_effect.find('protein-name'))
        snp_effect_gene_symbol = getContent(snp_effect.find('gene-symbol'))
        snp_effect_uniprot_id = getContent(snp_effect.find('uniprot-id'))
        snp_effect_allele = getContent(snp_effect.find('allele'))
        snp_effect_defining_change = getContent(snp_effect.find('defining-change'))
        snp_effect_description = getContent(snp_effect.find('description'))
        snp_effect_pubmed_id = getContent(snp_effect.find('pubmed-id'))
        snp_effectsList.append({
            'ptotein-name': snp_effect_protein_name,
            'gene-symbol': snp_effect_gene_symbol,
            'uniprot-id': snp_effect_uniprot_id,
            'allele': snp_effect_allele,
            'defining-change': snp_effect_defining_change,
            'pubmed-id': snp_effect_pubmed_id,
            'description': snp_effect_description
        })

    snp_adverse_drug_reactions_root = drug_root.find('snp-adverse-drug-reactions')
    snp_adverse_drug_reactions = snp_adverse_drug_reactions_root.findall('reaction')
    snp_adverse_drug_reactionsList = []
    for snp_adverse_drug_reaction in snp_adverse_drug_reactions:
        snp_adverse_drug_reaction_protein_name = getContent(snp_adverse_drug_reaction.find('protein-name'))
        snp_adverse_drug_reaction_gene_symbol = getContent(snp_adverse_drug_reaction.find('gene-symbol'))
        snp_adverse_drug_reaction_uniprot_id = getContent(snp_adverse_drug_reaction.find('uniprot-id'))
        snp_adverse_drug_reaction_allele = getContent(snp_adverse_drug_reaction.find('allele'))
        snp_adverse_drug_reaction_defining_change = getContent(snp_adverse_drug_reaction.find('defining-change'))
        snp_adverse_drug_reaction_description = getContent(snp_adverse_drug_reaction.find('description'))
        snp_adverse_drug_reaction_pubmed_id = getContent(snp_adverse_drug_reaction.find('pubmed-id'))
        snp_adverse_drug_reactionsList.append({
            'ptotein-name': snp_adverse_drug_reaction_protein_name,
            'gene-symbol': snp_adverse_drug_reaction_gene_symbol,
            'uniprot-id': snp_adverse_drug_reaction_uniprot_id,
            'allele': snp_adverse_drug_reaction_allele,
            'defining-change': snp_adverse_drug_reaction_defining_change,
            'pubmed-id': snp_adverse_drug_reaction_pubmed_id,
            'description': snp_adverse_drug_reaction_description
        }
        )

    targets_root = drug_root.find('targets')
    targets = targets_root.findall('target')
    targetsList = []
    for target in targets:
        target_id = getContent(target.find('id'))
        target_name = getContent(target.find('name'))
        target_organism = getContent(target.find('organism'))
        actions_root = getContent(target.find('actions'))
        target_actions = [getContent(i) for i in actions_root.findall('action')]

        target_articles_root = target.find('articles')
        target_articles = target_articles_root.findall('article')
        target_articlesList = []
        for target_article in target_articles:
            target_article_pubmed_id = getContent(target_article.find('pubmed-id'))
            target_article_citation = getContent(target_article.find('citation'))
            target_articlesList.append({
                'pubmed-id': target_article_pubmed_id,
                'citation': target_article_citation
            })

        target_textbooks_root = target.find("textbooks")
        target_textbooks = target_textbooks_root.findall("textbook")
        target_textbookList = []
        for target_textbook in target_textbooks:
            target_isbn = getContent(target_textbook.find("isbn"))
            target_citation = getContent(target_textbook.find("citation"))
            target_textbookList.append({'isbn': target_isbn, 'citation': target_citation})

        target_links_root = general_references.find("links")
        target_links = target_links_root.findall("link")
        target_LinkList = []
        for target_link in target_links:
            target_title = getContent(target_link.find("title"))
            target_url = getContent(target_link.find("url"))
            target_LinkList.append({'title': target_title, 'url': target_url})

        target_known_action = getContent(target.find('known-action'))

        target_polypetide = target.find('polypeptide')
        polypetide_id = target.attrib["id"]
        polypetide_source = target.attrib["source"]
        polypetide_name = getContent(target_polypetide.find('name'))
        polypetide_general_function = getContent(target_polypetide.find('general-function'))
        polypetide_specific_function = getContent(target_polypetide.find('specific-function'))
        polypetide_gene_name = getContent(target_polypetide.find('gene-name'))
        polypetide_locus = getContent(target_polypetide.find('locus'))
        polypetide_cellular_location = getContent(target_polypetide.find('cellular-location'))
        polypetide_transmembrane_regions = getContent(target_polypetide.find('transmembrane-regions'))
        polypetide_signal_regions = getContent(target_polypetide.find('signal-regions'))
        polypetide_theoretical_pi = getContent(target_polypetide.find('theoretical-pi'))
        polypetide_molecular_weight = getContent(target_polypetide.find('molecular-weight'))
        polypetide_chromosome_location = getContent(target_polypetide.find('chromosome-location'))
        polypetide_organism = getContent(target_polypetide.find('organism'))
        polypetide_organism_ncbi_taxonomy_id = target_polypetide.find('organism').attrib['ncbi-taxonomy-id']

        polypetide_externalIdentifiers_root = target_polypetide.find('external-identifiers')
        polypetide_externalIdentifiers = polypetide_externalIdentifiers_root.findall('external-identifier')
        polypetide_externalIdentifiersList = []
        for polypetide_externalIdentifier in polypetide_externalIdentifiers:
            polypetide_externalIdentifier_resource = getContent(polypetide_externalIdentifier.find('resource'))
            polypetide_externalIdentifier_identifier = getContent(polypetide_externalIdentifier.find('identifier'))
            polypetide_externalIdentifiersList.append({
                'resource': polypetide_externalIdentifier_resource,
                'identifier': polypetide_externalIdentifier_identifier
            })

        polypetide_synonym_root = target_polypetide.find("synonyms")
        polypetide_synonyms = [getContent(i) for i in polypetide_synonym_root.findall("synonym")]
        polypetide_amino_acid_sequence = getContent(target_polypetide.find('amino-acid-sequence'))
        polypetide_gene_sequence = getContent(target_polypetide.find('gene-sequence'))

        polypetide_pfams_root = target_polypetide.find('pfams')
        polypetide_pfams = target_polypetide.findall('pfam')
        for polypetide_pfam in polypetide_pfams:
            polypetide_identifier = getContent(polypetide_pfam.find('identifier'))
            polypetide_name = getContent(polypetide_pfam.find('name'))






        targetsList.append({
            'id': target_id,
            'name': target_name,
            'organism': target_organism,
            'actions': target_actions,
            'articles': target_articlesList,
            'textbooks': target_textbookList,
            'links': target_LinkList
        })


def getContent(node):
    if node is None:
        return None
    else:
        return node.text


parseXml("partial.xml")
