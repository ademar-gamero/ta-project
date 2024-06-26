from django.test import TestCase, Client
from ta_app.models import User, Course


class EditCourse(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(name='John Doe', username='jdoe', password='password123',
                                         email='jdoe@uwm.edu', role='Admin', phone_number='1234567890',
                                         address='Home', assigned=False)
        self.admin.save()

        # put some courses into the database.
        self.default = Course.objects.create(course_id=123,
                                            course_name='test course',
                                            description='this is a test',
                                            semester='Fall')

        self.cs351 = Course.objects.create(course_id=351,
                                           course_name='CompSci',
                                           description='data structures and algorithms',
                                           semester='Spring')

    def test_editCoursePageAdminAccess(self):
        # Test that the edit course page will load successfully with admin credentials
        resp = self.client.post("/login/", {"username": self.admin.username, "password": self.admin.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.default.pk}/")
        self.assertEqual(200, resp.status_code, "role error")  # check that the courseCreate page loads

    def test_editCoursePageInstructorAccess(self):
        # Test that the edit course page will not load successfully if not an admin
        self.ins = User.objects.create(name='Jake Jones', username='jjones', password='password123',
                                       email='jjones@uwm.edu', role='Instructor', phone_number='1234567890',
                                       address='Home', assigned=False)
        self.ins.save()

        resp = self.client.post("/login/", {"username": self.ins.username, "password": self.ins.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.default.pk}/")  # try to go to the editCourse page. Should not be allowed.
        self.assertRedirects(resp, "/Home/", 302,
                             msg_prefix="incorrectly allowed to access editCourse")

    def test_editCoursePageTAAccess(self):
        # Test that the edit course page will not load successfully if not an admin
        self.ta = User.objects.create(name='Jane Smith', username='jsmith', password='password123',
                                      email='jsmith@uwm.edu', role='Teacher-Assistant', phone_number='1234567890',
                                      address='Home', assigned=False)
        self.ta.save()

        resp = self.client.post("/login/", {"username": self.ta.username, "password": self.ta.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.default.pk}/")
        self.assertRedirects(resp, "/Home/", 302,
                             msg_prefix="incorrectly allowed to access editCourse")

    def test_editCourseAllFieldsGood(self):
        # Test that all fields can be edited and properly updated at the same time
        data = {
            'course_id': 100,
            'course_name': 'new test name',
            'description': 'new test description',
            'semester': 'Winter'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        self.assertEqual(2, Course.objects.all().count(),
                         "An extra course was created when it should not have been")
        # Now check that each altered field was properly updated in the database
        # Retrieve the most current version of the record from the database after editing using its known primary key
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual(100, course_from_db.course_id, "Course ID was not properly updated in the database")
        self.assertEqual('new test name', course_from_db.course_name,
                         "Course name was not properly updated in the database")
        self.assertEqual('new test description', course_from_db.description,
                         "Course description was not properly updated in the database")
        self.assertEqual('Winter', course_from_db.semester,
                         "Course semester was not properly updated in the database")

    def test_editCourseOnlyID(self):
        # Test that ID can be edited and properly updated on its own
        data = {
            'course_id': 100,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual(100, course_from_db.course_id, "Course ID was not properly updated in the database")

    def test_editCourseOnlyName(self):
        # Test that name can be edited and properly updated on its own
        data = {
            'course_id': 123,
            'course_name': 'new test name',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual('new test name', course_from_db.course_name,
                         "Course name was not properly updated in the database")

    def test_editCourseNameWhitespace(self):
        # Test that editing name will remove trailing and leading whitespace from input
        data = {
            'course_id': 123,
            'course_name': '  new test name  ',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual('new test name', course_from_db.course_name,
                         "Course name was not properly updated in the database")

    def test_editCourseOnlyDescription(self):
        # Test that description can be edited and properly updated on its own
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'new test description',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual('new test description', course_from_db.description,
                         "Course description was not properly updated in the database")

    def test_editCourseDescriptionWhitespace(self):
        # Test that editing description will remove trailing and leading whitespace from input
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': '  new test description  ',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual('new test description', course_from_db.description,
                         "Course description was not properly updated in the database")

    def test_editCourseOnlySemester(self):
        # Test that semester can be edited and properly updated on its own
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Winter'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual('Winter', course_from_db.semester,
                         "Course semester was not properly updated in the database")

    def test_editAllIntoConflict(self):
        # Test that a duplicate course cannot be made when editing all fields and that values return to original
        edit = {  # all fields match another database entry
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.cs351.pk}/", edit)
        self.assertEqual(resp.context['errorMessage'], "Exact course already exists!",
                         "Course was allowed to create conflict")
        course_from_db = Course.objects.get(pk=self.cs351.pk)
        # check that all values returned back to original
        self.assertEqual(351, course_from_db.course_id, "Course ID was not reverted back to original")
        self.assertEqual('CompSci', course_from_db.course_name, "Course name was not reverted back to original")
        self.assertEqual('data structures and algorithms', course_from_db.description,
                         "Course description was not reverted back to original")
        self.assertEqual('Spring', course_from_db.semester, "Course semester was not reverted back to original")

    def test_editOnlyIdFullConflict(self):
        # Test that a duplicate course cannot be made when editing only ID and that value returns to original
        new = Course.objects.create(course_id=100,
                              course_name='test course',
                              description='this is a test',
                              semester='Fall')
        edit = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{new.pk}/", edit)
        self.assertEqual(resp.context['errorMessage'], "Exact course already exists!",
                         "Course was allowed to create conflict")
        course_from_db = Course.objects.get(pk=new.pk)
        self.assertEqual(100, course_from_db.course_id, "Course ID was not reverted back to original")

    def test_editOnlyNameFullConflict(self):
        # Test that a duplicate course cannot be made when editing only name and that value returns to original
        new = Course.objects.create(course_id=123,
                              course_name='Anthro',
                              description='this is a test',
                              semester='Fall')
        edit = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{new.pk}/", edit)
        self.assertEqual(resp.context['errorMessage'], "Exact course already exists!",
                         "Course was allowed to create conflict")
        course_from_db = Course.objects.get(pk=new.pk)
        self.assertEqual('Anthro', course_from_db.course_name, "Course name was not reverted back to original")

    def test_editNameWhitespaceFullConflict(self):
        # Test that a duplicate course cannot be made when input has trailing or leading whitespace
        new = Course.objects.create(course_id=123,
                              course_name='Anthro',
                              description='this is a test',
                              semester='Fall')
        edit = {
            'course_id': 123,
            'course_name': '  test course  ',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{new.pk}/", edit)
        self.assertEqual(resp.context['errorMessage'], "Exact course already exists!",
                         "Course was allowed to create conflict")
        course_from_db = Course.objects.get(pk=new.pk)
        self.assertEqual('Anthro', course_from_db.course_name, "Course name was not reverted back to original")

    def test_editOnlySemesterFullConflict(self):
        # Test that a duplicate course cannot be made when editing only semester and that value returns to original
        new = Course.objects.create(course_id=123,
                              course_name='test course',
                              description='this is a test',
                              semester='Winter')
        edit = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{new.pk}/", edit)
        self.assertEqual(resp.context['errorMessage'], "Exact course already exists!",
                         "Course was allowed to create conflict")
        course_from_db = Course.objects.get(pk=new.pk)
        self.assertEqual('Winter', course_from_db.semester, "Course semester was not reverted back to original")

    def test_editCourseNegativeID(self):
        data = {
            'course_id': -1,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "ID cannot be negative",
                         "Course was mistakenly allowed to update bad ID")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual(123, course_from_db.course_id, "Course ID was not reverted back to original")

    def test_editCourseDigitName(self):
        data = {
            'course_id': 123,
            'course_name': '12345',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course name should not be solely numeric digits",
                         "Course was mistakenly allowed to update bad name")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual("test course", course_from_db.course_name, "Course name was not reverted back to original")

    def test_editCourseBadSemester(self):
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'bad'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.default.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Invalid semester",
                         "Course was mistakenly allowed to update bad semester")
        course_from_db = Course.objects.get(pk=self.default.pk)
        self.assertEqual("Fall", course_from_db.semester, "Course semester was not reverted back to original")
