import time
import xml.dom as dom
from _elementtree import Element
from xml.etree import ElementTree as ET

from drugbank.models import *


def parseXml(xmlFile):
    # drug = Drug()
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    for drug_root in root.findall("drug"):
        saveDrug(drug_root)



def saveDrug(drug_root):
    drug = Drug()
    drugbankIds = drug_root.findall("drugbank-id")

    # find ids of drugs
    drugbankIdsList = []
    for drugbankId in drugbankIds:
        if "primary" in drugbankId.attrib and drugbankId.attrib["primary"] == 'true':
            drugbankIdsList.insert(0, drugbankId.text)
        else:
            drugbankIdsList.append(drugbankId.text)
    drug.drugbankId = drugbankIdsList
    # find name
    name = getContent(drug_root.find("name"))
    drug.name = name
    # find description
    description = getContent(drug_root.find('description'))
    drug.description = description
    # find cas-number
    casNumber = getContent(drug_root.find('cas-number'))
    drug.casNumber = casNumber

    # find unii
    unii = getContent(drug_root.find('unii'))
    drug.unii = unii

    # find state
    state = getContent(drug_root.find('state'))
    drug.state = state

    # woc我忘了我写了这个函数
    find_all_elements = lambda subtree_root, tag: [getContent(sub) for sub in subtree_root.findall(tag)]

    # find groups
    group_root = drug_root.find('groups')
    groups = find_all_elements(group_root, 'group')
    drug.groups = groups

    # find general-references
    # ignore start
    # general_references = drug_root.find("general-references")
    # # find articles
    # articles_root = general_references.find("articles")
    # articles = articles_root.findall("article")
    # drugArticleList = []
    # for article in articles:
    #     pubmed_id = getContent(article.find("pubmed-id"))
    #     citation = getContent(article.find("citation"))
    #     drugArticleList.append({'pubmed_id': pubmed_id, 'citation': citation})
    # print(drugArticleList)
    # # find textbook
    # textbooks_root = general_references.find("textbooks")
    # textbooks = textbooks_root.findall("textbook")
    # drugTextbookList = []
    # for textbook in textbooks:
    #     isbn = getContent(textbook.find("isbn"))
    #     citation = getContent(textbook.find("citation"))
    #     drugTextbookList.append({'isbn': isbn, 'citation': citation})
    # print(drugArticleList)
    # # links
    # links_root = general_references.find("links")
    # links = links_root.findall("link")
    # drugLinkList = []
    # for link in links:
    #     title = getContent(link.find("title"))
    #     url = getContent(link.find("url"))
    #     drugLinkList.append({'title': title, 'url': url})
    # print(drugArticleList)
    # ignore end

    synthesisReference = getContent(drug_root.find("synthesis-reference"))
    drug.synthesisReference = synthesisReference

    indication = getContent(drug_root.find("indication"))
    drug.indication = indication

    pharmacodynamics = getContent(drug_root.find("pharmacodynamics"))
    drug.pharmacodynamics = pharmacodynamics

    mechanismOfAction = getContent(drug_root.find("mechanism-of-action"))
    drug.mechanismOfAction = mechanismOfAction

    toxicity = getContent(drug_root.find("toxicity"))
    drug.toxicity = toxicity

    metabolism = getContent(drug_root.find("metabolism"))
    drug.metabolism = metabolism

    absorption = getContent(drug_root.find("absorption"))
    drug.absorption = absorption

    halfLife = getContent(drug_root.find("half-life"))
    drug.halfLife = halfLife

    proteinBinding = getContent(drug_root.find("protein-binding"))
    drug.proteinBinding = proteinBinding

    routeOfElimination = getContent(drug_root.find("route-of-elimination"))
    drug.routeOfElimination = routeOfElimination

    volumeOfDistribution = getContent(drug_root.find("volume-of-distribution"))
    drug.volumeOfDistribution = volumeOfDistribution

    clearance = getContent(drug_root.find())
    drug.clearance = clearance

    affected_organisms_root = drug_root.find("affected_organisms")
    affected_organisms = affected_organisms_root.findall('affected_organism')
    affected_organismsList = [getContent(i) for i in affected_organisms]
    drug.affectedOrganisms = affected_organismsList

    ahfs_codes_root = drug_root.find('ahfs-codes')
    ahfs_codesList = [i.text for i in ahfs_codes_root.findall('ahfs-code')]
    drug.ahfsCodes = ahfs_codesList

    pdb_entries_root = drug_root.find('pdb-entries')
    pdb_entriesList = [i.text for i in pdb_entries_root.findall('pdb-entry')]
    drug.pdbEntries = pdb_entriesList

    fda_label = getContent(drug_root.find('fda_label'))
    drug.fdaLabel = fda_label

    msds = getContent(drug_root.find('msds'))
    drug.msds = msds

    foodInteractions_root = drug_root.find('food-interactions')
    foodInteractionsList = [i.text for i in foodInteractions_root.findall('food-interaction')]
    drug.foodInterations = foodInteractionsList

    sequences_root = drug_root.find('sequences')
    sequences = sequences_root.findall('sequence')
    sequencesList = [i.text for i in sequences]
    drug.sequences = sequencesList

    drug.save()

    synonym_root = drug_root.find("synonyms")
    if synonym_root is not None:
        synonyms = synonym_root.findall("synonym")
        synonymsList = []
        for synonym in synonyms:
            language = synonym.attrib["language"]
            coder = synonym.attrib["coder"]
            synonym_content = synonym.text
            synonymsList.append({"language": language, "coder": coder, "content": synonym_content})
            saved_synonym = Synonym()
            saved_synonym.coder = coder
            saved_synonym.language = language
            saved_synonym.content = synonym_content

    products_root = drug_root.find('products')
    if products_root is not None:
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

            saved_product = Product()
            saved_product.drug = drug
            saved_product.name = name
            saved_product.labeller = product_labeller
            saved_product.ndcId = product_ndcId
            saved_product.ndcProductCode = product_ndcProductCode
            saved_product.dpdId = product_dpdId
            saved_product.emaProductCode = product_emaProductCode
            saved_product.emaMaNumber = product_emaMaNumber
            saved_product.startedMarketingOn = product_startedMarketingOn
            saved_product.endedMarketingOn = product_endedMarketingOn
            saved_product.dosageForm = product_dosageForm
            saved_product.strength = product_strength
            saved_product.route = product_route
            saved_product.fdaApplicationNumber = product_fdaApplicationNumber
            saved_product.generic = product_generic
            saved_product.overTheCounter = product_overTheCounter
            saved_product.approved = product_approved
            saved_product.country = product_country
            saved_product.source = product_source
            saved_product.save()

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
    if internationalBrand_root is not None:
        internationalBrands = internationalBrand_root.findall("international-brand")
        internationalBrandsList = []
        for internationalBrand in internationalBrands:
            internationalBrand_name = getContent(internationalBrand.find("name"))
            internationalBrand_company = getContent(internationalBrand.find("company"))
            internationalBrandsList.append({"name": internationalBrand_name, "company": internationalBrand_company})
            saved_internationalBrand = InternationalBrand()
            saved_internationalBrand.name = internationalBrand_name
            saved_internationalBrand.company = internationalBrand_company
            saved_internationalBrand.drug = drug
            saved_internationalBrand.save()

    mixtures_root = drug_root.find('mixtures')
    if mixtures_root is not None:
        mixtures = mixtures_root.findall('mixture')
        mixturesList = []
        for mixture in mixtures:
            mixture_name = getContent(mixture.find("name"))
            mixture_ingredients = getContent(mixture.find("ingredients"))
            mixturesList.append({'name': mixture_name, 'ingredients': mixture_ingredients})
            saved_mixture = Mixture(name=mixture_name, ingredients=mixture_ingredients)
            saved_mixture.drug = drug
            saved_mixture.save()

    classification_root = drug_root.find("classification")
    if classification_root is None:
        classification_description = getContent(classification_root.find("description"))
        classification_directParent = getContent(classification_root.find("direct-parent"))
        classification_kingdom = getContent(classification_root.find("kingdom"))
        classification_superclass = getContent(classification_root.find("superclass"))
        classification_class = getContent(classification_root.find("class"))
        classification_subclass = getContent(classification_root.find("subclass"))

        saved_classification = Classification()
        saved_classification.description = classification_description
        saved_classification.directParent = classification_directParent
        saved_classification.kingdom = classification_kingdom
        saved_classification.superclass = classification_superclass
        saved_classification.kls = classification_class
        saved_classification.subclass = classification_subclass
        saved_classification.drug = drug
        saved_classification.save()
        # todo: save in database
    else:
        # todo: save None in database, classification of this drug there is None
        pass

    packagers_root = drug_root.find('packagers')
    if packagers_root is not None:
        packagers = packagers_root.findall('packager')
        packagersList = []
        for packager in packagers:
            packager_name = getContent(packager.find("name"))
            packager_url = getContent(packager.find("url"))
            packagersList.append({'name': packager_name, 'url': packager_url})
            saved_packager = Packager(name=packager_name, url=packager_url, drug=drug)
            saved_packager.save()

    manufacturers_root = drug_root.find('manugacturers')
    if manufacturers_root is not None:
        manufacturers = manufacturers_root.findall('manufacturer')
        manufacturersList = []
        for manufacturer in manufacturers:
            manufacturer_generic = manufacturer.attrib["generic"]
            manufacturer_url = manufacturer.attrib["url"]
            manufacturer_content = getContent(manufacturer)
            saved_manufacturer = Manufacturer(generic=manufacturer_generic, url=manufacturer_url,
                                              name=manufacturer_content)
            saved_manufacturer.save()
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
        price_unit = getContent(price.find('unit'))
        saved_price = Price(currency=currency, cost=price_cost, unit=price_unit, drug=drug)
        saved_price.save()
        pricesList.append({
            'description': price_description,
            'cost': price_cost,
            'unit': price_unit
        })

    categories_root = drug_root.find('categories')
    if categories_root is not None:
        categories = categories_root.findall('category')
        categoriesList = []
        for category in categories:
            category_category = getContent(category.find('category'))
            category_mesh_id = getContent(category.find('mesh-id'))
            categoriesList.append({
                'category': category_category,
                'mesh-id': category_mesh_id
            })
            saved_category = Category()
            saved_category.drug = drug
            saved_category.category = category_category
            saved_category.meshId = category_mesh_id
            saved_category.save()

    dosages_root = drug_root.find("dosages")
    if dosages_root is not None:
        dosages = dosages_root.findall("dosage")
        dosagesList = []
        for dosage in dosages:
            dosage_form = getContent(dosage.find('form'))
            dosage_route = getContent(dosage.find('route'))
            dosage_strength = getContent(dosage.find('strength'))
            saved_dosage = Dosage(form=dosage_form, route=dosage_route, strength=dosage_strength)
            saved_dosage.save()
            dosagesList.append({
                'form': dosage_form,
                'route': dosage_route,
                'strength': dosage_strength
            })

    atcCodes_root = drug_root.find('atc-codes')
    if atcCodes_root is not None:
        atcCodes = atcCodes_root.findall('atc-code')
        atcCodesList = []
        for atcCode in atcCodes:
            atcCode_code = atcCode.attrib['code']
            atcCode_levels = atcCode.findall('level')
            atcCode_levelsList = []
            saved_atcCode = AtcCode(code=atcCode_code, drug=drug)
            saved_atcCode.save()
            for atcCode_level in atcCode_levels:
                level_code = atcCode_level.attrib['code']
                level_content = getContent(atcCode_level)
                atcCode_levelsList.append({
                    'code': level_code,
                    'content': level_content
                })
                saved_level = Level(code=level_code, content=level_content, atcCode=saved_atcCode)
                saved_level.save()

            atcCodesList.append({
                'code': atcCode_code,
                'levels': atcCode_levelsList
            })
    patents_root = drug_root.find('patents')
    if patents_root is not None:
        patents = patents_root.findall('patent')
        patentsList = []
        for patent in patents:
            patent_number = getContent(patent.find('number'))
            patent_country = getContent(patent.find('country'))
            patent_approved = getContent(patent.find('approved'))
            patent_expires = getContent(patent.find('expires'))
            patent_pediatric_extension = getContent(patent.find('pediatric-extension'))
            saved_patent = Patent(drug=drug, number=patent_number, country=patent_country, approved=patent_approved,
                                  expires=patent_expires, pediatricExtension=patent_pediatric_extension)
            saved_patent.save()
            patentsList.append({
                'number': patent_number,
                'country': patent_country,
                'approved': patent_approved,
                'expires': patent_expires,
                'pediatric-extension': patent_pediatric_extension
            })

    drugInteractions_root = drug_root.find('drug-interactions')
    if drugInteractions_root is not None:
        drugInteractions = drugInteractions_root.findall('drug-interaction')
        drugInteractionsList = []

        for drugInteraction in drugInteractions:
            drugInteraction_drugbank_id = getContent(drugInteraction.find('drugbank-id'))
            drugInteraction_name = getContent(drugInteraction.find('name'))
            drugInteraction_description = getContent(drugInteraction.find('description'))
            saved_drugInteraction = DrugInteraction(drug=drug, drugbankId=drugInteraction_drugbank_id,
                                                    name=drugInteraction_name, description=drugInteraction_description)
            saved_drugInteraction.save()
            drugInteractionsList.append({
                'drugbank-id': drugInteraction_drugbank_id,
                'name': drugInteraction_name,
                'description': drugInteraction_description
            })

    experimentalProperties_root = drug_root.find('experimental-properties')
    if experimentalProperties_root is not None:
        properties = experimentalProperties_root.findall('property')
        propertiesList = []
        for property in properties:
            property_kind = getContent(property.find('kind'))
            property_value = getContent(property.find('value'))
            property_source = getContent(property.find('source'))
            saved_property = Property(kind=property_kind, value=property_value, source=property_source, drug=drug)
            saved_property.save()
            propertiesList.append({
                'kind': property_kind,
                'value': property_value,
                'source': property_source
            })

    externalIdentifiers_root = drug_root.find('external-identifiers')
    if externalIdentifiers_root is not None:
        externalIdentifiers = externalIdentifiers_root.findall('external-identifier')
        externalIdentifiersList = []
        for externalIdentifier in externalIdentifiers:
            externalIdentifier_resource = getContent(externalIdentifier.find('resource'))
            externalIdentifier_identifier = getContent(externalIdentifier.find('identifier'))
            saved_externalIdentifier = ExternalIdentifier(resource=externalIdentifier_resource,
                                                          identifier=externalIdentifier_identifier, drug=drug)
            saved_externalIdentifier.save()
            externalIdentifiersList.append({
                'resource': externalIdentifier_resource,
                'identifier': externalIdentifier_identifier
            })

    externalLinks_root = drug_root.find('external-links')
    if externalLinks_root is not None:
        externalLinks = externalLinks_root.findall('external-link')
        externalLinksList = []
        for externalLink in externalLinks:
            externalLink_resource = getContent(externalLink.find('resource'))
            externalLink_url = getContent(externalLink.find('url'))
            saved_externalLink = ExternalLink(drug=drug, url=externalLink_url, resource=externalLink_resource)
            saved_externalLink.save()
            externalLinksList.append({
                'resource': externalLink_resource,
                'url': externalLink_url
            })

    pathways_root = drug_root.find('pathways')
    if pathways_root is not None:
        pathways = pathways_root.findall('pathway')
        pathwaysList = []
        for pathway in pathways:
            saved_pathway = Pathway()
            pathway_smpdbId = getContent(pathway.find('smpdb-id'))
            saved_pathway.smpdbId = pathway_smpdbId

            pathway_name = getContent(pathway.find('name'))
            saved_pathway.name = pathway_name

            pathway_category = getContent(pathway.find('category'))
            saved_pathway.category = pathway_category

            enzymes = [i.text for i in pathway.find('enzymes').findall('uniprot-id')]
            saved_pathway.enzymes = enzymes

            saved_pathway.drug = drug
            saved_pathway.save()

            pathway_drugs_root = pathway.find('drugs')
            if pathway_drugs_root is not None:
                pathway_drugs = pathway_drugs_root.findall('drug')
                pathway_drugsList = []
                for pathway_drug in pathway_drugs:
                    pathway_drug_drugbank_id = getContent(pathway_drug.find('drugbank-id'))
                    pathway_drug_name = getContent(pathway_drug.find('name'))

                    saved_pathway_drug = PathwayDrug(drugbankId=pathway_drug_drugbank_id, name=pathway_drug_name,
                                                     pathway=saved_pathway)
                    saved_pathway_drug.save()

                    pathway_drugsList.append({
                        'drugbank-id': pathway_drug_drugbank_id,
                        'name': pathway_drug_name
                    })

    reactions_root = drug_root.find('reactions')
    if reactions_root is None:
        reactions = reactions_root.findall('reaction')
        reactionsList = []
        for reaction in reactions:
            reaction_sequence = reaction.find('sequence')

            saved_reaction = Reaction()
            saved_reaction.drug = drug
            saved_reaction.seqence = reaction_sequence
            saved_reaction.save()

            reaction_left_element_root = reaction.find('left-element')
            reaction_left_element_drugbank_id = getContent(reaction_left_element_root.find('drugbank-id'))
            reaction_left_element_name = getContent(reaction_left_element_root.find('name'))

            saved_left_element = Element()
            saved_left_element.type = True
            saved_left_element.name = reaction_left_element_name
            saved_left_element.drugbankId = reaction_left_element_drugbank_id
            saved_left_element.reaction = saved_reaction
            saved_left_element.save()

            reaction_right_element_root = reaction.find('right-element')
            reaction_right_element_drugbank_id = getContent(reaction_right_element_root.find('drugbank-id'))
            reaction_right_element_name = getContent(reaction_right_element_root.find('name'))

            saved_right_element = Element()
            saved_right_element.type = False
            saved_right_element.drugbankId = reaction_right_element_drugbank_id
            saved_right_element.name = reaction_right_element_name
            saved_right_element.reaction = saved_reaction
            saved_right_element.save()

            reaction_enzymes_root = reaction.find('enzymes')

            reaction_enzymes = reaction_enzymes_root.findall('enzyme')
            reaction_enzymesList = []
            for reaction_enzyme in reaction_enzymes:
                reaction_enzyme_drugbank_id = getContent(reaction_enzyme.find('drugbank-id'))
                reaction_enzyme_name = getContent(reaction_enzyme.find('name'))
                reaction_enzyme_uniprot_id = getContent(reaction_enzyme.find('uniprot-id'))
                saved_reaction_enzyme = ReactionEnzyme(drugbankId=reaction_enzyme_drugbank_id,
                                                       name=reaction_enzyme_name, uniprotId=reaction_enzyme_uniprot_id,
                                                       reaction=saved_reaction)
                saved_reaction_enzyme.save()
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
    if snp_effects_root is not None:
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

            saved_snp_effect = SnpEffect()
            saved_snp_effect.proteinName = snp_effect_protein_name
            saved_snp_effect.geneSymbol = snp_effect_gene_symbol
            saved_snp_effect.uniprotId = snp_effect_uniprot_id
            saved_snp_effect.allele = snp_effect_allele
            saved_snp_effect.definingChange = snp_effect_defining_change
            saved_snp_effect.description = snp_effect_description
            saved_snp_effect.pubmedId = snp_effect_pubmed_id
            saved_snp_effect.drug = drug
            saved_snp_effect.save()

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

        saved_snp_adverse_drug_reaction = SnpAdverseDrugReaction()
        saved_snp_adverse_drug_reaction.proteinName = snp_adverse_drug_reaction_protein_name
        saved_snp_adverse_drug_reaction.geneSymbol = snp_adverse_drug_reaction_gene_symbol
        saved_snp_adverse_drug_reaction.uniprotId = snp_adverse_drug_reaction_uniprot_id
        saved_snp_adverse_drug_reaction.allele = snp_adverse_drug_reaction_allele
        saved_snp_adverse_drug_reaction.definingChange = snp_adverse_drug_reaction_defining_change
        saved_snp_adverse_drug_reaction.description = snp_adverse_drug_reaction_description
        saved_snp_adverse_drug_reaction.pubmedId = snp_adverse_drug_reaction_pubmed_id
        saved_snp_adverse_drug_reaction.drug = drug
        saved_snp_adverse_drug_reaction.save()
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
    saveProtein('target', targets_root, drug)

    enzymes_root = drug_root.find('enzymes')
    saveProtein('enzyme', enzymes_root, drug)

    carriers_root = drug_root.find('carriers')
    saveProtein('carrier', carriers_root, drug)

    transporters_root = drug_root.find('transporters')
    saveProtein('transporter', transporters_root, drug)


def saveProtein(type, root, father):
    # check type in [target, carrier, transporter]

    proteins = root.findall(type)

    # targetsList = []

    for protein in proteins:

        global saved_protein
        if type == 'target':
            saved_protein = Target()
        if type == 'carrier':
            saved_protein = Carrier()
        if type == 'transporter':
            saved_protein = Transporter()
        id = getContent(protein.find('id'))
        saved_protein.id = id

        name = getContent(protein.find('name'))
        saved_protein.name = name

        organism = getContent(protein.find('organism'))
        saved_protein.organism = organism

        actions_root = getContent(protein.find('actions'))
        actions = [getContent(i) for i in actions_root.findall('action')]
        saved_protein.action = actions

        # todo: can you recover the part of ignorance?
        """  
        # ignore start
        protein_articles_root = protein.find('articles')
        protein_articles = protein_articles_root.findall('article')
        protein_articlesList = []
        for protein_article in protein_articles:
            article_pubmed_id = getContent(protein_article.find('pubmed-id'))
            article_citation = getContent(protein_article.find('citation'))
            protein_articlesList.append({
                'pubmed-id': article_pubmed_id,
                'citation': article_citation
            })
        target_textbooks_root = protein.find("textbooks")
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
        
        #ignore end
        """

        known_action = getContent(protein.find('known-action'))
        saved_protein.knownAction = known_action

        polypetide = protein.find('polypeptide')

        _polypetide = savePolypetide(polypetide)
        saved_protein.polypeptide = _polypetide

        saved_protein.drug = father

        saved_protein.save()


def savePolypetide(polypetide):
    saved_polypetide = Polypeptide()
    polypetide_id = polypetide.attrib["id"]
    saved_polypetide.id = polypetide_id

    polypetide_source = polypetide.attrib["source"]
    saved_polypetide.source = polypetide_source

    polypetide_name = getContent(polypetide.find('name'))
    saved_polypetide.name = polypetide_name

    polypetide_general_function = getContent(polypetide.find('general-function'))
    saved_polypetide.generalFunction = polypetide_general_function

    polypetide_specific_function = getContent(polypetide.find('specific-function'))
    saved_polypetide.specificFunction = polypetide_specific_function

    polypetide_gene_name = getContent(polypetide.find('gene-name'))
    saved_polypetide.geneName = polypetide_gene_name

    polypetide_locus = getContent(polypetide.find('locus'))
    saved_polypetide.locus = polypetide_locus

    polypetide_cellular_location = getContent(polypetide.find('cellular-location'))
    saved_polypetide.cellularLocation = polypetide_cellular_location

    polypetide_transmembrane_regions = getContent(polypetide.find('transmembrane-regions'))
    saved_polypetide.transmembraneRegions = polypetide_transmembrane_regions

    polypetide_signal_regions = getContent(polypetide.find('signal-regions'))
    saved_polypetide.signalRegions = polypetide_signal_regions

    polypetide_theoretical_pi = getContent(polypetide.find('theoretical-pi'))
    saved_polypetide.theoreticalPi = polypetide_theoretical_pi

    polypetide_molecular_weight = getContent(polypetide.find('molecular-weight'))
    saved_polypetide.molecularWeight = polypetide_molecular_weight

    polypetide_chromosome_location = getContent(polypetide.find('chromosome-location'))
    saved_polypetide.chromosomeLocation = polypetide_chromosome_location

    polypetide_organism = getContent(polypetide.find('organism'))
    saved_polypetide.organism = polypetide_organism

    polypetide_organism_ncbi_taxonomy_id = polypetide.find('organism').attrib['ncbi-taxonomy-id']
    saved_polypetide.organismNcbiTaxonomyId = polypetide_organism_ncbi_taxonomy_id

    polypetide_externalIdentifiers_root = polypetide.find('external-identifiers')
    polypetide_externalIdentifiers = polypetide_externalIdentifiers_root.findall('external-identifier')
    polypetide_externalIdentifiersList = []
    for polypetide_externalIdentifier in polypetide_externalIdentifiers:
        polypetide_externalIdentifier_resource = getContent(polypetide_externalIdentifier.find('resource'))
        polypetide_externalIdentifier_identifier = getContent(polypetide_externalIdentifier.find('identifier'))
        polypetide_externalIdentifiersList.append({
            'resource': polypetide_externalIdentifier_resource,
            'identifier': polypetide_externalIdentifier_identifier
        })
        polypetideExternalIdentifier = PolypeptideExternalIdentifier()
        polypetideExternalIdentifier.identifier = polypetide_externalIdentifier_identifier
        polypetideExternalIdentifier.resource = polypetide_externalIdentifier_resource
        polypetideExternalIdentifier.polypeptide = saved_polypetide
        polypetideExternalIdentifier.save()

    polypetide_synonym_root = polypetide.find("synonyms")
    polypetide_synonyms = [getContent(i) for i in polypetide_synonym_root.findall("synonym")]
    saved_polypetide.synonyms = polypetide_synonyms

    polypetide_amino_acid_sequence = getContent(polypetide.find('amino-acid-sequence'))
    saved_polypetide.aminoAcidSequence = polypetide_amino_acid_sequence

    polypetide_gene_sequence = getContent(polypetide.find('gene-sequence'))
    saved_polypetide.geneSequence = polypetide_gene_sequence

    polypetide_pfams_root = polypetide.find('pfams')
    polypetide_pfams = polypetide_pfams_root.findall('pfam')
    pfamsList = []
    for polypetide_pfam in polypetide_pfams:
        polypetide_pfam_identifier = getContent(polypetide_pfam.find('identifier'))
        polypetide_pfam_name = getContent(polypetide_pfam.find('name'))
        pfamsList.append({
            'identifier': polypetide_pfam_identifier,
            'name': polypetide_pfam_name
        })
        pfam = Pfam()
        pfam.polypeptide = saved_polypetide
        pfam.identifier = polypetide_pfam_identifier
        pfam.name = polypetide_pfam_name
        pfam.save()

    polypetide_go_classifiers_root = polypetide.find('go-classifiers')
    polypetide_go_classifiers = polypetide_go_classifiers_root.findall('go-classifier')
    polypetide_go_classifiersList = []
    for polypetide_go_classifier in polypetide_go_classifiers:
        polypetide_category = polypetide_go_classifier.find('category')
        polypetide_description = polypetide_go_classifier.find('description')
        polypetide_go_classifiersList.append({
            'category': polypetide_category,
            'description': polypetide_description
        })
        go_classifier = GoClassifier()
        go_classifier.description = polypetide_description
        go_classifier.category = polypetide_category
        go_classifier.polypeptide = saved_polypetide
        go_classifier.save()

    saved_polypetide.save()
    return saved_polypetide


def getContent(node):
    if node is None:
        return None
    else:
        return node.text


parseXml("partial.xml")
