import pandas as pd
import os

csv_filename = 'data-receiver-150ms.csv'
csv_directory = 'C:/Users/facun/OneDrive/Documentos/Extra Projects/SDCAN-G3V/Code/interface/interfaceProject/interfaceApp'
csv_path = os.path.join(csv_directory, csv_filename)

df = pd.read_csv(csv_path)
last_row = df.iloc[len(df)-1]

testDict = {
    'datetime': 'Wed Sep 27 13:23:21 2023',
    'dust': 2096,
    'mq135': 0,
    'mq131': 0,
    'mq4': 0,
    'temperature': 24.7,
    'pressure': 96343,
    'altitude': 422.95,
}

class processingClass():
    """
    MQ135:
    CO
    CO2
    Amonio
    Tolueno

    MQ131:
    O3

    MQ4:
    LPG
    Methane

    MQ135 example:    
    ADCVal = mq135Measurement
    if ADCVal == 0:
        RS = 100000
    else:
        RS = ((4.1*(10**6))/ADCVal) - 1000

    R0 = 100

    ratio = RS / R0

    CO_a = 605.18
    CO_b = -3.537
    CO_ppm = (CO_a*(ratio**CO_b))*1*(10**6)
    if CO_ppm > 100000:
        CO_ppm = 100000

    print(f'CO_ppm: {CO_ppm}')
    """

    def __init__(self, df_row = dict) -> None:
        ab_dict = {
            'MQ135':{
                'CO': {
                    'a':605.18,
                    'b': -3.537
                },
                'CO2': {
                    'a':110.47,
                    'b': -2.862
                },
                'Ammonia': {
                    'a':102.2,
                    'b': -2.473
                },
                'Toluene': {
                    'a':44.947,
                    'b': -3.445
                },
            },
            'MQ131':{
                '03': {
                    'a':23.943,
                    'b': -1.11
                },
            },
            'MQ4':{
                'LPG': {
                    'a':3811.9,
                    'b': -3.113
                },
                'Methane': {
                    'a':1012.7,
                    'b': -2.786
                },
            },
        }
        
        for mq in df_row.keys():

            if 'MQ' in str(mq).upper():
                ADCVal = df_row[mq]

                if ADCVal == 0:
                    RS = 100000
                else:
                    RS = ((4.1*(10**6))/ADCVal) - 1000

                R0 = 100

                ratio = RS / R0
                
                mq = str(mq).upper()
                
                for molecula in ab_dict[mq]:
                    a = ab_dict[mq][molecula]['a']
                    b = ab_dict[mq][molecula]['b']
                    ppm = ( a *(ratio** b )) *1*(10**6)
                    if ppm > 100000:
                        ppm = 100000
                        
                    setattr(self, molecula, ppm)  # Dynamically set the attribute

                    print(f'molecula: {molecula} ppm: {ppm}')

                    print(f'self.{molecula}: {getattr(self, molecula)}')


obj = processingClass(dict(last_row))
print(obj.__doc__)
