import pytest
from faker import Factory
from pytest_bdd import scenario, given, when, then

from lenders.models import Lender


@scenario('./update_lender.feature', 'Update the lender')
def test_update():
    pass


@pytest.fixture
def create_lender(db, django_user_model):
    faker = Factory.create()
    code = faker.bothify(text='???')

    def make_user(**kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = faker.name()

        return Lender.objects.create(
            name=name,
            code=code,
            upfront_commistion_rate=0.2,
            trait_commistion_rate=0.1,
            active=True)

    return make_user


@pytest.mark.django_db
@given("I get a lender", target_fixture="lender")
def lender(create_lender):
    return create_lender(name="test")


@pytest.mark.django_db
@when("I update it")
def update_lender(lender):
    print(lender.name)
    lender.name = "ttt"
    lender.save()
    return lender


@pytest.mark.django_db
@then("I should see the change")
def update_lender(lender):
    assert lender.name == 'ttt'
