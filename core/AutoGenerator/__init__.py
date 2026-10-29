from core.AutoGenerator.generator import AutoGenerator
from core.helpers import get_identities_apps, get_identity_app_name, app_is_exists

def GeneratorIdentityApps():

    identity_apps = get_identities_apps()
    if identity_apps and isinstance(identity_apps, dict):
        gen = AutoGenerator()
        for key, value in identity_apps.items():
            app_name = get_identity_app_name(key)
            if app_name:
                if not app_is_exists(app_name):
                    gen.generate(app_name)
                    # print(f'Generated <<{app_name}>> is Successfully')