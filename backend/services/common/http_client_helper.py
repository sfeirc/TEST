"""
Helper pour supprimer les proxies de l'environnement avant de créer des clients OpenAI
"""
import os

def remove_proxy_env_vars():
    """Supprime les variables de proxy de l'environnement et retourne les valeurs sauvegardées"""
    old_proxies = {}
    for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
        if key in os.environ:
            old_proxies[key] = os.environ[key]
            del os.environ[key]
    return old_proxies

def restore_proxy_env_vars(old_proxies):
    """Restaure les variables de proxy dans l'environnement"""
    for key, value in old_proxies.items():
        os.environ[key] = value

def create_http_client():
    """Crée un client HTTP synchrone sans proxies - désactivé, on laisse OpenAI créer son propre client"""
    # On ne crée plus de client ici, on laisse OpenAI en créer un après avoir supprimé les proxies
    return None

def create_async_http_client():
    """Crée un client HTTP asynchrone sans proxies - désactivé, on laisse OpenAI créer son propre client"""
    # On ne crée plus de client ici, on laisse OpenAI en créer un après avoir supprimé les proxies
    return None

