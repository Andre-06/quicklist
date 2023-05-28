import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUICKLIST.settings')
django.setup()

from users.models import User

def remove_non_superuser():

    non_superuser_users = User.objects.filter(is_staff=0)
    non_superuser_users.delete()

    print("Usuários não superusuários removidos com sucesso.")

print("Inciiando")
remove_non_superuser()
print("Cabo")
