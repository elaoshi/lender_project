from rest_framework.reverse import reverse

from lenders.dao.LenderRepository import LenderRepository
from lenders.models import Lender
import pytest
from faker import Factory

from django.test.client import RequestFactory
from lenders.services.lenderSerivce import LenderService
from lenders.views import LenderView, LenderDetailView


def test_example():
    assert 1 == 1


@pytest.mark.django_db
def test_create_lender_with_code():
    faker = Factory.create()
    name = faker.name()
    code = faker.bothify(text='???')
    lender = Lender.objects.create(name=name, code=code, upfront_commistion_rate=0.2,
                                   trait_commistion_rate=0.1,
                                   active=True)
    assert len(lender.code) == 3


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
def test_created_user(create_lender):
    lender = create_lender(name="test")
    print(lender.name)
    assert len(lender.code) == 3


@pytest.mark.django_db
def test_list_all_lender(create_lender):
    create_lender()
    lender_dao = LenderRepository()
    qs = lender_dao.list_all()
    print(qs)
    assert qs.count() == 1


test_data = [
    ('test', 'test', True),
    ('test2', 'test2', True)
]


@pytest.mark.django_db
@pytest.mark.parametrize("a,b,expected", test_data)
def test_list_all_lender(create_lender, a, b, expected):
    lender = create_lender(name=a)
    assert lender.name == a and lender.name == b
    lender_repository = LenderRepository()

    _id = lender.id
    qs = lender_repository.find_one({"id": _id})
    assert lender.id == qs.id
    assert (lender.name == qs.name and expected)


@pytest.mark.django_db
def test_lender_serveice_fetch(create_lender):
    name = 'test'
    create_lender(name=name)
    rf = RequestFactory()
    get_request = rf.get('/lender/')
    response = LenderView.as_view()(get_request)

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['name'] == name


@pytest.mark.django_db
def test_lender_serveice_filter(create_lender):
    name = 'test'
    lender = create_lender(name=name)
    rf = RequestFactory()
    kwargs = {"id": lender.id}
    get_request = rf.get(reverse('lender-detail', kwargs=kwargs))
    response = LenderDetailView.as_view()(get_request, **kwargs)

    assert response.status_code == 200
    assert response.data['name'] == name


@pytest.mark.django_db
def test_lender_update(create_lender):
    name = 'test'
    lender = create_lender(name=name)
    lender_service = LenderService()
    lender_service.update(lender.id, data={"name": "ttt"})

    item = Lender.objects.get(id=lender.id)
    assert item.name == 'ttt'


@pytest.mark.django_db
def test_lender_delete(create_lender):
    name = 'test'
    lender = create_lender(name=name)

    _id = lender.id
    lender_service = LenderService()
    res = lender_service.delete(lender.id)
    assert res is True

    lender_repository = LenderRepository()
    item = lender_repository.find_one({"id": _id})
    assert item is None


@pytest.mark.django_db
def test_lender_dump(create_lender):
    name = 'test'
    create_lender(name=name)
    name = 'test2'
    create_lender(name=name)

    lender_repository = LenderRepository()
    items = lender_repository.dump()
    assert len(items) > 0
    filename = lender_repository.dump()
    assert len(filename) > 0


@pytest.mark.django_db
def test_lender_create_from_json():
    faker = Factory.create()
    code = faker.bothify(text='???')
    name = faker.name()
    data = {
        "name": name,
        "code": code,
        "upfront_commistion_rate": "0.2",
        "trait_commistion_rate": "0.1",
        "active": True
    }
    code = faker.bothify(text='???')
    name = faker.name()
    data2 = {
        "name": name,
        "code": code,
        "upfront_commistion_rate": "0.2",
        "trait_commistion_rate": "0.1",
        "active": True
    }

    lender_repository = LenderRepository()

    objs = [
        lender_repository.createByObj(data),

        lender_repository.createByObj(data2),
    ]

    lender_repository.save_batch(objs)
    qs = lender_repository.list_all()
    assert qs.count() == 2
