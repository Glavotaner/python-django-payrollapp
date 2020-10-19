from datetime import date

def _age(self) -> int:
        today = date.today()
        try:
            birthday = self.date_of_birth.replace(year=today.year)

        except ValueError:
            birthday = self.date_of_birth.replace(year=today.year,
                                                  month=self.date_of_birth.month + 1, day=1)

        if birthday > today:
            return today.year - self.date_of_birth.year - 1
        else:
            return today.year - self.date_of_birth.year