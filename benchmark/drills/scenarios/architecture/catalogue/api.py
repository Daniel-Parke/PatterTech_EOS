"""The catalogue's public interface. Outsiders read this and nothing else."""

from catalogue.internal import repository


def get_product(product_id):
    return repository.load(product_id)


def list_products():
    return repository.load_all()
