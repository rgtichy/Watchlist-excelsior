from django.shortcuts import render, redirect
import time
from pprint import pprint
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from .models import Security, Company, Data_Tag, INTRINIO_TYPES
import os
INTRINIO_KEY = os.getenv('INTRINIO_TESTING_KEY')


# Create your views here.
def index(request):   #securities
    context = {'S' : Security.objects.all().order_by('name'),
               }
    context['count']= len(context['S'])

    request.session['formdata'] = ""

    if 'errors' in request.session:
        context['error'] = True
        context['errors'] = request.session.errors
    else:
        request.session['errors'] = []

    del request.session['errors']
    del request.session['formdata']

    return render(request, 'securities/securities.html', context)

def security(request, id):
    context = {'S' : Security.objects.get(id=id)
                   }
    return render(request, 'securities/security.html', context)

def companies(request):
    context = {'C' : Company.objects.all().order_by('name'),
               }
    context['count']= len(context['C'])

    return render(request, 'securities/companies.html', context)

def company(request, id):
    context = {'C' : Company.objects.get(id=id)
                   }
    return render(request, 'securities/company.html', context)

# This is the Index page for Data Tags
def datatags(request):
    context = {'D' : Data_Tag.objects.all().order_by('statement_code','parent','sequence','name'),
               }
    context['count']= len(context['D'])

    request.session['formdata'] = ""

    if 'errors' in request.session:
        context['error'] = True
        context['errors'] = request.session['errors']
    else:
        request.session['errors'] = []

    del request.session['errors']
    del request.session['formdata']

    return render(request, 'securities/datatags.html', context)

# This is the Edit page for Data Tags
def datatag(request, id):
    context =  {'edit':True,
                'D': Data_Tag.objects.get(id=id),
                'groupings' : INTRINIO_TYPES,
                'LEVEL': Data_Tag.LEVEL_CHOICES
                }

    if 'errors' in request.session and request.session['errors'] != []:
        # errors = request.session['errors']
        context['error'] = True
        context['errors'] = request.session['errors']
        context['formdata'] = request.session['formdata']

        del request.session['errors']
        del request.session['formdata']

    return render(request, 'securities/datatag_entry.html', context)

# This is the Add new Data Tag page for Data Tags
def datatag_add(request):
    # errors=[]
    # print(Data_Tag.LEVEL_CHOICES)
    context =  {'edit':False,
                'groupings' : INTRINIO_TYPES,
                'LEVEL': Data_Tag.LEVEL_CHOICES
                }

    if 'errors' in request.session:
        # errors = request.session['errors']
        context['error'] = True
        context['errors'] = request.session['errors']
        context['formdata'] = request.session['formdata']

        del request.session['errors']
        del request.session['formdata']

    return render(request, 'securities/datatag_entry.html', context)

# This is the Create for Data Tags
def data_tag(request):
    # print(":"*50)
    # pprint(request.POST)
    # print("-"*50)
    if request.method == 'POST':
        ( error, obj ) = Data_Tag.objects.newData_Tag(request.POST)
        if error:
            # request.session.error = True
            request.session.errors = obj['errors']
            request.session.formdata = obj['formdata']

            return redirect(datatag_add)

        request.session.data = obj
    return redirect('securities:datatags')

# This is the Update for Data Tags
def data_tag_edit(request, id):

    id = int(id)

    if request.method == 'POST':
        ( error, obj ) = Data_Tag.objects.editData_Tag(request.POST, int(id))
        if error:
            request.session.errors = obj['errors']
            request.session.formdata = obj['formdata']

            return redirect(datatag_edit, id=id)
        request.session.data = obj
    return redirect('securities:datatags')

# Delete function for Data Tags

def data_tag_del(request, id):

    if request.method == 'GET':
        d = Data_Tag.objects.get(id = int(id))
        d.delete()
        request.session.data = d
    return redirect('securities:datatags')

def create(request):
    return redirect('securities:index')

def update(request):
    return redirect('securities:index')

def delete(request):
    return redirect('securities:index')

def load(request):
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = INTRINIO_KEY
    # company_api = intrinio_sdk.CompanyApi()
    security_api = intrinio_sdk.SecurityApi()

    active = True # bool | When True, return securities that are active. When False, return securities that are not active. A security is considered active if it has traded or has had a corporate action in the past 30 days, and has not been merged into another security (such as due to ticker changes or corporate restructurings). (optional)
    delisted = False # bool | When True, return securities that have been delisted from their exchange. Note that there may be a newer security for the same company that has been relisted on a differente exchange. When False, return securities that have not been delisted. (optional)
    code = 'EQS' # str | Return securities classified with the given code reference [see - https://docs.intrinio.com/documentation/security_codes]. (optional)
    currency = '' # str | Return securities traded in the given 3-digit ISO 4217 currency code reference [see - https://en.wikipedia.org/wiki/ISO_4217]. (optional)
    ticker = '' # str | Return securities traded with the given ticker. Note that securities across the world (and through time) may trade with the same ticker but represent different companies. Use this in conjuction with other parameters for more specificity. (optional)
    name = '' # str | Return securities with the given text in their name (not case sensitive). (optional)
    composite_mic = 'USCOMP' # str | Return securities classified under the composite exchange with the given Market Identification Code (MIC). A composite exchange may or may not be a real exchange.  For example, the USCOMP exchange (our only composite exchange to date) is a combination of exchanges with the following MICs: ARCX, XASE, XPOR, FINR, XCIS, XNAS, XNYS, BATS.  This composite grouping is done for user convenience.  At this time, all US securities are classified under the composite exchange with MIC USCOMP.  To query for specific US exchanges, use the exchange_mic parameter below.  (optional)
    exchange_mic = '' # str | The MIC code of the exchange where the security is actually traded. (optional)
    stock_prices_after = '' # date | Return securities with end-of-day stock prices on or after this date. (optional)
    stock_prices_before = '' # date | Return securities with end-of-day stock prices on or before this date. (optional)
    cik = '' # str | Return securities belonging to the company with the given Central Index Key (CIK). (optional)
    figi = '' # str | Return securities with the given Exchange Level FIGI reference [see - https://www.openfigi.com/about]. (optional)
    composite_figi = '' # str | Return securities with the given Country Composite FIGI reference [see - https://www.openfigi.com/about]. (optional)
    share_class_figi = '' # str | Return securities with the given Global Share Class FIGI reference [see - https://www.openfigi.com/about]. (optional)
    figi_unique_id = '' # str | Return securities with the given FIGI Unique ID reference [see - https://www.openfigi.com/about]. (optional)
    include_non_figi = False # bool | When True, include securities that do not have a FIGI. By default, this is False. If this parameter is not specified, only securities with a FIGI are returned. (optional) (default to False)
    page_size = 100 # int | The number of results to return (optional) (default to 100)
    next_page = '' # str | Gets the next page of data from a previous API call (optional)


    try:
        next_page = ""
        first = True
        c = 0
        while first or next_page != "":
            api_response = security_api.get_all_securities(
                active=active,
                delisted=delisted,
                code=code,
                currency=currency,
                ticker=ticker, name=name,
                composite_mic=composite_mic,
                exchange_mic=exchange_mic,
                stock_prices_after=stock_prices_after,
                stock_prices_before=stock_prices_before,
                cik=cik,
                figi=figi, composite_figi=composite_figi,
                share_class_figi=share_class_figi,
                figi_unique_id=figi_unique_id,
                include_non_figi=include_non_figi,
                page_size=page_size,
                next_page=next_page
                )
            s = api_response.securities_dict
            for e in s:
                if first:
                    first = False
                    toDelete = Security.objects.all()
                    toDelete.delete()
                (flag, errors) = Security.objects.newSecurity(e)
                if flag:
                    print(e, errors)
                c += 1
        print("total securities count:", c)
    except ApiException as e:
        print("Exception when calling SecurityApi->get_all_securities: %s\r\n" % e)

    return redirect('securities:index')


def c_load(request):
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = INTRINIO_KEY
    company_api = intrinio_sdk.CompanyApi()

    latest_filing_date = '' # date | Return companies whose latest 10-Q or 10-K was filed on or after this date (optional)
    sic = '' # str | Return companies with the given Standard Industrial Classification code (optional)
    template = '' # str | Return companies with the given financial statement template (optional)
    sector = '' # str | Return companies in the given industry sector (optional)
    industry_category = '' # str | Return companies in the given industry category (optional)
    industry_group = '' # str | Return companies in the given industry group (optional)
    has_fundamentals = True # bool | Return only companies that have fundamentals when True (optional)
    has_stock_prices = True # bool | Return only companies that have stock prices when True (optional)
    page_size = 100 # int | The number of results to return (optional) (default to 100)
    next_page = '' # str | Gets the next page of data from a previous API call (optional)

    try:
        next_page = ""
        first = True
        i = 0
        while first or next_page != "":
            api_response = company_api.get_all_companies(
                latest_filing_date = '',
                sic = '',
                template = '',
                sector = '',
                industry_category = '',
                industry_group = '',
                has_fundamentals = True,
                has_stock_prices = True,
                page_size = 100,
                next_page = ''
                )
            c = api_response.companies_dict
            for e in c:
                if first:
                    first = False
                    toDelete = Company.objects.all()
                    toDelete.delete()
                (flag, errors) = Company.objects.newCompany(e)
                if flag:
                    print(e, errors)
                i += 1
        print("total companies count:", i)
    except ApiException as e:
        print("Exception when calling CompanyApi->get_all_companies: %s\r\n" % e)

    return redirect('securities:companies')


def data_tag_load(request):
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = INTRINIO_KEY
    # company_api = intrinio_sdk.CompanyApi()

    page_size = 100 # int | The number of results to return (optional) (default to 100)
    next_page = '' # str | Gets the next page of data from a previous API call (optional)

    STATEMENT_CODES = ['balance_sheet_statement',
                       'income_statement',
                       'cash_flow_statement',
                       'calculations',
                       # 'economic',
                       'current'
                      ]
    # first = True
    i = 0

    for each in STATEMENT_CODES:
        try:
            next_page = ""
            each_flag = True
            # while first or each_flag or next_page != None:
            while each_flag or next_page != None:

                api_response = intrinio_sdk.DataTagApi().get_all_data_tags(
                    tag="",
                    type="",
                    parent="",
                    statement_code=each,
                    fs_template="",
                    page_size=page_size,
                    next_page=next_page
                    )
                c = api_response.tags_dict
                for e in c:
                    # pprint(e)
                    # print("-"*40)
                    if each_flag:
                        # print(e)
                        each_flag = False
                    # if first:
                    #     first = False
                    #     toDelete = Data_Tag.objects.all()
                    #     toDelete.delete()
                    # (flag, errors) = Data_Tag.objects.load_Data_Tag(e)
                    u = Data_Tag.objects.filter(intrinio_id=e['id']).first()
                    flag = False
                    errors = []

                    for k in e.keys():
                        if e[k] == None:
                            e[k] = ""
                    if e['sequence'] == "":
                        e['sequence'] = 0

                    if u:
                        u.tag = e['tag']
                        u.name = e['name']
                        u.statement_code = e['statement_code']
                        u.template = e['statement_type']
                        u.parent = e['parent']
                        u.sequence = e['sequence']
                        u.factor = e['factor']
                        u.balance = e['balance']
                        u.nature = e['type']
                        u.units = e['unit']

                        try:
                            # pprint(u)
                            u.save()
                        except:
                            flag = True
                            errors += [f'Data Tag {e["tag"]} not updated successfully. Tag: {e}']
                    else:
                        (flag, errors) = Data_Tag.objects.load_Data_Tag(e)
                    if flag:
                        print(e, errors)
                    i += 1
                next_page = api_response.next_page
            print("After", each, "data_tags count:", i)
        except ApiException as e:
            print("Exception when calling DatatagApi->get_all_datatags: %s\r\n" % e)

    return redirect('securities:datatags')
