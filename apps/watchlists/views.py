from django.shortcuts import render, redirect
from django.urls import reverse
from ..userprofiles.models import User, ValidateLogin
from . import models
from ..securities.models import PERIOD_CHOICES, Security, Data_Tag
from decimal import *
# Create your views here.

def validatelogin(R):
    if 'login' in R and 'user_id' in R and 'key' in R:
        if not ValidateLogin(R['key'], R['user_id']) or not R['login'] == True:
            R.clear()
            return redirect('/')
        return True
    else:
        R.clear()
        return redirect('/')

def index(request):

    validatelogin(request.session)
    user = User.objects.filter(id=request.session['user_id']).first()
    lists = models.Watchlist_Head.objects.filter(user=user).order_by('name')

    context = {}
    context = {'title': "My Watchlists",
               'W': [{'name':e.name,
                      'id':e.id,
                      'description':e.description,
                      # 'values':[float(e.wval_1),float(e.wval_2),float(e.wval_3),float(e.wval_4),float(e.wval_5)],
                      # 'pctgs':[float(e.wpct_1),float(e.wpct_2),float(e.wpct_3),float(e.wpct_4),float(e.wpct_5)],
                      'size': len(models.Watchlist_Rows.objects.filter(watchlist = e.id))
                      } for e in lists],
               }
    context['count'] = len(context['W'])

    request.session['error'] = False
    request.session['errors'] = []

    return render(request, 'watchlists/index.html', context)

def add(request):

    validatelogin(request.session)

    context = {'title': "New Watchlist",
               'edit' : False,
               }

    if 'error' in request.session and request.session['error'] == True:
        context['error'] = True
        context['errors'] = request.session['errors']
        context['formdata'] = request.session['formdata']

    request.session['error'] = False
    request.session['errors'] = []

    return render(request, 'watchlists/add.html', context)


def edit(request, id):
    id = int(id)

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    w = models.Watchlist_Head.objects.filter(id=id, user=user).first()
    d = models.Watchlist_Rows.objects.filter(watchlist = id).order_by('seq')
    t = Data_Tag.objects.all()
    c = models.Watchlist_Cols.objects.filter(watchlist = id).order_by('seq')

    # if not 'error' in request.session:
    request.session['error'] = False
    request.session['errors'] = []

    if not w:
        return redirect('watchlists:index')

    context = {'title': "Edit Watchlist",
               'edit' : True,
               'W' : w,
               'R' : d,
               'tickers': ", ".join([e.ticker for e in d]),
               'PERIODS' : PERIOD_CHOICES,
               'T': [{'tag':'*' + e.tag, 'name':f'{e.name}, ({e.units})', 'desc':e.description, 'level':e.level,} for e in t],
               'cols': [{'left':'url', 'right':'url', 'heading':f"{e.tag}\n{e.period}"} for e in c],
               }
    # print(context)
    if 'error' in request.session and request.session['error'] == True:
        context['error'] = True
        context['errors'] = request.session['errors']
        context['formdata'] = request.session['formdata']

    request.session['error'] = False
    request.session['errors'] = []

    return render(request, 'watchlists/add.html', context)

def create(request):

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()

    # clear the errors on session before checking
    request.session['error'] = False
    request.session['errors'] = []

    key_error = models.Watchlist_Head.objects.filter(name=request.POST['name'], user=user)

    if len(key_error) != 0:
        request.session['error'] = True
        request.session['errors'] += [
        'Watchlist name already exists for this user.'
        ]


    if request.session['error'] == True:
        formdata = { k:v.strip() for k,v in request.POST.items() if not k in ['csrfmiddlewaretoken','submit']}
        request.session['formdata'] = formdata
        return redirect('watchlists:add')
    else:
        # pass
        c = user.watchlists.create(name=request.POST['name'], description=request.POST['description'])
    return redirect( 'watchlists:edit', id=c.id)

def validateWH(F):
    formdata = {}
    formdata['name'] = F['name']
    formdata['description'] = F['description']

    # formdata['wpct_1'] = Decimal(F['wpct_1'])
    # formdata['wpct_2'] = Decimal(F['wpct_2'])
    # formdata['wpct_3'] = Decimal(F['wpct_3'])
    # formdata['wpct_4'] = Decimal(F['wpct_4'])
    # formdata['wpct_5'] = Decimal(F['wpct_5'])
    #
    # formdata['wval_1'] = Decimal(F['wval_1'])
    # formdata['wval_2'] = Decimal(F['wval_2'])
    # formdata['wval_3'] = Decimal(F['wval_3'])
    # formdata['wval_4'] = Decimal(F['wval_4'])
    # formdata['wval_5'] = Decimal(F['wval_5'])

    return False, formdata

def update(request, id):
    id = int(id)
    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    w = models.Watchlist_Head.objects.filter(id=id, user=user).first()
    formdata = { k:v.strip() for k,v in request.POST.items() if not k in ['csrfmiddlewaretoken','submit']}
    # clear the errors on session before checking
    request.session['error'] = False
    request.session['errors'] = []

    if not w:
        return redirect('watchlists:index')

    if w.name != request.POST['name']:
        key_error = models.Watchlist_Head.objects.filter(name=request.POST['name'], user=user)

        if len(key_error) != 0:
            request.session['error'] = True
            request.session['errors'] += [
            'Watchlist name already exists for this user.'
            ]
        else:
            w.name = request.POST['name']

    (flag, data) = validateWH(formdata)

    if flag:
        request.session['error'] = True
        request.session['errors'] += data

        request.session['formdata'] = formdata
        return redirect('watchlists:add')
    else:
        w.name = formdata['name']
        w.description = formdata['description']
        # w.wval_1 = formdata['wval_1']
        # w.wval_2 = formdata['wval_2']
        # w.wval_3 = formdata['wval_3']
        # w.wval_4 = formdata['wval_4']
        # w.wval_5 = formdata['wval_5']
        # w.wpct_1 = formdata['wpct_1']
        # w.wpct_2 = formdata['wpct_2']
        # w.wpct_3 = formdata['wpct_3']
        # w.wpct_4 = formdata['wpct_4']
        # w.wpct_5 = formdata['wpct_5']
        w.save()

    return redirect('watchlists:index')

def add_col(request, h_id):

    h_id = int(h_id)

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    wh = models.Watchlist_Head.objects.filter(id=h_id, user=user).first()

    if not wh:
        return redirect('watchlists:index')

    print(request.POST)

    formdata = {'element': request.POST['element'],
                'period': request.POST['period']
                }

    if (formdata['element'])[0] == '*':
        periods = [e[0] for e in PERIOD_CHOICES]
        # it is a 'Tag,' not a 'Formula'
        t = Data_Tag.objects.filter(tag=(formdata['element'])[1:])
        if not t:
            request.session['error'] = true
            request.session['errors'] += ['Data Tag invalid.  Column not added.']
            request.session['formdata'] = formdata
        else:
            if formdata['period'] not in periods:
                request.session['error'] = true
                request.session['errors'] += ['Period invalid.  Column not added.']
                request.session['formdata'] = formdata
            else:
                last = models.Watchlist_Cols.objects.last()
                seq = 1
                if last:
                    seq = last.seq + 1
                new = models.Watchlist_Cols(seq=seq, tag=(formdata['element'])[1:], period=formdata['period'], watchlist=wh)
                new.save()

    return redirect( 'watchlists:edit', id=wh.id)

def add_ticker(request, h_id):

    h_id = int(h_id)

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    wh = models.Watchlist_Head.objects.filter(id=h_id, user=user).first()

    if not wh:
        return redirect('watchlists:index')

    print(request.POST)
    t = str(request.POST['ticker']).strip().upper()
    s = Security.objects.filter(ticker=t).first()
    if not s:
        request.session['show'] = 'modalTicker'
        request.session['error'] = True
        request.session['errors'] += [f'Security Ticker ({t}) does not exist in tables.']
        request.session['formdata'] = request.POST
    else:

        new = models.Watchlist_Rows()
        new.ticker = t
        new.watchlist = wh
        new.seq = 3
        new.save()

    return redirect( 'watchlists:edit', id=wh.id)

def destroy(request, id):
    id = int(id)

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    w = models.Watchlist_Head.objects.filter(id=id, user=user).first()
    d = models.Watchlist_Rows.objects.filter(watchlist = id).order_by('seq')
    c = models.Watchlist_Cols.objects.filter(watchlist = id)

    if not 'error' in request.session:
        request.session['error'] = False
        request.session['errors'] = []

    if not w:
        request.session['error'] = True
        request.session['errors'] += ['Not authorized to that Watchlist.  Watchlist not deleted.']

        return redirect('watchlists:index')
    for each in c:
        each.delete()
    for each in d:
        each.delete()
    w.delete()

    return redirect('watchlists:index')

def view(request, id):
    id = int(id)

    validatelogin(request.session)

    user = User.objects.filter(id=request.session['user_id']).first()
    w = models.Watchlist_Head.objects.filter(id=id, user=user).first()
    tickers = models.Watchlist_Rows.objects.filter(watchlist = id).order_by('seq')
    cols = models.Watchlist_Cols.objects.filter(watchlist = id).order_by('seq')

    request.session['error'] = False
    request.session['errors'] = []

    if not w:
        request.session['error'] = True
        request.session['errors'] += ['Not authorized to that Watchlist.']

        return redirect('watchlists:index')

    items = []
    for e in cols:
        asterisk = lambda T: T[1:] if T[0]=='*' else T
        if e.tag != "":
            t = asterisk(e.tag) #drop the asterisk off the front and add the tag into the list of items
            items += (t,e.period)
        else:
            pass
    context = {'tickers':tickers,
               'cols': cols,
               'items':items,
                }
    return render(request, 'watchlists/view.html', context)
