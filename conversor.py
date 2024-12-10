# Este script converte arquivos .xls para .xlsx para poder trabajarlos con el otro script.
import pyexcel as p

p.save_book_as(file_name="BASE_CASO_PRATICA_VIS_20230424.xls",
               dest_file_name="BASE_CASO_PRATICA_VIS_20230424.xlsx")

p.save_book_as(file_name="BASE_CASO_PRATICA_VIS_20230424_3.xls",
               dest_file_name="BASE_CASO_PRATICA_VIS_20230424_3.xlsx")

