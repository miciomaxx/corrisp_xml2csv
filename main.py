import pandas as pd
import xml.etree.ElementTree as ET
import os
import zipfile
import shutil

def format_currency(value):
    #Converte un valore in formato 9999.99 in formato 9999,99.
    if value is not None:
        try:
            value = float(value)
            return f'{value:.2f}'.replace('.', ',')
        except ValueError:
            return value
    return value

def xml_to_dataframe(xml_file):
    #Estrae dati da un file XML e li restituisce come DataFrame.
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    row = {}
    for elem in root:
        row[elem.tag] = elem.text
        for child2 in elem:
            row[child2.tag] = child2.text
            for child in child2:
                if child.tag == 'Imposta' or child.tag == 'Ammontare' or child.tag == 'ImportoParziale' or child.tag == 'PagatoContanti' or child.tag == 'PagatoElettronico':  # Modifica 'valuta' con il tag corretto
                    row[child.tag] = format_currency(child.text)
                else:
                    row[child.tag] = child.text
    data.append(row)
    return pd.DataFrame(data)

def main():
    zip_file_path = 'corrisp.zip'
    output_csv_file = 'output.csv'
    dataframes = []
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('temp_dir')

    # Elenca tutti i file XML estratti
    for filename in os.listdir('temp_dir'):
        if filename.endswith('.xml'):
            xml_file = os.path.join('temp_dir', filename)
            df = xml_to_dataframe(xml_file)
            dataframes.append(df)
            print(f'Processed {xml_file}')

    # Unisci tutti i DataFrame in uno solo
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Salva il DataFrame combinato come CSV
    combined_df.to_csv(output_csv_file, index=False)
    print(f'Saved combined CSV to {output_csv_file}')

    # Rimuove la \temp_dir e il suo contenuto
    shutil.rmtree('temp_dir')

if __name__ == "__main__":
    main()
