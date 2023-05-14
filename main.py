import datetime
from twilio.rest import Client


class Library:
    def __init__(self):
        self.name = "TU Dublin Library"
        self.files = {'members.txt':Member, 
                      'borrowing.txt':Items, 
                      'items.txt':Items, 
                      'library.txt':''}
          
    def __str__(self):
        return self.name
    
    def search(self, id, filename, repr=False):
        """Allows search by object id and  instatiates that object"""
        _type = self.files[filename]
        id = id.strip()
        id = id.strip("\n")
        with open(filename) as f:
            for line in f:
                attributes = line.split('|') # get the data from the file and convert to a list
                print(attributes)
                if id.strip() == attributes[-1].strip().strip('\n'):
                    if repr:
                        return attributes
                    return _type(*attributes) # create an instance of an object
        print("This ID was not found")
        return None
        
    def member_login(self):
        """ask the user to sign in or create a new member"""
        name = input('Enter member name: ')
        unique = self.is_unique(name)
        if unique:
            answer = input("This member is not in the system, answer 'y' if you would like to create a new member: ")
            if answer.strip()  =='y':
                phone = input('Enter member phone number: ')
                address = input('Enter member address: ')
                member = Member(name, phone, address)
                member.save()
                print("Now logged in as", member.name)
                return member
        else:
            member = lib.search_member(name)
            print("Now logged in as", member.name)
            return member
        return None
    
    def delete(self, id, filename):
        """This deletes a piece of data from a given database"""
        lines = []
        with open(filename, 'r') as f:    
            for line in f:
                attributes = tuple(line.split('|'))
                if id == attributes[-1].strip().strip("\n"):
                    pass
                else:
                    lines.append(line)
        with open(filename, 'w') as f:
            for l in lines:
                f.write(l)
                f.write("\n")
                  
    def is_unique(self, search_term):
        """Check that a member's name is unique"""
        term = search_term.lower()
        with open('members.txt') as file:
            for line in file:
                if len(line) <2:
                    continue
                member = line.lower()
                data = member.split('|')
                data = [el.strip() for el in data]
                data = [el.strip('\n') for el in data]
                if term == data[0].lower():
                    return False
        return True
    
    def notify_member(self, member_id, message="Hello from TUD Library"):
        """Send an sms to a member to notify of availablilty"""
        member = self.search(member_id, 'members.txt')
        account_sid = "AC93a12dedf4aa5c1836b42b571772793c"
        auth_token = "ef1838f85afcad52aabc9cb8d2ada4aa"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_="+12707175012",
            to=member.phone
        )


class Member:
    def __init__(self, name, phone, address='N/A', id=''):
        self.name = name
        self.phone = phone
        self.address = address
        self._id = ''.join([str(ord(char)) for char in ''.join([self.name,self.phone,self.address])])
        self.id = id if id else self._id

    def __str__(self) -> str:
        return f"Name: {self.name} | Phone: {self.phone} | Address: {self.address} | ID: {self.id}"
    
    def __repr__(self):
        return f"{self.name}|{self.phone}|{self.address}|{self.id}"

    def save(self):
        with open('members.txt', 'a') as file:
            file.write(self.__repr__())
            file.write("\n")
        print("This is the member's ID:", self.id)
        return self.id
    
    def borrow(self, item):
        library = Library()
        with open('borrowing.txt', 'a') as f:
            borrowed = library.search(item.id,'borrowing.txt')
            if not borrowed:
                f.write(f"{self.__repr__()}|{item.__repr__()}")
                f.write("\n")
            else:
                print("This item is currently being borrowed")

        lines = []

        with open('library.txt', 'r') as f:
            for line in f:
                data = line.split('|')
                data = [el.strip() for el in data]
                data = [el.strip('\n') for el in data]
                if len(data)<2:
                    pass
                elif data[3]==self.id and data[-1]==item.id:
                    pass
                else:
                    lines.append(line)
        with open('library.txt', 'w') as f:
            for l in lines:
                f.write(l)
                f.write('\n')
        

    def return_item(self, item):
        """This allows a member to return a borrowed item"""
        library = Library()
        lines = []

        with open('borrowing.txt', 'r') as f:
            for line in f:
                data = line.split('|')
                data = [el.strip() for el in data]
                data = [el.strip('\n') for el in data]
                if len(data)<2:
                    pass
                elif data[3]==self.id and data[-1]==item.id:
                    reserved = library.search(item.id,'library.txt', repr=True)
                    if len(reserved) > 2:
                        library.notify_member(reserved[3].strip(), f"Hello this is {library}. Your item has become available")
                else:
                    lines.append(line)
        with open('borrowing.txt', 'w') as f:
            for l in lines:
                f.write(l)
                f.write('\n')

    def reserve(self, item):
        library = Library()
        with open('library.txt', 'a') as f:
            reserved = library.search(item.id,'library.txt',repr=True)
            if not reserved:
                f.write(f"{self.__repr__()}|{item.__repr__()}")
                f.write("\n")
            else:
                print("This item is currently being reserved")


class Items:
    """This is the parent of all items available in the library"""
    def __init__(self, title, author, year, extra_info, id=''):
        self.title = title
        self.author = author
        self.year = year
        self.id = ''.join([str(ord(char)) for char in ''.join([self.title,self.author,self.year])])

    
    def __str__(self) -> str:
        return self.title
    
    def __repr__(self):
        return f"{self.title}|{self.author}|{self.year}|{self.id}"
    
    def save(self):
        with open('items.txt', 'a') as file:
            file.write(self.__repr__())
            file.write('\n')
    
    def search_item(self, search_term):
        len(search_term)
        term = search_term.lower()
        with open('borrowing.txt') as file:
            for line in file:
                member = line.read().lower()
                endpoint = len(member) - len(search_term)
                i=0
                while i < endpoint:
                    if member[i:i+len(search_term)]:
                        #return Member(line)
                        return line
                    i+=1

    def is_borrowed(self):
        """This shows if an item is being borrowed"""
        with open('borrowing.txt', 'r') as f:
            for line in f:
                data = line.split('|')
                data = [el.strip() for el in data]
                data = [el.strip('\n') for el in data]
                if len(data) < 2:
                    pass
                elif data[-1]==self.id:
                    return True
            return False

        
class Books(Items):
    item_type = 1
    def __init__(self, *args, **kwargs):
        self.genre = args[-1]
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"Title:  {self.title} | Author: {self.author} | Year: {self.year} | Genre: {self.genre} | ID: {self.id}"
    
    def __repr__(self):
        return f"{self.title}|{self.author}|{self.year}|{self.genre}|{self.id}"
 

class Articles(Items):
    item_type = 2
    def __init__(self, *args, **kwargs):
        self.journal = args[-1]
        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Title:  {self.title} | Author: {self.author} | Year: {self.year} | Journal: {self.journal} | ID: {self.id}"
    
    def __repr__(self):
        return f"{self.title}|{self.author}|{self.year}|{self.journal}|{self.id}"
 

class DigitalMedia(Items):
    item_type = 3
    def __init__(self, *args, **kwargs):
        self.file_format = args[-1]
        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Title:  {self.title} | Author: {self.author} | Year: {self.year} | File Format: {self.file_format} | ID: {self.id}"
     
    def __repr__(self):
        return f"{self.title}|{self.author}|{self.year}|{self.file_format}|{self.id}"
    

if __name__ == '__main__':
    lib = Library()
    member = None

while True:
    print(f'Welcome to the {lib}!')
    print('Please select an option:')
    print('1. Member Sign Up or Sign In')
    print('2. Add Item')
    print('3. Edit/Delete Member')
    print('4. Edit/Delete Item')
    print('5. Borrow Item')
    print('6. Return Item')
    print('7. Check Item Availability')
    print('8. List All Items')
    print('9. List All Members')
    print('10. Get Member Borrowed Items')
    print('11. Notify a Member')
    print('. Exit')
    choice = input().strip()
    if choice == '1':
        """This asks user for information and creates a new member"""
        
        member = lib.member_login()

    elif choice == '2':
        item_type = int(input('Enter item type \n 1. Book \n 2. Article \n 3. Digital Media \n'))
        title = input('Enter item title: ')
        author = input('Enter item author: ')
        year = input('Enter item year: ')
        
        types = [Books, Articles, DigitalMedia] 
        additional_info = ['genre', 'journal' ,'file format']
        input_str = f'Enter item {additional_info[item_type-1]}: '
        info = input(input_str)

        new_item = types[int(item_type)-1](title, author, year, info)
        new_item.save()
        print(new_item)

    elif choice == '3':
        if not member:
            member = lib.member_login()
        if not member:
            continue
        
        print("Now using Member:", member.name)
        delete = input('Enter \'.\' to delete member or enter to edit: ')
        if delete =='.':
            lib.delete(member.id, 'members.txt')
        if delete=='.':
            continue
            
        name = None
        phone = None
        address = None

        while not name:
            name = input('Enter member name or enter to skip: ')
            if name=='':
                name = member.name
        while not phone:
            phone = input('Enter member phone number or enter to skip: ')
            if phone=='':
                phone = member.phone
        while not address:
            address = input('Enter member address or enter to skip: ')
            if address=='':
                address = member.address

        new_member = Member(name, phone, address, member.id)
        new_member.save()
        print(new_member)

    elif choice == '4':
        with open('items.txt') as f:
            for line in f:
                if len(line)>3:
                    print(line.strip("\n"))
        item=None
        while not item:
            item_id = input('Enter item ID or \'.\' to exit: ')
            item = lib.search(item_id,'items.txt')
            if item_id=='.':
                break
        if item_id=='.':
            continue
        print("Now using Item:", item.title)
        delete = input('Enter \'.\' to delete item or enter to edit: ')
        if delete =='.':
            lib.delete(item_id, 'items.txt')
        if delete=='.':
            continue
            
        title = None
        author = None
        year = None

        while not title:
            name = input('Enter title or enter to skip: ')
            if title=='':
                title = item.title
        while not author:
            author = input('Enter author or enter to skip: ')
            if author=='':
                author = item.author
        while not year:
            year = input('Enter year or enter to skip: ')
            if year=='':
                year = item.year

        new_item = Items(title, author, year, item.id)
        new_item.save()
        print(new_item)

    elif choice == '5':
        if not member:
            member = lib.member_login()

        if not member:
            continue

        with open('items.txt') as f:
            for line in f:
                if len(line)>3:
                    print(line.strip("\n"))

        item = None
        while not item:
            item_id = input('Enter ID of an item to borrow or \'.\' to exit: ')
            item = lib.search(item_id,'items.txt')
            exit = (item_id=='.' or item.is_borrowed())
            if item.is_borrowed():
                reserve = input("This item is currently being borrowed\nHit 'y' to reserve this item? ")
                if reserve == 'y':
                    member.reserve(item)
            if exit:
                break
        if exit:
            continue

        member.borrow(item)

        print(member.name,'is now borrowing', item.title)

    elif choice == '6':
        if not member:
            member = lib.member_login()
        if member:
            print("Now using Member:", member.name)
        else:
            continue
        item = None
        while not item:
            item_id = input('Enter item ID or \'.\' to exit: ')
            item = lib.search(item_id,'items.txt')
            if item_id=='.':
                break
        if item_id=='.':
            continue
        member.return_item(item)

        print(member.name,'has returned', item.title)

    elif choice == '7': 
        item_id = input('Enter ID of an item to check if it is borrowed or \'.\' to exit: ')
        item = lib.search(item_id,'items.txt')
        if item:
            if item.is_borrowed():
                print("This item is currently being borrowed")
            else:
                print("This item is available")
    

    elif choice == '8':
        with open('items.txt') as f:
            for line in f:
                if len(line)>2:
                    print(line.strip("\n"))

    elif choice == '9':
        with open('members.txt') as f:
            for line in f:
                if len(line)>3:
                    print(line.strip("\n"))
                
    elif choice == '10':
        if not member:
            member = lib.member_login()
        if not member:
            continue

        print("Now using Member:", member.name)
        with open('borrowing.txt') as f:
            lines = []
            for line in f:
                data = line.split('|')
                if len(data)>2:
                    if member.id.strip()== data[3].strip():
                        attrs = data[4:]
                        lines.append(" ".join(attrs))
            for l in lines:
                print(l)


    elif choice == '11':
        message = input("What message would you like to send to user? " )
        if not member:
            member = lib.member_login()
        if not member:
            continue
        try:
            lib.notify_member(member.id, message)
        except:
            print("This user does not have a valid phone number")
    
    elif choice == '.':
        break
    else:
        print('Invalid choice. Please try again.')
    input("Press Enter to continue")
    print('\n')
