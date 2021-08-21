import pytest
from django.core.exceptions import ValidationError

from ARStore.apps.accounts.forms import UserAddressForm, RegisterForm, PwdResetForm


@pytest.mark.parametrize(
    "full_name, phone, address_line_1, address_line_2, city, postcode,validity",
    [('arif', '123', 'perelik', 'no 10', 'asenovgrad', '4230', True)],
)
def test_customer_address_form(full_name, phone, address_line_1, address_line_2, city, postcode, validity):
    form = UserAddressForm(
        data={
            'full_name': full_name, 'phone': phone, 'address_line_1': address_line_1, 'address_line_2': address_line_2,
            'city': city, 'postcode': postcode

        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize('user_name, email, password, repeat_password, validity', [
    ('arif', 'a@a.com', '123123', '123123', True),
    ('arif', 'a@a.com', '1231231', '123123', False),
], )
@pytest.mark.django_db
def test_customer_register_form(user_name, email, password, repeat_password, validity):
    form = RegisterForm(data={
        'user_name': user_name,
        'email': email,
        'password': password,
        'repeat_password': repeat_password,
    })
    assert form.is_valid() is validity


@pytest.mark.parametrize('user_name, email, password, repeat_password, validity', [
    ('arif', 'a@a.com', '123123', '123123', True),
], )
@pytest.mark.django_db
def test_customer_register_form_clean_username(user_name, email, password, repeat_password, validity):
    form = RegisterForm(data={
        'user_name': user_name,
        'email': email,
        'password': password,
        'repeat_password': repeat_password,
    })
    form.is_valid()
    assert form.clean_username() == 'arif'


@pytest.mark.parametrize('user_name, email, password, repeat_password, validity', [
    ('arif', 'a@a.com', '123123', '123123', True),
], )
@pytest.mark.django_db
def test_customer_pwd_reset_form_clean_email(user_name, email, password, repeat_password, validity):
    form = PwdResetForm(data={
        'email': 'a@a.com',
    })
    form.is_valid()
    with pytest.raises(ValidationError) as e:
        test = form.clean_email() == 'a@a.com'
    assert str(e.value) == "['Unfortunately we can not find that email address']"


@pytest.mark.parametrize('user_name, email, password, repeat_password, validity', [
    ('arif', 'a@a.com', '123123', '123123', True),
], )
@pytest.mark.django_db
def test_customer_pwd_reset_form_return_email(user_name, email, password, repeat_password, validity):
    form = PwdResetForm(data={
        'email': email,
    })
    assert form.is_valid() == False


def test_customer_register_form_username_exists_error(client, customer):
    user = customer
    client.force_login(user)
    response = client.post('account/add_address/',
                           data={'full_name': 'name'})
    assert response.status_code == 404
