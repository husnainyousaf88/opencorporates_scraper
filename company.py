from bs4 import BeautifulSoup


class Company:

    def __init__(self, soup: BeautifulSoup, company_name) -> None:
        self.soup = soup

        self.company_name = company_name

        self.name_1 = '-'
        self.name_2 = '-'
        self.name_3 = '-'
        self.name_4 = '-'

        self.last_name = '-'
        self.reg_address = '-'
        self.city = '-'
        self.state = '-'
        self.zip_code = '-'

    def download_addresses(self) -> None:
        try:
            address = self.soup.find("dd", {"class": "registered_address adr"})
        except Exception as ex:
            print(ex)
            return

        if len(address) > 0:
            for item in address:
                try:
                    self.reg_address = item.contents[0].text
                except Exception as ex:
                    print(ex)

                try:
                    self.city = item.contents[1].text
                except Exception as ex:
                    print(ex)

                try:
                    self.zip_code = item.contents[2].text
                except Exception as ex:
                    print(ex)

                try:
                    self.state = item.contents[3].text
                except Exception as ex:
                    print(ex)

    def download_names(self) -> None:
        try:
            names = self.soup.find("dd", {"class": "officers trunc8"})
        except Exception as ex:
            print(ex)
            return

        if len(names) > 0:
            index = 1
            for name in names.contents[0].contents:
                try:
                    if index == 1:
                        self.name_1 = name.contents[0].text
                    elif index == 2:
                        self.name_2 = name.contents[0].text
                    elif index == 3:
                        self.name_3 = name.contents[0].text
                    elif index == 4:
                        self.name_4 = name.contents[0].text
                    else:
                        break
                    index += 1

                except Exception as ex:
                    print(ex)

    def get_details(self) -> tuple:
        self.download_addresses()
        self.download_names()

        return self.company_name, self.name_1, self.name_2,  self.name_3, self.name_4, \
            self.reg_address, self.city, self.state, self.zip_code