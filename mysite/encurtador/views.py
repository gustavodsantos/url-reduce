from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render

from mysite.encurtador.forms import UrlRedirectForm

# Create your views here.
from mysite.encurtador.models import UrlLog, UrlRedirect


def criar_url(request):
    if request.method == 'POST':
        form = UrlRedirectForm(request.POST)
        if form.is_valid():
            url_redirect = form.save()
            url_reduzida = request.build_absolute_uri(f'/{url_redirect.slug}')
            contexto = {'form': form, 'url_reduzida': url_reduzida, 'slug': url_redirect.slug}
            return render(request, 'encurtador/home.html', contexto)
    else:
        form = UrlRedirectForm()
    return render(request, 'encurtador/home.html', {'form': form})


def relatorios(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisicao.build_absolute_uri(f'/{slug}')
    redirecionamentos_por_data = list(
        UrlRedirect.objects.filter(slug=slug)
        .annotate(data=TruncDate('logs__criado_em'))
        .annotate(cliques=Count('data'))
        .order_by('data')
    )
    contexto = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
        'redirecionamentos_por_data': redirecionamentos_por_data,
        'total_cliques': sum(r.cliques for r in redirecionamentos_por_data),
    }
    return render(requisicao, 'encurtador/relatorio.html', contexto)


def redirecionar(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    UrlLog.objects.create(
        origem=requisicao.META.get('HTTP_REFERER'),
        user_agent=requisicao.META.get('HTTP_USER_AGENT'),
        host=requisicao.META.get('HTTP_HOST'),
        ip=requisicao.META.get('REMOTE_ADDR'),
        url_redirect=url_redirect,
    )
    return redirect(url_redirect.destino)


def home(request):
    contexto = {
        'form': UrlRedirectForm(),
    }

    # Verifique se a URL reduzida foi criada para exibir o link do relatório
    if request.method == 'POST':
        url_original = request.POST.get('url_original')
        # Aqui você deve adicionar a lógica para criar um UrlRedirect e salvar
        # Em seguida, obtenha o slug do objeto criado
        url_redirect = UrlRedirect.objects.create(destino=url_original)
        contexto['url_reduzida'] = request.build_absolute_uri(f'/{url_redirect.slug}')
        contexto['slug'] = url_redirect.slug  # Passa o slug para o contexto

    return render(request, 'encurtador/home.html', contexto)
