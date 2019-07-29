from datetime import datetime
from faker import Faker

fake = Faker()

def test_batch_put():
    
    data_gen = document_data_generator()

    #for counter, author, text, date, num in enumerate(data_gen):
    for counter, data in enumerate(data_gen):

        date_fmt=datetime.strptime(data[2], '%Y-%M-%d')
        if counter%200 == 0: 
            print(counter, data[2])


def document_data_generator(iters=10000):
    for _ in range(iters):

        import random

        yield  (fake.name(), fake.sentence(), fake.date(), random.randint(2, 50))


if __name__=='__main__':
    test_batch_put()
