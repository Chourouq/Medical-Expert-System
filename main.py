import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QMessageBox

from aima.logic import FolKB, fol_bc_ask, expr

# Define the symptoms, rules, and facts
symptoms = ['Fever', 'Cough', 'Headache', 'SoreThroat', 'Fatigue', 'MuscleAches', 'RunnyNose',
            'ShortnessOfBreath', 'LossOfTaste', 'LossOfSmell', 'ChestPain', 'Nausea', 'Diarrhea',
            'Dizziness', 'DifficultySwallowing', 'JointPain', 'SkinRash', 'SwollenLymphNodes', 'AbdominalPain']

illnesses = {
    'CommonCold': ['Fever', 'Cough'],
    'Flu': ['Fever', 'Cough', 'Headache'],
    'StrepThroat': ['SoreThroat', 'Fever'],
    'Allergies': ['RunnyNose'],
    'COVID19': ['Fever', 'Cough', 'Fatigue', 'MuscleAches'],
    'Pneumonia': ['Fever', 'Cough', 'ShortnessOfBreath'],
    'Asthma': ['Cough', 'ChestPain', 'ShortnessOfBreath'],
    'Bronchitis': ['Fever', 'Cough', 'Wheezing'],
    'Gastroenteritis': ['Fever', 'Nausea', 'Diarrhea'],
    'Sinusitis': ['Fever', 'RunnyNose'],
    'Migraine': ['Headache', 'Nausea'],
    'LymeDisease': ['Fever', 'JointPain', 'SkinRash'],
    'Mononucleosis': ['Fever', 'Headache', 'SwollenLymphNodes'],
    'Hypertension': ['Fatigue', 'Headache', 'Hypertension'],
    'GERD': ['AbdominalPain', 'Nausea'],
    'UTI': ['Fever', 'PainDuringUrination'],
    'OtisMedia': ['EarPain', 'Fever']
}

rules = [
    # Rule 1: If someone has a fever and cough, it's a common cold
    "CommonCold(Fever) & CommonCold(Cough) ==> CommonCold(x)",

    # Rule 2: If someone has a fever, cough, and headache, it's the flu
    "Flu(Fever) & Flu(Cough) & Flu(Headache) ==> Flu(x)",

    # Rule 3: If someone has a sore throat and fever, it's strep throat
    "StrepThroat(SoreThroat) & StrepThroat(Fever) ==> StrepThroat(x)",

    # Rule 4: If someone has a runny nose, it's likely allergies
    "Allergies(RunnyNose) ==> Allergies(x)",

    # Rule 5: If someone has fever, cough, fatigue, and muscle aches, it's COVID-19
    "COVID19(Fever) & COVID19(Cough) & COVID19(Fatigue) & COVID19(MuscleAches) ==> COVID19(x)",

    # Rule 6: If someone has fever, cough, shortness of breath, and fatigue, it could be pneumonia
    "Pneumonia(Fever) & Pneumonia(Cough) & Pneumonia(ShortnessOfBreath) & Pneumonia(Fatigue) ==> Pneumonia(x)",

    # Rule 7: If someone has fever, cough, and loss of taste/smell, it could be COVID-19
    "COVID19(Fever) & COVID19(Cough) & COVID19(LossOfTaste) & COVID19(LossOfSmell) ==> COVID19(x)",

    # Rule 8: If someone has cough, chest pain, and shortness of breath, it could be asthma
    "Asthma(Cough) & Asthma(ChestPain) & Asthma(ShortnessOfBreath) ==> Asthma(x)",

    # Rule 9: If someone has fever, muscle aches, and diarrhea, it could be gastroenteritis
    "Gastroenteritis(Fever) & Gastroenteritis(MuscleAches) & Gastroenteritis(Diarrhea) ==> Gastroenteritis(x)",

    # Rule 10: If someone has fever and runny nose, it could be sinusitis
    "Sinusitis(Fever) & Sinusitis(RunnyNose) ==> Sinusitis(x)",

    # Rule 11: If someone has headache and nausea, it could be migraine
    "Migraine(Headache) & Migraine(Nausea) ==> Migraine(x)",

    # Rule 12: If someone has fever, headache, and swollen lymph nodes, it could be mononucleosis
    "Mononucleosis(Fever) & Mononucleosis(Headache) & Mononucleosis(SwollenLymphNodes) ==> Mononucleosis(x)",

    # Rule 13: If someone has fever, joint pain, and a skin rash, it could be Lyme disease
    "LymeDisease(Fever) & LymeDisease(JointPain) & LymeDisease(SkinRash) ==> LymeDisease(x)",

    # Rule 14: If someone has fever, headache, and difficulty swallowing, it could be strep throat
    "StrepThroat(Fever) & StrepThroat(Headache) & StrepThroat(DifficultySwallowing) ==> StrepThroat(x)",

    # Rule 15: If someone has fever, cough, and dizziness, it could be pneumonia
    "Pneumonia(Fever) & Pneumonia(Cough) & Pneumonia(Dizziness) ==> Pneumonia(x)",

    # Rule 16: If someone has abdominal pain and nausea, it could be gastro-esophageal reflux disease (GERD)
    "GERD(AbdominalPain) & GERD(Nausea) ==> GERD(x)",

    # Rule 17: If someone has fever and pain or burning sensation during urination, it could be a urinary tract
    # infection (UTI)
    "UTI(Fever) & UTI(PainDuringUrination) ==> UTI(x)",

    # Rule 18: If someone has fever, cough, and wheezing, it could be bronchitis
    "Bronchitis(Fever) & Bronchitis(Cough) & Bronchitis(Wheezing) ==> Bronchitis(x)",

    # Rule 19: If someone has fatigue, headache, and hypertension, it could be hypertension
    "Hypertension(Fatigue) & Hypertension(Headache) & Hypertension(Hypertension) ==> Hypertension(x)"
]


def setup_kb():
    # Function to set up the knowledge base (KB) with illnesses and their associated symptoms, and additional rules
    kb = FolKB()
    for illness, symptoms_list in illnesses.items():
        for symptom in symptoms_list:
            clause = expr(f"{illness}('{symptom}')")  # Representing each symptom of an illness as a clause
            print(clause)
            kb.tell(clause)
    # Add additional rules to the knowledge base
    for rule in rules:
        kb.tell(expr(rule))
    return kb


class MedicalExpertSystem(QWidget):
    # Class to define the GUI for the medical expert system
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medical Expert System')
        self.layout = QVBoxLayout()

        # Create checkboxes for symptoms dynamically based on the 'symptoms' list
        self.checkboxes = []
        for symptom in symptoms:
            checkbox = QCheckBox(symptom)
            self.checkboxes.append(checkbox)
            self.layout.addWidget(checkbox)

        # Create submit button to trigger diagnosis
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.show_illness)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def show_illness(self):
        # Function to handle diagnosis based on selected symptoms
        selected_symptoms = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        kb = setup_kb()  # Set up the knowledge base
        possible_illnesses = []
        for illness in illnesses.keys():
            result = fol_bc_ask(kb, expr(f"{illness}(x)"))  # Use backward chaining to infer possible illnesses
            if result:
                all_symptoms_matched = all(symptom in selected_symptoms for symptom in illnesses[illness])
                if all_symptoms_matched:
                    possible_illnesses.append(illness)

        if possible_illnesses:
            message = f"Possible illnesses: {', '.join(possible_illnesses)}"
            QMessageBox.information(self, "Diagnosis Result", message)
        else:
            QMessageBox.information(self, "Diagnosis Result", "No matching illness found.")


# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MedicalExpertSystem()
    window.show()
    sys.exit(app.exec_())
