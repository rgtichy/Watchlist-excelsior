from django.db import models

# Create your models here.

INTRINIO_TYPES = [
                ('IS', "Income Statement"),
                ('BS', "Balance Sheet"),
                ('CF', "Cash Flow Statement"),
                ('CA', "Calculations"),
                ('PR', "Prices"),
                ('CT', "Current")
                ]
QTR0 = 'QTR0'
QTR1 = 'QTR1'
QTR2 = 'QTR2'
QTR3 = 'QTR3'
QTR4 = 'QTR4'
QTR5 = 'QTR5'
QTR6 = 'QTR6'
QTR7 = 'QTR7'
QTR8 = 'QTR8'
TTM0 = 'TTM0'
TTM1 = 'TTM1'
TTM2 = 'TTM2'
TTM3 = 'TTM3'
TTM4 = 'TTM4'
TTM5 = 'TTM5'
TTM6 = 'TTM6'
TTM7 = 'TTM7'
TTM8 = 'TTM8'
PERIOD_CHOICES = [
    (QTR0,'Most Recent Quarter'),
    (QTR1,'2nd Most Recent Quarter'),
    (QTR2,'3rd Most Recent Quarter'),
    (QTR3,'4th Most Recent Quarter'),
    (QTR4,'5th Most Recent Quarter (12 Mos. Prior)'),
    (QTR5,'6th Most Recent Quarter'),
    (QTR6,'7th Most Recent Quarter'),
    (QTR7,'8th Most Recent Quarter'),
    (QTR8,'9th Most Recent Quarter (24 Mos. Prior)'),
    (TTM0,'Most Recent Trailing 12 Months'),
    (TTM1,'Trailing 12 Months, 1 Quarter Arrears'),
    (TTM2,'Trailing 12 Months, 2 Quarters Arrears'),
    (TTM3,'Trailing 12 Months, 3 Quarters Arrears'),
    (TTM4,'Trailing 12 Months, 1 Year in Arrears'),
    (TTM5,'Trailing 12 Months, 5 Quarters Arrears'),
    (TTM6,'Trailing 12 Months, 6 Quarters Arrears'),
    (TTM7,'Trailing 12 Months, 7 Quarters Arrears'),
    (TTM8,'Trailing 12 Months, 2 Years in Arrears'),
]

def validateSecurity(security_dict):
    error = False
    errors = []
    return (error,errors)

def validateCompany(company_dict):
    error = False
    errors = []
    return (error,errors)

def validateData_Tag(data_tag_dict):
    error = False
    errors = []
    formdata = {}

    # formdata is a santized version of the returned data from the form and the req.POST object
    # nothing can be updated but the fields listed here, after being placed into formdata
    formdata['tag'] = data_tag_dict['tag']
    formdata['name'] = data_tag_dict['name']
    formdata['statement_code'] = data_tag_dict['statement_code']
    formdata['units'] = data_tag_dict['unit']
    formdata['template'] = data_tag_dict['statement_type']
    formdata['historical'] = data_tag_dict['historical']
    formdata['screenable'] = data_tag_dict['screenable']

    if data_tag_dict['grouping'] not in [e[0] for e in INTRINIO_TYPES]:
        error = True
        errors += ['Must Select a Valid Group Type']
    return (error,{'errors':errors, 'formdata': formdata})

class SecurityManager(models.Manager):



    def newSecurity(self, data):

        (error,errors) = validateSecurity(data)

        if not error:
            security = Security.objects.create(
                intrinio_id = data['id'],
                company_id = data['company_id'],
                name = data['name'],
                code = data['code'],
                currency = data['currency'],
                ticker = data['ticker'],
                composite_ticker = data['composite_ticker'],
                figi = data['figi'],
                composite_figi = data['composite_figi'],
                share_class_figi = data['share_class_figi']
                )
            return (True, security)
        else:
            return (False, errors)

    def editSecurity(self, data):

        (error,errors) = validateSecurity(data)
        if not error:
            existing = Security.objects.get(id = data['id'])
            for e in data.keys():
                existing[e] = data[e]
            existing.save()
            return (False, existing)
        else:
            return (True, errors)



class Security(models.Model):
    intrinio_id = models.CharField(max_length=255)
    company_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    composite_ticker = models.CharField(max_length=255)
    figi = models.CharField(max_length=255)
    composite_figi = models.CharField(max_length=255)
    share_class_figi = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = SecurityManager()


class CompanyManager(models.Manager):

    def newCompany(self, data):
        for e in data.keys():
            if data[e] == None:
                data[e] = ""
        (error,errors) = validateCompany(data)
        if not error:
            company = Company.objects.create(
                company_id = data['id'],
                ticker = data['ticker'],
                name = data['name'],
                lei = data['lei'],
                cik = data['cik'],
                )
            return (True, company)
        else:
            return (False, errors)

    def editCompany(self, data):

        (error,errors) = validateCompany(data)
        if not error:
            existing = Company.objects.get(id = data['id'])
            for e in data.keys():
                existing[e] = data[e]
            existing.save()
            return (False, existing)
        else:
            return (True, errors)

class Company(models.Model):
    company_id = models.CharField(max_length=255) # The Intrinio ID of the company (string)
    ticker = models.CharField(max_length=255) # The stock market ticker symbol associated with the company's common stock securities (string)
    name = models.CharField(max_length=255) # The company's common name (string)
    lei = models.CharField(max_length=255) # The Legal Entity Identifier (LEI) assigned to the company (string)
    cik = models.CharField(max_length=255) # The Central Index Key (CIK) assigned to the company (string)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CompanyManager()

class Data_TagManager(models.Manager):
    def load_Data_Tag(self, data):
        try:
            for e in data.keys():
                if data[e] == None:
                    data[e] = ""
            if data['sequence'] == "":
                data['sequence'] = 0
            data_tag = Data_Tag.objects.create(
                                            intrinio_id=data['id'],
                                            tag = data['tag'], # The Intrinio Data Tag
                                            name = data['name'], # The short human readable name
                                            statement_code = data['statement_code'],
                                            template = data['statement_type'],
                                            parent=data['parent'],
                                            sequence=data['sequence'],
                                            factor = data['factor'],
                                            balance = data['balance'],
                                            nature = data['type'],
                                            units = data['unit'],
                                            )
        except failure:
            return (True, [f'Data Tag {data["tag"]} not created successfully. {failure}'])
        return False, data_tag

    def newData_Tag(self, data):
        (error, obj) = validateData_Tag(data)
        if not error:
            data_tag = Data_Tag.objects.create(
                                            intrinio_id=data['id'],
                                            tag = data['tag'], # The Intrinio Data Tag
                                            name = data['name'], # The short human readable name
                                            statement_code = data['statement_code'],
                                            template = data['statement_type'],
                                            parent=data['parent'],
                                            sequence=data['sequence'],
                                            factor = data['factor'],
                                            balance = data['balance'],
                                            nature = data['type'],
                                            units = data['unit'],
                                            )
            return (False, data_tag)
        else:
            return (True, obj)

    def editData_Tag(self, data, id):

        (error,obj) = validateData_Tag(data)
        if not error:
            formdata = obj['formdata']
            existing = Data_Tag.objects.get(id = id)
            existing.tag = formdata['tag']
            existing.name = formdata['name']
            existing.grouping = formdata['grouping']
            existing.units = formdata['units']
            existing.description = formdata['description']
            existing.templates = formdata['templates']
            existing.historical = formdata['historical']
            existing.screenable = formdata['screenable']
            existing.save()
            return (False, existing)
        else:
            return (True, obj)

class Data_Tag(models.Model):

    COMPANY = 'C'
    SECURITY = 'S'
    LEVEL_CHOICES = [
        (COMPANY, 'Company'),
        (SECURITY, 'Security'),
    ]
    #id	str	The Intrinio ID for the Data Tag
    # name	str	The readable name of the Data Tag
    # tag	str	The code-name of the Data Tag
    # statement_code	str	The code of the financial statement to which this Data Tag belongs
    # statement_type	str	The format of the financial statment to which this Data Tag belongs
    # parent	str	The parent Data Tag forming the statement relationship with the factor
    # sequence	float	The order in which the Data Tag appears in its logical group (such as a financial statement)
    # factor	str	The operator forming the statement relationship between the child Data Tag (or Data Tags) and the parent Data Tag
    # balance	str	Whether the Data Tag represents a credit or debit
    # type	str	The nature of the Data Tag, operating or nonoperating
    # unit	str	The unit of the Data Tag
    intrinio_id = models.CharField(max_length=255) # The Intrinio ID of the company (string)
    name = models.CharField(max_length=255) # The short human readable name
    tag = models.CharField(max_length=225) # The Intrinio Data Tag
    statement_code = models.CharField(max_length=255) # category of the data (organization)
    description = models.TextField()
    template = models.CharField(max_length=45, default="")  # Format of the financial statement to which this Data Tag belongs
    parent = models.CharField(max_length=255, default="")     # a Parent to a tag as if a sub category of non-current liabilities on Balance Sheet
    sequence = models.FloatField(default=0) #sequence on the Parent
    factor = models.CharField(max_length=1)  #    + - = /
    balance = models.CharField(max_length=255) # debit or credit
    nature = models.CharField(max_length=255, default="")    # The nature of the Data Tag, operating or nonoperating
    units = models.CharField(max_length=255, default="") # The Central Index Key (CIK) assigned to the company (string)
    historical = models.CharField(max_length=1, default='Y')  # Code determines whether ??????
    screenable = models.CharField(max_length=1, default='Y')  # Code will identify which filters can be screened at the service provider
    api = models.CharField(max_length=2, default="A")     # Code will determine which API call to use to retrieve data
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default=COMPANY)   # Company or Security
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Data_TagManager()

class Historical_Retrieval_Log(models.Model):

    ticker = models.CharField(max_length=255, db_index=True)
    data_tag = models.CharField(max_length=25, db_index=True)
    period = models.CharField(max_length=3)
    # value = models.DecimalField(max_digits=24, decimal_places=6)
    val_0 = models.DecimalField(max_digits=24, decimal_places=6)
    val_1 = models.DecimalField(max_digits=24, decimal_places=6)
    val_2 = models.DecimalField(max_digits=24, decimal_places=6)
    val_3 = models.DecimalField(max_digits=24, decimal_places=6)
    val_4 = models.DecimalField(max_digits=24, decimal_places=6)
    val_5 = models.DecimalField(max_digits=24, decimal_places=6)
    val_6 = models.DecimalField(max_digits=24, decimal_places=6)
    val_7 = models.DecimalField(max_digits=24, decimal_places=6)
    val_8 = models.DecimalField(max_digits=24, decimal_places=6)
    divisor = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
