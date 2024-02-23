import os
import configparser
import logging
import re


class transform:

    def __init__(self, ini_file, log_file):

        self.ini_file = ini_file
        self.log_file = log_file
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        if os.path.exists(self.ini_file):
            self.config.read(self.ini_file)

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def extract_fields(self, df):

        years = []
        trims = []
        transmissions = []
        bodystyles = []

        year_regex = re.compile(r'\b(19|20)\d{2}\b')
        trim_regex = re.compile(r'(Carrera|Targa) (S|4S|GTS|4)?')
        transmission_regex = re.compile(r'(\d)-Speed')

        for title in df['title']:
            year_match = year_regex.search(title)
            years.append(int(year_match.group()) if year_match else None)
            trim_match = trim_regex.search(title)
            trims.append(trim_match.group() if trim_match else 'Carrera')
            transmissions.append(
                'M' if transmission_regex.search(title) else 'A')

            if 'Targa' in title:
                bodystyles.append('Targa')
            elif 'Cabriolet' in title:
                bodystyles.append('Cabriolet')
            else:
                bodystyles.append('Coupe')

        df['year'] = years
        df['trim'] = trims
        df['transmission'] = transmissions
        df['bodystyle'] = bodystyles

        df = df.dropna(subset=['year'])
        df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(int)

        print(df)

        return df
