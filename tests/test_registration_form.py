import allure
from data.student_data import Student
from pages.registration_page import RegistrationPage


@allure.title("Успешная регистрация пользователя через UI")
def test_submit_registration_form():
    student = Student()
    registration_page = RegistrationPage()

    with allure.step("Открыть страницу регистрации"):
        registration_page.open()

    with allure.step("Заполнить и отправить форму"):
        registration_page.register(student)

    with allure.step("Проверить успешную регистрацию"):
        registration_page.should_have_registered(student)
