from faker import Faker

import random

fake = Faker()

data_struct={
    'index': 'MY-INDEX',
    'attributes': [
            'TextField',
            'DateField',
            'TextField',
            'NumberField'
    ]}

def createDataIndex():
    fake.text()

def testLoops():
    import time
    loops=[10, 100, 1000, 10000]
    for loop in loops:
        print("Testing function with {} loops".format(str(loop)))
        start = time.time()
        for _ in range(loop):
            createDataIndex()
        end = time.time()
        print("Function execution took {} ms".format((end-start)*1000))


def dataGenerator(iters):
    for _ in range(iters):
        data_to_append = ""
        for element in data_struct['attributes']:
            if element == 'TextField':
                data_to_append+=fake.sentence()
            
            if element == 'NumberField':
                num = random.randint(5,100)
                data_to_append+=str(num)

            if element == 'DateField':
                data_to_append+=fake.date()
                
            
            data_to_append+=","

        yield data_to_append[:-1]


if __name__=='__main__':
    # Test the amount of Loops we can make
    # testLoops()

    # Test generator
    my_file = open('data.csv', 'w')
    gen = dataGenerator(10000)
    for entry in gen:
        #print(entry)
        my_file.write(entry+"\n")
