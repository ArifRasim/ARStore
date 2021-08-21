import pytest


def test_customer_str(customer):
    assert customer.__str__() == 'arif'


def test_super_user(admin_user):
    assert admin_user.__str__() == 'arif'


def test_super_user_no_email(customer_factory):
    with pytest.raises(ValueError)as e:
        test = customer_factory.create(email='')
    assert str(e.value) == 'Email must be provided'


@pytest.mark.django_db
def test_super_user_not_staff(customer_factory):
    with pytest.raises(ValueError)as e:
        test = customer_factory.create(is_superuser=True, is_staff=False)
    assert str(e.value) == 'superuser must be a staff member'


@pytest.mark.django_db
def test_super_user_not_active(customer_factory):
    with pytest.raises(ValueError)as e:
        test = customer_factory.create(is_superuser=True, is_active=False)
    assert str(e.value) == 'superuser must be an active member'


@pytest.mark.django_db
def test_super_user_not_superuser(customer_factory):
    with pytest.raises(ValueError)as e:
        test = customer_factory.create(is_superuser=False)
    assert str(e.value) == 'superuser must be a superuser'


def test_address_factory(address):
    assert address.__str__() == 'Arif Rasim'
