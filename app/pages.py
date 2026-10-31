# Static content pages: slug -> (title, intro, [(heading, text), ...])
PAGES = {
 "about": ("About Ganga Care", "A 150-bed multi-specialty hospital serving Patna and Bihar since 2005.", [
  ("Our approach", "We built the hospital around one idea: patients should spend their time getting care, not waiting for it. Every OPD visit is booked by slot, and every doctor sees a limited number of patients each session."),
  ("Accreditation and standards", "Placeholder: list your NABH, NABL and other accreditations here."),
  ("Our people", "Over 60 consultants, 200 nurses and a 24-hour support team across emergency, ICU, surgery and diagnostics.")]),
 "departments": ("Departments", "Five OPD departments, each with a named consultant and fixed session hours.", [
  ("General Medicine", "Fever, diabetes, blood pressure, thyroid and routine adult care."),
  ("Cardiology", "ECG, echo, stress tests and heart-failure follow-up."),
  ("Pediatrics", "Newborn care, vaccination and child illness."),
  ("Orthopedics", "Fractures, joint pain, sports injuries and replacement consults."),
  ("Gynecology", "Antenatal care, family planning and women's health.")]),
 "packages": ("Health checkup packages", "Fixed-price packages. Fasting for 10 hours is needed before blood tests.", [
  ("Basic wellness, Rs 1,499", "CBC, blood sugar, lipid profile, liver and kidney tests, ECG and a physician review."),
  ("Senior citizen, Rs 3,499", "Basic wellness plus thyroid, vitamin D and B12, bone density screen and an eye check."),
  ("Cardiac care, Rs 4,999", "Lipid profile, ECG, echo, treadmill test and a cardiologist consult.")]),
 "faq": ("Frequently asked questions", "Quick answers about booking and visiting.", [
  ("How do I book an OPD appointment?", "Use Book OPD appointment, choose a doctor, date and slot, and keep your booking number."),
  ("Can I cancel or change a booking?", "Yes. Open Manage booking, enter your booking number and mobile number, and cancel. Then book a new slot."),
  ("What should I bring?", "Your booking number, a photo ID and any previous reports or prescriptions."),
  ("What are the OPD hours?", "Monday to Saturday, 10:00 to 13:00. Closed on Sundays. Emergency is open 24 hours."),
  ("Is there parking?", "Yes, free visitor parking with wheelchair access.")]),
 "careers": ("Careers", "We hire doctors, nurses, technicians and administrators.", [
  ("Open roles", "Placeholder: Staff Nurse, Lab Technician, Front Desk Executive."),
  ("How to apply", "Email your resume to careers@gangacare.example with the role in the subject line.")]),
 "privacy": ("Privacy policy", "Placeholder text for a demo project. Have a lawyer review it before real use.", [
  ("What we collect", "When you book, we collect the patient's name, mobile number, chosen doctor, date, slot and an optional reason for the visit."),
  ("Why we collect it", "Only to schedule and manage your appointment and to contact you about it."),
  ("Storage and security", "Data is stored in the hospital's database on secured servers. Access is limited to authorised staff."),
  ("Your rights", "Under the Digital Personal Data Protection Act, 2023, you may ask us to access, correct or erase your data by writing to privacy@gangacare.example."),
  ("Cookies", "This site does not use tracking cookies.")]),
 "terms": ("Terms of use", "Placeholder text for a demo project.", [
  ("Use of the site", "You agree to give accurate information and not to misuse the booking system, for example by booking slots you do not plan to use."),
  ("Appointments", "A booking reserves a time slot but does not guarantee a consultation if a doctor is unavailable. We will contact you to reschedule."),
  ("Changes", "We may update these terms. The latest version is always on this page.")]),
 "disclaimer": ("Medical disclaimer", "Placeholder text for a demo project.", [
  ("Not medical advice", "Information on this website is general and is not a substitute for a doctor's advice."),
  ("Emergencies", "In an emergency, do not use online booking. Call 0612-000-0000 or go to the casualty department."),
  ("Demo notice", "Ganga Care Hospital is a fictional hospital created for a college cloud computing project.")]),
 "cancellation": ("Cancellation policy", "Placeholder text for a demo project.", [
  ("Cancelling", "Cancel any time from Manage booking. Cancelling frees the slot for another patient."),
  ("Late arrival", "Slots are held for 15 minutes after the booked time."),
  ("Fees", "Consultation fees are paid at the counter, so there is nothing to refund online.")]),
}
