# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookspiderPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # strip all whitespace
        field_names = adapter.field_names() 
        for field_name in field_names:
            if field_name != 'description':
                # ItemAdapter wrapper retrieves value of user-defined field
                value = adapter.get(field_name)
                # this is the method that removes whitespace
                adapter[field_name] = value[0].strip()

        # for 'category' and 'product_type', we make their strings lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # convert price to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)


        availability_string = adapter.get('availability')
        # splits string into a list, and we retrieve only the number of available books
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability '] = 0
        else:   
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        stars_string = adapter.get('stars')
        star_rating = stars_string.split(' ')

        star_number = star_rating[1].lower()
        if(star_number=='one'):
            adapter['stars'] = 1
        elif(star_number=='two'):
            adapter['stars'] = 2
        elif(star_number=='three'):
            adapter['stars'] = 3
        elif(star_number=='four'):
            adapter['stars'] = 4
        elif(star_number=='one'):
            adapter['five'] = 5

        return item
    

