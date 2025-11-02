from abc import ABC, abstractmethod


# ABC (Abstract Base Classes) module - to achieve polymorphism
class DataManagerInterface(ABC):
    """
    define the abstract my_data manager interface methods
    serves as a blueprint for all my_data managers
    """

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_user_by_name(self, user_name):
        pass

    @abstractmethod
    def get_user_by_email(self, user_email):
        pass

    @abstractmethod
    def get_user_chats(self, user_id):
        pass

    @abstractmethod
    def get_chat_by_id(self, chat_id):
        pass

    @abstractmethod
    def create_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user_id):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def create_chat(self, chat, user_id):
        pass

    @abstractmethod
    def update_chat(self, chat_id):
        pass

    @abstractmethod
    def delete_chat(self, chat_id):
        pass