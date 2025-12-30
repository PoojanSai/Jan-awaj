def generate_letter(text, dept, district, state):
    return f"""
To,
The Officer,
{dept},
{district}, {state}

Subject: Citizen Grievance Submission

Respected Sir/Madam,

I would like to bring to your attention the following issue:

{text}

Kindly take necessary action.

Sincerely,
Concerned Citizen
"""
