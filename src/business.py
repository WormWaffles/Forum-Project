from src.models import db, Business

class Businesses:

    def get_all_businesses(self):
        '''Returns all businesses'''
        return Business.query.all()
    
    def get_business_by_id(self, business_id):
        '''Returns business by id'''
        return Business.query.get(business_id)
    
    def get_business_by_name(self, business_name):
        '''Returns business by name'''
        return Business.query.filter_by(business_name=business_name).first()
    
    def get_business_by_email(self, email):
        '''Returns business by email'''
        return Business.query.filter_by(email=email).first()
    
    def create_business(self, business_name, email, password):
        '''Creates a business'''
        business = Business(business_name=business_name, email=email, password=password)
        db.session.add(business)
        db.session.commit()
        return business
    
    def update_business(self, business_id, business_name, email, password, business_description, address, city, state, zip_code, phone, website):
        '''Updates a business'''
        business = self.get_business_by_id(business_id)
        business.business_name = business_name
        business.email = email
        business.password = password
        business.business_description = business_description
        business.address = address
        business.city = city
        business.state = state
        business.zip_code = zip_code
        business.phone = phone
        business.website = website
        db.session.commit()
        return business
    
    def delete_business(self, business_id):
        '''Deletes a business'''
        business = self.get_business_by_id(business_id)
        db.session.delete(business)
        db.session.commit()

    def clear_businesses(self):
        '''Clears all businesses'''
        businesses = self.get_all_businesses()
        for business in businesses:
            db.session.delete(business)
        db.session.commit()

business_users = Businesses()