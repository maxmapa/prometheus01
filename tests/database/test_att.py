import pytest
from modules.common.att import ATT

@pytest.mark.att
def test_database_connection():
    db = ATT()
    db.test_connection()


@pytest.mark.att
def test_passengers():
    db = ATT()
    data = db.get_passengers()
    errors = []
    for row in data:
        id, Classe, Adultos, Criancas, Bebes, Provenincia = row
        # Ensure none of the values are None, if they are convert them to 0
        Adultos = Adultos if Adultos is not None else 0
        Criancas = Criancas if Criancas is not None else 0
        Bebes = Bebes if Bebes is not None else 0
        total_passengers = Adultos + Criancas + Bebes
        try:
            if "1-3PAX" in Classe:
                assert total_passengers < 4, f"Pax! {Provenincia} made a mistake for Id: {id}"
            elif "4-8PAX" in Classe:
                assert total_passengers >= 4, f"Pax! {Provenincia} made a mistake for Id: {id}"
            elif "1 - 4 Pax" in Classe:
                assert total_passengers < 5, f"Pax! {Provenincia} made a mistake for Id: {id}"    
            elif "5 - 8 Pax" in Classe:
                assert total_passengers >= 5, f"Pax! {Provenincia} made a mistake for Id: {id}"   
            else:
                assert False, f"Unknown class {Classe} for Id: {id}"

        except AssertionError as e:
            errors.append(str(e))
            #print(errors)
    if errors:
        with open("test_errors.txt", "a") as file:
            file.write("\n".join(errors) + "\n")
        pytest.fail("\n".join(errors))
        
@pytest.mark.att
def test_operador():
    db = ATT()
    data = db.get_operador()
    errors = []
    for row in data:
        id, Tickets, Operador, Cob_Operador, Cob_Motorista, Cob_Parceiro, Provenincia = row
        # Ensure Cob_Operador is treated as a float
        Cob_Operador = float(Cob_Operador.replace(',', '.'))
        Cob_Motorista = float(Cob_Motorista.replace(',', '.'))
        Cob_Parceiro = float(Cob_Parceiro.replace(',', '.'))
       
        try:
            if "&" in Operador:
                assert Cob_Operador == 0.00, f"ATT! {Provenincia} made a mistake for Id: {id}"
            if "Alfagar" in Operador:
                assert Cob_Motorista == 0.00 and Cob_Parceiro == 0.00, f"Alfagar! {Provenincia} made a mistake for Id: {id}"
            if "Alto" in Operador:
                assert Cob_Motorista == 0.00 and Cob_Parceiro == 0.00, f"Colina! {Provenincia} made a mistake for Id: {id}"    
        except AssertionError as e:
            errors.append(str(e))
            #print(errors)
    if errors:
        with open("test_errors.txt", "a") as file:
            file.write("\n".join(errors) + "\n")
        pytest.fail("\n".join(errors))    

@pytest.mark.att
def test_rate():
    db = ATT()
    data = db.get_rate_by_hour()
    errors = []
    for row in data:
        id, Hora, Categoria, Val_Servico, Provenincia = row
        # Ensure Cob_Operador is treated as a float
        Val_Servico = float(Val_Servico.replace(',', '.'))
       
        try:
            # Check if Hora is between 00:00 and 07:00 and Categoria is "Airport"
            hour = int(Hora.split(':')[0])
            if 0 <= hour < 7 and "Airport" in Categoria:
                assert Val_Servico != 65.00 and Val_Servico != 55.00, f"Night rate! {Provenincia} made a mistake for Id: {id}"
        except AssertionError as e:
            errors.append(str(e))
            #print(errors)
    if errors:
        with open("test_errors.txt", "a") as file:
            file.write("\n".join(errors) + "\n")
        pytest.fail("\n".join(errors))