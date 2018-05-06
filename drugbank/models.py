# Simth woatermen
import ast

from django.db import models


# Create your models here.


class ListField(models.TextField):
    # 存储字符串列表
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

#
class Drug(models.Model):
    drugbankId = models.TextField()  # type:list
    # drugbank第一个为primary的
    # drugbankId 可以有多个，但是只有一个是primary的。就比如Lepirudin有DB00001\BTD00024\BI0D00024
    # 三种。具体怎么安排不明，但是primary只有DB00001
    name = models.TextField()  # type: str
    description = models.TextField()  # type: str
    casNumber = models.TextField()  # type: str
    unii = models.TextField()  # type: str
    state = models.TextField()  # type: str
    groups = ListField()  # type: list[str]
    # groups 不明
    # articles = models.TextField()  # type: list[Article]
    # textbooks  # type: list[Textbook]
    synthesisReference = models.TextField()  # type: str
    indication = models.TextField()
    pharmacodynamics = models.TextField()
    mechanismOfAction = models.TextField()
    toxicity = models.TextField()
    selfmetabolism = models.TextField()
    absorption = models.TextField()
    halfLife = models.TextField()
    proteinBinding = models.TextField()  # type: str
    routeOfElimination = models.TextField()
    volumeOfDistribution = models.TextField()
    clearance = models.TextField()
    # classification = models.OneToOneField(Classification, on_delete=models.DO_NOTHING) # type: Classification
    # salts  # type:list[Salt]
    # self.synonyms  # type: list[Synonym]
    # self.products  # type: list[Product]
    # self.mixtures  # type: list[Mixture]
    # self.packages  # type: list[Packager]
    # self.manufacturers  # type: list[Manufacturer]
    # self.prices  # type: list[Price]
    # self.categories  # type: list[Category]
    # self.affectedOrganisms  # type: list[AffectedOrganism]
    # self.dosages  # type: list[Dosage]
    # self.atcCodes  # type: AtcCode
    ahfsCodes = models.TextField()
    pdbEntries = models.TextField()
    fdaLabel = models.TextField()
    msds = models.TextField()
    # self.patents  # type: list[Patent]
    foodInterations = ListField()  # type: # list[FoodInteraction] todo: change it to table
    # self.drugInteractions  # type: list[DrugInteraction]
    sequences = ListField()  # type: # list[str] format一直都是FASTA吗
    # self.experimentalProerties  # type: list[Property]
    # self.externalIdentifiers  # type: list[ExternalIdentifier]
    # self.externalLink  # type: list[ExternalLink]
    # self.pathways  # type: list[Pathway]
    # self.reactions  # type: list[Reaction]
    # self.snpEffects  # type: list[Effect]
    # self.snpAdverseDrugReactions  # 这里很迷啊……Effect的属性Reaction的头
    # self.targets  # type: # list[Target]
    enzymes = ListField()  # type: # list[str]
    # self.carriers  # type: # list[Target]
    # self.transporters: list[Target]


# class Effect(models.Model):
#     proteinName = models.TextField()
#     geneSymbol = models.TextField()
#     uniprotId = models.TextField()
#     rsId = models.TextField()
#     allele = models.TextField()
#     definingChange = models.TextField()
#     description = models.TextField()
#     pubmedId = models.TextField()


class SnpAdverseDrugReactions(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpAdverseDrugReactions")
    proteinName = models.TextField()
    geneSymbol = models.TextField()
    uniprotId = models.TextField()
    rsId = models.TextField()
    allele = models.TextField()
    definingChange = models.TextField()
    description = models.TextField()
    pubmedId = models.TextField()


class SnpEffect(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_snpEffects")
    proteinName = models.TextField()
    geneSymbol = models.TextField()
    uniprotId = models.TextField()
    rsId = models.TextField()
    allele = models.TextField()
    definingChange = models.TextField()
    description = models.TextField()
    pubmedId = models.TextField()


class Salt(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_salt")
    drugbankId = ListField()  # type: list[str]
    name = models.TextField()
    unii = models.TextField()
    casNumber = models.TextField()
    inchikey = models.TextField()

# ignore
class Polypeptide(models.Model):
    id = models.TextField(primary_key=True)
    source = models.TextField()
    name = models.TextField()
    generalFunction = models.TextField()
    specificFunction = models.TextField()
    geneName = models.TextField()
    locus = models.TextField()
    cellularLocation = models.TextField()
    transmembraneRegions = models.TextField()
    signalRegions = models.TextField()
    theoreticalPi = models.TextField()
    molecularWeight = models.TextField()
    chromosomeLocation = models.TextField()
    organism = models.TextField()
    organismNcbiTaxonomyId = models.TextField()
    aminoAcidSequence = models.TextField()
    geneSequence = models.TextField()
    externalIdentifiers = models.TextField()
    synonyms = ListField()
    # pfams: list[Pfam]
    # goClassifiers: list[GoClassifier]


class GoClassifier(models.Model):
    polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_goClassifiers")
    category = models.TextField()
    description = models.TextField()


class Pfam(models.Model):
    polypeptide = models.ForeignKey(Polypeptide, on_delete=models.DO_NOTHING, related_name="polypeptide_pfams")

    identifier = models.TextField()
    name = models.TextField()


class ExternalIdentifier(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_externalIdentifiers")

    resource = models.TextField()
    identifier = models.TextField()


class Pathway(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_pathways")
    smpdbId = models.TextField()
    name = models.TextField()
    category = models.TextField()


class ExternalLink(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_externalLinks")
    resource = models.TextField()
    url = models.TextField()


class Property(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_properties")

    kind = models.TextField()
    value = models.TextField()
    source = models.TextField()


class DrugInteraction(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_drugInteractions")

    drugbankId = models.TextField()
    name = models.TextField()
    description = models.TextField()


class Patent(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_patents")
    number = models.TextField()
    country = models.TextField()
    approved = models.TextField()
    expires = models.TextField()
    pediatricExtension = models.TextField()


class AtcCode(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_atcCodes")
    code = models.TextField()


class Level(models.Model):
    atcCode = models.ForeignKey(AtcCode, on_delete=models.DO_NOTHING, related_name="atcCode_levels")
    code = models.TextField()
    content = models.TextField()


# class Dosage(models.Model):
#     drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_dosages")
#     form = models.TextField()
#     route = models.TextField()
#     strength = models.TextField()


class AffectedOrganism(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_affectedOrganisms")
    content = models.TextField()  # ???看不懂


class Category(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_categories")
    category = models.TextField()
    meshId = models.TextField()


class Price(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_prices")

    description = models.TextField()
    cost = models.TextField()
    unit = models.TextField()


class Manufacturer(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_manufacturers")

    generic = models.TextField()
    url = models.TextField()
    name = models.TextField(primary_key=True)


class Packager(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_packagers")

    name = models.TextField(primary_key=True)
    url = models.TextField()


class Mixture(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_mixtures")

    name = models.TextField(primary_key=True)
    ingredients = models.TextField()


class Product(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_products")

    name = models.TextField(primary_key=True)
    labeller = models.TextField()
    ndcId = models.TextField()
    ndcProductCode = models.TextField()
    dpdId = models.TextField()
    emaProductCode = models.TextField()
    emaMaNumber = models.TextField()
    startedMarketingOn = models.TextField()
    endedMarketingOn = models.TextField()
    dosageForm = models.TextField()
    strength = models.TextField()
    route = models.TextField()
    fdaApplicationNumber = models.TextField()
    generic = models.TextField()
    overTheCounter = models.TextField()
    approved = models.TextField()
    country = models.TextField()
    source = models.TextField()


class Synonym(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_synonym")

    language = models.TextField()
    coder = models.TextField()


class Protein(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    organism = models.TextField()
    # textbooks = models.ForeignKey(Textbook, on_delete=models.DO_NOTHING, related_name="textBookRecord_protein") #todo: this is wrong
    # article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="articleRecord_protein") #todo: this is wrong
    action = ListField()
    knownAction = models.TextField()
    polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING)


class Article(models.Model):
    pumbedId = models.TextField()  # type: str
    citation = models.TextField()  # type: str
    protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING, related_name="protein_article")
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_article")


class Textbook(models.Model):
    links = models.TextField()
    protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING, related_name="protein_textbook")
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_textbook")


class Link(models.Model):
    title = models.TextField()
    url = models.TextField()


class Classification(models.Model):
    drug = models.OneToOneField(Drug, on_delete=models.DO_NOTHING)

    description = models.TextField()
    directParent = models.TextField()
    kingdom = models.TextField()
    superclass = models.TextField()
    kls = models.TextField()
    subclass = models.TextField()


class Carrier(models.Model):
    drug = models.ManyToManyField(Drug, related_name="drug_carriers")
    id = models.TextField(primary_key=True)
    name = models.TextField()
    organism = models.TextField()
    action = ListField()
    knownAction = models.TextField()
    polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING)

class InternationalBrands(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drug_internationalBrands")
    name = models.TextField()
    company = models.TextField()


class Transporter(models.Model):
    drug = models.ManyToManyField(Drug, related_name="drug_transporters")
    id = models.TextField(primary_key=True)
    name = models.TextField()
    organism = models.TextField()
    action = ListField()
    knownAction = models.TextField()
    polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING)


class Target(models.Model):
    drug = models.ManyToManyField(Drug, related_name="drug_targets")
    id = models.TextField(primary_key=True)
    name = models.TextField()
    organism = models.TextField()
    action = ListField()
    knownAction = models.TextField()
    polypeptide = models.OneToOneField(Polypeptide, on_delete=models.DO_NOTHING)


class Reaction(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, related_name="drugs_reactions")
    seqence = models.IntegerField()
    # leftElement = models.OneToOneField(Element, on_delete=models.DO_NOTHING)
    # rightElement = models.OneToOneField(Element, on_delete=models.DO_NOTHING)


class Element(models.Model):
    drugbankId = models.TextField()
    name = models.TextField()
    type = models.BooleanField()  # left is true, right is false
    reaction = models.ForeignKey(Reaction, on_delete=models.DO_NOTHING, related_name="relation_elements")
