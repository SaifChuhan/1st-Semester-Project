import os
import json

PATIENTS_FILE = "patients.json"
DOCTORS_FILE = "doctors.json"

class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty

    def display_info(self):
        print(f"Doctor: {self.name}, Specialty: {self.specialty}")

    def to_dict(self):
        return {"name": self.name, "specialty": self.specialty}

class Patient:
    def __init__(self, name, age, weight, height, blood_type, gender):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.blood_type = blood_type
        self.gender = gender
        self.bmi = self.calculate_bmi()
        self.bmi_category = self.get_bmi_category()
        self.fat_loss_recommendation = self.fat_loss_recommendation()
        self.bmi_prime = self.calculate_bmi_prime()

    def calculate_bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    def get_bmi_category(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def fat_loss_recommendation(self):
        ideal_bmi = 22
        ideal_weight = ideal_bmi * (self.height ** 2)
        return max(self.weight - ideal_weight, 0)

    def calculate_bmi_prime(self):
        return 22.5 if self.gender == 'M' else 21.5

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.bmi,
            "bmi_category": self.bmi_category,
            "fat_loss_recommendation": self.fat_loss_recommendation,
            "blood_type": self.blood_type,
            "bmi_prime": self.bmi_prime,
            "gender": self.gender
        }

def load_data_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data_to_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_patients():
    patients_data = load_data_from_json(PATIENTS_FILE)
    return [Patient(**p) for p in patients_data]

def save_patient(patient):
    patients = load_data_from_json(PATIENTS_FILE)
    patients.append(patient.to_dict())
    save_data_to_json(PATIENTS_FILE, patients)

def load_doctors():
    doctors_data = load_data_from_json(DOCTORS_FILE)
    return [Doctor(**d) for d in doctors_data]

def save_doctor(doctor):
    doctors = load_data_from_json(DOCTORS_FILE)
    doctors.append(doctor.to_dict())
    save_data_to_json(DOCTORS_FILE, doctors)

def validate_positive_input(prompt, data_type):
    while True:
        try:
            value = data_type(input(prompt))
            if value > 0:
                return value
            else:
                print("Value must be greater than zero. Try again.")
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}.")

def main():
    patients = load_patients()
    doctors = load_doctors()

    while True:
        print("\n--- Hospital Management System ---")
        user_type = input("Are you a doctor or a patient? (Enter 'doctor' or 'patient' or 'exit'): ").lower()
        
        if user_type == 'patient':
            print("\n--- Patient Options ---")
            print("1. Add a Patient")
            print("2. View Patient Records")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter patient's name: ")
                age = validate_positive_input("Enter patient's age: ", int)
                weight = validate_positive_input("Enter patient's weight (kg): ", float)
                height = validate_positive_input("Enter patient's height (m): ", float)
                blood_type = input("Enter patient's blood type (e.g., A, B, AB, O): ").upper()
                gender = input("Enter patient's gender (M/F): ").upper()

                patient = Patient(name, age, weight, height, blood_type, gender)
                save_patient(patient)
                print("\nPatient record saved successfully!")

            elif choice == '2':
                print("\n--- Patient Records ---")
                if not patients:
                    print("No patient records found.")
                else:
                    for patient in patients:
                        print(f"Name: {patient.name}, Age: {patient.age}, BMI: {patient.bmi}, "
                              f"Category: {patient.bmi_category}, Fat Loss Needed: {patient.fat_loss_recommendation}kg")

            elif choice == '3':
                break

            else:
                print("Invalid choice. Please try again.")

        elif user_type == 'doctor':
            print("\n--- Doctor Options ---")
            print("1. Add a Doctor")
            print("2. View Doctor Information")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter doctor's name: ")
                specialty = input("Enter doctor's specialty (e.g., Cardiology, Surgery, etc.): ")
                doctor = Doctor(name, specialty)
                save_doctor(doctor)
                print(f"Doctor {name} added successfully!")

            elif choice == '2':
                print("\n--- Doctor Information ---")
                if not doctors:
                    print("No doctors available.")
                else:
                    for doctor in doctors:
                        doctor.display_info()

            elif choice == '3':
                break

            else:
                print("Invalid choice. Please try again.")

        elif user_type == 'exit':
            print("Exiting system...")
            break

        else:
            print("Invalid input. Please enter 'doctor' or 'patient'.")

if __name__ == "__main__":
    main()
