from lenders.dao.LenderRepository import LenderDao
from lenders.models import Lender
import pytest
from faker import Faker,Factory

def test_example():

    assert 1==1

@pytest.mark.django_db
def test_create_lender_with_code():
    faker = Factory.create()
    name = faker.name()
    code = faker.bothify(text='???')
    lender = Lender.objects.create(name=name,code=code,upfront_commistion_rate=0.2,
                                   trait_commistion_rate=0.1,
                                   active=True)
    assert len(lender.code)  == 3


@pytest.fixture
def create_lender(db, django_user_model):
    faker = Factory.create()
    code = faker.bothify(text='???')
    name = faker.name()
    def make_user(**kwargs):
        return Lender.objects.create(
            name=name,
            code=code,
            upfront_commistion_rate=0.2,
            trait_commistion_rate=0.1,
            active=True)

    return make_user


@pytest.mark.django_db
def test_created_user(create_lender):
    lender = create_lender()
    # print(lender.name)
    assert len(lender.code) == 3



@pytest.mark.django_db
def test_list_all_lender(create_lender):
    create_lender()
    lenderDao = LenderDao()
    qs = lenderDao.list_all()

    assert qs.count() == 1