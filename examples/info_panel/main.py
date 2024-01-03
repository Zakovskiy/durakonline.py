import sys
from durakonline import durakonline

FILE_DIRECTORY: str = "./accounts.txt"


class InfoPanel:
    def __init__(self) -> None:
        self.load_accounts()

    def load_accounts(self) -> int:
        """
        data accounts in file by format:
            "
            token
            token
            ...
            "
        """
        with open(FILE_DIRECTORY, 'r') as file:
            tokens = file.read().split()
        for token in tokens:
            durak = durakonline.Client(server_id="u1")
            durak.authorization.signin_by_access_token(token)
            user = durak.get_user_info(durak.uid)

            print(f"""\n
                    Токен: {token}
                    Ник: {user.name}
                    Баланс: {durak.info.get('points')}
                    Рейтинг: {durak.info.get('score')}
                    Победы: {durak.info.get('wins')}
                    Победы за сезон: {durak.info.get('wins_s', 0)}

                    Смайлики:
                    Мишек: {self.get_smiles(user.coll, "smile_bear")}
                    Роботов: {self.get_smiles(user.coll, "smile_robot")}
                    Вампиров: {self.get_smiles(user.coll, "smile_vampire")}
                    Львов: {self.get_smiles(user.coll, "smile_lion")}
                    Гномов: {self.get_smiles(user.coll, "smile_gnome")}
                    Единорогов: {self.get_smiles(user.coll, "smile_unicorn")}
                    Быков: {self.get_smiles(user.coll, "smile_bull")}
                    Тигров: {self.get_smiles(user.coll, "smile_tiger")}
                    Крысы: {self.get_smiles(user.coll, "smile_rat")}

                    Рубашки:
                    Покерные: {self.get_smiles(user.coll, "shirt_bicycle", 52)}
                    Русские: {self.get_smiles(user.coll, "shirt_rstyle", 52)}
            """)

    def get_smiles(self, data: dict, type: str, count: int = 25) -> str:
        return f"{len(data.get(type, {'items': {}})['items'])} {'+' if len(data.get(type, {'items': {}})['items']) >= count else '-'}"

if __name__ == "__main__":
    script = InfoPanel
    script()
