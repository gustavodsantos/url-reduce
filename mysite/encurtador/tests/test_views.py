import pytest
from django.urls import reverse

from mysite.encurtador.models import UrlLog, UrlRedirect


@pytest.mark.django_db
def test_criar_url_view_post(client):
    url = reverse('encurtador:criar_url')
    response = client.post(url, {'destino': 'https://example.com'})

    # Verifica se redireciona para a página com a URL reduzida
    assert response.status_code == 200

    # Verifica se 'form' está no contexto
    form_in_context = 'form' in response.context
    assert form_in_context

    # Verifica se o formulário não é válido
    form = response.context['form']
    assert not form.is_valid()


@pytest.mark.django_db
def test_criar_url_view_get(client):
    url = reverse('encurtador:criar_url')
    response = client.get(url)

    # Verifica se a página inicial é carregada com o formulário
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_relatorios_view(client):
    url_redirect = UrlRedirect.objects.create(destino='https://example.com')
    url = reverse('encurtador:relatorios', args=[url_redirect.slug])
    response = client.get(url)

    # Verifica se o relatório é carregado com as informações corretas
    assert response.status_code == 200
    assert response.context['reduce'] == url_redirect
    assert 'redirecionamentos_por_data' in response.context
    assert 'total_cliques' in response.context


@pytest.mark.django_db
def test_redirecionar_view(client):
    url_redirect = UrlRedirect.objects.create(destino='https://example.com')
    url = reverse('encurtador:redirecionar', args=[url_redirect.slug])
    response = client.get(url)

    # Verifica se redireciona para o destino correto e se o log é criado
    assert response.status_code == 302
    assert response.url == url_redirect.destino
    assert UrlLog.objects.filter(url_redirect=url_redirect).exists()


@pytest.mark.django_db
def test_home_view_get(client):
    url = reverse('encurtador:home')
    response = client.get(url)

    # Verifica se o formulário é exibido na página inicial
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_home_view_post(client):
    url = reverse('encurtador:home')
    response = client.post(url, {'url_original': 'https://example.com'})

    # Verifica se a URL reduzida é criada e retornada no contexto
    assert response.status_code == 200
    assert 'url_reduzida' in response.context
    assert response.context['url_reduzida'].startswith('http')
    assert 'slug' in response.context
