import mariadb
from mariadb import Error
import pandas as pd



import yaml

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
class Backend:
    print(mariadb.__version__)
    
    def db_connection(datafile):
        
        # with open('data.yml', 'r') as yml_file:
        #       data_temp = yaml.safe_load(yml_file)
        

        try:
            conn = mariadb.connect(**config)
            
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            print('Creating table...')
            
            with open('zipname.txt', 'r') as file:
                name = file.read()
            
            
            name = name[0:-4] #remove the file extension

            #Create table statement
            cursor.execute(f"""CREATE OR REPLACE TABLE {name}(`ActualCurrent[A]` float,`ActualCurrent_Smooth[A]` float UNSIGNED, `DesiredCurrent[A]` float UNSIGNED,`DesiredPosition[tbd] float UNSIGNED,`DesiredVelocity[tbd/s]` float UNSIGNED,`EffectivePosition[m]` float UNSIGNED, `EffectivePosition_Smooth[cm]` float UNSIGNED, `EffectivePosition_Smooth[m]` float UNSIGNED, `PositionError[tbd]` float UNSIGNED)""")
            print("Table is created...")
            
            df = pd.DataFrame(data_temp)
            for row in df.iterrows():
                #here %S means string values
                sql = "INSERT INTO stinganalyzer_db.%s VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
                format_tuple = (name,) + tuple(row)
                cursor.execute(sql, format_tuple)
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                conn.commit()
     
        except Error as e:
                    print("Error while connecting to MySQL", e)
        except Exception as e:
                    print(f"Unexpected error occurred: {e}")

        finally:
             conn.close()

def main():
     b = Backend()
     b.db_connection()


if __name__ == '__main__':
    main()