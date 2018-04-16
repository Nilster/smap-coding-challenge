from django.core.management.base import BaseCommand
from django.conf  import settings
from django.apps import apps
import os
import sqlite3, csv
from datetime import datetime
from decimal import *

class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):

        #To do - hardcoded data directory and filenames. Pass them as arguments
        data_dir = os.path.join(os.path.dirname(settings.BASE_DIR), 'data')
        consumption_dir = os.path.join(data_dir, 'consumption')
        csv_user_data = os.path.join(data_dir, 'user_data.csv')

        sqlite_db = settings.DATABASES['default']['NAME']
        conn = sqlite3.connect(sqlite_db)

        #Upload the user data
        self.stdout.write(self.style.SUCCESS("Uploading User data.."))
        try:
            user_model = apps.get_model('consumption','User')

            with open(csv_user_data, 'r') as f:
                reader = csv.DictReader(f)
                to_db = [(int(row['id']), row['area'], row['tariff']) for row in reader]
            
            conn.executemany("INSERT INTO consumption_user(user_id,area,tariff) VALUES(?,?,?);", to_db )
            conn.commit()

        except LookupError:
            self.stdout.write(self.style.ERROR("The User model does not exist. Please create the model first."))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR("Problem in reading user_data.csv file. %s" %(e.args[0])))
        except sqlite3.Error as e:
            self.stdout.write(self.style.ERROR("Problem in writing to sqlite db. %s" %(e.args[0])))

        #self.stdout.write(','.join([data_dir, consumption_dir, csv_user_data])) 

        #Upload the consumption data
        try:
            usage_model = apps.get_model('consumption','Usage')

            files = [afile for afile in os.listdir(consumption_dir) if afile.endswith('.csv')]

            if len(files)==0:
                self.stdout.write(self.style.NOTICE("No consumption csv files found in %s" %(consumption_dir)))
            else:
                for afile in files:
                    try:
                        consumption_csv = os.path.join(consumption_dir,afile)
                        self.stdout.write(self.style.SUCCESS("Uploading comsumption file %s" %(consumption_csv)))
                        user_id = int(os.path.splitext(afile)[0])
                        with open(consumption_csv, 'r') as f:
                            reader = csv.DictReader(f)
                            to_db = [(datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S'), 
                                      Decimal(row['consumption']),
                                      consumption_csv,
                                      user_id) 
                                      for row in reader]
                        
                        conn.executemany("INSERT INTO consumption_usage(timestamp,consumption,filename,user_id_id) VALUES(?,?,?,?);", to_db )
                        conn.commit()
                        
                    except csv.Error as e:
                        self.stdout.write(self.style.ERROR("Problem in reading consumption csv file: %s %s" %(consumption_csv, e.args[0])))
                    except sqlite3.Error as e:
                        self.stdout.write(self.style.ERROR("Problem in writing consumption csv file: %s to sqlite db. %s" %(consumption_csv, e.args[0])))

        except LookupError:
            self.stdout.write(self.style.ERROR("The Usage model does not exist. Please create the model first."))
        
        conn.close()
        self.stdout.write(self.style.SUCCESS("Upload completed."))