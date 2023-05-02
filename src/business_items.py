from src.models import db, BusinessItems

class BusinessItem:
    
    def get_all_items(self):
        '''Returns rating by post id'''
        items = BusinessItems.query.all()
        return items
    
    def get_business_items_by_user_id(self, user_id):
        '''Returns all ratings'''
        return BusinessItems.query.filter_by(business_id=user_id).scalar()
    
    def get_all_menu_titles(self, user_id):
        '''Returns all menu titles'''
        business_items = self.get_business_items_by_user_id(user_id)
        menu_titles = [business_items.title_menu_1, business_items.title_menu_2, business_items.title_menu_3]
        return menu_titles
    
    def create_business_items(self, user_id):
        '''Creates business items'''
        business_items = BusinessItems(business_id=user_id)
        db.session.add(business_items)
        db.session.commit()
        return business_items

    def get_all_menus(self, user_id):
        '''Returns all menus'''
        business_items = self.get_business_items_by_user_id(user_id)
        menus = [business_items.file_menu_1, business_items.file_menu_2, business_items.file_menu_3]
        return menus
    
    def ammend_features(self, user_id, features):
        '''Change or add features'''
        business_items = self.get_business_items_by_user_id(user_id)
        business_items.features=features
        db.session.commit()
        return  business_items.features
    
    def add_menu():
        '''Add menu'''
        pass

business_items = BusinessItem()