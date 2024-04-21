from django.test import TestCase
from ta_app.classes.UserClass import UserClass
from ta_app.models import Course, Section, User
from datetime import datetime

class TestUserClass(TestCase):

    def setUp(self):
        date_string = "Tue 2:30pm"
        date_object = datetime.strptime(date_string, "%a %H:%M%p")

        self.admin = User(name="ad",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False)
        self.admin.save()

    def test_createNullAll(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid entry"):
            temp = UserClass()
    # shouldn't be able to create a user with no name, password, etc

    def test_createNullUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid username"):
            temp = UserClass(None, "pass", "name", "TA", "email@email.com")
    # shouldn't be able to create a user with a null username

    def test_createNullPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid password"):
            temp = UserClass("username", None, "name", "TA", "email@email.com")
    # shouldn't be able to create a user with a null password

    def test_createNullName(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid name"):
            temp = UserClass("username", "pass", None, "TA", "email@email.com")
    # shouldn't be able to create a user with a null name

    def test_createNullRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid role"):
            temp = UserClass("username", "pass", "name", None, "email@email.com")
    # shouldn't be able to create a user with a null role

    def test_createNullEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid email"):
            temp = UserClass("username", "pass", "name", "TA", None)
    # shouldn't be able to create a user with a null email

    def test_createEmptyUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass("", "pass", "name", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty username

    def test_createEmptyPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "", "name", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty password

    def test_createEmptyName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty name

    def test_createEmptyRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", "", "email@email.com")
    # shouldn't be able to create a user with an empty role

    def test_createEmptyEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "TA", "")
    # shouldn't be able to create a user with an empty email

    def test_createWhitespaceUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass(" ", "pass", "name", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty username

    def test_createWhitespacePassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "  ", "name", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty password

    def test_createWhitespaceName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "   ", "TA", "email@email.com")
    # shouldn't be able to create a user with an empty name

    def test_createWhitespaceRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", " ", "email@email.com")
    # shouldn't be able to create a user with an empty role

    def test_createWhitespaceEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "TA", "  ")
    # shouldn't be able to create a user with an empty email

    def test_createBadEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch bad email"):
            temp = UserClass("username", "pass", "name", "TA", "randomwords")
    # shouldn't be able to create a user with a bad email (no @something.something)

    def test_createBadRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch bad role"):
            temp = UserClass("username", "pass", "name", "Batman", "email@email.com")

    def test_createAdmin(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Admin")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Admin", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : AD", "toString returns incorrectly")
    # check if creating an Admin with all necessary inputs returns successfully

    def test_createInstructor(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Instructor")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Instructor", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : IN", "toString returns incorrectly")
    # check if creating an Instructor with all necessary inputs returns successfully

    def test_createTA(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Teacher-Assistant")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Teacher-Assistant", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : TA", "toString returns incorrectly")
    # check if creating a TA with all necessary inputs returns successfully

    def test_createWithDetails(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="AD",
                    phone_number="123-4567", address="123 Fake Street")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "AD", "Role is wrong")
        self.assertEqual(temp.phone_number, "123-4567", "Phone number is wrong")
        self.assertEqual(temp.address, "123 Fake Street", "Address is wrong")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : AD", "toString returns incorrectly")
    # check if creating a user with additional details (phone/address) returns successfully

    def test_createToDB(self):
        date_string = "Tue 2:30pm"
        date_object = datetime.strptime(date_string, "%a %H:%M%p")
        algos = Course(course_id=351,course_name="compsci",description="blah blah blah")
        algos.save() 

        section = Section(course_parent=algos,section_id=12345,meeting_time = date_object,type="Lecture")
        section.save()

        slist = [section]
        self.assigned_user = UserClass("ta","ta","apoorv","Teacher-Assistant","email@email.com","1","1",True,slist)
        self.assigned_user.create_user()
        db_user = User.objects.get(name="apoorv")

        self.assertEqual(db_user.username, self.assigned_user.username, "Username is wrong")
        self.assertEqual(db_user.password,self.assigned_user.password, "Password is wrong")
        self.assertEqual(db_user.name, self.assigned_user.name, "Name is wrong")
        self.assertEqual(db_user.role, self.assigned_user.role, "Role is wrong")
        self.assertEqual(db_user.email, self.assigned_user.email, "Email is wrong")
        self.assertEqual(db_user.phone_number, self.assigned_user.phone_number, "Phone is wrong")
        self.assertEqual(db_user.address, self.assigned_user.address, "Address is wrong")
        self.assertEqual(db_user.assigned, self.assigned_user.assigned, "Assigned is incorrect")
        j = 0;
        for i in db_user.assigned_section.all():
            self.assertEqual(self.assigned_user.assigned_sections[j],i,"assigned sections not present")
            j=j+1

    def test_deleteToDB(self):
        self.assigned_user.delete_user()
        db_user = User.objects.filter(name="apoorv")
        self.assertEqual(db_user,None,"accoutn was not deleted from the db")

