class LoginPage:
    def __init__(self, driver, user, password) :
        self.driver = driver
        self.user = user
        self.password = password

    def get_login_page(self):
        self.driver.get_page("https://mysaga.gruposaga.com.br/public/index.jsf")
            
    def login(self):
        self.get_login_page()
        self.driver.fill_loop("input#saga_username", self.user)
        self.driver.fill_loop("input#saga_password", self.password)
        self.driver.click_loop("input#btnLoginId")