# A simple example for multi tenant SaaS project with Django.

## Simple Documentation

### Install Packed
[django-tenants](https://github.com/django-tenants/django-tenants) & [django-tenant-users](https://github.com/Corvia/django-tenant-users)

```python
pip install django-tenants
pip install django-tenant-users
```

Here’s an example, suppose we have an app named `customers` and we want to create a model called `Client`.
```python
# apps/companies/models.py

from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase

class Client(TenantBase):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)

    auto_create_schema = True
    """
    Default: True
    Set this flag to false on a parent class if you don't want the schema
    to be automatically created upon save.
    """
    
    auto_drop_schema = True
    """
    Default: False
    USE THIS WITH CAUTION!
    Set this flag to true on a parent class if you want the schema to be
    automatically deleted if the tenant row gets deleted.
    """

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')


class Domain(DomainMixin):

    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domains')
```

```python
# apps/account/models.py

from django.db import models
from tenant_users.tenants.models import UserProfile

# Your custom user model
# You can create only `pass`. These all optional.
class User(UserProfile):
    # pass

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
```

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        # ..
    }
}
```

```python
# settings.py

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
```

Add the middleware `django_tenants.middleware.main.TenantMainMiddleware` to the top of `MIDDLEWARE`, so that each request can be set to use the correct schema.
```python
# settings.py

MIDDLEWARE = (
    'django_tenants.middleware.main.TenantMainMiddleware',
    #...
)
```

Make sure you have `django.template.context_processors.request` listed under the `context_processors` option of `TEMPLATES` otherwise the tenant will not be available on `request`.
```python
# settings.py

TEMPLATES = [
    {
        #...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                #...
            ],
        },
    },
]
```

```python
# settings.py

SHARED_APPS=[
    # ...
    'django.contrib.auth', # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes', # Defined in both shared apps and tenant apps
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
    'tenant_users.tenants', # defined only in shared apps
    'companies', # Custom defined app that contains the TenantModel. Must NOT exist in TENANT_APPS
    'account', # Custom app that contains the new User Model (see below). Must NOT exist in TENANT_APPS
    # ...
]

TENANT_APPS=[
    # ...
    'django.contrib.auth', # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes', # Defined in both shared apps and tenant apps
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
    # ...
]
```

```python
# settings.py

AUTH_USER_MODEL = 'account.TenantUser'
```

```python
# settings.py

AUTHENTICATION_BACKENDS = (
    'tenant_users.permissions.backend.UserBackend',
)
```

```python
# settings.py

TENANT_USERS_DOMAIN = "example.com"
```

```python
# settings.py

SESSION_COOKIE_DOMAIN = '.mydomain.com'
```

### Let's Start

```python
./manage.py makemigrations
```

```python
./manage.py migrate
```

#### 1. Creating Public Tenant (The main schema of your project)
tenant_users has method for this, but it doesn't give any access for admin user of public tenant. I recommend read `create_public_tenant`'s inside.
```python
from tenant_users.tenants.utils import create_public_tenant

create_public_tenant("example.com", "admin@example.com")
```
However, my solution/prefer is:
```python
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
)

UserModel = get_user_model()
TenantModel = get_tenant_model()
public_schema_name = get_public_schema_name()

# Create super super admin
profile = UserModel.objects.create(email='admin@example.com', is_active=True)
profile.set_password('topsecret')
profile.save()

# Create public tenant
public_tenant = TenantModel.objects.create(
    schema_name=public_schema_name, # usually 'public'
    name='Public Tenant',
    owner=profile,
)

# Add one or more domains for the tenant
get_tenant_domain_model().objects.create(
    domain='example.com',
    tenant=public_tenant,
    is_primary=True,
)

public_tenant.add_user(profile, is_superuser=True, is_staff=True)
```



#### 2. Creating New Tenant
````python
from tenant_users.tenants.tasks import provision_tenant

fqdn = provision_tenant("My Tenant", "mytenant", "admin@mytenant.com", True)
# Return FQDN (Fully Qualified Domain Name | eg: mytenant.example.com)
````